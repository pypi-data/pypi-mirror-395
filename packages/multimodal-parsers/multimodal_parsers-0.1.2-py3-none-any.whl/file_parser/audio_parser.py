"""
Audio Parser Module
Handles diarization and transcription of audio files to markdown.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Any
import librosa
import numpy as np
import soundfile as sf
import tempfile
import torch
from omegaconf import open_dict
from nemo.collections.asr.models import SortformerEncLabelModel, ASRModel

DEFAULT_STREAMING_CONFIG = {
    "chunk_len": 512,
    "chunk_right_context": 1,
    "fifo_len": 124,
    "spkcache_update_period": 124,
    "spkcache_len": 188,
}


@dataclass
class Segment:
    start: float
    end: float
    speaker_id: int


@dataclass
class TranscriptSegment:
    start: float
    end: float
    speaker_label: str
    text: str


def load_audio(path: Path, target_sr: int = 16000) -> tuple[np.ndarray, int]:
    """Load audio file and resample to target sample rate."""
    samples, sr = librosa.load(str(path), sr=target_sr, mono=True)
    return samples, sr


def save_temp_audio(samples: np.ndarray, sample_rate: int) -> Path:
    """Save audio samples to a temporary WAV file."""
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tmp_path = Path(tmp.name)
    tmp.close()
    sf.write(str(tmp_path), samples, sample_rate)
    return tmp_path


def load_diarization_model(
    model_name: str = "nvidia/diar_streaming_sortformer_4spk-v2",
    config: dict[str, int] | None = None,
) -> SortformerEncLabelModel:
    """Load and configure the diarization model."""
    model = SortformerEncLabelModel.from_pretrained(model_name)
    model.eval()
    streaming_config = config or DEFAULT_STREAMING_CONFIG
    for attr, value in streaming_config.items():
        setattr(model.sortformer_modules, attr, value)
    model.sortformer_modules._check_streaming_parameters()
    return model


def normalize_segments(raw_segments) -> list[Segment]:
    """
    Normalize diarization segments to Segment objects.
    Format: list of lists of strings like ["25.840 34.960 speaker_0", ...]
    """
    normalized = []
    # raw_segments is a list of lists (one list per audio file)
    for segment_list in raw_segments:
        for segment_str in segment_list:
            # Format: "start end speaker_id" (space-separated)
            parts = segment_str.split()
            start = float(parts[0])
            end = float(parts[1])
            # Extract number from "speaker_0", "speaker_1", etc.
            speaker = int(parts[2].replace("speaker_", ""))
            normalized.append(Segment(start, end, speaker))
    return normalized


def merge_segments(segments: Iterable[Segment], gap_tolerance: float = 0.05) -> list[Segment]:
    """Merge adjacent segments from the same speaker."""
    merged: list[Segment] = []
    for segment in sorted(segments, key=lambda item: item.start):
        if not merged:
            merged.append(segment)
            continue
        last = merged[-1]
        if segment.speaker_id == last.speaker_id and segment.start <= last.end + gap_tolerance:
            last.end = max(last.end, segment.end)
        else:
            merged.append(segment)
    return merged


def align_transcription_to_diarization(
    word_timestamps: list[dict], 
    diarization_segments: list[Segment]
) -> list[TranscriptSegment]:
    """
    Align word-level timestamps from ASR with diarization segments.
    """
    transcripts: list[TranscriptSegment] = []
    
    current_segment_idx = 0
    current_text = []
    
    # Filter out empty segments or invalid ones
    diarization_segments = sorted([s for s in diarization_segments if s.end > s.start], key=lambda x: x.start)
    if not diarization_segments:
        return []

    # Helper to create a transcript segment
    def push_segment(idx, text_list):
        if not text_list:
            return
        seg = diarization_segments[idx]
        transcripts.append(TranscriptSegment(
            start=seg.start,
            end=seg.end,
            speaker_label=f"Speaker {seg.speaker_id + 1}",
            text=" ".join(text_list).strip()
        ))

    for word_info in word_timestamps:
        word_start = word_info['start_offset']  # already in seconds now
        word_end = word_info['end_offset']
        word_text = word_info.get('char') or word_info.get('word', "")
        
        # Find which diarization segment this word belongs to
        # Simple logic: midpoint of word falls into segment
        word_mid = (word_start + word_end) / 2
        
        # Advance segment pointer if needed
        while current_segment_idx < len(diarization_segments) - 1 and word_mid > diarization_segments[current_segment_idx].end:
             push_segment(current_segment_idx, current_text)
             current_text = []
             current_segment_idx += 1
        
        # Check if word falls in current segment
        cur_seg = diarization_segments[current_segment_idx]
        if word_mid >= cur_seg.start:
            # It belongs to this segment
            current_text.append(word_text)
        elif word_mid < cur_seg.start and current_segment_idx > 0:
            # Falls between segments or before first segment
            current_text.append(word_text)
            
    # Push last segment
    push_segment(current_segment_idx, current_text)
    
    return transcripts


def transcribe_file_with_timestamps(
    asr_model: Any,
    audio_path: str,
    diarization_segments: list[Segment],
    model_type: str = "parakeet",
    source_lang: str | None = None,
    target_lang: str | None = None,
    taskname: str | None = None,
) -> list[TranscriptSegment]:
    """Transcribe audio file with word-level timestamps and align with diarization."""
    
    print("  - Transcribing full audio with timestamps...")
    
    # Build transcribe kwargs
    transcribe_kwargs = {
        "batch_size": 1,
        "return_hypotheses": False,
        "timestamps": True,
        "verbose": True
    }
    
    # Add Canary-specific parameters if model is "canary"
    if model_type == "canary":
        if source_lang is not None:
            transcribe_kwargs["source_lang"] = source_lang
        if target_lang is not None:
            transcribe_kwargs["target_lang"] = target_lang
        if taskname is not None:
            transcribe_kwargs["taskname"] = taskname
    
    hypotheses = asr_model.transcribe([audio_path], **transcribe_kwargs)
    
    if not hypotheses:
        print("Warning: No hypotheses returned.")
        return []
    
    # Extract timestamps from hypothesis
    first_hyp = hypotheses[0]
    timestamp_dict = None
    
    if hasattr(first_hyp, 'timestamp'):
        timestamp_dict = first_hyp.timestamp
    
    if not timestamp_dict:
        print("Warning: No timestamps found in hypothesis.")
        return []
        
    word_timestamps = timestamp_dict.get('word', [])
    print(f"    Extracted {len(word_timestamps)} words.")
    
    # Normalize timestamp format
    cleaned_timestamps = []
    for w in word_timestamps:
        start = w.get('start', w.get('start_offset', 0.0))
        end = w.get('end', w.get('end_offset', 0.0))
        text = w.get('word', w.get('char', ''))
        
        cleaned_timestamps.append({
            'start_offset': start,
            'end_offset': end,
            'char': text
        })

    return align_transcription_to_diarization(cleaned_timestamps, diarization_segments)


def infer_model_type(model_name: str) -> str:
    """
    Infer model type (canary or parakeet) from model name.
    
    Args:
        model_name: Full model name (e.g., "nvidia/canary-1b-v2" or "nvidia/parakeet-tdt-0.6b-v3")
        
    Returns:
        str: "canary" or "parakeet"
    """
    model_name_lower = model_name.lower()
    if "canary" in model_name_lower:
        return "canary"
    elif "parakeet" in model_name_lower:
        return "parakeet"
    else:
        # Default to parakeet if cannot infer
        print(f"Warning: Cannot infer model type from '{model_name}', defaulting to 'parakeet'")
        return "parakeet"


def load_asr_model(model_name: str = "nvidia/parakeet-tdt-0.6b-v3") -> ASRModel:
    """Load ASR model by model name."""
    model = ASRModel.from_pretrained(model_name=model_name)
    
    if torch.cuda.is_available():
        model.to(torch.float16)
        
    model.eval()

    # Fix configs if needed
    if hasattr(model, 'cfg'):
         for ds in ['test_ds', 'train_ds', 'validation_ds']:
             if ds in model.cfg:
                 with open_dict(model.cfg[ds]):
                     model.cfg[ds].pretokenize = False
                     if 'trim_silence' in model.cfg[ds]:
                         del model.cfg[ds].trim_silence
                     if 'enable_chunking' in model.cfg[ds]:
                         del model.cfg[ds].enable_chunking
    return model


class AudioExtractor:
    """Extract transcriptions from audio files with speaker diarization."""
    
    def __init__(
        self,
        audio_path: Path,
        output_path: Path,
        diar_model: SortformerEncLabelModel | None = None,
        asr_model: ASRModel | None = None,
        model_name: str = "nvidia/parakeet-tdt-0.6b-v3",
        source_lang: str | None = None,
        target_lang: str | None = None,
        taskname: str | None = None,
    ):
        self.audio_path = audio_path
        self.output_path = output_path
        self.diar_model = diar_model
        self.asr_model = asr_model
        self.model_name = model_name
        self.model_type = infer_model_type(model_name)  # Infer from model name
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.taskname = taskname
    
    def run(self) -> bool:
        """
        Process audio file: diarize and transcribe.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Load audio
            audio_samples, sample_rate = load_audio(self.audio_path)
            temp_audio_path = save_temp_audio(audio_samples, sample_rate)
            
            try:
                # Diarize
                print("  - Diarizing...")
                raw_segments = self.diar_model.diarize(audio=str(temp_audio_path), batch_size=1)
                normalized = normalize_segments(raw_segments)
                merged_segments = merge_segments(normalized)
                
                # Transcribe
                transcript_segments = transcribe_file_with_timestamps(
                    self.asr_model,
                    str(temp_audio_path),
                    merged_segments,
                    model_type=self.model_type,
                    source_lang=self.source_lang,
                    target_lang=self.target_lang,
                    taskname=self.taskname,
                )
                
            finally:
                temp_audio_path.unlink(missing_ok=True)
            
            if not transcript_segments:
                print("No speech segments detected or transcription failed.")
                return False
            
            # Write markdown output
            self._write_markdown(transcript_segments)
            return True
            
        except Exception as e:
            print(f"Error processing audio {self.audio_path}: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _write_markdown(self, transcript_segments: list[TranscriptSegment]):
        """Write transcript segments to markdown file."""
        with open(self.output_path, "w", encoding="utf-8") as f:
            f.write(f"# Transcript: {self.audio_path.name}\n\n")
            
            f.write("## Transcript\n\n")
            for item in transcript_segments:
                if not item.text:
                    continue
                f.write(f"- **[{item.start:.2f}s - {item.end:.2f}s] {item.speaker_label}:** {item.text}\n")



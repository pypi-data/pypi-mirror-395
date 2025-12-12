import fitz
from file_parser.categorizer import PDFTextBlockCategorizer


class PDFExtractor:
    def __init__(self, pdf_path, pdf_output):
        self.pdf_output = pdf_output
        self.pdf_doc = fitz.open(pdf_path)
        self.batch = 10

    def get_min_sample_param(self, n_pages):
        if n_pages <= 6:
            return 2
        elif n_pages <= 8:
            return 3
        return 4

    def calc_rect_center(self, rect, reverse_y=False):
        if reverse_y:
            x0, y0, x1, y1 = rect[0], -rect[1], rect[2], -rect[3]
        else:
            x0, y0, x1, y1 = rect

        x_center = (x0 + x1) / 2
        y_center = (y0 + y1) / 2
        return (x_center, y_center)

    def extract_all_text_blocks(self, visualize=False):
        pages = list(enumerate(self.pdf_doc)) + [(None, None)] * (self.batch - len(self.pdf_doc) % self.batch)
        page_groups = list(zip(*[iter(pages)] * self.batch))
        for page_group in page_groups:
            page_group = list(page_group)
            while page_group[-1][0] is None:
                page_group.pop()
            rect_centers = []
            rects = []
            visual_label_texts = []
            categorize_vectors = []
            for page_idx, page in page_group:
                page_height = page.rect.height
                bbox = page.get_bboxlog()
                blocks = [x[1][:4] for x in bbox] + [b[:4] for b in page.get_text("blocks")]
                blocks = [x for x in blocks if x[3] <= 0.2 * page_height or x[1] >= 0.9 * page_height]
                page_cnt = page_idx + 1
                for idx, block in enumerate(blocks):
                    block_rect = block
                    rects.append((block_rect, page_idx))
                    block_text = ''
                    block_num = idx
                    block_cnt = block_num + 1

                    rect_center = self.calc_rect_center(block_rect, reverse_y=True)
                    rect_centers.append(rect_center)
                    visual_label_text = f"({page_cnt}.{block_cnt})"
                    visual_label_texts.append(visual_label_text)
                    categorize_vectors.append((*block_rect, block_text))

            categorizer = PDFTextBlockCategorizer(categorize_vectors)
            categorizer.run(min_samples=self.get_min_sample_param(len(page_group)))
            for i, rect_center in enumerate(rect_centers):
                label_idx = categorizer.labels[i]
                x0, y0, x1, y1 = rects[i][0]
                if label_idx == 1:
                    rect = fitz.Rect(x0, y0, x1, y1)
                    self.pdf_doc[rects[i][1]].add_redact_annot(rect)
                    self.pdf_doc[rects[i][1]].apply_redactions(1, 2, 0)

        self.pdf_doc.save(self.pdf_output)

    def run(self):
        self.extract_all_text_blocks()


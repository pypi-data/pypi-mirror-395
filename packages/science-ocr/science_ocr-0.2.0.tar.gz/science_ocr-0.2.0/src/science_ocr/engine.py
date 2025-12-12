from huggingface_hub import snapshot_download
from surya.foundation import FoundationPredictor
from surya.recognition import RecognitionPredictor
from surya.detection import DetectionPredictor
from surya.layout import LayoutPredictor
from surya.recognition.util import DEFAULT_TAGS_TO_FILTER
from surya.settings import settings


class SuryaOCREngine:
	LAYOUT_LABELS = {
		# "PageHeader",
		# "PageFooter",
		# "Footnote",
		# "Picture",
		# "Figure",
		"Text",
		"Caption",
		"ListItem",
		"SectionHeader",
		# "Table",
		# "TableOfContents",
		"Form",
		"Equation",
		# "Code",
	}

	FILTER_TAGS = DEFAULT_TAGS_TO_FILTER + [
		'br', 'u', 'del', 'mark',
		'i', 'b', 'sup', 'sub',
		'math'
	]

	def __init__(self):
		super().__init__()
		self.download_models()
		self.recognition_predictor = RecognitionPredictor(FoundationPredictor())
		self.detection_predictor = DetectionPredictor()
		self.layout_predictor = LayoutPredictor(FoundationPredictor(checkpoint=settings.LAYOUT_MODEL_CHECKPOINT))

	def download_models(self):
		snapshot_download(
			repo_id="TomasGD/surya-ocr-mirror-models-2025_05_07",
			repo_type="model"  # or "dataset", "space"
		)

	def layout_driven_ocr(self, images):
		# img can be numpy array, PIL, or file path
		layout_predictions = self.layout_predictor(images)
		ocr_predictions = self.recognition_predictor(
			images,
			task_names=["ocr_without_boxes"]*len(images),
			det_predictor=self.detection_predictor, math_mode=False,
			filter_tag_list=DEFAULT_TAGS_TO_FILTER + SuryaOCREngine.FILTER_TAGS
		)

		pages_result_text = []
		for page_idx in range(len(images)):
			layout_boxes = layout_predictions[page_idx].bboxes
			layout_boxes = list(filter(lambda lb: lb.label in SuryaOCREngine.LAYOUT_LABELS, layout_boxes))
			text_lines = ocr_predictions[page_idx].text_lines

			# Map of layout -> assigned lines
			layout_text_map = {id(l): [] for l in layout_boxes}

			# Assign each line to the layout box with maximum overlap
			for line in text_lines:
				best_layout = None
				best_area = 0

				for layout in layout_boxes:
					area = layout.intersection_area(line)
					if area > best_area:
						best_area = area
						best_layout = layout

				if best_layout:
					layout_text_map[id(best_layout)].append(line)

			# Sort text inside each block top-to-bottom
			for key in layout_text_map:
				layout_text_map[key].sort(key=lambda x: x.bbox[1])

			# Flatten into clean text for this page
			page_text = self.join_text_no_hyper(
				[self.join_text_no_hyper([l.text for l in lines], " ") for lines in layout_text_map.values() if lines],
				"\n"
			)

			pages_result_text.append(page_text)

		return self.join_text_no_hyper(pages_result_text, "\n")

	def join_text_no_hyper(self, texts, joint):
		result = []
		for text in texts:
			if result and result[-1].endswith('-'):
				result[-1] = result[-1][:-1] + text
			else:
				result.append(text)

		return joint.join(result)

	def join_lines(self, lines):
		result = []
		for line in lines:
			line = line.text.strip()
			if result and result[-1].endswith('-'):
				result[-1] = result[-1][:-1] + line
			else:
				result.append(line)

		return " ".join(result)

	def cleanup_text(self, text):
		return text.rstrip("-")

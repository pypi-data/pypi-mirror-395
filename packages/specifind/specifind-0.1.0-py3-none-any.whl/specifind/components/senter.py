import torch

from specifind.vendor.wtpsplit import SaT


class Senter:
	def __init__(self):
		self.splitter = SaT("sat-12l-sm")
		if torch.cuda.is_available():
			self.splitter.half().to("cuda")

	def __call__(self, doc):
		sentences = self.splitter.split(doc.text, split_on_input_newlines=True)

		for token in doc:
			token.is_sent_start = False

		char_offset = 0
		for sent_text in sentences:
			sent_start = doc.text.find(sent_text, char_offset)
			if sent_start == -1:
				print("OCR text disalignment")
				continue

			token = doc.char_span(sent_start, sent_start + 1, alignment_mode="expand")
			token[0].is_sent_start = True

			char_offset = sent_start + len(sent_text)

		if len(doc) > 0:
			doc[0].is_sent_start = True

		return doc
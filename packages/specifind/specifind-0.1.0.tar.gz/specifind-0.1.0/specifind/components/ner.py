import spacy

from huggingface_hub import snapshot_download
from spacy.util import filter_spans


class NamedEntityRecognizer:
	def __init__(self):
		model_path = self.download_models()
		self.nlp = spacy.load(model_path)

	def download_models(self):
		return snapshot_download(
			repo_id="TomasGD/specifind_ner",
			repo_type="model"  # or "dataset", "space"
		)

	def predict_with_windows(self, doc, window_size=384, stride=128):
		entities = []
		start_idx = 0

		while start_idx < len(doc):
			end_idx = min(start_idx + window_size, len(doc))
			window_text = doc[start_idx:end_idx]

			window_doc = self.nlp(window_text.text)

			for ent in window_doc.ents:
				adjusted_start = window_text.start_char + ent.start_char
				adjusted_end = adjusted_start + ent.end_char - ent.start_char
				entities.append(doc.char_span(adjusted_start, adjusted_end, label=ent.label_, alignment_mode="expand"))

			start_idx += stride

		return entities

	def __call__(self, doc):
		ner_spans = self.predict_with_windows(doc)

		doc.ents = filter_spans(list(doc.ents) + ner_spans)

		return doc
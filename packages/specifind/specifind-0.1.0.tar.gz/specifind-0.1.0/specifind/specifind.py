import os
import spacy
import warnings
import torch
import logging

from . import vendor
from spacy import Language, displacy
from specifind.components import NamedEntityRecognizer, CoreferenceResolution, RelationExtractor, Senter
from science_ocr import ScienceOCR


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger("specifind")
warnings.filterwarnings("ignore")
torch.set_warn_always(False)


@Language.factory("sat_senter")
def create_sentencer(nlp, name):
	return Senter()


@Language.factory("coreference_ner_extension")
def create_coreference_ner_extension(nlp, name):
	logger.info("Loading CR model")
	return CoreferenceResolution()


@Language.factory("specifind_ner")
def create_specifind_ner(nlp, name):
	logger.info("Loading NER model")
	return NamedEntityRecognizer()


@Language.factory("specifind_re")
def create_specifind_re(nlp, name):
	logger.info("Loading RE model")
	return RelationExtractor()


class Specifind:
	def __init__(self, debug=False):
		super().__init__()
		if torch.cuda.is_available():
			device_name = torch.cuda.get_device_name(0)
			try:
				spacy.require_gpu()
				print(f"Using GPU: {device_name}")
			except Exception as e:
				warnings.warn(
					f"GPU detected ({device_name}), but spaCy couldn't use it. "
					"Make sure you have a GPU-enabled PyTorch installed."
					f"Error: {str(e)}"
				)
		else:
			warnings.warn("No GPU detected, running on CPU.")

		self.nlp = spacy.Language()
		self.nlp.add_pipe("sat_senter")
		self.nlp.add_pipe("specifind_ner")
		self.nlp.add_pipe("coreference_ner_extension")
		self.nlp.add_pipe("specifind_re")

		self.ocr = ScienceOCR()
		self.debug = debug

	@staticmethod
	def _parse_ents(ents):
		geo, spe = [], []
		for ent in ents:
			if ent.label_ == 'Coref':
				for coref in ent._.coref:
					ents.append(coref)
			elif ent.label_ == 'Geography':
				geo.append(ent)
			elif ent.label_ == 'Species':
				spe.append(ent)

		return geo, spe

	def analyze_file(self, path, first_page=None, last_page=None, coref=True, dpi=None, return_doc=False):
		txt_path = f"{os.path.splitext(path)[0]}.txt"

		if os.path.exists(txt_path):
			print(f"Found OCR file! {txt_path}")
			with open(txt_path, 'r', encoding='utf-8') as f:
				full_text = f.read()
		else:
			if dpi is None:
				if torch.cuda.is_available():
					dpi = 192
					logger.info(f"GPU detected: setting {dpi} DPI for high quality OCR results. If you are running out of memory, please consider decreasing the DPI.")
				else:
					dpi = 96
					logger.info(f"No GPU found: setting {dpi} DPI. If you are running out of memory, please consider decreasing the DPI.")

			full_text = self.ocr.parse_text(path, first_page, last_page, dpi=dpi)

			with open(txt_path, 'w+', encoding='utf-8') as f:
				f.write(full_text)

		return self.analyze(full_text, coref, return_doc)

	def analyze(self, text, coref=True, return_doc=False):
		doc = self.nlp(
			text,
			component_cfg={
				"coreference_ner_extension": {"enabled": coref},
			}
		)

		if self.debug:
			displacy.serve(doc, auto_select_port=True, style="ent")

		if return_doc:
			return doc

		ner_loc = set()
		ner_spe = set()
		relations = {}
		explanation = {}

		ents = list(doc.ents)
		geo, spe = self._parse_ents(ents)
		for s in spe:
			ner_spe.add(s.text)
		for g in geo:
			ner_loc.add(g.text)

		for rel in doc._.relations:
			sent, spe, geo, _ = rel
			if spe.text not in relations:
				relations[spe.text] = set()
			relations[spe.text].add(geo.text)

			if spe.text not in explanation:
				explanation[spe.text] = {}
			if geo.text not in explanation[spe.text]:
				explanation[spe.text][geo.text] = set()

			explanation[spe.text][geo.text].add(sent.text)

		results = {
			'species': list(ner_spe),
			'geography': list(ner_loc),
			'occurrences': {key: list(value) for key, value in relations.items()},
			'evidence': {spe: {geo: list(sents) for geo, sents in value.items()} for spe, value in explanation.items()}
		}

		return results

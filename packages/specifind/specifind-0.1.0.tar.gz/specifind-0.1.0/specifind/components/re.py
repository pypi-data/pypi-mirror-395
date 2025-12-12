import torch
import itertools

from huggingface_hub import snapshot_download
from spacy.tokens import Doc
from transformers import RobertaTokenizerFast, RobertaForSequenceClassification


class RelationExtractor:
	def __init__(self):
		model_path = self.download_models()
		self.tokenizer = RobertaTokenizerFast.from_pretrained(model_path)
		self.model = RobertaForSequenceClassification.from_pretrained(model_path)
		self.model.eval()
		self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
		self.model.to(self.device)

		if not Doc.has_extension("relations"):
			Doc.set_extension("relations", default=[])

	def download_models(self):
		return snapshot_download(
			repo_id="TomasGD/specifind_re",
			repo_type="model"  # or "dataset", "space"
		)

	@staticmethod
	def collect_ents(ents):
		geo, spe, corefs = [], [], []
		for ent in ents:
			if ent.label_ == 'Coref':
				corefs.append(ent)
			elif ent.label_ == 'Geography':
				geo.append(ent)
			elif ent.label_ == 'Species':
				spe.append(ent)
			else:
				raise Exception(f"Unknown ent {ent.label_}")

		return geo, spe, corefs

	@staticmethod
	def generate_re_model_input(sent, ent1, ent1_coref, ent2, ent2_coref):
		if ent2.start < ent1.start:
			ent1, ent2 = ent2, ent1
			ent1_coref, ent2_coref = ent2_coref, ent1_coref

		text = sent.text
		e1_start = ent1.start_char - sent.start_char
		e1_end = ent1.end_char - sent.start_char

		e1_label = ent1_coref.label_[0]
		e1_text = ent1_coref.text

		e2_start = ent2.start_char - sent.start_char
		e2_end = ent2.end_char - sent.start_char

		e2_label = ent2_coref.label_[0]
		e2_text = ent2_coref.text

		return f'{text[:e1_start]}[{e1_label}] {e1_text} [/{e1_label}]{text[e1_end:e2_start]}[{e2_label}] {e2_text} [/{e2_label}]{text[e2_end:]}'

	@staticmethod
	def resolve_coreferences(ent):
		coents = {}

		for coref in ent._.coref:
			for cent in coref.ents:
				if cent.label_ == 'Coref':
					pass
				else:
					if cent.label_ not in coents:
						coents[cent.label_] = set()
					coents[cent.label_].add(cent)

		if "Species" in coents:
			return coents["Species"]
		elif "Geography" in coents:
			return coents["Geography"]
		else:
			return []

	def __call__(self, doc):
		rel_candidates = []
		for sent in doc.sents:
			geos, species, corefs = self.collect_ents(sent.ents)
			for spe in species:
				for geo in geos:
					text = RelationExtractor.generate_re_model_input(sent, spe, spe, geo, geo)
					rel_candidates.append((text, sent, spe, geo))

				for coref in corefs:
					for c in RelationExtractor.resolve_coreferences(coref):
						if c.label_ == 'Geography':
							text = RelationExtractor.generate_re_model_input(sent, spe, spe, coref, c)
							rel_candidates.append((text, sent, spe, c))

			for geo in geos:
				for coref in corefs:
					for c in RelationExtractor.resolve_coreferences(coref):
						if c.label_ == 'Species':
							text = RelationExtractor.generate_re_model_input(sent, coref, c, geo, geo)
							rel_candidates.append((text, sent, c, geo))

			for coref_1, coref_2 in itertools.combinations(corefs, 2):
				for cr_1 in RelationExtractor.resolve_coreferences(coref_1):
					for cr_2 in RelationExtractor.resolve_coreferences(coref_2):
						if {cr_1.label_, cr_2.label_} == {'Species', 'Geography'}:
							text = RelationExtractor.generate_re_model_input(sent, coref_1, cr_1, coref_2, cr_2)
							if cr_2.label_ == 'Species':
								cr_1, cr_2 = cr_2, cr_1
							rel_candidates.append((text, sent, cr_1, cr_2))


		relations = []
		if rel_candidates:
			for i in range(0, len(rel_candidates), 32):
				batch = rel_candidates[i:i + 32]
				inputs = self.tokenizer([rc[0] for rc in batch], return_tensors="pt", truncation=True, padding=True, max_length=256).to(self.device)

				with torch.no_grad():
					outputs = self.model(**inputs)
					preds = torch.argmax(outputs.logits, dim=1)

					for pred, (_, sent, ent1_coref, ent2_coref) in zip(preds, batch):
						if pred.item() == 1:
							relations.append((sent, ent1_coref, ent2_coref, "is_located"))
						# else:
						# 	print((sent, ent2_coref, ent1_coref))

		doc._.relations = relations

		return doc
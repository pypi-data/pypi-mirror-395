from fastcoref import FCoref
from collections import Counter
from spacy.util import filter_spans
from spacy.tokens import Span


class CoreferenceResolution:
	def __init__(self):
		# device to None, automatically selects cuda if available
		self.fcoref_model = FCoref(device=None, enable_progress_bar=False)

		if not Span.has_extension("coref"):
			Span.set_extension("coref", default=None)

	@staticmethod
	def resolve_cluster_entities(doc, cluster, min_confidence=0.75):
		"""
		Naive entity resolver with relative-frequency-based threshold.
		Returns the entity with highest confidence above a minimum relative threshold.
		"""
		entity_counter = Counter()
		entity_head = {}

		for span_start, span_end in cluster:
			span = doc.char_span(span_start, span_end, alignment_mode="expand")
			if not span or len(span.ents) == 0:
				continue

			entity_text = span.text.lower().strip()
			entity_counter[entity_text] += 1
			entity_head[entity_text] = span

		resolved_entities = []
		if entity_counter:
			total = sum(entity_counter.values())
			most_common_entity, freq = entity_counter.most_common(1)[0]
			relative_threshold = freq / total
			for entity, count in entity_counter.items():
				if count / total >= relative_threshold * min_confidence:
					resolved_entities.append(entity_head[entity])

		return resolved_entities

	def __call__(self, doc, enabled=False):
		if enabled:
			try:
				coref_clusters = self.fcoref_model.predict(texts=doc.text, max_tokens_in_batch=2000)
				# coref_clusters_str = coref_clusters.get_clusters(as_strings=True)
				coref_clusters = coref_clusters.get_clusters(as_strings=False)

				new_spans = []
				for (idx, cluster) in enumerate(coref_clusters):
					resolved_entities = self.resolve_cluster_entities(doc, cluster)
					if len(resolved_entities) == 0:
						continue

					for span_start, span_end in cluster:
						full_coref = doc.char_span(span_start, span_end, alignment_mode="expand")
						if not full_coref:
							raise Exception(f"Span coref {span_start}-{span_end} not found!")
						if not full_coref.ents:
							new_entity = Span(doc, full_coref.start, full_coref.end, label="Coref")
							new_entity._.coref = list(resolved_entities)
							new_spans.append(new_entity)
				if new_spans:
					doc.ents = filter_spans(list(doc.ents) + new_spans)
			except Exception as e:
				raise Exception(f"Coref failed!\n{e}")

		return doc
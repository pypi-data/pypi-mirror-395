# **Specifind**

<div style="display: flex; justify-content: center; margin-bottom: 15px;">
  <img alt="Specifind logo" src="specifind_logo.png" />
</div>

**Specifind** is a Python toolkit built to automatically extract **species occurrence information** from unstructured ecological literature. It identifies scientific species names, geographic entities, and the relations connecting them—unlocking occurrence data hidden in text.

The toolkit integrates **OCR**, **layout analysis**, **Named Entity Recognition**, **Coreference Resolution**, and **Relation Extraction** into a unified and traceable pipeline. It is powered by a newly developed, expertly annotated dataset of 1,000+ ecological abstracts spanning **biogeography, botany, entomology, mycology, and zoology**.

---
## 🌿 Key Features

* 📄 **Science-OCR** for domain-optimized OCR of scientific papers
* 🔍 **NER** for scientific species names & geographic entities
* 🌍 **Relation Extraction** connecting species to locations
* 🧠 **FastCOREF** for high-performance coreference resolution
* 🧩 **Built on spaCy** for extensibility, speed, and NLP interoperability
* 🧱 Full pipeline for **text & PDF** extraction
* 🧭 **Traceability** that links extractions back to the original text

---

## 📦 Installation

```bash
pip install specifind
```

---

## 🚀 Quick Start

### **Basic Usage**

```python
from specifind import Specifind

s = Specifind()

s.analyze("Upupa epops is an exotic bird. It is widely extended over Spain.")

# or

s.analyze_file("path/to/file.pdf")

# Output:
# {
#     "species": [
#         "Upupa epops"
#     ],
#     "geography": [
#         "Spain"
#     ],
#     "occurrences": {
#         "Upupa epops": [
#             "Spain"
#         ]
#     },
#     "evidence": {
#         "Upupa epops": {
#             "Spain": [
#                 "It is widely extended over Spain."
#             ]
#         }
#     }
# }
```

---

## 📘 API Reference

### `analyze_file(...)`

Process and extract information from a **PDF file**.

**Parameters**

| Name         | Type | Default                          | Description                                                                                            |
| ------------ | ---- |----------------------------------|--------------------------------------------------------------------------------------------------------|
| `path`       | str  | —                                | Path to the file to analyze.                                                                           |
| `first_page` | int  | 0                                | First page to process (inclusive).                                                                     |
| `last_page`  | int  | PDF page length                  | Last page to process (exclusive).                                                                      |
| `coref`      | bool | True                             | Enable coreference resolution.                                                                         |
| `dpi`        | int  | `192` if GPU available else `96` | Rendering DPI for PDF pages. Consider lowering the value if running out of memory (OOM).               |
| `return_doc` | bool | False                            | If `True`, return Spacy Doc object with the annotations available in `doc.ents` and `doc._.relations`. |

**Returns**

* Dictionary including parsed entities, relations and evidences.
* *(optional)* internal doc object (if `return_doc=True`)

---

### `analyze(...)`

Process and extract information directly from **raw text**.

**Parameters**

| Name         | Type | Default | Description                                              |
| ------------ | ---- | ------- |----------------------------------------------------------|
| `text`       | str  | —       | Raw text to analyze.                                     |
| `coref`      | bool | True    | Enable coreference resolution.                           |
| `return_doc` | bool | False   | If `True`, return Spacy Doc object with the annotations. |

**Returns**

* Dictionary including parsed entities, relations and evidences.
* *(optional)* internal doc object

---

## 🚀 **Benchmarks**

### **Named Entity Recognition (NER)**

*Species & Locations*

| 🔍 Match Type         | 🎯 Precision | 📈 Recall | 🏆 F1 |
| --------------------- | ------------ | --------- | ----- |
| **Exact**             | 0.904        | 0.935     | 0.919 |
| **Partial/Intersect** | 0.938        | 0.969     | 0.958 |

---

### **Relation Extraction (RE)**

*Occurrences*

| 🎯 Precision | 📈 Recall | 🏆 F1 |
| ------------ | --------- | ----- |
| 0.964        | 0.993     | 0.978 |


---

## 🤝 Contributing

Contributions, issue reports, and feature suggestions are welcome.
Feel free to open a Pull Request or discussion.

---

## 📄 License

**Specifind** is licensed under **AGPL-3.0**. See [LICENSE](LICENSE) for details.

---

## 📚 Citing **Specifind**

If you use **Specifind** in your research, please cite our pre-print:

### BibTeX

```bibtex
@article{specifind2025,
  title   = {Specifind: A Natural Language Processing Tool for Automating Species Occurrence (Re-)Discovery from Scientific Literature},
  author  = {Golomb Durán Tomas, Díaz Anna, Barroso María, Far Antoni Josep, Roldán Alejandro, Cancellario Tommaso},
  year    = {2025},
  journal = {BioRxiv},
  url     = {https://github.com/ToGo347/specifind}
}
```

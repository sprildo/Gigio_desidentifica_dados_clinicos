# pt_Gigio_desidentifica: Clinical NER Model for Brazilian Portuguese

## A Natural Language Processing (NLP) model developed for the de-identification and anonymization of Electronic Health Records (EHR) in Brazilian Portuguese. 
This package is built on top of [spaCy](https://spacy.io/) and specifically trained to assist medical research and healthcare institutions in complying with the Brazilian General Data Protection Law (LGPD) by identifying and masking Protected Health Information (PHI).
Details about the model's training can be found in [`docs/guidelines_anotacao.md`](docs/guidelines_anotacao.md). The data used was sourced from a single tertiary hospital in the state of São Paulo. It is strongly recommended that the model undergoes fine-tuning for generalization to other clinical contexts, and that a secondary rule-based de-identification method is utilized alongside it. This NER model was designed to work in conjunction with a previous layer of Regular Expressions (Regex) or anonymization heuristics.

### Performance by Entity

The metrics below detail the performance of the final trained model (`pt_Gigio_desidentifica`). The overall F1-score of 0.93.

| Entity Class | Precision | Recall (Sensitivity) | F1-Score |
| :--- | :--- | :--- | :--- |
| **TELEFONE** | 100.00% | 100.00% | 1.000 |
| **DOCUMENTO** | 99.61% | 99.22% | 0.994 |
| **NOME** | 97.08% | 91.99% | 0.945 |
| **REGISTRO_HOSPITAL** | 80.00% | 100.00% | 0.889 |
| **CIDADE** | 93.83% | 84.19% | 0.888 |
| **INSTITUICAO** | 75.16% | 74.19% | 0.747 |
| **GLOBAL (All)** | **95.42%** | **90.94%** | **0.931** |

The `ENDERECO` entity is part of the model's vocabulary but does not appear in this evaluation report, likely due to a lack of occurrences in the specific test dataset.*

### Requirements
spaCy: 3.8.14
Pandas: 2.2.2
NumPy: 2.4.4


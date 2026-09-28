# pt_Gigio_desidentifica: Clinical NER Model for Brazilian Portuguese


## A Natural Language Processing (NLP) model developed for the de-identification and anonymization of Electronic Health Records (EHR) in Brazilian Portuguese. 
This package is built on top of [spaCy](https://spacy.io/) and specifically trained to assist medical research and healthcare institutions in complying with the Brazilian General Data Protection Law (LGPD) by identifying and masking Protected Health Information (PHI).
Details about the model's training can be found in [`docs/guidelines_anotacao.md`](docs/guidelines_anotacao.md). The data used was sourced from a single tertiary hospital in the state of São Paulo. It is strongly recommended that the model undergoes fine-tuning for generalization to other clinical contexts, and that a secondary rule-based de-identification method is utilized alongside it. This NER model was designed to work in conjunction with a previous layer of Regular Expressions (Regex) or anonymization heuristics.

### Versions

Repository release v1.1.0. Model package: `pt_Gigio_desidentifica` 1.0.0 (all reported metrics refer to this model version; the model was not retrained after release v1.0.0).

### Performance by Entity

The metrics below were obtained for the model package `pt_Gigio_desidentifica` 1.0.0 on the held-out test set (n = 550 hospital admissions; see the article for its composition). Overall F1-score: 0.9168.

| Entity Class | N | Precision | Recall (Sensitivity) | F1-Score |
| :--- | ---: | :--- | :--- | :--- |
| **NOME** | 6646 | 95.26% | 92.33% | 0.9377 |
| **DOCUMENTO** | 915 | 97.87% | 95.30% | 0.9657 |
| **CIDADE** | 542 | 95.29% | 70.85% | 0.8127 |
| **INSTITUICAO** | 397 | 78.54% | 48.87% | 0.6025 |
| **TELEFONE** | 79 | 93.18% | 51.90% | 0.6667 |
| **ENDERECO** | 21 | 0% | 0% | 0.0 |
| **REGISTRO_HOSPITAL** | 3 | 0% | 0% | 0.0 |
| **GLOBAL (All)** | **8603** | **94.91%** | **88.66%** | **0.9168** |

N = number of annotated entities (TP + FN). REGISTRO_HOSPITAL occurred only 3 times in the test set, so its estimate is unreliable. Human review of the output is mandatory.

### Installation

To use the **pt_Gigio_desidentifica** model:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sprildo/Gigio_desidentifica_dados_clinicos/blob/main/exemplo_de_uso.ipynb)

```bash
pip install "pt_Gigio_desidentifica @ https://github.com/sprildo/Gigio_desidentifica_dados_clinicos/releases/download/v1.0.0/pt_Gigio_desidentifica-1.0.0-py3-none-any.whl"
```
Note: tratar_texto is not included in the installed package. It is distributed separately as scripts/preprocessamento.py in this repository and can only be used after cloning the repository — it cannot be imported from the pip-installed package alone.

### Usage

```python
import spacy
# Importing the handling function from your scripts folder.
from scripts.preprocessamento import tratar_texto

# Carregando o modelo NER
nlp = spacy.load("pt_Gigio_desidentifica")

# 1. Texto original (exemplo)
texto_bruto = """# ID: MARIA MIGUEL SOUZA, 52 ANOS, PROCEDENTE DE RIBEIRÃO PRETO, NATURAL DE Pontal
reg: 004567a, contato telefone: (16) 99999-1111

# QUEIXA PRINCIPAL: DISARTRIA E DIFICULDADE PARA DEAMBULAR HÁ 1 DIA. 

# HMA: PACIENTE VEM À UNIDADE POR DEMANDA ESPONTÂNEA ACOMPANHADA DA FILHA Juliana REFERINDO QUE ACORDOU ONTEM
COM DISARTRIA E PERDA DE FORÇA EM MEMBRO INFERIOR DIREITO DIFICULTANDO DEAMBULAÇÃO. FILHA REFERE QUE NO DIA
ANTEIROR MÃE ENCONTRAVA-SE BEM, SEM DEFICITS FOCAIS. AINDA ONTEM DE MANHÃ, FILHA LEVOU MÃE AO
PRONTO SOCORRO Hospital Santo Antonio, ONDE FOI AVALIADA POR NEUROLOGISTA, QUE INFORMOU BAIXA PROBABILIDADE
DE SER SECUNDARIO A AVC E ORIENTOU QUE ELA DEVERIA REALIZAR EXAME DE IMAGEM. INFORMA QUE HOJE PERCEBEU PERDA DE FORÇA EM MSD. 
REFERE QUE QUINTA FEIRA MEDICOS PRESCREVERAM MORFINA 10MG 4/4H + DIPIRONA PARA CONTROLE ALGICO.
FOI PRESCRITO TAMBEM BISACODIL E LACTULOSE. REFERE CONSTIPAÇÃO DESDE SABADO. DIURESE PRESENTE, SEM PRODUTOS PATOLOGICOS,
SEM DISURIA. REFERE BEIXA ACEITAÇÃO DA DIETA HÁ 2 DIAS. BOA INGESTA DE LIQUIDOS. 
REFERE QUE HÁ 30 DIAS REALIZOU FIXACAO PROFILATICA EM TIBIA ESQUERDA POR LESÃO LITICA (META?)

#AP:
1) NÓDULO PULMONAR A DIREITA
- realizada bx por broncoscopia em 17/07, sem intercorrências, aguarda ap
- PET-CT METABOLISMO GLICOLÍTICO EM LINFONODOS DE CADEIA TORÁCICA INTERNA, MEDIASTINAL E HILAR PULMONAR DIREITA,
CERVICAIS DIREITA, REGIÃO INGUINAL DIREITA, LESÕES OSTEOLÍTICAS EM 9º ARCO COSTAL DIREITO, ÍSQUIO E TÍBIA DIREITA.
SE CONFIRMAÇÃO DE SÍTIO PRIMÁRIO PULMONAR PROVÁVEL T1CN3M1C exame número:123485679

2) DPOC GOLD IIIB

3) LESÃO LÍTICA NA TÍBIA DIREITA (META PULMONAR?)
23/07 - FIXAÇÃO PROFILÁTICA DE TIBIA ESQUERDA COM HASTE INTRAMEDULAR

# MUC:
- MORFINA 10MG 4/4H
- DIPIRONA 1G 6/6H SN
- LACTULOSE
- BISACODIL
- ANORO 1 PUFF/DIA

# ALERGIAS: NEGA
Discutido com Prof. Antonio e Dra. Iara, condudas mantidas"""

# 2. text processing
texto_tratado = tratar_texto(texto_bruto)

# 3. NER Model
doc = nlp(texto_tratado)

# 4. Results
print(f"Texto após tratamento: {texto_tratado}\n")
for ent in doc.ents:
    print(f"Entidade: {ent.text} | Categoria: {ent.label_}")


# 5. Masking (performed by the calling application, not by the package)
texto_mascarado = texto_tratado
for ent in sorted(doc.ents, key=lambda e: e.start_char, reverse=True):
    texto_mascarado = texto_mascarado[:ent.start_char] + f"[{ent.label_}]" + texto_mascarado[ent.end_char:]
print(texto_mascarado)

```

### expected results

Entidade: maria miguel souza | Categoria: NOME <br>
Entidade: ribeirão preto | Categoria: CIDADE<br>
Entidade: pontal | Categoria: CIDADE<br>
Entidade: 004567a | Categoria: REGISTRO_HOSPITAL<br>
Entidade: 16 99999-1111 | Categoria: TELEFONE<br>
Entidade: juliana | Categoria: NOME<br>
Entidade: hospital santo antonio | Categoria: INSTITUICAO<br>
Entidade: número:123485679 | Categoria: DOCUMENTO<br>
Entidade: antonio | Categoria: NOME<br>
Entidade: iara | Categoria: NOME<br>

### how to cite

### How to cite

**APA:**

> Silva, Rildo Pinto da; Pazin-Filho, Antonio (2026). *pt_Gigio_desidentifica: Modelo NER para Desidentificação de Dados Clínicos em Português* (Version 1.1.0) [Software]. GitHub. https://github.com/sprildo/Gigio_desidentifica_dados_clinicos

**BibTeX:**

```bibtex
@software{pt_gigio_desidentifica,
  author  = {Silva, Rildo Pinto da and Pazin-Filho, Antonio},
  title   = {pt_Gigio_desidentifica: Modelo NER para Desidentificação de Dados Clínicos em Português},
  year    = {2026},
  version = {1.1.0},
  url     = {https://github.com/sprildo/Gigio_desidentifica_dados_clinicos}
}
```

## Acknowledgements
APF author CNPq Research Productivity Scholarship - Level 2 Brazil - 303187/2022-0

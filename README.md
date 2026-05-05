# pt_Gigio_desidentifica: Clinical NER Model for Brazilian Portuguese

[![DOI](https://zenodo.org/badge/1216268919.svg)](https://doi.org/10.5281/zenodo.19678716)


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

### Installation

To use the **pt_Gigio_desidentifica** template:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sprildo/Gigio_desidentifica_dados_clinicos/blob/main/exemplo_de_uso.ipynb)

```bash
pip install "pt_Gigio_desidentifica @ https://github.com/sprildo/Gigio_desidentifica_dados_clinicos/releases/download/v1.0.0/pt_Gigio_desidentifica-1.0.0-py3-none-any.whl"
```

### Usage

```bash
import spacy
# Importing the handling function from your scripts folder.
from scripts.preprocessamento import tratar_texto

# Carregando o modelo NER
nlp = spacy.load("pt_Gigio_desidentifica")

# 1. Texto original (exemplo)
texto_bruto = "# ID: MARIA MIGUEL SOUZA, 52 ANOS, PROCEDENTE DE RIBEIRÃO PRETO, NATURAL DE Pontal
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
Discutido com Prof. Antonio e Dra. Iara, contudas mantidas"

# 2. text processing
texto_tratado = tratar_texto(texto_bruto)

# 3. NER Model
doc = nlp(texto_tratado)

# 4. Results
print(f"Texto após tratamento: {texto_tratado}\n")
for ent in doc.ents:
    print(f"Entidade: {ent.text} | Categoria: {ent.label_}")
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

**Formato APA:**

> Silva, Rildo Pinto da.; Pazin-Filho, Antonio (2026). *pt_Gigio_desidentifica: Modelo NER para Desidentificação de Dados Clínicos em Português* [Software]. Zenodo. https://doi.org/10.5281/zenodo.19678717

**BibTeX:**

```bibtex
@software{pt_gigio_desidentifica,
  author       = {Silva, Rildo Pinto da, Pazin-Filho, Antonio}
  title        = {pt_Gigio_desidentifica: Modelo NER para Desidentificação de Dados Clínicos em Português},
  year         = {2026},
  publisher    = {Zenodo},
  doi          = {https://doi.org/10.5281/zenodo.19678717}
}
```

## Acknowledgements
APF author CNPq Research Productivity Scholarship - Level 2 Brazil - 303187/2022-0

# test_ner_pipeline.py
import pytest
import spacy

LABELS_ESPERADOS = {"NOME", "TELEFONE", "DOCUMENTO", "REGISTRO_HOSPITAL", "CIDADE", "INSTITUICAO", "ENDERECO"}


@pytest.fixture(scope="module")
def nlp():
    return spacy.load("pt_Gigio_desidentifica")


def test_model_loads_successfully(nlp):
    assert nlp is not None


def test_pipeline_has_ner_component(nlp):
    assert "ner" in nlp.pipe_names


def test_predicted_labels_are_within_expected_taxonomy(nlp):
    doc = nlp("paciente joão silva, telefone (16) 99999-8888, internado em ribeirão preto")
    for ent in doc.ents:
        assert ent.label_ in LABELS_ESPERADOS


def test_detects_at_least_one_entity_in_simple_example(nlp):
    doc = nlp("paciente maria oliveira, telefone (16) 98888-7777")
    assert len(doc.ents) > 0

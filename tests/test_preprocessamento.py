# test_preprocessamento.py
import pytest
from scripts.preprocessamento import tratar_texto


def test_lowercases_text():
    assert tratar_texto("Paciente CARLOS") == "paciente carlos"


def test_masks_hospital_registration_number():
    resultado = tratar_texto("registro 1234567a do paciente")
    assert "[registro]" in resultado
    assert "1234567a" not in resultado


def test_does_not_mask_numbers_of_different_length():
    # 8 dígitos não deve ser mascarado pelo padrão de registro (7 dígitos + letra)
    resultado = tratar_texto("numero 12345678a de identificacao")
    assert "[registro]" not in resultado


def test_removes_hashtags_and_quotes():
    resultado = tratar_texto('paciente #1 disse "estou bem"')
    assert "#" not in resultado
    assert '"' not in resultado


def test_replaces_parentheses_with_space():
    resultado = tratar_texto("exame (normal) hoje")
    assert "(" not in resultado
    assert ")" not in resultado


def test_replaces_underscores_with_space():
    resultado = tratar_texto("campo___vazio")
    assert "_" not in resultado


def test_collapses_repeated_symbols():
    resultado = tratar_texto("linha ---- separadora")
    assert "----" not in resultado


def test_normalizes_whitespace_and_strips():
    resultado = tratar_texto("   texto   com   espacos   \n\n\n")
    assert resultado == resultado.strip()
    assert "   " not in resultado

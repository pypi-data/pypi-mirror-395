# test/test_operacoes.py
from matematica_utils.operacoes import somar, subtrair, multiplicacao, divisao

def test_somar():
    assert somar(2, 3) == 5

def test_subtrair():
    assert subtrair(4, 3) == 1

def test_multiplicacao():
    assert multiplicacao(2, 3) == 6

def test_divisao():
    assert divisao(10, 2) == 5


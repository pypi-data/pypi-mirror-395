# test_nie.py

import pytest
from PyDNI import verificar_nie

def test_nie_valido():
    assert verificar_nie("X1234567L") is True

def test_nie_invalido_letra_control():
    assert verificar_nie("X1234567A") is False

def test_nie_invalido_formato():
    assert verificar_nie("Y12L") is False

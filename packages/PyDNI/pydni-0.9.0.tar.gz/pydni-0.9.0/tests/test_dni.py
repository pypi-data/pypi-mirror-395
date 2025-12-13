# test_dni.py

import pytest
from PyDNI import verificar_dni

def test_dni_valido():
    assert verificar_dni("12345678Z") is True

def test_dni_invalido_letra():
    assert verificar_dni("12345678A") is False

def test_dni_invalido_formato():
    assert verificar_dni("1234Z") is False
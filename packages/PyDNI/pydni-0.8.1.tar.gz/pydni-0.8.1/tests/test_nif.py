# test_nif.py

import pytest
from PyDNI import verificar_nif

def test_nif_dni_valido():
    assert verificar_nif("12345678Z") == "DNI válido"

def test_nif_nie_valido():
    assert verificar_nif("X1234567L") == "NIE válido"

def test_nif_cif_valido():
    assert verificar_nif("A58818501") == "CIF válido"

def test_nif_invalido():
    assert verificar_nif("00000000A") == "DNI no válido"

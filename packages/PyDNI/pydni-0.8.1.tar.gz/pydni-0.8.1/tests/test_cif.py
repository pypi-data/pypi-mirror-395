# test_cif.py

import pytest
from PyDNI import verificar_cif

def test_cif_valido_telefonica():
    # CIF real de Telefónica
    assert verificar_cif("A58818501") is True

def test_cif_valido_ayuntamiento_madrid():
    # CIF real de Ayuntamiento de Madrid (excepción)
    assert verificar_cif("Q2816003A") is True

def test_cif_invalido():
    assert verificar_cif("B12345678") is False

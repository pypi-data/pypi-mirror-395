# test_utils.py

import pytest
from PyDNI import verificar_identificador

def test_identificador_dni():
    assert verificar_identificador("12345678Z") == "DNI válido"

def test_identificador_nie():
    assert verificar_identificador("X1234567L") == "NIE válido"

def test_identificador_cif():
    assert verificar_identificador("A58818501") == "CIF válido"

def test_identificador_formato_invalido():
    assert verificar_identificador("ABC") == "Formato no reconocido"

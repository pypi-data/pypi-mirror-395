from .dni import verificar_dni
from .cif import verificar_cif
from .nie import verificar_nie
from .nif import verificar_nif
from .utils import verificar_identificador
from .generator import Generator
from .emails import EmailGenerator
from .birthdates import BirthDateGenerator
from .phone import PhoneGenerator
from .faker_provider import PyDNIFakerProvider

__all__ = [
    "verificar_dni",
    "verificar_cif",
    "verificar_nie",
    "verificar_nif",
    "verificar_identificador",
    "Generator",
    "EmailGenerator",
    "BirthDateGenerator",
    "PhoneGenerator",
    "PyDNIFakerProvider",
]

__version__ = "0.9.0"

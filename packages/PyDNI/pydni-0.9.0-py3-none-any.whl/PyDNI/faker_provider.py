from faker.providers import BaseProvider
from .generator import Generator


class PyDNIFakerProvider(BaseProvider):
    """
    Provider oficial de PyDNI para Faker
    Permite generar personas, DNIs, NIEs, CIFs, teléfonos, emails y fechas
    """

    def __init__(self, generator=None):
        super().__init__(generator)
        self.gen = Generator()

    def dni(self):
        return self.gen.generar_dni()

    def nie(self):
        return self.gen.generar_nie()

    def cif(self):
        return self.gen.generar_cif()

    def documento(self):
        return self.gen.generar_documento()

    def persona(self, sexo=None, tipo_doc=None, edad="aleatorio"):
        return self.gen.generar_persona(sexo=sexo, tipo_doc=tipo_doc, edad=edad)

    def nombre(self, sexo=None):
        return self.gen.generar_nombre(sexo)

    def email_persona(self, dominio=None):
        persona = self.gen.generar_persona()
        if dominio:
            return self.gen.email_gen.generar_email_nombre(
                persona["nombre"], dominio
            )
        return persona["email"]

    def telefono(self, tipo="movil"):
        return self.gen.phone_gen.generar_telefono(tipo)

    def fecha_nacimiento(self, tipo="aleatorio"):
        return self.gen.birth_gen.generar_fecha(tipo)

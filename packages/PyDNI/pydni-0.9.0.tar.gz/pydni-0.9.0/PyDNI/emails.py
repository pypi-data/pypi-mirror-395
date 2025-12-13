import random
import string
import unicodedata


class EmailGenerator:
    DOMINIOS_POR_DEFECTO = [
        "gmail.com",
        "hotmail.com",
        "yahoo.es",
        "outlook.com",
        "proton.me",
        "icloud.com"
    ]

    def _limpiar(self, texto: str) -> str:
        """
        Elimina acentos y caracteres especiales.
        """
        return "".join(
            c
            for c in unicodedata.normalize("NFD", texto)
            if unicodedata.category(c) != "Mn"
        ).lower()

    def generar_email_aleatorio(self, dominio: str | None = None) -> str:
        """
        Genera un email aleatorio:
        - usuario aleatorio de 8–12 caracteres
        - dominio aleatorio o indicado por el usuario
        """
        letras = string.ascii_lowercase + string.digits
        usuario = "".join(random.choices(letras, k=random.randint(8, 12)))

        if dominio is None:
            dominio = random.choice(self.DOMINIOS_POR_DEFECTO)

        return f"{usuario}@{dominio}"

    def generar_email_nombre(self, nombre_completo: str, dominio: str | None = None) -> str:
        """
        Genera un email basado en:
        - primera letra del nombre
        - primer apellido
        Ej: 'María Ruiz Gómez' → mruiz@dominio.com
        """
        partes = nombre_completo.split()
        if len(partes) < 3:
            raise ValueError("El nombre completo debe incluir nombre y dos apellidos.")

        nombre = self._limpiar(partes[0])
        apellido1 = self._limpiar(partes[-2])

        usuario = f"{nombre[0]}{apellido1}"

        if dominio is None:
            dominio = random.choice(self.DOMINIOS_POR_DEFECTO)

        return f"{usuario}@{dominio}"

    def generar_email(self, nombre_completo: str | None = None, dominio: str | None = None) -> str:
        """
        Genera un email:
        - Si se pasa nombre completo → email personalizado.
        - Si no → email aleatorio.
        """
        if nombre_completo:
            return self.generar_email_nombre(nombre_completo, dominio)
        else:
            return self.generar_email_aleatorio(dominio)

from datetime import date, timedelta
import random


class BirthDateGenerator:
    """
    Genera fechas de nacimiento realistas para pruebas.
    Permite generar:
    - Personas menores de edad (<18)
    - Personas adultas (≥18)
    - Fechas aleatorias sin restricciones
    - Fechas con rango personalizado
    """

    def __init__(self, seed: int | None = None):
        if seed is not None:
            random.seed(seed)

    @staticmethod
    def _random_date_between(start: date, end: date) -> date:
        """Devuelve una fecha aleatoria entre dos fechas."""
        delta = end - start
        dias = random.randint(0, delta.days)
        return start + timedelta(days=dias)


    def menor_de_edad(self) -> date:
        """Devuelve una fecha para alguien con 0-17 años."""
        hoy = date.today()
        fecha_max = hoy  # recién nacido
        fecha_min = hoy.replace(year=hoy.year - 18)  # casi 18 pero aún menor
        return self._random_date_between(fecha_min, fecha_max)

    def mayor_de_edad(self) -> date:
        """Devuelve una fecha para alguien con ≥18 años."""
        hoy = date.today()
        fecha_max = hoy.replace(year=hoy.year - 18)
        fecha_min = hoy.replace(year=hoy.year - 100)
        return self._random_date_between(fecha_min, fecha_max)

    def aleatoria(self) -> date:
        """Devuelve una fecha aleatoria sin requisitos de edad."""
        hoy = date.today()
        fecha_min = hoy.replace(year=hoy.year - 100)
        fecha_max = hoy
        return self._random_date_between(fecha_min, fecha_max)

    def rango(self, edad_min: int, edad_max: int) -> date:
        """Genera una fecha para una edad dentro del rango dado."""
        hoy = date.today()
        fecha_max = hoy.replace(year=hoy.year - edad_min)
        fecha_min = hoy.replace(year=hoy.year - edad_max - 1)
        return self._random_date_between(fecha_min, fecha_max)

    def generar(self, tipo: str = "aleatorio") -> date:
        """
        Genera una fecha según el tipo:
        - 'menor'   → <18
        - 'mayor'   → ≥18
        - 'aleatorio'
        """
        tipo = tipo.lower()

        if tipo == "menor":
            return self.menor_de_edad()

        if tipo == "mayor":
            return self.mayor_de_edad()

        if tipo in ("aleatorio", "random"):
            return self.aleatoria()

        raise ValueError(f"Tipo de fecha desconocido: {tipo}")

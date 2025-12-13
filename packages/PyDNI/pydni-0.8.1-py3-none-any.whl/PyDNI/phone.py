import random

class PhoneGenerator:
    def generar_movil(self) -> str:
        prefijo = random.choice(["6", "7"])
        return prefijo + "".join(str(random.randint(0, 9)) for _ in range(8))

    def generar_fijo(self) -> str:
        prefijo = random.choice(["8", "9"])
        return prefijo + "".join(str(random.randint(0, 9)) for _ in range(8))

    def generar_telefono(self, tipo: str = "AUTO") -> str:
        tipo = tipo.upper()
        if tipo == "MOVIL":
            return self.generar_movil()
        elif tipo == "FIJO":
            return self.generar_fijo()
        elif tipo == "AUTO":
            return random.choice([self.generar_movil, self.generar_fijo])()
        else:
            raise ValueError("Tipo de teléfono inválido")

# generator.py

import random
from .dni import verificar_dni
from .cif import verificar_cif
from .emails import EmailGenerator
from .birthdates import BirthDateGenerator
from .phone import PhoneGenerator


LETRAS_DNI = "TRWAGMYFPDXBNJZSQVHLCKE"
LETRAS_CIF = "ABCDEFGHJKLMNPQRSUVW"


class Generator:
    """Generador de DNIs, NIEs, CIFs, NIF y nombres para pruebas."""

    NOMBRES_MASCULINOS = ['ANTONIO', 'MANUEL', 'JOSE', 'FRANCISCO', 'DAVID', 'JAVIER', 'DANIEL', 'JUAN', 'JOSE ANTONIO', 'FRANCISCO JAVIER', 'JOSE LUIS', 'CARLOS', 'ALEJANDRO', 'JESUS', 'JOSE MANUEL', 'MIGUEL', 'MIGUEL ANGEL', 'PABLO', 'RAFAEL', 'SERGIO', 'ANGEL', 'PEDRO', 'JORGE', 'FERNANDO', 'JOSE MARIA', 'ALBERTO', 'LUIS', 'ALVARO', 'ADRIAN', 'JUAN CARLOS', 'DIEGO', 'JUAN JOSE', 'RAUL', 'IVAN', 'RUBEN', 'JUAN ANTONIO', 'OSCAR', 'ENRIQUE', 'JUAN MANUEL', 'MARIO', 'SANTIAGO', 'ANDRES', 'RAMON', 'VICTOR', 'VICENTE', 'JOAQUIN', 'EDUARDO', 'HUGO', 'MARCOS', 'ROBERTO', 'JAIME', 'FRANCISCO JOSE', 'IGNACIO', 'JORDI', 'MOHAMED', 'ALFONSO', 'RICARDO', 'MARTIN', 'MARC', 'SALVADOR', 'GABRIEL', 'GUILLERMO', 'GONZALO', 'EMILIO', 'JOSE MIGUEL', 'NICOLAS', 'LUCAS', 'JULIO', 'JULIAN', 'TOMAS', 'SAMUEL', 'AGUSTIN', 'ISMAEL', 'CRISTIAN', 'JOSE RAMON', 'JOAN', 'AITOR', 'HECTOR', 'ALEX', 'MATEO', 'FELIX', 'IKER', 'JUAN FRANCISCO', 'JOSE CARLOS', 'SEBASTIAN', 'RODRIGO', 'CESAR', 'JOSEP', 'JOSE ANGEL', 'ALFREDO', 'VICTOR MANUEL', 'MARIANO', 'JOSE IGNACIO', 'DOMINGO', 'FELIPE', 'LUIS MIGUEL', 'PAU', 'MOHAMMED', 'IZAN', 'XAVIER', 'JOSE', 'ANTONIO', 'JUAN', 'MANUEL', 'FRANCISCO', 'LUIS', 'JAVIER', 'MIGUEL', 'CARLOS', 'ANGEL', 'JESUS', 'DAVID', 'DANIEL', 'ALEJANDRO', 'PEDRO', 'ALBERTO', 'PABLO', 'MARIA', 'FERNANDO', 'RAFAEL', 'JORGE', 'RAMON', 'SERGIO', 'ANDRES', 'DIEGO', 'ENRIQUE', 'ADRIAN', 'VICTOR', 'ALVARO', 'VICENTE', 'IGNACIO', 'RAUL', 'EDUARDO', 'IVAN', 'OSCAR', 'RUBEN', 'SANTIAGO', 'JOAQUIN', 'MARIO', 'GABRIEL', 'ROBERTO', 'MARCOS', 'ALFONSO', 'JAIME', 'HUGO', 'RICARDO', 'MARTIN', 'JULIO', 'MOHAMED', 'EMILIO', 'GUILLERMO', 'NICOLAS', 'SALVADOR', 'TOMAS', 'GONZALO', 'JULIAN', 'JORDI', 'CRISTIAN', 'CESAR', 'MARC', 'AGUSTIN', 'SEBASTIAN', 'LUCAS', 'SAMUEL', 'FELIX', 'JOAN', 'JOSEP', 'HECTOR', 'FELIPE', 'ISMAEL', 'ALFREDO', 'ALEXANDER', 'MATEO', 'ALEX', 'DOMINGO', 'RODRIGO', 'AITOR', 'IKER', 'MARIANO', 'MARCO', 'ESTEBAN', 'XAVIER', 'ARTURO', 'DARIO', 'JOEL', 'GREGORIO', 'AARON', 'LORENZO', 'MOHAMMED', 'ISAAC', 'BORJA', 'ALBERT', 'ERIC', 'JONATHAN', 'OMAR', 'CHRISTIAN', 'BRUNO', 'PAU', 'IZAN', 'CRISTOBAL']
    NOMBRES_FEMENINOS = ['MARIA CARMEN', 'MARIA', 'CARMEN', 'ANA MARIA', 'LAURA', 'MARIA PILAR', 'MARIA DOLORES', 'ISABEL', 'ANA', 'MARIA TERESA', 'JOSEFA', 'MARTA', 'CRISTINA', 'LUCIA', 'MARIA ANGELES', 'MARIA JOSE', 'MARIA ISABEL', 'FRANCISCA', 'ANTONIA', 'SARA', 'PAULA', 'DOLORES', 'ELENA', 'MARIA LUISA', 'RAQUEL', 'ROSA MARIA', 'MANUELA', 'MARIA JESUS', 'JULIA', 'PILAR', 'CONCEPCION', 'ALBA', 'MERCEDES', 'BEATRIZ', 'SILVIA', 'NURIA', 'IRENE', 'PATRICIA', 'ROCIO', 'ANDREA', 'ROSARIO', 'MONTSERRAT', 'JUANA', 'MONICA', 'TERESA', 'ENCARNACION', 'ALICIA', 'MARIA MAR', 'MARINA', 'SANDRA', 'SONIA', 'NATALIA', 'SOFIA', 'SUSANA', 'ANGELA', 'YOLANDA', 'CLAUDIA', 'ROSA', 'CARLA', 'EVA', 'MARGARITA', 'MARIA JOSEFA', 'INMACULADA', 'ANA ISABEL', 'MARIA MERCEDES', 'MARIA ROSARIO', 'NOELIA', 'DANIELA', 'ESTHER', 'VERONICA', 'CAROLINA', 'MARTINA', 'NEREA', 'INES', 'MIRIAM', 'EVA MARIA', 'MARIA VICTORIA', 'LORENA', 'MARIA ELENA', 'ANA BELEN', 'VICTORIA', 'MARIA ROSA', 'ALEJANDRA', 'ANGELES', 'MARIA CONCEPCION', 'CELIA', 'LIDIA', 'FATIMA', 'MARIA ANTONIA', 'AMPARO', 'AINHOA', 'OLGA', 'CATALINA', 'MARIA NIEVES', 'CLARA', 'ADRIANA', 'VALERIA', 'ANNA', 'MARIA CRISTINA', 'EMMA', 'MARIA', 'CARMEN', 'ANA', 'ISABEL', 'DOLORES', 'PILAR', 'TERESA', 'ROSA', 'JOSEFA', 'CRISTINA', 'LAURA', 'ANGELES', 'ELENA', 'LUCIA', 'ANTONIA', 'MARTA', 'FRANCISCA', 'MERCEDES', 'LUISA', 'PAULA', 'JOSE', 'ROSARIO', 'CONCEPCION', 'SARA', 'RAQUEL', 'PATRICIA', 'ROCIO', 'EVA', 'BEATRIZ', 'ANDREA', 'VICTORIA', 'JULIA', 'MANUELA', 'JESUS', 'JUANA', 'BELEN', 'ALBA', 'SILVIA', 'ESTHER', 'SOFIA', 'IRENE', 'NURIA', 'SANDRA', 'ANGELA', 'MONICA', 'MONTSERRAT', 'ENCARNACION', 'ALICIA', 'MARINA', 'INMACULADA', 'MAR', 'SONIA', 'YOLANDA', 'CLAUDIA', 'NATALIA', 'CAROLINA', 'SUSANA', 'MARGARITA', 'ALEJANDRA', 'DANIELA', 'INES', 'CARLA', 'VERONICA', 'GLORIA', 'LUZ', 'LOURDES', 'AMPARO', 'LORENA', 'FATIMA', 'NIEVES', 'SOLEDAD', 'NOELIA', 'BEGOÑA', 'BLANCA', 'OLGA', 'MARTINA', 'MIRIAM', 'NEREA', 'CLARA', 'ADRIANA', 'MILAGROS', 'LIDIA', 'ESPERANZA', 'ANNA', 'CONSUELO', 'ASUNCION', 'CATALINA', 'CELIA', 'VALENTINA', 'VALERIA', 'DIANA', 'AURORA', 'GABRIELA', 'MAGDALENA', 'ALEXANDRA', 'ELIZABETH', 'VANESA', 'ELISA', 'AINHOA', 'EMILIA']
    APELLIDOS = ['GARCIA', 'RODRIGUEZ', 'GONZALEZ', 'FERNANDEZ', 'LOPEZ', 'MARTINEZ', 'SANCHEZ', 'PEREZ', 'GOMEZ', 'MARTIN', 'JIMENEZ', 'HERNANDEZ', 'RUIZ', 'DIAZ', 'MORENO', 'MUÑOZ', 'ALVAREZ', 'ROMERO', 'GUTIERREZ', 'ALONSO', 'TORRES', 'NAVARRO', 'DOMINGUEZ', 'RAMIREZ', 'RAMOS', 'VAZQUEZ', 'GIL', 'SERRANO', 'MORALES', 'MOLINA', 'SUAREZ', 'CASTRO', 'BLANCO', 'DELGADO', 'ORTEGA', 'ORTIZ', 'MARIN', 'RUBIO', 'MEDINA', 'NUÑEZ', 'CASTILLO', 'SANZ', 'CORTES', 'IGLESIAS', 'SANTOS', 'GARRIDO', 'GUERRERO', 'LOZANO', 'FLORES', 'CANO', 'CRUZ', 'MENDEZ', 'HERRERA', 'PEÑA', 'PRIETO', 'LEON', 'CABRERA', 'MARQUEZ', 'REYES', 'GALLEGO', 'VIDAL', 'CALVO', 'CAMPOS', 'VEGA', 'FUENTES', 'AGUILAR', 'CARRASCO', 'VARGAS', 'CABALLERO', 'DIEZ', 'NIETO', 'SANTANA', 'GIMENEZ', 'HIDALGO', 'MONTERO', 'ROJAS', 'BENITEZ', 'PASCUAL', 'HERRERO', 'ARIAS', 'SANTIAGO', 'LORENZO', 'DURAN', 'MORA', 'IBAÑEZ', 'FERRER', 'CARMONA', 'VICENTE', 'SOTO', 'ROMAN', 'CRESPO', 'RIVERA', 'PARRA', 'SILVA', 'VELASCO', 'PASTOR', 'BRAVO', 'SAEZ', 'MOYA', 'MENDOZA']

    def __init__(self):
        self.email_gen = EmailGenerator()
        self.birth_gen = BirthDateGenerator()
        self.phone_gen = PhoneGenerator()

    def generar_dni(self) -> str:
        numero = random.randint(0, 99999999)
        letra = LETRAS_DNI[numero % 23]
        return f"{numero:08d}{letra}"

    def generar_nie(self) -> str:
        inicial = random.choice("XYZ")
        numero = random.randint(0, 9999999)
        # Transformación NIE → DNI para cálculo
        mapa = {"X": "0", "Y": "1", "Z": "2"}
        numero_transformado = int(mapa[inicial] + f"{numero:07d}")
        letra = LETRAS_DNI[numero_transformado % 23]
        return f"{inicial}{numero:07d}{letra}"

    def generar_cif(self) -> str:
        inicial = random.choice(LETRAS_CIF)
        numero = f"{random.randint(0, 9999999):07d}"

        # Cálculo control (AEAT)
        suma_pares = sum(int(numero[i]) for i in range(1, 7, 2))
        suma_impares = 0
        for i in range(0, 7, 2):
            doble = int(numero[i]) * 2
            suma_impares += doble if doble < 10 else doble - 9

        total = suma_pares + suma_impares
        digito = (10 - (total % 10)) % 10

        control_letras = "JABCDEFGHI"
        control_letra = control_letras[digito]

        # Reglas según tipo
        if inicial in "PQRSNW":     # Solo letra
            control = control_letra
        elif inicial in "ABEH":     # Solo número
            control = str(digito)
        else:                       # Ambos válidos
            control = random.choice([str(digito), control_letra])

        return f"{inicial}{numero}{control}"

    def generar_varios(self, cantidad: int, tipo: str) -> list:
        """Genera una lista de documentos válidos sin repetir."""
        generados = set()

        while len(generados) < cantidad:
            if tipo == "DNI":
                doc = self.generar_dni()
            elif tipo == "NIE":
                doc = self.generar_nie()
            elif tipo == "CIF":
                doc = self.generar_cif()
            elif tipo == "AUTO":
                # Genera un tipo aleatorio
                doc = random.choice([
                    self.generar_dni(),
                    self.generar_nie(),
                    self.generar_cif()
                ])
            else:
                raise ValueError("Tipo no reconocido (DNI, NIE, CIF, AUTO)")

            generados.add(doc)

        return list(generados)
    
    def generar_nombre(self, sexo: str | None = None) -> str:
        sexo = sexo.lower() if sexo else "aleatorio"

        if sexo == "aleatorio":
            sexo = random.choice(["masculino", "femenino"])

        if sexo not in ["masculino", "femenino"]:
            raise ValueError("El sexo debe ser 'masculino', 'femenino' o 'aleatorio'")

        if sexo == "masculino":
            nombre = random.choice(self.NOMBRES_MASCULINOS)
        else:
            nombre = random.choice(self.NOMBRES_FEMENINOS)

        apellido1, apellido2 = random.sample(self.APELLIDOS, 2)

        return f"{nombre} {apellido1} {apellido2}"

    
    def generar_persona(self, sexo: str | None = None, tipo_doc: str | None = None, edad: str = "aleatorio") -> dict:
        """
        Genera una persona completa con:
        - Nombre completo
        - Sexo (masculino, femenino o aleatorio)
        - Documento válido (DNI, NIE o CIF)
        - Email basado en nombre
        - Fecha de nacimiento (menor, mayor o aleatoria)

        Parámetros:
            sexo: "masculino", "femenino", "aleatorio" o None
            tipo_doc: "DNI", "NIE", "CIF", "AUTO" o None
            edad: "menor", "mayor", "aleatorio"
        """

        # Resolver sexo
        if sexo is None or sexo.lower() == "aleatorio":
            sexo_resuelto = random.choice(["masculino", "femenino"])
        elif sexo.lower() in ("masculino", "femenino"):
            sexo_resuelto = sexo.lower()
        else:
            raise ValueError(f"Sexo desconocido: {sexo}")

        # Nombre
        nombre = self.generar_nombre(sexo_resuelto)

        # Documento
        if (
            tipo_doc is None
            or tipo_doc.lower() == "aleatorio"
            or tipo_doc.upper() == "AUTO"
        ):
            tipo_doc_resuelto = random.choice(["DNI", "NIE", "CIF"])
        else:
            tipo_doc_resuelto = tipo_doc.upper()

        if tipo_doc_resuelto == "DNI":
            documento = self.generar_dni()
        elif tipo_doc_resuelto == "NIE":
            documento = self.generar_nie()
        elif tipo_doc_resuelto == "CIF":
            documento = self.generar_cif()
        else:
            raise ValueError(f"Tipo de documento desconocido: {tipo_doc}")

        # Email
        email = self.email_gen.generar_email(nombre)

        # Fecha de nacimiento
        fecha_nacimiento = self.birth_gen.generar(edad)

        # Telefono
        telefono = self.phone_gen.generar_telefono()


        return {
            "nombre": nombre,
            "sexo": sexo_resuelto,
            "tipo_documento": tipo_doc_resuelto,
            "documento": documento,
            "email": email,
            "fecha_nacimiento": fecha_nacimiento.isoformat(),
            "telefono": telefono,
        }


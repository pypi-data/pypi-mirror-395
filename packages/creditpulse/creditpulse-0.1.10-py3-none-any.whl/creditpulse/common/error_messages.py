"""
Manejo de error generales
"""

AUTORIZACION_BASE_DE_DATOS = """
    Es necesario obtener autorizacion para el el uso y lectura de base de datos
"""

TRUORA_API_KEY = """
    Debe obtener un API key de truora para consulta bases de datos externas, mas info en: https://dev.truora.com/checks/account/
"""

AUTHORIZATION_EXTERNAL_DB = """
    Para leer fuentes externas, se debe obtener previamente autorizacion del Titular de la información 
"""


class AutorizacionDatosPersonales(Exception):
    """
    Error por falta de autorizacion para uso de datos personales
    """

    def __init__(self):
        super().__init__(AUTORIZACION_BASE_DE_DATOS)


class TruoraApiKeyRequired(Exception):
    """
    Error por falta de api key de truora
    """

    def __init__(self):
        super().__init__(TRUORA_API_KEY)


class TruoraGeneralError(Exception):
    """
    Error general de truora que permite dar mensaje de error como paramtero
    """

    def __init__(self, msg: str):
        super().__init__(msg)

class AutorizacionNoOtorgada(Exception):
    """
    Error por no haber autorizado la
    """

    def __init__(self):
        super().__init__(AUTHORIZATION_EXTERNAL_DB)
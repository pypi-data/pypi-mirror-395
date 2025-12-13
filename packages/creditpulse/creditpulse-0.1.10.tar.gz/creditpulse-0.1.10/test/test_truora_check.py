import unittest

from creditpulse.bases_externas.truora import Truora
from creditpulse.bases_externas.schema import CountryCode, PersonType, TruoraCustomSchema


class TestTruoraCheck(unittest.TestCase):

    def test_simple_request_persona(self):
        client = Truora()
        client.create_check(
            identificacion='1053778047',
            person_type=PersonType.PERSONA,
            pais=CountryCode.COLOMBIA,
            autorizacion_datos=True
        )

    def test_simple_request_compania(self):
        client = Truora()
        client.create_check(
            identificacion='1053778047',
            person_type=PersonType.COMPANIA,
            pais=CountryCode.COLOMBIA,
            autorizacion_datos=True
        )

    def test_custom_type(self):
        client = Truora()
        check_name = "StandardCheck"
        schema = TruoraCustomSchema(
            type=check_name,
            country="CO",
        )
        response = client.create_custom_type(model=schema)
        print(response)

        client.create_check(
            identificacion='1053778047',
            person_type=check_name,
            pais=CountryCode.COLOMBIA,
            autorizacion_datos=True
        )

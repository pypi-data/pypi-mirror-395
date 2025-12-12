"""
Clase pincipal para analysis de creditos financieros

"""
import logging
from typing import Union
from pathlib import Path

from pydantic import BaseModel

from creditpulse.bases_externas.schema import CountryCode, BasesDeDatos, PersonType
from creditpulse.bases_externas.truora import Truora
from creditpulse.bases_externas.database import Database
from creditpulse.common.error_messages import AutorizacionNoOtorgada

logger = logging.getLogger(__name__)


class Check:
    """
        Clase que provee interfaz para analysis the personas
    """

    def __init__(self, truora_api_key: str = None):
        # Module logger

        self.external: Database = Truora(api_key=truora_api_key)
        # TODO implementar otras bases de datos

    def create_check(
            self,
            identificacion: str,
            autorizacion: bool,
            check_type: Union[PersonType, str] = PersonType.COMPANIA,
            check_name: str = 'default',
            force_creation: bool = False

    ):
        """
        Crea un check general en truora
        :return: Analysis financiero de la persona natural o juridica
        """
        if not autorizacion:
            raise AutorizacionNoOtorgada()

        return self.external.create_check(
            identificacion=identificacion,
            person_type=check_type,
            autorizacion_datos=autorizacion,
            pais=CountryCode.COLOMBIA,
            check_name=check_name,
            force_creation=force_creation
        )

    def get_existing_check(self, check_id: str):
        """
        Retorna
        :param check_id:
        :return:
        """
        return self.external.get_check(check_id=check_id)

    def get_existing_check_details(self, check_id: str):
        """

        :param check_id:
        :return:
        """
        return self.external.get_check_details(check_id=check_id)

    def get_existing_check_summary(self, check_id: str):
        """

        :param check_id:
        :return:
        """
        return self.external.get_check_summary(check_id=check_id)

    def to_general(self, check_id: str):
        """
        Create standard output for a check
        :param check_id:
        :return:
        """

        return self.external.to_general(check_id=check_id)

    def get_custom_types(self):
        """

        :return:
        """
        return self.external.configuration.list_configuration()

    def create_default_check(self):
        """

        :return:
        """
        return self.external.configuration.create_default_configuration()

    def delete_custom_check(self, name: str):
        """

        :param name:
        :return:
        """
        model = self.external.configuration.base_model_class.construct(type=name, country=CountryCode.COLOMBIA)
        return self.external.configuration.delete_configuration(model=model)

    def set_up_database(self):
        """

        :return:
        """
        return self.external.configuration.create_default_configuration()

    def create_custom_type(self, model: BaseModel):
        """
        Crea un custom type en truora
        :param model:
        :return:
        """
        return self.external.configuration.create_configuration(model=model)

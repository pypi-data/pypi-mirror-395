"""
    Request manager ara base de datos externa truora
"""
import json
import os
import logging
import requests
from typing import Optional, Union
from pydantic import BaseModel, Field, computed_field

from creditpulse.requests.request_manager import RequestManager
from creditpulse.bases_externas.schema import (
    TruoraCheckData,
    CountryCode, PersonType,
    CheckStatus,
    GeneralDatabase,
    BasesDeDatos,
    TruoraCustomSchema,
    TruoraCreditScoreCompanySchema,
    TruoraCreditScorePersonSchema,
    parse_json_to_model,
    CreditScoreData,
    PersonalDetails,
    parse_check_to_score,
    Scores,
    PersonaJuridica,
    PersonaNatural
)
from creditpulse.common.error_messages import (
    AutorizacionDatosPersonales,
    TruoraApiKeyRequired,
    TruoraGeneralError
)

from creditpulse.bases_externas.database import Database, DatabaseConfiguration, DatabaseParams

logger = logging.getLogger(__name__)

settings_data = {
    'names_matching_type': 'exact',
    'retries': True,
    'max_duration': '3m'
}


class TruoraParams(DatabaseParams):
    host_url: str = Field(
        default='https://api.checks.truora.com',
        description="Database host URL"
    )

    version: str = Field(
        default='v1',
        description="Database api version"
    )

    @computed_field
    @property
    def api_url(self) -> str:
        return f"{self.host_url}"

    @computed_field
    @property
    def check_url(self) -> str:
        return f"{self.base_url}/checks"

    @computed_field
    @property
    def check_details_url(self) -> str:
        return self.check_url + "/{}/details"

    @computed_field
    @property
    def check_summarize_url(self) -> str:
        return self.check_url + "/checks/{}/summarize"


class TruoraConfiguration(DatabaseConfiguration):
    base_model_class = TruoraCustomSchema
    credit_model_company = TruoraCreditScoreCompanySchema
    credit_model_person = TruoraCreditScorePersonSchema

    def list_configuration(self):
        response = self.session.get(self.database_url)
        if response.status_code not in range(200, 203):
            raise TruoraGeneralError(response.text)
        return json.loads(response.text)

    def update_configuration(self, model: BaseModel):
        return self.session.put(self.database_url, data=model.model_dump())

    def create_configuration(self, model: BaseModel):
        try:
            response = self.session.post(self.database_url, data=model.model_dump())
            if response.status_code not in range(200, 203):
                raise TruoraGeneralError(response.text)
            return json.loads(response.text)
        except Exception as e:
            self.logger.error(msg=str(e))

    def delete_configuration(self, model: BaseModel):
        try:
            params = model.model_dump(include={'type', 'country'})
            response = self.session.delete(self.database_url, params=params)
            if response.status_code not in range(200, 203):
                raise TruoraGeneralError(response.text)
            return json.loads(response.text)
        except Exception as e:
            self.logger.error(msg=str(e))

    def reset_default_configuration(self):
        return self.update_configuration(model=self.base_model_class())

    def create_default_configuration(self):

        models = [self.base_model_class(), self.credit_model_company(), self.credit_model_person()]
        for model in models:
            try:
                update_response = self.update_configuration(model=model)
                self.logger.info('Creating default model')
                if update_response.status_code in range(200, 204):
                    self.logger.info(msg="Database has been updated: default model")
                elif update_response.status_code == 400 and update_response.json()['code'] == 10400:
                    self.logger.error(msg="Database configuration does not exists")
                    try:
                        response = self.create_configuration(model=model)
                        self.logger.info(msg=response)
                    except Exception as e:
                        self.logger.error(msg=str(e))

            except Exception as e:
                self.logger.error(msg=str(e))


class Truora(Database):
    """

    Clase principal para consultar base de datos externa truora
    """

    def __init__(self, api_key: str = None):
        """

        :param api_key:
        """

        self.params = TruoraParams()

        self.api_key = api_key if api_key is not None else os.environ.get(self.params.api_key_name)

        if self.api_key is None:
            e = TruoraApiKeyRequired()
            logger.error(e)
            raise e

        self.session = requests.session()

        self.session.headers.update({
            "Truora-API-Key": self.api_key,
            'Accept': 'application/json'
        })

        self.request_manager = RequestManager(
            manager=self,
            max_retries=30
        )

        self.tcheck: Optional[TruoraCheckData] = None

        self.status: CheckStatus = CheckStatus.NOT_STARTED

        self.configuration = TruoraConfiguration(session=self.session)
        self.configuration.database_url = self.params.check_config_url

    def get_name(self) -> BasesDeDatos:
        return BasesDeDatos.TRUORA

    def _get_check(self, check_id: str):
        return self.session.get(self.params.check_url + "/" + check_id)

    def on_execute(self) -> requests.Response:
        return self._get_check(self.tcheck.check.check_id)

    def success_callback(self, response: requests.Response) -> None:
        logger.info("Consulta a Base De datos ha sido finalizada")
        response_json = response.json()
        self.tcheck = TruoraCheckData(**response_json)
        self.status = self.tcheck.check.status

    def error_callback(self, response: requests.Response) -> None:
        response_json = response.json()
        inter_check: TruoraCheckData = TruoraCheckData(**response_json)

        if inter_check.check.status == CheckStatus.DELAYED:
            self.request_manager.update_backoff_factor(self.request_manager.backoff_factor + 0.5)
            logger.warning("Consulta base de datos ha sido delayed")

        self.status = inter_check.check.status

    def is_request_successful(self, response: requests.Response) -> bool:
        """

        :param response:
        :return:
        """
        if response.status_code in [200, 203]:
            response_json = response.json()
            try:
                t_checker: TruoraCheckData = TruoraCheckData(**response_json)
                return t_checker.check.status == CheckStatus.COMPLETED
            except:
                return False
        return False

    def create_check(
            self,
            identificacion: str,
            person_type: Union[PersonType, str],
            autorizacion_datos: bool = False,
            pais: CountryCode = CountryCode.COLOMBIA,
            check_name: str = 'default',
            force_creation: bool = False
    ) -> str:
        """
        Funcion principal para consultar base de datos externa truora

        :param identificacion:
        :param person_type:
        :param autorizacion_datos:
        :param pais:
        :param check_name:
        :param force_creation:
        :return:
        """

        if not autorizacion_datos:
            raise AutorizacionDatosPersonales()

        id_field_name = 'national_id'
        if person_type == PersonType.COMPANIA:
            id_field_name = 'tax_id'

        form_data = {
            id_field_name: identificacion,
            'country': pais,
            'type': check_name,
            'user_authorized': autorizacion_datos,
            'force_creation': force_creation
        }
        response = self.session.post(self.params.check_url, data=form_data)
        response_json = response.json()

        if response.status_code not in [200, 201, 202, 203]:
            logger.error(f"Error al crear consulta base de datos externa: {response_json['message']}")
            raise TruoraGeneralError(f"Error al crear consulta base de datos externa: {response_json['message']}")

        self.tcheck = TruoraCheckData(**response_json)

        if self.tcheck is None:
            raise TruoraGeneralError('Check de truora no fue creado')

        self.request_manager.start()

        return self.tcheck.check.check_id

    def get_check(self, check_id: str):
        """

        :param check_id:
        :return:
        """
        response = self._get_check(check_id=check_id)
        if response.status_code not in range(200, 203):
            logger.error(response.text)
            raise TruoraGeneralError(response.text)

        return json.loads(response.text)

    def get_check_summary(self, check_id: str):
        """

        :param check_id:
        :return:
        """
        response = self.session.get(self.params.check_summarize_url.format(check_id))
        if response.status_code not in range(200, 203):
            logger.error(response.text)
            raise TruoraGeneralError(response.text)

        return json.loads(response.text)

    def get_check_details(self, check_id: str):
        """

        :param check_id:
        :return:
        """
        response = self.session.get(self.params.check_details_url.format(check_id))
        if response.status_code not in range(200, 203):
            logger.error(response.text)
            raise TruoraGeneralError(response.text)

        return json.loads(response.text)

    def get_next_details(self, next_url: str):
        """

        :param next_url:
        :return:
        """
        response = self.session.get("{}/{}".format(self.params.api_url, next_url))
        if response.status_code not in range(200, 203):
            logger.error(response.text)
            raise TruoraGeneralError(response.text)

        return json.loads(response.text)

    def to_general(self, check_id: str) -> GeneralDatabase:
        """
        Traduce truora a general
        :return:
        """
        check_data = self.get_check(check_id=check_id)
        scores = parse_check_to_score(json_data=check_data, model_class=Scores)

        details = self.get_check_details(check_id=check_id)
        credit_data = parse_json_to_model(json_data=details, model_class=CreditScoreData)

        personal_details = PersonalDetails()

        next = details.get('next')

        juridica = parse_json_to_model(json_data=details, model_class=PersonaJuridica)

        natural = parse_json_to_model(json_data=details, model_class=PersonaNatural)

        if next or not isinstance(next, str):
            next_details = self.get_next_details(next_url=details.get('next'))
            personal_details = parse_json_to_model(json_data=next_details, model_class=PersonalDetails)

        return GeneralDatabase(
            check_id=check_id,
            credit_data=credit_data,
            personal_data=personal_details,
            scores=scores,
            juridica=juridica,
            natural=natural
        )

"""
Definicion de tipos de datos para base de datos externas
"""
import re
from datetime import datetime
from enum import Enum
from typing import Dict, Union, Optional, Any, Type, TypeVar
from pydantic import BaseModel, Field


class BasesDeDatos(str, Enum):
    """
    
    Bases de Datos actualmente soportadas
    """
    TRUORA = "truora"


class CountryCode(str, Enum):
    """Supported country codes for checks"""
    ALL = "ALL"  # International Lists
    BRAZIL = "BR"  # Brazil
    COLOMBIA = "CO"  # Colombia
    CHILE = "CL"  # Chile
    COSTA_RICA = "CR"  # Costa Rica
    MEXICO = "MX"  # Mexico
    PERU = "PE"  # Peru


class PersonType(str, Enum):
    """Supported country codes for checks"""
    PERSONA = "person"  # Used to perform a background check on a person.
    VEHICULO = "vehicle"  # Used to perform a background check on a driver and their vehicle
    COMPANIA = "company"  # Used to perform a background check on a company


class CheckStatus(str, Enum):
    """Status values for checks"""
    NOT_STARTED = "not_started"  # The check is enqueued and the data collection has not started yet
    IN_PROGRESS = "in_progress"  # Data is being collected but some data sources may have finished already
    DELAYED = "delayed"  # One or more data sources are taking a long time to query the data. Most data sources will have already finished
    COMPLETED = "completed"  # The check finished and 70% or more of the data sources did not end in error status
    ERROR = "error"  # The check finished and more than 30% of the data sources ended in error status


class TruoraCheck(BaseModel):
    """
    Definicion para Check de truora
    """
    check_id: str = Field(..., description="Unique identifier for the check")
    country: CountryCode = Field(
        ...,
        description="""
            Country code - 
            ALL for International Lists, 
            BR for Brazil, 
            CO for Colombia, 
            CL for Chile, 
            CR for Costa Rica, 
            MX for Mexico, 
            PE for Peru
        """
    )
    type: str = Field(..., description="Check type")
    status: CheckStatus = Field(..., description="Current status of the check")
    creation_date: datetime = Field(..., description="When the check was created")
    update_date: datetime = Field(..., description="When the check was last updated")
    national_id: str = Field(default=None, description="National ID number being checked")
    tax_id: str = Field(default=None, description="National ID number being checked")

    # These are optional
    name_score: Optional[float] = Field(default=0, description="Score for name matching")
    id_score: Optional[float] = Field(default=-1, description="Score for ID matching")
    score: Optional[float] = Field(default=-1, description="Overall check score")
    previous_check: Optional[str] = Field(default=None, description="Overall check score")


class TruoraCheckData(BaseModel):
    """
    Definicion para la respuesta de truora
    """
    check: TruoraCheck = Field(..., description="Check details")
    details: Optional[str] = Field(default=None, description="API endpoint for detailed check information")
    self: Optional[str] = Field(default=None, description="API endpoint for this check resource")


class TruoraCustomSchema(BaseModel):
    type: str = Field(default='default', description="CustomTypeName")
    country: CountryCode = Field(
        default=CountryCode.COLOMBIA,
        description="""
            Country code - 
            ALL for International Lists, 
            BR for Brazil, 
            CO for Colombia, 
            CL for Chile, 
            CR for Costa Rica, 
            MX for Mexico, 
            PE for Peru
        """
    )

    dataset_affiliations_and_insurances: float = Field(default=0.1, description="dataset_affiliations_and_insurances")
    dataset_taxes_and_finances: float = Field(default=0.1, description="dataset_taxes_and_finances")
    dataset_legal_background: float = Field(default=0.1, description="dataset_legal_background")
    dataset_criminal_record: float = Field(default=0.1, description="dataset_criminal_record")
    dataset_personal_identity: float = Field(default=0.1, description="dataset_personal_identity")
    dataset_professional_background: float = Field(default=0.1, description="dataset_professional_background")
    dataset_international_background: float = Field(default=0.1, description="dataset_international_background")
    dataset_business_background: float = Field(default=0.1, description="dataset_business_background")
    dataset_credit_history: float = Field(default=0.1, description="dataset_credit_history")
    dataset_document_validation: float = Field(default=0.05, description="dataset_document_validation")
    dataset_alert_in_media: float = Field(default=0.05, description="dataset_alert_in_media")

    # dataset_traffic_fines: float = Field(default=0, description="dataset_traffic_fines")
    # dataset_driving_licenses: float = Field(default=0, description="dataset_driving_licenses")
    # dataset_vehicle_information: float = Field(default=0, description="dataset_vehicle_information")
    # dataset_vehicle_permits: float = Field(default=0, description="dataset_vehicle_permits")


class TruoraCreditScoreCompanySchema(BaseModel):
    type: str = Field(default='credit-company', description="CustomTypeName")
    country: CountryCode = Field(
        default=CountryCode.COLOMBIA,
        description="""
            Country code - 
            ALL for International Lists, 
            BR for Brazil, 
            CO for Colombia, 
            CL for Chile, 
            CR for Costa Rica, 
            MX for Mexico, 
            PE for Peru
        """
    )

    dataset_credit_history: float = Field(default=0.4, description="dataset_credit_history")#8
    dataset_business_background: float = Field(default=0.1, description="dataset_business_background")#7
    dataset_legal_background: float = Field(default=0.1, description="dataset_legal_background")#6
    dataset_affiliations_and_insurances: float = Field(default=0.1, description="dataset_affiliations_and_insurances")#5
    dataset_taxes_and_finances: float = Field(default=0.1, description="dataset_taxes_and_finances")#4
    dataset_alert_in_media: float = Field(default=0.05, description="dataset_alert_in_media")#3
    dataset_international_background: float = Field(default=0.1, description="dataset_international_background")#2
    dataset_criminal_record: float = Field(default=0.05, description="dataset_criminal_record")#1

class TruoraCreditScorePersonSchema(BaseModel):
    type: str = Field(default='credit-person', description="CustomTypeName")
    country: CountryCode = Field(
        default=CountryCode.COLOMBIA,
        description="""
            Country code - 
            ALL for International Lists, 
            BR for Brazil, 
            CO for Colombia, 
            CL for Chile, 
            CR for Costa Rica, 
            MX for Mexico, 
            PE for Peru
        """
    )

    dataset_credit_history: float = Field(default=0.4, description="dataset_credit_history")#1
    dataset_personal_identity: float = Field(default=0.1, description="dataset_personal_identity")#2
    dataset_legal_background: float = Field(default=0.1, description="dataset_legal_background")#3
    dataset_affiliations_and_insurances: float = Field(default=0.1, description="dataset_affiliations_and_insurances")#4
    dataset_taxes_and_finances: float = Field(default=0.1, description="dataset_taxes_and_finances")#5
    dataset_alert_in_media: float = Field(default=0.05, description="dataset_alert_in_media")#6
    dataset_international_background: float = Field(default=0.1, description="dataset_international_background")#7
    dataset_criminal_record: float = Field(default=0.05, description="dataset_criminal_record")#8

class PersonaNatural(BaseModel):
    estado_afiliacion: Optional[str] = Field(
        default=None,
        description="Estado",
        title="Información afiliación"
    )
    tipo_afiliacion: Optional[str] = Field(
        default=None,
        description="Tipo de afiliado",
        title="Información afiliación"
    )
    regimen_afiliacion: Optional[str] = Field(
        default=None,
        description="Regimen",
        title="Información afiliación"
    )


class PersonaJuridica(BaseModel):
    razon_social: Optional[str] = Field(
        default=None,
        description="Razón social",
        title="Información General"
    )

    estado: Optional[str] = Field(
        default=None,
        description="Estado de Matrícula",
        title="Información General"
    )

    fecha_matricula: Optional[str] = Field(
        default=None,
        description="Fecha de Matrícula",
        title="Registro Mercantil"
    )

    representante_legal: Optional[str] = Field(
        default=None,
        description="Nombre",
        title="Representantes legales"
    )

    documento_representante_legal: Union[str, int, float, None] = Field(
        default=None,
        description="Número de documento",
        title="Representantes legales"
    )


class Scores(BaseModel):
    general: Optional[float] = Field(
        default=None,
        description="Overal Score",
    )

    credit_history: Optional[float] = Field(
        default=None,
        description="credit_history",
        title="credit_history",
    )

    criminal_record: Optional[float] = Field(
        default=None,
        description="criminal_record",
        title="criminal_record",
    )

    legal_background: Optional[float] = Field(
        default=None,
        description="legal_background",
        title="legal_background",
    )

    international_background: Optional[float] = Field(
        default=None,
        description="international_background",
        title="international_background",
    )

    personal_identity: Optional[float] = Field(
        default=None,
        description="personal_identity",
        title="personal_identity",
    )

    business_background: Optional[float] = Field(
        default=None,
        description="business_background",
        title="business_background",
    )

    alert_in_media: Optional[float] = Field(
        default=None,
        description="alert_in_media",
        title="alert_in_media",
    )

    taxes_and_finances: Optional[float] = Field(
        default=None,
        description="taxes_and_finances",
        title="taxes_and_finances",
    )


class PersonalDetails(BaseModel):
    nombre: Optional[str] = Field(
        default=None,
        description="Nombre Completo",
        title="Información general"
    )

    nuip: Union[str, int, None] = Field(
        default=None,
        description="NUIP",
        title="Información general"
    )


class CreditScoreData(BaseModel):
    """Modelo para datos extraídos del cliente"""

    score: Optional[float] = Field(
        default=None,
        ge=0,
        le=1000,
        description="Score",
        title="Score"
    )

    mora_actual: Optional[float] = Field(
        default=0,
        ge=0,
        description="Días de mora actual",
        title="Mora Maxima del portafolio a la fecha"
    )

    mora_maxima_6m: Optional[float] = Field(
        default=0, ge=0,
        description="Mora máxima últimos 6 meses",
        title="Mora Maxima en los Ultimos 6 meses"
    )

    mora_maxima_12m: Optional[float] = Field(
        default=0, ge=0,
        description="Mora máxima últimos 12 meses",
        title="Mora Maxima en los Ultimos 12 meses"
    )

    mora_historica: Optional[float] = Field(
        default=0, ge=0,
        description="Mora Maxima del portafolio a la fecha",
        title="Desempeño actual en todos los portafolios"
    )

    productos_al_dia: Optional[float] = Field(
        default=0, ge=0,
        description="Numero total de productos al dia a la fecha",
        title="Desempeño actual en todos los portafolios"
    )

    productos_castigados: Optional[float] = Field(
        default=0, ge=0,
        description="Numero total de productos castigados a la fecha",
        title="Desempeño actual en todos los portafolios"
    )

    ever_120_6m: Optional[float] = Field(
        default=0, ge=0,
        description="productos Ever 120 en los ultimos 6 meses",
        title="Desempeño a corto plazo en todos los portafolios"
    )

    ever_90_6m: Optional[float] = Field(
        default=0, ge=0,
        description="productos Ever 90 en los ultimos 6 meses",
        title="Desempeño a corto plazo en todos los portafolios"
    )

    ever_60_6m: Optional[float] = Field(
        default=0, ge=0,
        description="productos Ever 60 en los ultimos 6 meses",
        title="Desempeño a corto plazo en todos los portafolios"
    )

    ever_30_6m: Optional[float] = Field(
        default=0, ge=0,
        description="productos Ever 30 en los ultimos 6 meses",
        title="Desempeño a corto plazo en todos los portafolios"
    )

    ever_120_12m: Optional[float] = Field(
        default=0, ge=0,
        description="productos Ever 120 en los ultimos 12 meses",
        title="Desempeño a mediano plazo en todos los portafolios"
    )

    ever_90_12m: Optional[float] = Field(
        default=0, ge=0,
        description="productos Ever 90 en los ultimos 12 meses",
        title="Desempeño a mediano plazo en todos los portafolios"
    )

    ever_60_12m: Optional[float] = Field(
        default=0, ge=0,
        description="productos Ever 60 en los ultimos 12 meses",
        title="Desempeño a mediano plazo en todos los portafolios"
    )

    ever_30_12m: Optional[float] = Field(
        default=0, ge=0,
        description="productos Ever 30 en los ultimos 12 meses",
        title="Desempeño a mediano plazo en todos los portafolios"
    )

    siempre_al_dia_6m: Optional[float] = Field(
        default=0, ge=0,
        description="Productos siempre al día 6 meses",
        title="Productos siempre al día 6 meses"
    )

    siempre_al_dia_12m: Optional[float] = Field(
        default=0, ge=0,
        description="Productos siempre al día 12 meses",
        title="Productos siempre al día 12 meses"
    )

    cuota_total: Optional[float] = Field(
        default=0.0, ge=0,
        description="Cuota total en salarios mínimos",
        title="Cuota total en salarios mínimos"
    )

    saldo_rotativo: Optional[float] = Field(
        default=0.0, ge=0,
        description="Saldo rotativo",
        title="Saldo rotativo"
    )

    saldo_consumo: Optional[float] = Field(
        default=0.0, ge=0,
        description="Saldo consumo",
        title="Saldo consumo"
    )

    estrato: Optional[float] = Field(
        default=0.0, ge=0, le=8,
        description="Estrato socioeconómico",
        title="Estrato socioeconómico"
    )

    estado_civil: Optional[float] = Field(
        default="soltero",
        description="Estado civil",
        title="Estado civil"
    )

    nivel_estudios: Optional[float] = Field(
        default="primaria",
        description="Nivel de estudios",
        title="Nivel de estudios"
    )

    # Campos calculados
    saldo_total: Optional[float] = Field(
        default=0.0, ge=0,
        description="Saldo total calculado"
    )

    productos_totales: Optional[float] = Field(
        default=0.0, ge=0,
        description="Total productos"
    )

    # experiencia financiera

    meses_producto_antiguo: Optional[float] = Field(
        default=0.0, ge=0,
        description="Meses desde la apertura del producto mas antiguo en todos los portafolios",
        title="Experiencia financiera"
    )

    meses_producto_abierto_antiguo: Optional[float] = Field(
        default=0.0, ge=0,
        description="Meses desde la apertura del producto abierto mas antiguo en todos los portafolios",
        title="Experiencia financiera"
    )
    meses_producto_reciente: Optional[float] = Field(
        default=0.0, ge=0,
        description="Meses desde la apertura del producto mas reciente en todos los portafolios",
        title="Experiencia financiera"
    )

    numero_productos_creditos_rotativos: Optional[float] = Field(
        default=0.0, ge=0,
        description="Numero de Productos Abiertos en el portafolio: créditos rotativos, cartera bancaria, microcrédito, cartera compañías de financiamiento comercial, Tarjetas de Crédito",
        title="Experiencia financiera"
    )

    numero_productos_tarjeta_credito: Optional[float] = Field(
        default=0.0, ge=0,
        description="Numero de Productos Abiertos en el portafolio tarjetas de crédito",
        title="Experiencia financiera"
    )

    numero_productos_fondo_empleados: Optional[float] = Field(
        default=0.0, ge=0,
        description="Numero de Productos Abiertos en el portafolio: cartera bancaria, cartera de corporaciones financieras, cartera de fondos de empleados, cartera de compañías de leasing, cartera compañías de financiamiento comercial, cartera de compensación y salud, créditos de consumo, microcrédito",
        title="Experiencia financiera"
    )

    numero_productos_credito_automotriz: Optional[float] = Field(
        default=0.0, ge=0,
        description="Numero de Productos Abiertos en el portafolio: cartera automotriz",
        title="Experiencia financiera"
    )

    numero_productos_credito_vivienda: Optional[float] = Field(
        default=0.0, ge=0,
        description="Numero de Productos Abiertos en el portafolio: cartera de vivienda",
        title="Experiencia financiera"
    )

    numero_productos_cuenta_corriente: Optional[float] = Field(
        default=0.0, ge=0,
        description="Numero de Productos Abiertos en el portafolio cuenta corriente",
        title="Experiencia financiera"
    )

    numero_productos_otros_tipos: Optional[float] = Field(
        default=0.0, ge=0,
        description="Numero de Productos Abiertos en el portafolio otros tipos de cartera",
        title="Experiencia financiera"
    )

    numero_productos_cuenta_ahorros: Optional[float] = Field(
        default=0.0, ge=0,
        description="Numero de Productos Abiertos en el portafolio cuentas de ahorros bancarias",
        title="Experiencia financiera"
    )

    numero_productos_codeudores: Optional[float] = Field(
        default=0.0,
        description="Numero de Productos Abiertos en el portafolio codeudores",
        title="Experiencia financiera"
    )

    cuota_todos_portafolio: Optional[float] = Field(
        default=0.0,
        description="Cuota total en productos a la fecha en todos los portafolios",
        title="Endeudamiento financiero"
    )

    saldo_total_rotativos: Optional[float] = Field(
        default=0.0,
        description="Saldo total en productos a la fecha en el portafolio cartera bancaria, cartera de corporaciones financieras, cartera de fondos de empleados, cartera de compañías de leasing, cartera compañías de financiamiento comercial, cartera de compensación y salud, créditos de consumo, microcrédito",
        title="Endeudamiento financiero"
    )


def extract_numeric_value_or_leave(text: str):
    """
    Extrae valor numérico de un texto si empieza con número, sino retorna el texto original
    :param text: Textio a extraer datos numericos
    :return:
    """
    if not text or text in ["No tiene información en el portafolio", "No tiene cuentas abiertas", None]:
        return 0.0

    text = str(text).strip()

    tokens = text.split(" ")

    if len(tokens) > 1:
        match = re.match(r'^(\d+(?:\.\d+)?)', tokens[0])
        if match:
            return float(match.group(1))
        else:
            return text
    else:
        return text


T = TypeVar('T', bound=BaseModel)


def _is_valid_dict(obj: Any) -> bool:
    """
    Verifica si el objeto es un diccionario válido y no vacío.
    :param obj:
    :return:
    """
    return obj is not None and isinstance(obj, dict)


def _get_field_title_safely(field_info: Any, field_name: str) -> str:
    """
    Obtiene el título del campo de forma segura.
    :param field_info:
    :return:
    """
    try:
        # Intentar obtener title como atributo
        if hasattr(field_info, field_name) and getattr(field_info, field_name):
            return str(getattr(field_info, field_name)).lower()

        if isinstance(field_info, dict) and field_name in field_info:
            title = field_info.get(field_name)
            if title:
                return str(title).lower()

        return ""

    except Exception:
        return ""


def _safe_string_extract(value: Any) -> str:
    """
    Extrae string de forma segura, manejando None y otros tipos.
    :param value:
    :return:
    """
    if value is None:
        return ""

    try:
        return str(value).strip()
    except Exception:
        return ""


def _process_cell_safely(cell: Any, raw_data: Dict[str, Any], model_class: Type[T], section_title: str) -> None:
    """
    Procesa una celda individual de forma segura.

    :param cell: Celda a procesar
    :param raw_data: Diccionario donde almacenar los datos extraídos
    :param model_class: Clase del modelo para obtener los campos
    """
    if not _is_valid_dict(cell):
        return

    # Extraer label y value de forma segura
    label = _safe_string_extract(cell.get('label'))
    value = _safe_string_extract(cell.get('value'))

    # Skip si no hay label válido
    if not label:
        return

    # Buscar coincidencias con los campos del modelo
    label_lower = label.lower()

    try:
        for field_name, field_info in model_class.model_fields.items():

            # Skip si ya tenemos este campo
            if field_name in raw_data:
                continue

            # Obtener el título del campo de forma segura
            field_description = _get_field_title_safely(field_info=field_info, field_name='description')
            field_title = _get_field_title_safely(field_info=field_info, field_name='title')

            if len(field_description) > 0:
                if section_title.lower() in field_title.lower() or field_title.lower() in section_title.lower():
                    # Verificar coincidencia
                    if field_description and field_description in label_lower:
                        try:
                            extracted_value = extract_numeric_value_or_leave(value)
                            raw_data[field_name] = extracted_value

                            break  # Salir del loop una vez encontrada la coincidencia

                        except Exception as e:

                            continue

    except Exception as e:
        pass


def _filter_valid_data(raw_data: Dict[str, Any], model_class: Type[T]) -> Dict[str, Any]:
    """
    Filtra los datos para mantener solo los que son válidos para el modelo.

    :param raw_data: Datos sin filtrar
    :param model_class: Clase del modelo
    :return: Datos filtrados
    """
    valid_data = {}

    try:
        model_fields = getattr(model_class, 'model_fields', {})

        for field_name, value in raw_data.items():
            if field_name in model_fields:
                # Intentar validar el campo individualmente
                try:
                    # Crear un modelo temporal solo con este campo
                    temp_data = {field_name: value}
                    model_class(**temp_data)
                    valid_data[field_name] = value
                except Exception:
                    continue

    except Exception as e:
        pass

    return valid_data


def _create_model_safely(model_class: Type[T], raw_data: Dict[str, Any]) -> T:
    """
    Crea el modelo de forma segura con manejo de errores.

    :param model_class: Clase del modelo a crear
    :param raw_data: Datos extraídos
    :return: Instancia del modelo
    """
    try:
        if raw_data:
            return model_class(**raw_data)
        else:
            return model_class()

    except Exception as e:

        # Intentar crear con un subconjunto de datos válidos
        try:
            valid_data = _filter_valid_data(raw_data, model_class)
            if valid_data:
                return model_class(**valid_data)
        except Exception as e2:
            pass

        # Retornar con valores por defecto si todo falla
        return model_class()


def parse_json_to_model(json_data: Dict[str, Any], model_class: Type[T]) -> T:
    """
    Extrae y valida los datos del JSON usando Pydantic de forma segura.

    :param json_data: Data 'cruda' para extraer los datos de
    :param model_class: Clase del modelo Pydantic a crear
    :return: Instancia del modelo con datos extraídos o valores por defecto
    """
    raw_data = {}

    try:
        # Validar entrada básica
        if not isinstance(json_data, dict):
            return model_class()

        if not hasattr(model_class, 'model_fields'):
            return model_class()

        # Obtener detalles de forma segura
        details = json_data.get('details')
        if not details or not isinstance(details, list):
            return model_class()

        # Procesar cada detalle
        for detail_idx, detail in enumerate(details):
            if not _is_valid_dict(detail):
                continue

            # Obtener tablas de forma segura
            tables = detail.get('tables')
            if not tables or not isinstance(tables, list):
                continue

            # Procesar cada tabla
            for table_idx, table in enumerate(tables):
                if not _is_valid_dict(table):
                    continue

                # Obtener filas de forma segura
                rows = table.get('rows')
                if not rows or not isinstance(rows, list):
                    continue

                section_title = table.get('title')

                if not section_title or not isinstance(section_title, str):
                    continue

                # Procesar cada fila
                for row_idx, row in enumerate(rows):
                    if not _is_valid_dict(row):
                        continue

                    # Obtener celdas de forma segura
                    cells = row.get('cells')
                    if not cells or not isinstance(cells, list):
                        continue

                    # Procesar cada celda
                    for cell_idx, cell in enumerate(cells):
                        try:
                            _process_cell_safely(
                                cell=cell,
                                raw_data=raw_data,
                                model_class=model_class,
                                section_title=section_title
                            )
                        except Exception as e:
                            continue

    except Exception as e:
        return model_class()

    # Crear y validar el modelo Pydantic
    return _create_model_safely(model_class, raw_data)


def parse_check_to_score(json_data: Dict[str, Any], model_class: Type[T]) -> T:
    """
    Extrae y valida los datos del JSON usando Pydantic de forma segura.

    :param json_data: Data 'cruda' para extraer los datos de
    :param model_class: Clase del modelo Pydantic a crear
    :return: Instancia del modelo con datos extraídos o valores por defecto
    """
    raw_data = {}

    try:
        # Validar entrada básica
        if not isinstance(json_data, dict):
            return model_class()

        if not hasattr(model_class, 'model_fields'):
            return model_class()

        check = json_data.get('check')

        if not check or not isinstance(check, dict):
            return model_class()

        raw_data['general'] = check.get('score', 0.0)
        scores = check.get('scores')

        if not scores or not isinstance(scores, list):
            return model_class()

        for cell_idx, score in enumerate(scores):
            if "data_set" in score and "score" in score:
                raw_data[score["data_set"]] = score["score"]

        return _create_model_safely(model_class, raw_data)
    except Exception as e:
        return model_class()


class GeneralDatabase(BaseModel):
    check_id: str = Field(..., description="Check details")
    credit_data: CreditScoreData = Field(..., description="Credit Score Details")
    personal_data: PersonalDetails = Field(..., description="Personal Data")
    scores: Scores = Field(..., description="Dataset Scores")
    juridica: PersonaJuridica = Field(..., description="Datos persona Juridica")
    natural: PersonaNatural = Field(..., description="Datos persona Natural")

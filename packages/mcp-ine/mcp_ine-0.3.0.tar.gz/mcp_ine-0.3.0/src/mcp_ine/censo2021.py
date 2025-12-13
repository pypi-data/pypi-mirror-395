"""
Censo 2021 (SDC21) API Module

API endpoint: POST https://www.ine.es/Censo2021/api
Content-Type: application/json

This module provides access to Spain's 2021 Census data through the SDC21 API.
"""

import requests
from typing import List, Dict, Any, Optional
from .common import logger

# Censo 2021 API Configuration
CENSO_API_URL = "https://www.ine.es/Censo2021/api"

# Available tables in SDC21
CENSO_TABLES = {
    "hog": {"es": "Hogares", "en": "Households"},
    "nuc": {"es": "Parejas y otros núcleos familiares", "en": "Couples and other family nuclei"},
    "per.estu": {"es": "Personas en establecimientos colectivos", "en": "Persons in collective housing"},
    "per.ocu": {"es": "Personas residentes en viviendas familiares", "en": "Persons in family dwellings"},
    "per.ppal": {"es": "Total de Personas", "en": "All persons"},
    "viv.fam": {"es": "Viviendas familiares", "en": "Dwellings"},
    "viv.ppal": {"es": "Ocupados de 16 y más años", "en": "Employed persons aged 16+"}
}

# Available metrics by table
CENSO_METRICS = {
    "hog": ["SHOGARES"],
    "nuc": ["SNUCLEOS"],
    "per.estu": ["SPERSONAS"],
    "per.ocu": ["SPERSONAS"],
    "per.ppal": ["SPERSONAS"],
    "viv.fam": ["SVIVIENDAS"],
    "viv.ppal": ["SPERSONAS"]
}

# Common variables available across tables
CENSO_COMMON_VARIABLES = {
    "ID_RESIDENCIA_N1": "CC.AA. de residencia / Autonomous Community",
    "ID_RESIDENCIA_N2": "Provincia de residencia / Province of residence",
    "ID_RESIDENCIA_N3": "Municipio de residencia / Municipality of residence",
    "ID_RESIDENCIA_N4": "Distrito / District",
    "ID_RESIDENCIA_N5": "Sección / Section",
    "ID_SEXO": "Sexo / Sex",
    "ID_EDAD": "Edad año a año / Age year to year",
    "ID_GRAN_GRUPO_EDAD": "Edad en grandes grupos / Age in large groups",
    "ID_GRUPO_Q_EDAD": "Edad (grupos quinquenales) / Age (five-year groups)",
    "ID_NACIONALIDAD_N1": "Nacionalidad (española/extranjera) / Nationality (Spanish/foreign)",
    "ID_NACIONALIDAD_N2": "Nacionalidad (grandes grupos) / Nationality (large groups)",
    "ID_NACIONALIDAD_N3": "País de nacionalidad / Country of nationality",
    "ID_LUGAR_NAC_NAC_N1": "CC.AA. de nacimiento / Autonomous Community of birth",
    "ID_LUGAR_NAC_NAC_N2": "Provincia de nacimiento / Province of birth",
    "ID_LUGAR_NAC_NAC_N3": "Municipio de nacimiento / Municipality of birth",
    "ID_ESREAL_CNEDA": "Nivel de estudios (detalle) / Educational attainment (detail)",
    "ID_ESREAL_GR5": "Nivel de estudios (grado) / Educational attainment (grade)",
    "ID_ESTADO_CIVIL": "Estado Civil / Legal Marital Status",
    "ID_RELA": "Relación con la actividad (detalle) / Current activity status (detail)",
    "ID_RELA2": "Relación con la actividad (activo/inactivo) / Activity status (active/inactive)"
}

# Housing-specific variables
CENSO_HOUSING_VARIABLES = {
    "ID_CLASE_VIV": "Clase de vivienda / Class of Dwelling",
    "ID_TENEN_VIV": "Régimen de tenencia de la vivienda / Tenure status of dwelling",
    "ID_SUP_VIV": "Superficie / Useful floor space",
    "ID_SUP_OCU_VIV": "Superficie por ocupante / Useful floor space per occupant",
    "ID_TAM_HOG_6": "Tamaño del hogar / Size of the household",
    "ID_ANO_CONS": "Año de construcción (todo) / Year of construction (detail)",
    "ID_ANO_CONS_GR11": "Año de construcción (agregado) / Year of construction (aggregated)",
    "ID_TIPO_EDIF_VIV": "Tipo de viviendas según tipo de edificio / Type of dwellings by building type"
}

# Household-specific variables
CENSO_HOUSEHOLD_VARIABLES = {
    "ID_TAM_HOG_6": "Tamaño del hogar / Size of the household",
    "ID_TIPO_HOG_1": "Tipo de Hogar (detalle) / Type of Household (detail)",
    "ID_NUC_HOG": "Número núcleos en el hogar / Number of family nuclei in household"
}

# Nucleus-specific variables
CENSO_NUCLEUS_VARIABLES = {
    "ID_TIPO_NUC_1": "Tipo de núcleo / Type of Family Nucleus",
    "ID_TIPO_PAR_NUC_1": "Tipo de pareja (de hecho o de derecho) / Type of couple",
    "ID_TIPO_PAR_NUC_2": "Tipo de pareja (mismo sexo, distinto sexo) / Type of couple (same/different sex)",
    "ID_NHIJOS_NUC": "Número de hijos / Number of children",
    "ID_TAM_NUC_1": "Tamaño del núcleo / Family nucleus size"
}


def censo_request(
    tabla: str,
    metrica: List[str],
    variables: List[str],
    idioma: str = "ES",
    filtro: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Execute a request to the Censo 2021 SDC21 API.
    
    Args:
        tabla: Table ID (hog, nuc, per.estu, per.ocu, per.ppal, viv.fam, viv.ppal)
        metrica: List of metrics to retrieve (SHOGARES, SNUCLEOS, SPERSONAS, SVIVIENDAS)
        variables: List of grouping variables (ID_RESIDENCIA_N1, ID_SEXO, etc.)
        idioma: Language ES or EN (default: ES)
        filtro: Optional list of filters [{"variable": "VAR_NAME", "valores": ["val1", "val2"]}]
    
    Returns:
        API response with metadata and data arrays
    """
    payload = {
        "idioma": idioma,
        "metrica": metrica,
        "tabla": tabla,
        "variables": variables
    }
    
    if filtro:
        payload["filtro"] = filtro
    
    try:
        response = requests.post(
            CENSO_API_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Censo 2021 API error: {e}")
        return {"error": str(e)}


def get_censo_tables() -> Dict[str, Any]:
    """Get available tables in Censo 2021"""
    return {
        "tables": [
            {"id": k, "description_es": v["es"], "description_en": v["en"]}
            for k, v in CENSO_TABLES.items()
        ],
        "total": len(CENSO_TABLES)
    }


def get_censo_metrics(tabla: Optional[str] = None) -> Dict[str, Any]:
    """Get available metrics, optionally for a specific table"""
    if tabla:
        if tabla not in CENSO_METRICS:
            return {"error": f"Unknown table: {tabla}"}
        return {"table": tabla, "metrics": CENSO_METRICS[tabla]}
    return {"metrics_by_table": CENSO_METRICS}


def get_censo_variables(tabla: Optional[str] = None) -> Dict[str, Any]:
    """
    Get available variables for census queries.
    Returns common variables and table-specific variables if tabla is specified.
    """
    result = {
        "common_variables": CENSO_COMMON_VARIABLES,
        "housing_variables": CENSO_HOUSING_VARIABLES,
        "household_variables": CENSO_HOUSEHOLD_VARIABLES,
        "nucleus_variables": CENSO_NUCLEUS_VARIABLES
    }
    
    if tabla:
        result["table"] = tabla
        if tabla in ["viv.fam", "viv.ppal"]:
            result["recommended"] = {**CENSO_COMMON_VARIABLES, **CENSO_HOUSING_VARIABLES}
        elif tabla == "hog":
            result["recommended"] = {**CENSO_COMMON_VARIABLES, **CENSO_HOUSEHOLD_VARIABLES}
        elif tabla == "nuc":
            result["recommended"] = {**CENSO_COMMON_VARIABLES, **CENSO_NUCLEUS_VARIABLES}
        else:
            result["recommended"] = CENSO_COMMON_VARIABLES
    
    return result


def get_censo_data(
    tabla: str,
    variables: List[str],
    metrica: Optional[str] = None,
    idioma: str = "ES"
) -> Dict[str, Any]:
    """
    Get census data for specified table and grouping variables.
    
    Args:
        tabla: Table ID (hog, nuc, per.estu, per.ocu, per.ppal, viv.fam, viv.ppal)
        variables: List of grouping variables
        metrica: Metric to use (auto-detected if not provided)
        idioma: Language ES or EN
    
    Returns:
        Census data grouped by specified variables
    """
    if tabla not in CENSO_TABLES:
        return {"error": f"Unknown table: {tabla}. Available: {list(CENSO_TABLES.keys())}"}
    
    # Auto-detect metric if not provided
    if not metrica:
        metrica = CENSO_METRICS.get(tabla, ["SPERSONAS"])[0]
    
    return censo_request(
        tabla=tabla,
        metrica=[metrica],
        variables=variables,
        idioma=idioma
    )


def get_population_by_location(
    level: str = "N1",
    idioma: str = "ES"
) -> Dict[str, Any]:
    """
    Get population by geographic level.
    
    Args:
        level: Geographic level (N1=CCAA, N2=Province, N3=Municipality)
        idioma: Language ES or EN
    
    Returns:
        Population data by location
    """
    variable = f"ID_RESIDENCIA_{level}"
    return censo_request(
        tabla="per.ppal",
        metrica=["SPERSONAS"],
        variables=[variable],
        idioma=idioma
    )


def get_population_pyramid(
    location_level: str = "N1",
    location_value: Optional[str] = None,
    idioma: str = "ES"
) -> Dict[str, Any]:
    """
    Get population pyramid data (by age and sex).
    
    Args:
        location_level: Geographic level for location filter
        location_value: Location value to filter (e.g., "Madrid, Comunidad de")
        idioma: Language ES or EN
    
    Returns:
        Population by age and sex
    """
    variables = ["ID_GRUPO_Q_EDAD", "ID_SEXO"]
    
    filtro = None
    if location_value:
        filtro = [{"variable": f"ID_RESIDENCIA_{location_level}", "valores": [location_value]}]
    
    return censo_request(
        tabla="per.ppal",
        metrica=["SPERSONAS"],
        variables=variables,
        idioma=idioma,
        filtro=filtro
    )


def get_housing_by_tenure(
    location_level: str = "N1",
    idioma: str = "ES"
) -> Dict[str, Any]:
    """
    Get housing data by tenure status (owned, rented, etc.).
    
    Args:
        location_level: Geographic level (N1=CCAA, N2=Province, N3=Municipality)
        idioma: Language ES or EN
    
    Returns:
        Housing counts by tenure status and location
    """
    return censo_request(
        tabla="viv.fam",
        metrica=["SVIVIENDAS"],
        variables=[f"ID_RESIDENCIA_{location_level}", "ID_TENEN_VIV"],
        idioma=idioma
    )


def get_households_by_size(
    location_level: str = "N1",
    idioma: str = "ES"
) -> Dict[str, Any]:
    """
    Get households by size.
    
    Args:
        location_level: Geographic level (N1=CCAA, N2=Province, N3=Municipality)
        idioma: Language ES or EN
    
    Returns:
        Household counts by size and location
    """
    return censo_request(
        tabla="hog",
        metrica=["SHOGARES"],
        variables=[f"ID_RESIDENCIA_{location_level}", "ID_TAM_HOG_6"],
        idioma=idioma
    )


def get_education_level(
    location_level: str = "N1",
    idioma: str = "ES"
) -> Dict[str, Any]:
    """
    Get population by education level.
    
    Args:
        location_level: Geographic level (N1=CCAA, N2=Province, N3=Municipality)
        idioma: Language ES or EN
    
    Returns:
        Population by education level and location
    """
    return censo_request(
        tabla="per.ppal",
        metrica=["SPERSONAS"],
        variables=[f"ID_RESIDENCIA_{location_level}", "ID_ESREAL_GR5"],
        idioma=idioma
    )


def get_nationality_data(
    level: int = 1,
    location_level: str = "N1",
    idioma: str = "ES"
) -> Dict[str, Any]:
    """
    Get population by nationality.
    
    Args:
        level: Nationality detail (1=Spanish/Foreign, 2=Large groups, 3=Country)
        location_level: Geographic level (N1=CCAA, N2=Province, N3=Municipality)
        idioma: Language ES or EN
    
    Returns:
        Population by nationality and location
    """
    return censo_request(
        tabla="per.ppal",
        metrica=["SPERSONAS"],
        variables=[f"ID_RESIDENCIA_{location_level}", f"ID_NACIONALIDAD_N{level}"],
        idioma=idioma
    )


def get_family_nuclei(
    nucleus_type: bool = True,
    location_level: str = "N1",
    idioma: str = "ES"
) -> Dict[str, Any]:
    """
    Get family nuclei data.
    
    Args:
        nucleus_type: Include nucleus type grouping
        location_level: Geographic level (N1=CCAA, N2=Province, N3=Municipality)
        idioma: Language ES or EN
    
    Returns:
        Family nuclei counts by type and location
    """
    variables = [f"ID_RESIDENCIA_{location_level}"]
    if nucleus_type:
        variables.append("ID_TIPO_NUC_1")
    
    return censo_request(
        tabla="nuc",
        metrica=["SNUCLEOS"],
        variables=variables,
        idioma=idioma
    )

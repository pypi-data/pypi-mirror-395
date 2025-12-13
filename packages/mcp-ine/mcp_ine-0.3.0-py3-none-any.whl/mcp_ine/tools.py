"""INE MCP Tools - Wrappers for INE resources exposed as MCP tools"""
from typing import Optional, List, Dict, Any
from .common import mcp
from . import resources as r

# =============================================================================
# Operations
# =============================================================================

@mcp.tool()
def List_Operations(filter_text: Optional[str] = None, detail_level: Optional[int] = None,
                   geo_filter: Optional[int] = None, page: Optional[int] = None) -> List[Dict[str, Any]]:
    """List available INE statistical operations
    
    Args:
        filter_text: Optional filter by code or name (e.g., 'IPC', 'población')
        detail_level: Detail level 0, 1, or 2 for more information
        geo_filter: 1=with geographic breakdown, 0=national only
        page: Page number for pagination (500 results per page)
    
    Returns:
        List of operations with Id, Codigo, Nombre, and Url
    """
    return r.list_operations(filter_text, detail_level, geo_filter, page)

@mcp.tool()
def Get_Operation_Info(operation_code: str, detail_level: Optional[int] = None) -> Dict[str, Any]:
    """Get detailed information about a specific operation
    
    Args:
        operation_code: Operation code (e.g., 'IPC', 'EPA', 'ECV')
        detail_level: Detail level 0, 1, or 2 for more information
    
    Returns:
        Operation details with Id, Codigo, Nombre, Url, FK_Periodicidad, etc.
    """
    return r.get_operation(operation_code, detail_level)

@mcp.tool()
def Get_Operation_Tables(operation_code: str, detail_level: Optional[int] = None,
                        geo_filter: Optional[int] = None, friendly_output: bool = False) -> List[Dict[str, Any]]:
    """Get available tables for a statistical operation
    
    Args:
        operation_code: Operation code (e.g., 'IPC', 'IPI', 'EPA')
        detail_level: Detail level 0, 1, or 2 for more information
        geo_filter: 1=with geographic breakdown, 0=national only
        friendly_output: If True, returns user-friendly output
    
    Returns:
        List of tables with Id, Nombre, Codigo, FK_Periodicidad, etc.
    """
    return r.get_operation_tables(operation_code, detail_level, geo_filter, friendly_output)

@mcp.tool()
def Get_Operation_Variables(operation_code: str, page: Optional[int] = None) -> List[Dict[str, Any]]:
    """Get all variables used in a given operation
    
    Args:
        operation_code: Operation code (e.g., 'IPC', 'EPA')
        page: Page number for pagination
    
    Returns:
        List of variables with Id, Nombre, and Codigo
    """
    return r.get_operation_variables(operation_code, page)

@mcp.tool()
def Get_Variable_Values_Operation(variable_id: int, operation_code: str,
                                  detail_level: Optional[int] = None) -> List[Dict[str, Any]]:
    """Get values for a variable within a specific operation
    
    Args:
        variable_id: Variable ID (e.g., 762 for ECOICOP groups)
        operation_code: Operation code (e.g., 'IPC')
        detail_level: Detail level 0, 1, or 2
    
    Returns:
        List of values with Id, FK_Variable, Nombre, and Codigo
    """
    return r.get_variable_values_operation(variable_id, operation_code, detail_level)

# =============================================================================
# Tables
# =============================================================================

@mcp.tool()
def Get_Table_Groups(table_id: int) -> List[Dict[str, Any]]:
    """Get selection groups (combos) that define a table structure
    
    Args:
        table_id: Table ID (e.g., 50913)
    
    Returns:
        List of groups with Id and Nombre
    """
    return r.get_table_groups(table_id)

@mcp.tool()
def Get_Group_Values(table_id: int, group_id: int, 
                    detail_level: Optional[int] = None) -> List[Dict[str, Any]]:
    """Get values belonging to a specific group in a table
    
    Args:
        table_id: Table ID
        group_id: Group ID (from Get_Table_Groups)
        detail_level: Detail level 0, 1, or 2
    
    Returns:
        List of values with Id, FK_Variable, Nombre, and Codigo
    """
    return r.get_group_values(table_id, group_id, detail_level)

@mcp.tool()
def Get_Table_Series(table_id: int, detail_level: Optional[int] = None,
                    friendly_output: bool = False, include_metadata: bool = False,
                    variable_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get all series codes from a table (without data)
    
    Args:
        table_id: Table ID (e.g., 50913)
        detail_level: Detail level 0, 1, or 2
        friendly_output: If True, returns user-friendly output
        include_metadata: If True, includes metadata
        variable_filter: Filter by variable:value format (e.g., '115:29')
    
    Returns:
        List of series with COD, Nombre, FK_Operacion, etc.
    """
    return r.get_table_series(table_id, detail_level, friendly_output, include_metadata, variable_filter)

@mcp.tool()
def Get_Table_Data(table_id: int, last_periods: Optional[int] = None,
                  date_range: Optional[str] = None, detail_level: Optional[int] = None,
                  friendly_output: bool = False, include_metadata: bool = False,
                  variable_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get data from a specific table
    
    Args:
        table_id: Table ID (e.g., 50902 for national CPI)
        last_periods: Last N periods to retrieve
        date_range: Date range 'YYYYMMDD:YYYYMMDD' (e.g., '20240101:20241231')
        detail_level: Detail level 0, 1, or 2
        friendly_output: If True, returns user-friendly output
        include_metadata: If True, includes metadata
        variable_filter: Filter by variable:value (e.g., '115:29')
    
    Returns:
        List of series with COD, Nombre, and Data array
    """
    return r.get_table_data(table_id, last_periods, date_range, detail_level, 
                           friendly_output, include_metadata, variable_filter)

# =============================================================================
# Series
# =============================================================================

@mcp.tool()
def Get_Series_Info(series_code: str, detail_level: Optional[int] = None,
                   friendly_output: bool = False, include_metadata: bool = False) -> Dict[str, Any]:
    """Get series metadata without data
    
    Args:
        series_code: Series code (e.g., 'IPC251852')
        detail_level: Detail level 0, 1, or 2
        friendly_output: If True, returns user-friendly output
        include_metadata: If True, includes metadata
    
    Returns:
        Series info with COD, Nombre, FK_Periodicidad, etc.
    """
    return r.get_series_info(series_code, detail_level, friendly_output, include_metadata)

@mcp.tool()
def Get_Series_Values(series_code: str, detail_level: Optional[int] = None) -> List[Dict[str, Any]]:
    """Get variables and values that define a series
    
    Args:
        series_code: Series code (e.g., 'IPC251852')
        detail_level: Detail level 0, 1, or 2
    
    Returns:
        List of values defining the series
    """
    return r.get_series_values(series_code, detail_level)

@mcp.tool()
def Get_Series_Data(series_code: str, last_periods: Optional[int] = None,
                   date_range: Optional[str] = None, detail_level: Optional[int] = None,
                   friendly_output: bool = False, include_metadata: bool = False) -> Dict[str, Any]:
    """Get data from a specific time series
    
    Args:
        series_code: Series code (e.g., 'IPC251856')
        last_periods: Last N periods to retrieve
        date_range: Date range 'YYYYMMDD:YYYYMMDD'
        detail_level: Detail level 0, 1, or 2
        friendly_output: If True, returns user-friendly output
        include_metadata: If True, includes metadata
    
    Returns:
        Series with COD, Nombre, and Data array
    """
    return r.get_series_data(series_code, last_periods, date_range, detail_level,
                            friendly_output, include_metadata)

@mcp.tool()
def Get_Operation_Series(operation_code: str, detail_level: Optional[int] = None,
                        friendly_output: bool = False, include_metadata: bool = False,
                        page: Optional[int] = None, name_filter: Optional[str] = None,
                        periodicity_filter: Optional[int] = None,
                        max_results: int = 100) -> List[Dict[str, Any]]:
    """Get series of an operation with optional filtering
    
    WARNING: Operations like IPC have 220,000+ series across 23 pages.
    Always use filters or pagination to avoid timeouts.
    
    Args:
        operation_code: Operation code (e.g., 'IPC')
        detail_level: Detail level 0, 1, or 2
        friendly_output: If True, returns user-friendly output
        include_metadata: If True, includes metadata
        page: Page number (up to 10000 results per API page)
        name_filter: Filter series by name (case-insensitive, e.g., 'Madrid', 'anual')
        periodicity_filter: Filter by periodicity ID (1=monthly, 3=quarterly, 12=annual)
        max_results: Maximum results to return (default 100, max 1000)
    
    Returns:
        List of series belonging to the operation (filtered and limited)
    """
    result = r.get_operation_series(operation_code, detail_level, friendly_output, 
                                    include_metadata, page)
    
    # Apply filters if provided
    if isinstance(result, list) and (name_filter or periodicity_filter):
        filtered = result
        if name_filter:
            nf = name_filter.lower()
            filtered = [s for s in filtered if nf in s.get('Nombre', '').lower()]
        if periodicity_filter:
            filtered = [s for s in filtered if s.get('FK_Periodicidad') == periodicity_filter]
        result = filtered
    
    # Apply limit
    limit = min(max_results, 1000)
    if isinstance(result, list) and len(result) > limit:
        total = len(result)
        return result[:limit] + [{"_info": f"Showing {limit} of {total} results. Use filters or pagination for more."}]
    
    return result

# =============================================================================
# Filtered queries
# =============================================================================

@mcp.tool()
def Get_Operation_Data_Filtered(operation_code: str, periodicity: Optional[int] = None,
                               last_periods: Optional[int] = None, detail_level: Optional[int] = None,
                               friendly_output: bool = False, include_metadata: bool = False,
                               filter_g1: Optional[str] = None, filter_g2: Optional[str] = None,
                               filter_g3: Optional[str] = None, filter_g4: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get operation data with advanced metadata filters
    
    Args:
        operation_code: Operation code (e.g., 'IPC', 'EPA')
        periodicity: Periodicity ID (1=monthly, 3=quarterly, 6=half-yearly, 12=annual)
        last_periods: Last N periods to retrieve
        detail_level: Detail level 0, 1, or 2
        friendly_output: If True, returns user-friendly output
        include_metadata: If True, includes metadata
        filter_g1: First filter 'variable_id:value_id' (e.g., '115:29' for Madrid)
        filter_g2: Second filter 'variable_id:value_id'
        filter_g3: Third filter 'variable_id:value_id' (e.g., '762:' for all ECOICOP)
        filter_g4: Fourth filter 'variable_id:value_id'
    
    Returns:
        Filtered series data from the operation
    
    Example: CPI for Madrid, monthly variation, all ECOICOP groups:
        Get_Operation_Data_Filtered('IPC', periodicity=1, filter_g1='115:29', 
                                    filter_g2='3:84', filter_g3='762:')
    """
    return r.get_operation_data_filtered(operation_code, periodicity, last_periods, detail_level,
                                         friendly_output, include_metadata, filter_g1, filter_g2,
                                         filter_g3, filter_g4)

@mcp.tool()
def Get_Series_Metadata_Operation(operation_code: str, periodicity: Optional[int] = None,
                                  detail_level: Optional[int] = None, friendly_output: bool = False,
                                  include_metadata: bool = False, filter_g1: Optional[str] = None,
                                  filter_g2: Optional[str] = None, filter_g3: Optional[str] = None,
                                  filter_g4: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get series definitions filtered by metadata (without data)
    
    Args:
        operation_code: Operation code (e.g., 'IPC')
        periodicity: Periodicity ID (1=monthly, 3=quarterly, etc.)
        detail_level: Detail level 0, 1, or 2
        friendly_output: If True, returns user-friendly output
        include_metadata: If True, includes metadata
        filter_g1: First filter 'variable_id:value_id'
        filter_g2: Second filter
        filter_g3: Third filter
        filter_g4: Fourth filter
    
    Returns:
        Series definitions matching the criteria
    """
    return r.get_series_metadata_operation(operation_code, periodicity, detail_level, 
                                           friendly_output, include_metadata, filter_g1,
                                           filter_g2, filter_g3, filter_g4)

# =============================================================================
# Variables
# =============================================================================

@mcp.tool()
def Get_All_Variables(page: Optional[int] = None) -> List[Dict[str, Any]]:
    """Get all available variables in the system
    
    Args:
        page: Page number for pagination (500 per page)
    
    Returns:
        List of variables with Id, Nombre, and Codigo
    """
    return r.get_all_variables(page)

@mcp.tool()
def Get_Variable_Values(variable_id: int, detail_level: Optional[int] = None,
                       classification: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get all possible values for a variable
    
    Args:
        variable_id: Variable ID (e.g., 115 for Provinces)
        detail_level: Detail level 0, 1, or 2
        classification: Classification code for filtering
    
    Returns:
        List of values with Id, FK_Variable, Nombre, and Codigo
    """
    return r.get_variable_values(variable_id, detail_level, classification)

@mcp.tool()
def Get_Child_Values(variable_id: int, value_id: int, 
                    detail_level: Optional[int] = None) -> List[Dict[str, Any]]:
    """Get child values within a hierarchical structure
    
    Args:
        variable_id: Variable ID (e.g., 70 for autonomous communities)
        value_id: Parent value ID (e.g., 8997 for Andalusia)
        detail_level: Detail level 0, 1, or 2
    
    Returns:
        List of child values
    """
    return r.get_child_values(variable_id, value_id, detail_level)

# =============================================================================
# Reference data
# =============================================================================

@mcp.tool()
def Get_Periodicities() -> List[Dict[str, Any]]:
    """Get all available periodicities (monthly, quarterly, annual, etc.)
    
    Returns:
        List of periodicities with Id, Nombre, and Codigo
    """
    return r.get_periodicities()

@mcp.tool()
def Get_Publications(detail_level: Optional[int] = None, 
                    friendly_output: bool = False) -> List[Dict[str, Any]]:
    """Get all available publications
    
    Args:
        detail_level: Detail level 0, 1, or 2
        friendly_output: If True, returns user-friendly output
    
    Returns:
        List of publications
    """
    return r.get_publications(detail_level, friendly_output)

@mcp.tool()
def Get_Classifications() -> List[Dict[str, Any]]:
    """Get all available classifications in the system
    
    Returns:
        List of classifications with Id, Nombre, and date
    """
    return r.get_classifications()

# =============================================================================
# Search and convenience functions
# =============================================================================

@mcp.tool()
def Search_Data(query: str, operation_filter: Optional[str] = None, 
               max_results: int = 10) -> List[Dict[str, Any]]:
    """Search for data across operations and tables
    
    Args:
        query: Search term (e.g., 'inflación', 'paro', 'población')
        operation_filter: Optional operation code to filter (e.g., 'IPC')
        max_results: Maximum number of results to return
    
    Returns:
        List of matching operations and tables
    """
    results = []
    query_lower = query.lower()
    
    # Search in operations
    operations = r.list_operations()
    for op in operations[:max_results]:
        if query_lower in op.get('Nombre', '').lower() or query_lower in op.get('Codigo', '').lower():
            results.append({"type": "operation", "code": op.get('Codigo'), 
                           "name": op.get('Nombre'), "id": op.get('Id')})
    
    # Search in tables if operation specified
    if operation_filter and len(results) < max_results:
        tables = r.get_operation_tables(operation_filter)
        for table in tables:
            if len(results) >= max_results:
                break
            if query_lower in table.get('Nombre', '').lower():
                results.append({"type": "table", "id": table.get('Id'),
                               "name": table.get('Nombre'), "operation": operation_filter})
    
    return results[:max_results]

@mcp.tool()
def Get_Latest_Data(operation_code: str, table_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get the most recent data from an operation
    
    Args:
        operation_code: Operation code (e.g., 'IPC', 'EPA')
        table_filter: Optional table name filter
    
    Returns:
        Latest data with table info and most recent values
    """
    tables = r.get_operation_tables(operation_code)
    if not tables or (isinstance(tables[0], dict) and "error" in tables[0]):
        return tables
    
    # Filter tables
    if table_filter:
        fl = table_filter.lower()
        tables = [t for t in tables if fl in t.get('Nombre', '').lower() or str(t.get('Id')) == table_filter]
    
    if not tables:
        return [{"error": f"No tables match filter '{table_filter}'"}]
    
    # Get latest data
    table = tables[0]
    data = r.get_table_data(table.get('Id'), nult=1)
    
    results = []
    for series in data[:10]:
        if series.get('Data'):
            point = series['Data'][-1] if isinstance(series['Data'], list) else series['Data']
            results.append({
                "operation": operation_code, "table_id": table.get('Id'),
                "table_name": table.get('Nombre'), "series_code": series.get('COD'),
                "series_name": series.get('Nombre'),
                "value": point.get('Valor') if isinstance(point, dict) else point,
                "date": point.get('Fecha') if isinstance(point, dict) else None
            })
    
    return results

# =============================================================================
# Censo 2021 (SDC21) Tools
# =============================================================================

from . import censo2021 as c21

@mcp.tool()
def Censo_List_Tables() -> Dict[str, Any]:
    """List available tables in Spain's 2021 Census (Censo 2021)
    
    Available tables:
    - hog: Hogares (Households)
    - nuc: Parejas y otros núcleos familiares (Couples and family nuclei)
    - per.estu: Personas en establecimientos colectivos (Persons in collective housing)
    - per.ocu: Personas residentes en viviendas familiares (Persons in family dwellings)
    - per.ppal: Total de Personas (All persons)
    - viv.fam: Viviendas familiares (Dwellings)
    - viv.ppal: Ocupados de 16 y más años (Employed persons aged 16+)
    
    Returns:
        List of tables with id and descriptions in ES/EN
    """
    return c21.get_censo_tables()

@mcp.tool()
def Censo_List_Variables(tabla: Optional[str] = None) -> Dict[str, Any]:
    """List available variables for Censo 2021 queries
    
    Variables are used to group/aggregate census data. Common variables include:
    - ID_RESIDENCIA_N1/N2/N3: Geographic level (CCAA/Province/Municipality)
    - ID_SEXO: Sex
    - ID_EDAD: Age year by year
    - ID_NACIONALIDAD_N1/N2/N3: Nationality (Spanish/Foreign, groups, country)
    
    Args:
        tabla: Optional table ID to get recommended variables for that table
    
    Returns:
        Dictionary of available variables organized by category
    """
    return c21.get_censo_variables(tabla)

@mcp.tool()
def Censo_Get_Data(
    tabla: str,
    variables: str,
    metrica: Optional[str] = None,
    idioma: str = "ES"
) -> Dict[str, Any]:
    """Get census data from Censo 2021 with flexible grouping
    
    This is the main tool for querying Spain's 2021 Census. Specify a table and
    grouping variables to aggregate census data.
    
    Args:
        tabla: Table ID (hog, nuc, per.estu, per.ocu, per.ppal, viv.fam, viv.ppal)
        variables: Comma-separated grouping variables (e.g., "ID_RESIDENCIA_N1,ID_SEXO")
        metrica: Metric to use (auto-detected if not provided):
                 - SPERSONAS: Count of persons
                 - SHOGARES: Count of households
                 - SVIVIENDAS: Count of dwellings
                 - SNUCLEOS: Count of family nuclei
        idioma: Language ES or EN (default: ES)
    
    Returns:
        Census data with metadata and data arrays
    
    Example:
        Censo_Get_Data("per.ppal", "ID_RESIDENCIA_N1,ID_SEXO")
        → Population by Autonomous Community and Sex
    """
    # Parse comma-separated variables into list
    var_list = [v.strip() for v in variables.split(",") if v.strip()]
    return c21.get_censo_data(tabla, var_list, metrica, idioma)

@mcp.tool()
def Censo_Population_By_Location(
    level: str = "N1",
    idioma: str = "ES"
) -> Dict[str, Any]:
    """Get population by geographic level from Censo 2021
    
    Quick access to population counts by administrative division.
    
    Args:
        level: Geographic level:
               - N1: Comunidad Autónoma (Autonomous Community)
               - N2: Provincia (Province)
               - N3: Municipio (Municipality)
        idioma: Language ES or EN (default: ES)
    
    Returns:
        Population counts by location
    """
    return c21.get_population_by_location(level, idioma)

@mcp.tool()
def Censo_Population_Pyramid(
    location_level: str = "N1",
    idioma: str = "ES"
) -> Dict[str, Any]:
    """Get population pyramid data (by age groups and sex)
    
    Returns population data broken down by 5-year age groups and sex,
    suitable for building population pyramids.
    
    Args:
        location_level: Geographic level for aggregation (N1=CCAA, N2=Province, N3=Municipality)
        idioma: Language ES or EN (default: ES)
    
    Returns:
        Population by age group and sex
    """
    return c21.get_population_pyramid(location_level, None, idioma)

@mcp.tool()
def Censo_Housing_By_Tenure(
    location_level: str = "N1",
    idioma: str = "ES"
) -> Dict[str, Any]:
    """Get housing data by tenure status (owned, rented, etc.)
    
    Returns dwelling counts classified by tenure regime:
    - En propiedad (Owned)
    - En alquiler (Rented)
    - Otro régimen de tenencia (Other tenure)
    
    Args:
        location_level: Geographic level (N1=CCAA, N2=Province, N3=Municipality)
        idioma: Language ES or EN (default: ES)
    
    Returns:
        Housing counts by tenure status and location
    """
    return c21.get_housing_by_tenure(location_level, idioma)

@mcp.tool()
def Censo_Households_By_Size(
    location_level: str = "N1",
    idioma: str = "ES"
) -> Dict[str, Any]:
    """Get households by size (number of members)
    
    Returns household counts by size: 1, 2, 3, 4, 5 or more persons.
    
    Args:
        location_level: Geographic level (N1=CCAA, N2=Province, N3=Municipality)
        idioma: Language ES or EN (default: ES)
    
    Returns:
        Household counts by size and location
    """
    return c21.get_households_by_size(location_level, idioma)

@mcp.tool()
def Censo_Education_Level(
    location_level: str = "N1",
    idioma: str = "ES"
) -> Dict[str, Any]:
    """Get population by education level
    
    Returns population counts by educational attainment level.
    
    Args:
        location_level: Geographic level (N1=CCAA, N2=Province, N3=Municipality)
        idioma: Language ES or EN (default: ES)
    
    Returns:
        Population by education level and location
    """
    return c21.get_education_level(location_level, idioma)

@mcp.tool()
def Censo_Nationality(
    level: int = 1,
    location_level: str = "N1",
    idioma: str = "ES"
) -> Dict[str, Any]:
    """Get population by nationality
    
    Returns population counts by nationality/country of origin.
    
    Args:
        level: Nationality detail level:
               - 1: Spanish/Foreign (Española/Extranjera)
               - 2: Large groups (Grandes grupos)
               - 3: Country (País)
        location_level: Geographic level (N1=CCAA, N2=Province, N3=Municipality)
        idioma: Language ES or EN (default: ES)
    
    Returns:
        Population by nationality and location
    """
    return c21.get_nationality_data(level, location_level, idioma)

@mcp.tool()
def Censo_Family_Nuclei(
    include_type: bool = True,
    location_level: str = "N1",
    idioma: str = "ES"
) -> Dict[str, Any]:
    """Get family nuclei data
    
    Returns counts of family nuclei (couples with/without children, 
    single parent families).
    
    Types of nuclei:
    - Pareja sin hijos (Couple without children)
    - Pareja con hijos (Couple with children)
    - Progenitor 1 con hijo(s) (Single parent 1 with children)
    - Progenitor 2 con hijo(s) (Single parent 2 with children)
    
    Args:
        include_type: Include nucleus type grouping (default: True)
        location_level: Geographic level (N1=CCAA, N2=Province, N3=Municipality)
        idioma: Language ES or EN (default: ES)
    
    Returns:
        Family nuclei counts by type and location
    """
    return c21.get_family_nuclei(include_type, location_level, idioma)

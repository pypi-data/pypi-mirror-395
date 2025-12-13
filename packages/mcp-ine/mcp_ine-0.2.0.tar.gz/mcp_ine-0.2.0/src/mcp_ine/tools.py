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

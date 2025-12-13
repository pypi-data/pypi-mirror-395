"""INE API Resources - Read operations for INE statistical data"""
from typing import Optional, List, Dict, Any
from .common import ine_request, logger

# =============================================================================
# Helper functions
# =============================================================================

def _build_tip_param(friendly: bool = False, metadata: bool = False) -> Optional[str]:
    """Build tip parameter from boolean flags"""
    tip = ('A' if friendly else '') + ('M' if metadata else '')
    return tip if tip else None

def _safe_result(data: Any) -> List[Dict[str, Any]]:
    """Ensure result is always a list"""
    if isinstance(data, dict) and "error" in data:
        return [data]
    return data if isinstance(data, list) else [data]

# =============================================================================
# Operations
# =============================================================================

def list_operations(filter_text: Optional[str] = None, det: int = None, 
                   geo: int = None, page: int = None) -> List[Dict[str, Any]]:
    """List available INE statistical operations (OPERACIONES_DISPONIBLES)"""
    params = {k: v for k, v in {'det': det, 'geo': geo, 'page': page}.items() if v is not None}
    result = ine_request("OPERACIONES_DISPONIBLES", params=params)
    
    if filter_text and isinstance(result, list):
        fl = filter_text.lower()
        result = [op for op in result if fl in op.get('Codigo', '').lower() or fl in op.get('Nombre', '').lower()]
    
    return _safe_result(result)

def get_operation(operation_code: str, det: int = None) -> Dict[str, Any]:
    """Get details of a specific operation (OPERACION)"""
    params = {'det': det} if det else None
    return ine_request("OPERACION", operation_code, params)

def get_operation_variables(operation_code: str, page: int = None) -> List[Dict[str, Any]]:
    """Get all variables used in an operation (VARIABLES_OPERACION)"""
    params = {'page': page} if page else None
    return _safe_result(ine_request("VARIABLES_OPERACION", operation_code, params))

def get_variable_values_operation(variable_id: int, operation_code: str, 
                                  det: int = None) -> List[Dict[str, Any]]:
    """Get variable values for a specific operation (VALORES_VARIABLEOPERACION)"""
    params = {'det': det} if det else None
    return _safe_result(ine_request("VALORES_VARIABLEOPERACION", f"{variable_id}/{operation_code}", params))

# =============================================================================
# Tables
# =============================================================================

def get_operation_tables(operation_code: str, det: int = None, geo: int = None,
                        friendly: bool = False) -> List[Dict[str, Any]]:
    """Get tables for an operation (TABLAS_OPERACION)"""
    params = {k: v for k, v in {'det': det, 'geo': geo}.items() if v is not None}
    if friendly:
        params['tip'] = 'A'
    return _safe_result(ine_request("TABLAS_OPERACION", operation_code, params))

def get_table_groups(table_id: int) -> List[Dict[str, Any]]:
    """Get selection groups for a table (GRUPOS_TABLA)"""
    return _safe_result(ine_request("GRUPOS_TABLA", str(table_id)))

def get_group_values(table_id: int, group_id: int, det: int = None) -> List[Dict[str, Any]]:
    """Get values of a group in a table (VALORES_GRUPOSTABLA)"""
    params = {'det': det} if det else None
    return _safe_result(ine_request("VALORES_GRUPOSTABLA", f"{table_id}/{group_id}", params))

def get_table_series(table_id: int, det: int = None, friendly: bool = False,
                    metadata: bool = False, tv: str = None) -> List[Dict[str, Any]]:
    """Get series codes from a table without data (SERIES_TABLA)"""
    params = {k: v for k, v in {'det': det, 'tv': tv}.items() if v is not None}
    tip = _build_tip_param(friendly, metadata)
    if tip:
        params['tip'] = tip
    return _safe_result(ine_request("SERIES_TABLA", str(table_id), params))

def get_table_data(table_id: int, nult: int = None, date: str = None, det: int = None,
                  friendly: bool = False, metadata: bool = False, tv: str = None) -> List[Dict[str, Any]]:
    """Get data from a table (DATOS_TABLA)"""
    params = {k: v for k, v in {'nult': nult, 'date': date, 'det': det, 'tv': tv}.items() if v is not None}
    tip = _build_tip_param(friendly, metadata)
    if tip:
        params['tip'] = tip
    return _safe_result(ine_request("DATOS_TABLA", str(table_id), params))

# =============================================================================
# Series
# =============================================================================

def get_series_info(series_code: str, det: int = None, friendly: bool = False,
                   metadata: bool = False) -> Dict[str, Any]:
    """Get series metadata without data (SERIE)"""
    params = {'det': det} if det else {}
    tip = _build_tip_param(friendly, metadata)
    if tip:
        params['tip'] = tip
    return ine_request("SERIE", series_code, params if params else None)

def get_series_values(series_code: str, det: int = None) -> List[Dict[str, Any]]:
    """Get variables/values that define a series (VALORES_SERIE)"""
    params = {'det': det} if det else None
    return _safe_result(ine_request("VALORES_SERIE", series_code, params))

def get_series_data(series_code: str, nult: int = None, date: str = None, det: int = None,
                   friendly: bool = False, metadata: bool = False) -> Dict[str, Any]:
    """Get data from a series (DATOS_SERIE)"""
    params = {k: v for k, v in {'nult': nult, 'date': date, 'det': det}.items() if v is not None}
    tip = _build_tip_param(friendly, metadata)
    if tip:
        params['tip'] = tip
    return ine_request("DATOS_SERIE", series_code, params if params else None)

def get_operation_series(operation_code: str, det: int = None, friendly: bool = False,
                        metadata: bool = False, page: int = None) -> List[Dict[str, Any]]:
    """Get all series of an operation (SERIES_OPERACION)"""
    params = {k: v for k, v in {'det': det, 'page': page}.items() if v is not None}
    tip = _build_tip_param(friendly, metadata)
    if tip:
        params['tip'] = tip
    return _safe_result(ine_request("SERIES_OPERACION", operation_code, params if params else None))

# =============================================================================
# Filtered data (metadata-based queries)
# =============================================================================

def get_operation_data_filtered(operation_code: str, p: int = None, nult: int = None,
                               det: int = None, friendly: bool = False, metadata: bool = False,
                               g1: str = None, g2: str = None, g3: str = None, 
                               g4: str = None) -> List[Dict[str, Any]]:
    """Get operation data with variable filters (DATOS_METADATAOPERACION)"""
    params = {k: v for k, v in {'p': p, 'nult': nult, 'det': det, 'g1': g1, 'g2': g2, 'g3': g3, 'g4': g4}.items() if v is not None}
    tip = _build_tip_param(friendly, metadata)
    if tip:
        params['tip'] = tip
    return _safe_result(ine_request("DATOS_METADATAOPERACION", operation_code, params if params else None))

def get_series_metadata_operation(operation_code: str, p: int = None, det: int = None,
                                  friendly: bool = False, metadata: bool = False,
                                  g1: str = None, g2: str = None, g3: str = None,
                                  g4: str = None) -> List[Dict[str, Any]]:
    """Get series definitions with filters (SERIE_METADATAOPERACION)"""
    params = {k: v for k, v in {'p': p, 'det': det, 'g1': g1, 'g2': g2, 'g3': g3, 'g4': g4}.items() if v is not None}
    tip = _build_tip_param(friendly, metadata)
    if tip:
        params['tip'] = tip
    return _safe_result(ine_request("SERIE_METADATAOPERACION", operation_code, params if params else None))

# =============================================================================
# Variables
# =============================================================================

def get_all_variables(page: int = None) -> List[Dict[str, Any]]:
    """Get all system variables (VARIABLES)"""
    params = {'page': page} if page else None
    return _safe_result(ine_request("VARIABLES", params=params))

def get_variable_values(variable_id: int, det: int = None, 
                       clasif: str = None) -> List[Dict[str, Any]]:
    """Get all values for a variable (VALORES_VARIABLE)"""
    params = {k: v for k, v in {'det': det, 'clasif': clasif}.items() if v is not None}
    return _safe_result(ine_request("VALORES_VARIABLE", str(variable_id), params if params else None))

def get_child_values(variable_id: int, value_id: int, det: int = None) -> List[Dict[str, Any]]:
    """Get child values in hierarchy (VALORES_HIJOS)"""
    params = {'det': det} if det else None
    return _safe_result(ine_request("VALORES_HIJOS", f"{variable_id}/{value_id}", params))

# =============================================================================
# Reference data
# =============================================================================

def get_periodicities() -> List[Dict[str, Any]]:
    """Get available periodicities (PERIODICIDADES)"""
    return _safe_result(ine_request("PERIODICIDADES"))

def get_publications(det: int = None, friendly: bool = False) -> List[Dict[str, Any]]:
    """Get all publications (PUBLICACIONES)"""
    params = {'det': det} if det else {}
    if friendly:
        params['tip'] = 'A'
    return _safe_result(ine_request("PUBLICACIONES", params=params if params else None))

def get_operation_publications(operation_code: str, det: int = None, 
                               friendly: bool = False) -> List[Dict[str, Any]]:
    """Get publications for an operation (PUBLICACIONES_OPERACION)"""
    params = {'det': det} if det else {}
    if friendly:
        params['tip'] = 'A'
    return _safe_result(ine_request("PUBLICACIONES_OPERACION", operation_code, params if params else None))

def get_classifications() -> List[Dict[str, Any]]:
    """Get all classifications (CLASIFICACIONES)"""
    return _safe_result(ine_request("CLASIFICACIONES"))

def get_operation_classifications(operation_code: str) -> List[Dict[str, Any]]:
    """Get classifications for an operation (CLASIFICACIONES_OPERACION)"""
    return _safe_result(ine_request("CLASIFICACIONES_OPERACION", operation_code))

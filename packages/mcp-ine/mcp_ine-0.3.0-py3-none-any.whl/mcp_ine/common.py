import os, logging, requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Minimal logging - only file, avoid stderr noise in MCP
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('mcp_ine.log')]
)
logger = logging.getLogger('mcp_ine')

load_dotenv()

# Configuration
INE_LANGUAGE = os.getenv('INE_LANGUAGE', 'ES')
INE_DEFAULT_PERIODS = int(os.getenv('INE_DEFAULT_PERIODS', '12'))
INE_BASE_URL = "https://servicios.ine.es/wstempus/js"

if INE_LANGUAGE not in ['ES', 'EN']:
    INE_LANGUAGE = 'ES'

mcp = FastMCP(
    name="mcp_ine",
    instructions="INE (Spanish Statistical Office) public data API. Access 109+ statistical operations: "
                 "IPC (CPI), EPA (Labor Force), Population, economic indicators. "
                 "Also includes Censo 2021 (Census) data: population, housing, households by location."
)

def ine_request(function: str, input_param: Optional[str] = None, 
                params: Optional[Dict] = None) -> Any:
    """Execute INE API request"""
    url = '/'.join([INE_BASE_URL, INE_LANGUAGE, function] + ([str(input_param)] if input_param else []))
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"INE API error: {url} - {e}")
        return {"error": str(e)}

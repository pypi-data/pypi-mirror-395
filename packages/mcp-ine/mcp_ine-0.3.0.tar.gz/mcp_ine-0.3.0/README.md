# INE MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/mcp-ine.svg)](https://badge.fury.io/py/mcp-ine)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

MCP Server for seamless integration with INE (Instituto Nacional de Estadística - Spanish Statistical Office) public data API. Access 109+ statistical operations including economic indicators, demographics, social statistics, and **Spain's 2021 Census (Censo 2021)** data through the Model Context Protocol.

**Perfect for:** AI assistants, data analysis tools, economic dashboards, research applications, demographic analysis, and any system that needs direct access to Spain's official statistics.

Developed by [sofias tech](https://github.com/Sofias-ai/mcp-ine/).

---

## 🚀 Quick Start

### Installation

```bash
pip install mcp-ine
```

### Basic Usage with Claude Desktop

Add to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "ine": {
      "command": "mcp-ine"
    }
  }
}
```

Restart Claude Desktop and start asking questions like:
- "¿Cuál es la inflación actual en España?"
- "Show me the unemployment rate trends for the last year"
- "Get housing price evolution in País Vasco"

### Standalone Usage

```bash
# Run the server
mcp-ine

# Or with Python
python -m mcp_ine
```

---

## ✨ What Can You Do?

This server provides a clean interface to INE's comprehensive statistical data through the Model Context Protocol (MCP), with optimized access to Spain's official statistics.

### 💡 Real-World Use Cases

**📊 Economic Analysis**
```
"Get the latest CPI data and compare it with last year"
"Show me industrial production trends for the manufacturing sector"
"What's the current housing price index?"
```

**👥 Demographics & Employment**
```
"Get unemployment rates by age group for the last quarter"
"Show population growth in major Spanish cities"
"What are the latest labor force participation rates?"
```

**🏢 Business Intelligence**
```
"Compare wage evolution across different sectors"
"Get tourism statistics for the summer season"
"Show me construction activity indicators"
```

**🔬 Research & Analysis**
```
"Download time series data for mortality rates"
"Get detailed population projections by region"
"Extract quarterly GDP components for econometric analysis"
```

### 🛠️ Available MCP Tools

The server implements **33 comprehensive tools** organized by category:

#### 🔍 **Discovery & Search**

| Tool | Purpose | Example Usage |
|------|---------|---------------|
| **`List_Operations`** | Browse 109+ statistical operations | "List all available operations" or "Find operations about prices" |
| **`Search_Data`** | Search across all data by keywords | "Search for inflation data" or "Find employment statistics" |
| **`Get_Operation_Tables`** | Get tables for a specific operation | "Show me all CPI tables" |
| **`Get_Operation_Info`** | Detailed info about an operation | "Get details about IPC operation" |

#### 📊 **Data Access**

| Tool | Purpose | Example Usage |
|------|---------|---------------|
| **`Get_Latest_Data`** | Quick access to most recent data | "Get the latest unemployment figures" |
| **`Get_Table_Data`** | Full table data with flexible filters | "Get CPI data for the last 12 months" |
| **`Get_Series_Data`** | Specific time series by code | "Get series IPC251856 for last 24 periods" |
| **`Get_Operation_Data_Filtered`** | Advanced filtering with g1-g4 params | "Get CPI for Madrid, monthly variation" |

#### 📋 **Series & Metadata**

| Tool | Purpose | Example Usage |
|------|---------|---------------|
| **`Get_Table_Series`** | List series codes from a table | "Get all series in table 50913" |
| **`Get_Operation_Series`** | List series from an operation (with filters) | "Get IPC series filtered by name" |
| **`Get_Series_Info`** | Metadata for a specific series | "Get info about series IPC251856" |
| **`Get_Series_Values`** | Variables that define a series | "What variables define IPC251856?" |
| **`Get_Series_Metadata_Operation`** | Series definitions without data | "Get CPI series metadata" |

#### 🎯 **Variables & Structure**

| Tool | Purpose | Example Usage |
|------|---------|---------------|
| **`Get_Table_Groups`** | Selection groups in a table | "What groups are in table 50913?" |
| **`Get_Group_Values`** | Values for a specific group | "Get values for group 110541" |
| **`Get_Variable_Values`** | All values for a variable | "Show all provinces (variable 115)" |
| **`Get_Operation_Variables`** | Variables used in an operation | "What variables does IPC use?" |
| **`Get_Variable_Values_Operation`** | Variable values within an operation | "Get ECOICOP groups for IPC" |

#### 📚 **Reference Data**

| Tool | Purpose | Example Usage |
|------|---------|---------------|
| **`Get_Periodicities`** | List all periodicities | "What periodicities are available?" |
| **`Get_Classifications`** | List all classifications | "Show available classifications" |
| **`Get_All_Variables`** | List all system variables (paginated) | "Get all available variables" |
| **`Get_Child_Values`** | Navigate hierarchical structures | "Get provinces within Madrid region" |
| **`Get_Publications`** | List all publications | "Show INE publications" |

---

### 🏠 **Censo 2021 (Spain's 2021 Census)** *(NEW in v0.3.0)*

Access comprehensive demographic, housing, and household data from Spain's 2021 Census through **10 specialized tools**:

#### 📋 Discovery & Variables

| Tool | Purpose | Example Usage |
|------|---------|---------------|
| **`Censo_List_Tables`** | List all available census tables | "What census tables are available?" |
| **`Censo_List_Variables`** | Get variables for grouping/aggregation | "Show variables for the persons table" |

#### 👥 Population Data

| Tool | Purpose | Example Usage |
|------|---------|---------------|
| **`Censo_Get_Data`** | Flexible census queries with custom grouping | "Get population by CCAA and sex" |
| **`Censo_Population_By_Location`** | Population by geographic level | "Population by autonomous community" |
| **`Censo_Population_Pyramid`** | Age/sex distribution for pyramids | "Get population pyramid data" |
| **`Censo_Nationality`** | Population by nationality/origin | "Show Spanish vs foreign population" |
| **`Censo_Education_Level`** | Population by educational attainment | "Education levels by region" |

#### 🏡 Housing & Households

| Tool | Purpose | Example Usage |
|------|---------|---------------|
| **`Censo_Housing_By_Tenure`** | Dwellings by ownership status | "Rented vs owned housing by CCAA" |
| **`Censo_Households_By_Size`** | Households by number of members | "How many single-person households?" |
| **`Censo_Family_Nuclei`** | Family structure data | "Couples with/without children stats" |

#### 🗺️ Geographic Levels

All Censo tools support multiple geographic levels:
- **N1**: Comunidad Autónoma (Autonomous Community) - 19 regions
- **N2**: Provincia (Province) - 52 provinces
- **N3**: Municipio (Municipality) - 8,000+ municipalities

#### 💡 Censo 2021 Usage Examples

**Natural Language Queries:**
```
"¿Cuántos habitantes tiene cada comunidad autónoma?"
"Show me housing ownership rates by province"
"Get population pyramid for Spain"
"How many single-parent families are there?"
"What's the education level distribution in Cataluña?"
```

**Programmatic Usage:**
```python
from mcp_ine.tools import (
    Censo_List_Tables,
    Censo_Get_Data,
    Censo_Population_By_Location,
    Censo_Housing_By_Tenure
)

# List available census tables
tables = Censo_List_Tables()

# Get population by autonomous community and sex
population = Censo_Get_Data(
    tabla="per.ppal",
    variables="ID_RESIDENCIA_N1,ID_SEXO"
)

# Get population by province
pop_provinces = Censo_Population_By_Location(level="N2")

# Housing tenure by region
housing = Censo_Housing_By_Tenure(location_level="N1")
```

#### 📊 Available Census Tables

| Table ID | Description (ES) | Description (EN) |
|----------|------------------|------------------|
| `per.ppal` | Total de Personas | All persons |
| `per.ocu` | Personas en viviendas familiares | Persons in family dwellings |
| `per.estu` | Personas en establecimientos | Persons in collective housing |
| `hog` | Hogares | Households |
| `nuc` | Núcleos familiares | Family nuclei |
| `viv.fam` | Viviendas familiares | Dwellings |
| `viv.ppal` | Ocupados 16+ años | Employed persons 16+ |

---

### 📊 **Available Statistical Operations**

Access to major Spanish statistical operations including:

- **IPC**: Índice de Precios de Consumo (Consumer Price Index)
- **IPCA**: Índice de Precios de Consumo Armonizado (Harmonized CPI)
- **EPA**: Encuesta de Población Activa (Labor Force Survey)
- **IPI**: Índices de Producción Industrial (Industrial Production Index)
- **IPV**: Índice de Precios de la Vivienda (Housing Price Index)
- **DPOP**: Cifras Oficiales de Población (Official Population Figures)
- **ECM**: Estadística de Defunciones (Mortality Statistics)
- **CNT**: Contabilidad Nacional (National Accounts)
- And 100+ more operations covering economy, demographics, and social statistics

### 🎯 **Key Features**

- **No Authentication Required**: Public API access, no credentials needed
- **Multi-language Support**: ES, EN, FR, CA language options
- **Flexible Time Filtering**: By last N periods, date ranges, or specific years
- **Rich Metadata**: Full access to variable definitions, units, and scales
- **Smart Search**: Find data across all operations by keywords
- **Clean JSON Responses**: Structured, easy-to-parse data format

## 🏗️ Architecture

The server is built with resource efficiency and maintainability in mind:

- **Simple HTTP client** using requests library for REST API calls
- **No authentication complexity** - public API with direct access
- **Clear separation of concerns** between configuration, server logic, and tools
- **Minimal dependencies** - only mcp, requests, and python-dotenv required
- **Efficient caching strategy** available via environment variables

---

## 📦 Installation & Setup

### Prerequisites

- Python 3.10 or higher
- Internet connection (to access INE public API)
- **No API keys required** - INE's API is public and free!

### Option 1: Install from PyPI (Recommended)

```bash
pip install mcp-ine
```

### Option 2: Install from Source

```bash
git clone https://github.com/Sofias-ai/mcp-ine.git
cd mcp-ine
pip install -e .
```

### Configuration (Optional)

The server works out of the box with sensible defaults. You can customize behavior with environment variables:

Create a `.env` file:

```bash
INE_LANGUAGE=ES              # Language: ES, EN, FR, CA (default: ES)
INE_DEFAULT_PERIODS=12       # Default periods to fetch (default: 12)
```

Or set them in your MCP client configuration:

```json
{
  "mcpServers": {
    "ine": {
      "command": "mcp-ine",
      "env": {
        "INE_LANGUAGE": "EN",
        "INE_DEFAULT_PERIODS": "24"
      }
    }
  }
}
```

---

## 🎯 How to Use

### Using with AI Assistants (Claude Desktop)

Once installed and configured, you can ask natural language questions:

**Discovery:**
```
"What statistical operations are available?"
"Find data about inflation"
"Show me employment-related datasets"
```

**Getting Data:**
```
"Get the latest CPI figures"
"Show unemployment data for the last 12 months"
"What's the current housing price index?"
```

**Analysis:**
```
"Compare CPI trends year over year"
"Get population data for Andalucía"
"Show me wage growth in the tech sector"
```

### Using Programmatically

You can also use the tools directly in your Python code:

```python
from mcp_ine.tools import (
    List_Operations, 
    Get_Latest_Data,
    Get_Table_Data,
    Get_Operation_Data_Filtered,
    Search_Data
)

# Discovery
operations = List_Operations(filter_text="precio")
search_results = Search_Data(query="inflación", max_results=5)

# Get latest data
cpi_latest = Get_Latest_Data(operation_code="IPC")

# Get historical data
cpi_history = Get_Table_Data(
    table_id=50902, 
    last_periods=12
)

# Advanced filtering: CPI for Madrid, monthly variation, all ECOICOP groups
cpi_madrid = Get_Operation_Data_Filtered(
    operation_code="IPC",
    periodicity=1,
    filter_g1="115:29",   # Province: Madrid
    filter_g2="3:84",     # Type: Monthly variation
    filter_g3="762:",     # All ECOICOP groups
    last_periods=12
)
```

### Running as Standalone Server

```bash
# Start the server
mcp-ine

# Or with Python module
python -m mcp_ine
```

The server will run and wait for MCP protocol messages via stdin/stdout.

## API Structure

### Base URL
```
https://servicios.ine.es/wstempus/js/{language}/{function}/{input}?{parameters}
```

### Common Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `nult` | Last N periods | `nult=12` for last 12 months |
| `det` | Detail level (0, 1, or 2) | `det=2` for full metadata |
| `date` | Date range | `20240101:20241231` |
| `p` | Periodicity filter | `p=1` for monthly |
| `page` | Pagination (500 results/page) | `page=2` |

### Advanced Filtering (g1-g4 parameters)

For precise data queries, use filter parameters in `variable_id:value_id` format:

```
g1=115:29     → Province: Madrid (variable 115, value 29)
g2=3:84       → Data type: Monthly variation (variable 3, value 84)
g3=762:       → All ECOICOP groups (variable 762, all values)
```

**Example:** Get CPI for Madrid, monthly variation, food products:
```
DATOS_METADATAOPERACION/IPC?g1=115:29&g2=3:84&g3=762:239699&p=1&nult=12
```

### Response Format

All responses are JSON with consistent structure:
- Operations: Array of `{Id, Codigo, Nombre, Url}`
- Tables: Array of `{Id, Nombre, Codigo, FK_Periodicidad, ...}`
- Data: Array of series with `{COD, Nombre, FK_Unidad, Data: [{Fecha, Valor, Anyo, ...}]}`

## Development

### Project Structure

```
mcp-ine/
├── src/
│   └── mcp_ine/
│       ├── __init__.py      # Entry point with asyncio
│       ├── server.py        # Main async server loop
│       ├── common.py        # Configuration, logging, HTTP client
│       └── tools.py         # MCP tool implementations
├── pyproject.toml           # Package configuration
├── README.md
├── LICENSE
├── .gitignore
└── .env.example
```

### Code Statistics

- **Total Lines**: ~320
- **Tools**: 8 comprehensive data access tools
- **Dependencies**: 3 (mcp, requests, python-dotenv)
- **Complexity**: Low - simple REST API wrapper

### Adding New Tools

Follow the minimalist pattern:

```python
@mcp.tool()
def New_Tool(param: str) -> Dict[str, Any]:
    """Tool description
    
    Args:
        param: Parameter description
    
    Returns:
        Description of return value
    """
    try:
        result = ine_request("ENDPOINT", param)
        logger.info(f"Tool executed successfully")
        return result
    except Exception as e:
        logger.error(f"Error: {e}")
        return {"error": str(e)}
```

---

## 📚 Detailed Examples

### Example 1: Economic Dashboard

Build a real-time economic indicators dashboard:

```python
from mcp_ine.tools import Get_Latest_Data

# Get key indicators
cpi = Get_Latest_Data("IPC")           # Consumer prices
ipi = Get_Latest_Data("IPI")           # Industrial production  
ipv = Get_Latest_Data("IPV")           # Housing prices
epa = Get_Latest_Data("EPA")           # Employment

print(f"CPI: {cpi}")
print(f"Industrial Production: {ipi}")
print(f"Housing Prices: {ipv}")
print(f"Employment: {epa}")
```

**With Claude Desktop:**
```
"Create a dashboard with the latest CPI, industrial production, 
housing prices, and employment data"
```

### Example 2: Inflation Analysis

Analyze inflation trends over time:

```python
from mcp_ine.tools import Get_Table_Data

# Get 2 years of monthly CPI data
cpi_data = Get_Table_Data(
    table_id=50902,      # National CPI table
    last_periods=24,     # Last 24 months
    period_type="M"      # Monthly data
)

# Process the data
for series in cpi_data:
    print(f"{series['Nombre']}: {series['Data'][:5]}")
```

**With Claude Desktop:**
```
"Show me CPI trends for the last 2 years and calculate 
the annual inflation rate"
```

### Example 3: Regional Comparison

Compare data across regions:

```python
from mcp_ine.tools import Get_Table_Variables, Get_Variable_Values

# Get available regions
variables = Get_Table_Variables(table_id=50902)
regions = Get_Variable_Values(variable_id=3, table_id=50902)

# Now get data for specific regions
for region in regions[:5]:
    print(f"Region: {region['Nombre']}")
```

**With Claude Desktop:**
```
"Compare unemployment rates across all Spanish autonomous communities"
```

### Example 4: Custom Date Range

Get data for a specific period:

```python
from mcp_ine.tools import Get_Table_Data

# Get data for calendar year 2024
data_2024 = Get_Table_Data(
    table_id=50902,
    date_range="20240101:20241231"
)
```

**With Claude Desktop:**
```
"Get CPI data specifically for the year 2024"
```

### Example 5: Search and Discover

Find relevant datasets:

```python
from mcp_ine.tools import Search_Data, List_Operations

# Search for housing-related data
housing = Search_Data(query="vivienda", max_results=10)

# List all price-related operations
prices = List_Operations(filter_text="precio")

# Search within specific operation
cpi_general = Search_Data(
    query="general", 
    operation_filter="IPC"
)
```

**With Claude Desktop:**
```
"Find all available data about housing and real estate"
"Search for wage and salary statistics"
```

---

## ⚠️ Limitations & Best Practices

### API Limitations
- **Public API** - No rate limits documented, but please use responsibly
- **Data freshness** - Depends on INE publication schedules (usually monthly/quarterly)
- **Historical data** - Availability varies by operation (some go back decades, others only recent years)
- **No authentication** - Public data only, no access to restricted datasets

### Best Practices
- **Cache responses** when possible to reduce API calls
- **Use date ranges** for large historical queries instead of fetching all data
- **Start with Search_Data** when exploring to find relevant operations
- **Check metadata** (variables, values) before requesting large tables
- **Use `last_periods`** parameter for recent data instead of full date ranges

### Performance Tips
- Use `detail_level` parameter (0-3) to control response size
- Filter by `period_type` (A/M) to get only annual or monthly data
- Use `Get_Latest_Data` for quick checks instead of full table queries

---

## 🤝 Contributing

Contributions are welcome! This project follows minimalist MCP architecture patterns.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/Sofias-ai/mcp-ine.git
cd mcp-ine

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Run tests
python test_ine_complete.py
```

### Coding Guidelines

1. **Keep it simple** - Follow the minimalist pattern
2. **Type hints** - Use type annotations for all functions
3. **Docstrings** - Document all public functions
4. **Error handling** - Always handle exceptions gracefully
5. **Logging** - Log important operations for debugging

### Running Tests

The project includes a comprehensive test suite:

```bash
python test_ine_complete.py
```

This runs 100+ tests covering all tools and edge cases.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 📋 Changelog

### v0.2.0 (December 2025)
- **18+ tools** with complete INE API coverage
- Added `Get_Operation_Data_Filtered` with g1-g4 advanced filtering
- Added `Get_Table_Series` for listing series codes from tables
- Added `Get_Operation_Info` for detailed operation metadata
- Added `Get_Operation_Series` with name/periodicity filters and pagination
- Added `Get_Series_Info`, `Get_Series_Values` for series metadata
- Added `Get_Operation_Variables`, `Get_Variable_Values_Operation`
- Added `Get_Periodicities`, `Get_Classifications`, `Get_All_Variables`, `Get_Child_Values`
- Fixed `Get_Table_Groups` (corrected endpoint from VARIABLES_TABLA to GRUPOS_TABLA)
- Fixed `Get_Variable_Values` parameter format
- Reduced logging noise (no more stderr warnings)

### v0.1.0 (November 2025)
- Initial release with 8 basic tools
- Support for List_Operations, Search_Data, Get_Table_Data, Get_Series_Data

## 🙏 Acknowledgments

- [INE (Instituto Nacional de Estadística)](https://www.ine.es/) for providing free public API access
- [Anthropic](https://www.anthropic.com/) for the Model Context Protocol
- [FastMCP](https://github.com/jlowin/fastmcp) for the excellent MCP framework

---

## 📖 Resources

### Documentation
- [INE Official Website](https://www.ine.es/)
- [INE API Documentation](https://www.ine.es/dyngs/DAB/index.htm?cid=1100)
- [API Operations Reference](https://www.ine.es/dyngs/DAB/index.htm?cid=1128)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)

### Support
- **GitHub Issues**: [mcp-ine/issues](https://github.com/Sofias-ai/mcp-ine/issues)
- **INE Official Support**: https://www.ine.es/
- **Email**: sss@sofias.ai

### Related Projects
- [mcp-sharepoint](https://github.com/Sofias-ai/mcp-sharepoint) - MCP Server for SharePoint
- [mcp-outlook](https://github.com/Sofias-ai/mcp-outlook) - MCP Server for Outlook

---

**Made with ❤️ by [sofias tech](https://github.com/Sofias-ai)**

*Following minimalist MCP architecture patterns for clean, maintainable integrations.*

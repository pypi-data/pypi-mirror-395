# inepandas

Un wrapper de Python para la API del Instituto Nacional de Estadística (INE) de España que devuelve datos como DataFrames de pandas.

> ⚠️ Este es un paquete no oficial, no está afiliado al INE.

[English version below](#english)

## Instalación

```bash
pip install inepandas
```

## Uso rápido

```python
import inepandas as ine

# Operaciones disponibles
operaciones = ine.get_operations()

# Datos de una tabla (últimos 5 periodos del IPC)
ipc = ine.get_table_data(50902, nlast=5)

# Datos de una serie
serie = ine.get_series_data("IPC251856", nlast=12)

# Datos por rango de fechas
datos_2024 = ine.get_table_data(50902, date_start="2024/01/01", date_end="2024/12/31")
```

## Funciones principales

| Función | Descripción |
|---------|-------------|
| `get_operations()` | Lista de operaciones estadísticas |
| `get_tables(operation)` | Tablas de una operación |
| `get_table_data(table_id)` | Datos de una tabla |
| `get_series_data(series_code)` | Datos de una serie |
| `get_variables(operation)` | Variables de una operación |
| `get_values(variable)` | Valores de una variable |

## IDs comunes

| ID | Descripción |
|----|-------------|
| 50902 | IPC - Índices nacionales |
| IPC251856 | IPC - Variación anual |

## Enlaces

- [Documentación](https://JonathanMair.github.io/inepandas/)
- [Documentación API INE](https://www.ine.es/dyngs/DAB/index.htm?cid=1099)
- [Referencia API](https://www.ine.es/dyngs/DAB/index.htm?cid=1100)

## Proyectos relacionados

- [ineapir](https://github.com/es-ine/ineapir) - Paquete oficial en R
- [ineware](https://github.com/rgameroe/ineware) - Wrapper Python
- [extractor_ine](https://github.com/dani537/extractor_ine) - Extractor de datos INE
- [INEAPIpy](https://github.com/VanceVisarisTenenbaum/INEAPIpy) - Cliente Python para INE
- [mcp-ine](https://pypi.org/project/mcp-ine/) - Servidor MCP para INE

## Licencia

MIT

---

# English

A Python wrapper for the Spanish National Statistics Institute (INE) API that returns data as pandas DataFrames.

> ⚠️ This is an unofficial package, not affiliated with INE.

## Installation

```bash
pip install inepandas
```

## Quick start

```python
import inepandas as ine

# Available operations
operations = ine.get_operations()

# Table data (last 5 periods of CPI)
cpi = ine.get_table_data(50902, nlast=5)

# Series data
series = ine.get_series_data("IPC251856", nlast=12)

# Date range
data_2024 = ine.get_table_data(50902, date_start="2024/01/01", date_end="2024/12/31")
```

## Main functions

| Function | Description |
|----------|-------------|
| `get_operations()` | List statistical operations |
| `get_tables(operation)` | Tables for an operation |
| `get_table_data(table_id)` | Data from a table |
| `get_series_data(series_code)` | Data from a series |
| `get_variables(operation)` | Variables for an operation |
| `get_values(variable)` | Values for a variable |

## Common IDs

| ID | Description |
|----|-------------|
| 50902 | CPI - National indices |
| IPC251856 | CPI - Annual variation |

## Links

- [Documentation](https://JonathanMair.github.io/inepandas/)
- [INE API Documentation](https://www.ine.es/dyngs/DAB/en/index.htm?cid=1099)
- [API Reference](https://www.ine.es/dyngs/DAB/en/index.htm?cid=1100)

## License

MIT
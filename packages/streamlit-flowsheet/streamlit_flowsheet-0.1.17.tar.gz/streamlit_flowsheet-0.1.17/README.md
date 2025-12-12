# Streamlit Flowsheet Component

A Streamlit component for rendering interactive process flowsheet diagrams with node selection capabilities.

## Features

- Interactive process flowsheet visualization with ReactFlow
- Node selection with detailed properties panel
- Collapsible navigation panel for easy node browsing
- Theme-aware (automatically adapts to Streamlit light/dark themes)
- Configurable display options (navigation panel, properties panel, node borders)
- Returns selected node data to Streamlit
- **NEW**: Support for multiple data formats (Model Revision API, legacy formats)
- **NEW**: Array property values with smart formatting
- **NEW**: Structured unit support with quantity information
- **NEW**: Full backward compatibility with existing flowsheet formats

## Installation

```bash
pip install streamlit-flowsheet
```

## Usage

### Basic Usage

```python
import streamlit as st
from streamlit_flowsheet import render_flowsheet
import json

# Load flowsheet data
with open("flowsheet.json", "r") as f:
    flowsheet_data = json.load(f)

# Render the flowsheet - component handles format detection automatically
selected_node = render_flowsheet(
    data=flowsheet_data,
    show_navigation_panel=True,
    show_properties=True,
    show_border=True,
    height=800
)

# Handle selection
if selected_node:
    st.write(f"Selected: {selected_node[0]['name']}")
```

### Supported Data Formats

The component automatically detects and handles multiple data formats:

#### 1. Model Revision Format (New)
```json
{
  "modelRevisionExternalId": "my-model-1",
  "flowsheets": [
    {
      "simulatorObjectNodes": [...],
      "simulatorObjectEdges": [...],
      "thermodynamics": {...}
    }
  ],
  "dataSetId": 123,
  "createdTime": 1234567890,
  "lastUpdatedTime": 1234567890
}
```

#### 2. Direct Flowsheet Format
```json
{
  "simulatorObjectNodes": [...],
  "simulatorObjectEdges": [...],
  "thermodynamics": {...}
}
```

#### 3. Legacy Format
```json
{
  "items": [
    {
      "flowsheet": {
        "simulatorObjectNodes": [...],
        "simulatorObjectEdges": [...]
      }
    }
  ]
}
```

### Property Display Features

The component now supports:

- **Array Values**: Automatically formats and truncates long arrays
  - `[1.2, 2.3, 3.4]` for short arrays
  - `[1.2, ..., 9.8] (100 items)` for long arrays

- **Scientific Notation**: Auto-formats extreme values
  - Numbers < 0.0001 or > 1,000,000 use exponential notation

- **Structured Units**: Supports both simple and complex unit formats
  ```json
  {
    "name": "Temperature",
    "value": 363.15,
    "unit": {
      "name": "K",
      "quantity": "temperature"
    }
  }
  ```

### Examples

See the `examples/` folder for complete examples:
- `iise.json` - IISE format flowsheet
- `dwsim.json` - DWSIM format flowsheet (large, complex example)

Run the example app:
```bash
streamlit run example_app.py
```

## Parameters

- `data` (dict): Flowsheet data in any supported format (automatically detected)
  - Model Revision format with `modelRevisionExternalId` and `flowsheets[]`
  - Direct flowsheet format with `simulatorObjectNodes` and `simulatorObjectEdges`
  - Legacy format with `items[]` array
- `show_navigation_panel` (bool): Show/hide the left navigation panel (default: True)
- `show_properties` (bool): Show/hide the properties panel on node selection (default: True)
- `show_border` (bool): Show/hide node borders (default: True)
- `height` (int): Component height in pixels (default: 800)

## Data Format Details

### Edges
Supports both old and new edge formats:
- New: `sourceId`, `targetId`, `connectionType`
- Legacy: `source`, `target`, `sourcePort`, `targetPort`

### Reference Objects
Supports multiple reference object formats:
- Legacy: `{ "address": "TANK.001.Volume" }`
- IISE: `{ "link": "Source.F", "components": "H2O|CO2|..." }`
- DWSIM: `{ "objectName": "Stream1", "objectType": "Material Stream", "objectProperty": "PROP_MS_0" }`

### Units
Supports both simple and structured units:
- Simple: `"unit": "K"`
- Structured: `"unit": { "name": "K", "quantity": "temperature" }`

## Development

### Setup

```bash
cd streamlit-flowsheet
uv sync --dev
cd streamlit_flowsheet/frontend
npm install
```

### Build Frontend

```bash
cd streamlit_flowsheet/frontend
npm run build
```

### Build Package

```bash
uv build
```

## License

MIT
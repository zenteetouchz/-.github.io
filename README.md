# สาบาย Stock

Inventory management dashboard for product stock tracking and sales overview, built with Streamlit.

## Features
- Executive dashboard
- Product detail view
- Stock management and editing
- Search and filtering
- Analytics charts
- JSON-based local data storage
- Optional password protection via environment variable

## Requirements
- Python 3.10+
- pip

## Installation

```bash
python -m pip install -r requirements.txt
```

## Run locally

```bash
streamlit run qpp.py
```

Then open the local URL shown by Streamlit in the terminal, usually:

```text
http://localhost:8501
```

## Mobile access

Run the app on your computer and open it from your phone using the computer's local network IP and the Streamlit port.

Example:

```text
http://192.168.1.25:8501
```

## Optional password protection
Set an environment variable before running:

```bash
INVENTORY_APP_PASSWORD=your_password_here
```

## Project data files
- `inventory_db.json` — product inventory data
- `inventory_history.json` — history log of changes

## Notes
- This version uses JSON files for simple local storage.
- It is suitable for small inventory use and demo projects.
- For production scaling, you can later migrate to a database-backed service.

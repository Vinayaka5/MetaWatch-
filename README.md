# MetaWatch Dashboard 🛡️
### Data Quality Monitoring Tool for OpenMetadata

> WeMakeDevs x OpenMetadata Hackathon 2026 — **Track T-02: Data Observability**

---

## The Problem

Data teams managing hundreds of tables have no single, unified view to monitor data quality across their entire data ecosystem. Issues like NULL values, stale data, and failed test cases go unnoticed until they cause downstream failures — costing time and trust.

## The Solution

**MetaWatch** is a Flask web dashboard that connects to OpenMetadata's REST API, retrieves data quality test results, and presents them in a clean real-time monitoring interface — giving data teams instant, visual clarity on which tables are healthy and which need attention.

---

## Features

- 📊 **Overview Dashboard** — Summary cards: Total Tables, Healthy, Warning, Critical, Tests Run, Pass Rate
- 📈 **7-Day Trend Chart** — Line chart showing quality score movement over time (Chart.js)
- 🍩 **Health Distribution** — Donut chart showing the breakdown of table health statuses
- 🚨 **Alert Panel** — Highlighted sections for Critical and Warning tables requiring immediate action
- 🗂️ **Table Health Page** — Full table list with color-coded health scores, progress bars, and status badges
- 🧪 **Test Results Page** — Detailed view of every individual test case with pass/fail status
- 🔄 **Auto-Refresh** — Dashboard refreshes every 60 seconds (live monitoring feel)
- 🔌 **Demo Mode** — Works with realistic mock data even without a running OpenMetadata instance

---

## Tech Stack

| Technology | Role |
|---|---|
| Python 3.10+ | Core language |
| Flask | Web framework and routing |
| OpenMetadata REST API | Data quality data source |
| Pandas | Data processing |
| Bootstrap 5 | Responsive layout |
| Chart.js | Trend and distribution charts |
| DM Sans + JetBrains Mono | Typography |

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- Docker Desktop (for live OpenMetadata connection)

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/metawatch-dashboard
cd metawatch-dashboard

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app (works in Demo Mode without Docker)
python app.py

# 5. Open in browser
# http://localhost:5000
```

### Live Mode with OpenMetadata (Optional)

```bash
# Download and start OpenMetadata via Docker
docker compose up --detach

# Wait 5 minutes, then open:
# http://localhost:8585  →  admin / admin

# MetaWatch will auto-connect when OpenMetadata is running
```

---

## Demo Video

[▶️ Watch the Demo on YouTube](https://www.youtube.com/watch?v=HXMeiJy8uTw)

---

## Screenshots

### Overview Dashboard
![Overview Dashboard](https://drive.google.com/drive/u/0/folders/1xr-Nz5MmZ7RIhRqy_dtxCNB028zWvD-E)
![Overview Dashboard](https://drive.google.com/drive/u/0/folders/1xr-Nz5MmZ7RIhRqy_dtxCNB028zWvD-E)

### Table Health Page
![Table Health](https://drive.google.com/drive/u/0/folders/1xr-Nz5MmZ7RIhRqy_dtxCNB028zWvD-E)

### Test Results Page
![Test Results](https://drive.google.com/drive/u/0/folders/1xr-Nz5MmZ7RIhRqy_dtxCNB028zWvD-E)

---

## Project Structure

```
metawatch-dashboard/
│
├── app.py                      # Flask application & routes
├── openmetadata_client.py      # OpenMetadata API client + mock data
├── data_processor.py           # Data transformation with Pandas
├── requirements.txt
│
├── templates/
│   ├── base.html               # Master layout (sidebar, nav)
│   ├── index.html              # Overview dashboard
│   ├── tables.html             # Table health list
│   └── tests.html              # Test results detail
│
└── static/
    └── style.css               # Custom dark theme CSS
```

---

## How It Works

1. `openmetadata_client.py` makes HTTP GET requests to OpenMetadata's REST API using Basic Auth
2. `data_processor.py` processes the raw JSON responses into health scores using Pandas
3. Flask routes serve the processed data to Jinja2 HTML templates
4. Chart.js renders the trend and distribution charts client-side via a `/api/trend` endpoint
5. If OpenMetadata is unreachable, rich mock data is used automatically (Demo Mode)

---

## Hackathon

**WeMakeDevs x OpenMetadata — #BackToTheMetadata Hackathon 2026**
Track: **Paradox T-02 — Data Observability**

---

*Built with Python + Flask + OpenMetadata API · April 2026*

# Tojo Assistant - Architecture

## Overview
Tojo Assistant is a business data assistant themed after Kirumi Tojo from Danganronpa.
It provides an Electron desktop GUI that wraps OpenClaw (Claude Code CLI) with
specialized business capabilities: file organization, Salesforce integration,
Excel/Google Sheets processing & error checking, database connectivity, and
dynamic API discovery for building data pipelines.

## System Architecture

```
+---------------------------+
|   Electron Desktop App    |
|  (Kirumi Tojo themed UI)  |
|   - Chat interface        |
|   - Pipeline builder      |
|   - File browser          |
+----------+----------------+
           | IPC / HTTP
+----------v----------------+
|   Python Backend (FastAPI) |
|   - REST API server        |
|   - WebSocket for streaming|
+----------+-----------------+
           |
    +------+------+------+------+------+
    |      |      |      |      |      |
  Core  Integrations  Pipeline  OpenClaw  WSL
    |      |            |        Bridge   Mgr
    |      +-- Salesforce
    |      +-- Google Suite
    |      +-- Databases
    |      +-- API Discovery
    |
    +-- File Organizer
    +-- Excel/Sheets Error Checker
    +-- Data Processor
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Desktop App | Electron 28+ |
| Frontend | HTML/CSS/JS (vanilla, hackathon-speed) |
| Backend | Python 3.13 + FastAPI |
| IPC | HTTP REST + WebSocket |
| Installer | electron-builder (.exe) |
| AI Engine | OpenClaw (Claude Code CLI) via WSL |
| Testing | pytest (Python), GitHub Actions |

## Directory Structure

```
tojo-assistant/
├── electron/              # Electron desktop app
│   ├── main.js            # Main process
│   ├── preload.js         # Preload script (context bridge)
│   └── renderer/          # Frontend
│       ├── index.html     # Main UI
│       ├── styles.css     # Kirumi Tojo theme
│       ├── app.js         # Frontend logic
│       └── assets/        # UI assets
├── backend/               # Python backend
│   ├── server.py          # FastAPI entry point
│   ├── core/              # Core business logic
│   │   ├── file_organizer.py
│   │   ├── excel_checker.py
│   │   └── data_processor.py
│   ├── integrations/      # External service connectors
│   │   ├── salesforce.py
│   │   ├── google_suite.py
│   │   ├── databases.py
│   │   └── api_discovery.py
│   ├── pipeline/          # Data pipeline builder
│   │   └── builder.py
│   └── openclaw/          # OpenClaw bridge
│       └── bridge.py
├── tests/                 # Test suite
│   └── backend/           # Python tests
├── .github/workflows/     # CI/CD
├── assets/                # Shared assets (avatar, icons)
├── installer/             # Installer config
└── planning/              # Architecture docs
```

## Key Design Decisions

1. **Electron + Python**: Electron for accessible GUI, Python for data processing
   power and library ecosystem (pandas, openpyxl, simple-salesforce, etc.)

2. **FastAPI backend**: Async-capable, auto-generates OpenAPI docs, WebSocket
   support for streaming OpenClaw output to the UI.

3. **WSL bridge**: OpenClaw runs in WSL. The bridge detects WSL, translates
   paths, and manages the subprocess lifecycle.

4. **Plugin-style integrations**: Each integration (Salesforce, G-Suite, DB)
   is a self-contained module with a common interface for the pipeline builder.

5. **Excel error checker**: Dedicated module for detecting common spreadsheet
   errors (#REF!, #VALUE!, circular refs, type mismatches, etc.)

## Data Flow

1. User sends request via Electron chat UI
2. Electron forwards to Python backend (FastAPI)
3. Backend routes to appropriate module:
   - Simple data ops -> Core modules handle directly
   - Complex reasoning -> OpenClaw bridge delegates to Claude
   - External data -> Integration modules fetch/push
4. Results stream back via WebSocket to Electron UI
5. Pipeline builder chains multiple steps together

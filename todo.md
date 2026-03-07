# Tojo Assistant - TODO

## Completed
- [x] Project architecture and directory structure
- [x] Planning documentation (planning/architecture.md)
- [x] Python backend core modules (file_organizer, excel_checker, data_processor)
- [x] Integration modules (salesforce, google_suite, databases, api_discovery)
- [x] Pipeline builder
- [x] OpenClaw bridge with WSL manager
- [x] FastAPI server with REST + WebSocket endpoints
- [x] Electron desktop app with Kirumi Tojo theme
- [x] Full test suite (8 test files)
- [x] GitHub Actions CI workflow
- [x] electron-builder config for .exe installer
- [x] requirements.txt and package.json
- [x] Competitor analysis module with web scraping + Blue Ocean Strategy
- [x] Competitor analysis REST endpoints and WebSocket chat handler
- [x] Strategy section in Electron sidebar UI
- [x] Competitor analysis test suite

## Security Notes
- [ ] **Brave Search API key exposure risk**: If we bundle a Brave API key in the app for out-of-the-box web search, the key is exposed in the distributed binary. For the hackathon demo this is acceptable, but for any real release we need a proper solution (proxy server, user-provided keys, or a different search approach). May not be needed if browser relay handles web research.

## Installer - Full Zero-to-Working Setup
The .exe installer must handle everything for non-technical users:
- [ ] **Install WSL** if not present (`wsl --install` requires admin + reboot)
- [ ] **Install Ubuntu distro** in WSL
- [ ] **Install Chromium** in WSL Ubuntu (`apt install chromium-browser`)
- [ ] **Install OpenClaw** in WSL (`npm install -g openclaw`)
- [ ] **Configure OpenClaw** (gateway, browser relay, managed browser profile)
- [ ] **Start gateway + browser relay** automatically on app launch
- [ ] Handle the reboot requirement after WSL install (resume setup after reboot)
- [ ] Handle admin elevation (WSL install needs it, rest doesn't)
- [ ] Progress UI during first-time setup (could take several minutes)

## Next Steps
- [ ] Run tests and fix any failures
- [ ] Add integration tests with mock external services
- [ ] Polish the Electron UI (error states, loading indicators)
- [ ] Add OpenClaw command routing in the chat interface
- [ ] Set up Google OAuth2 credential flow in Electron
- [ ] Add Salesforce credential management UI
- [ ] Implement pipeline visual builder in the frontend
- [ ] Add data preview/visualization in the chat
- [ ] Package and test the .exe installer end-to-end
- [ ] Write user documentation

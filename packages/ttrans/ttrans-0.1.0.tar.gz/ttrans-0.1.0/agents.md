# ttrans: macOS Meeting Transcription Assistant

## Project Overview
`ttrans` is a terminal-based meeting assistant for macOS. It captures audio from both the microphone and system output (Zoom, Teams, etc.), transcribes it locally using Apple's MLX framework (Whisper), and generates AI-powered summaries using an LLM (OpenAI compatible).

## Key Features
*   **Dual Audio Capture:** Simultaneously records microphone and system audio (using `ScreenCaptureKit`).
*   **Local Transcription:** Uses `lightning-whisper-mlx` for fast, private, on-device transcription.
*   **TUI Interface:** Built with `textual` for a rich terminal user experience.
*   **AI Summaries:** Generates meeting summaries and action items.
*   **Transcript Management:** Browse, view, and manage saved transcripts directly from the TUI.

## Tech Stack
*   **Language:** Python 3.11+
*   **UI Framework:** [Textual](https://textual.textualize.io/)
*   **ML Framework:** [MLX](https://github.com/ml-explore/mlx) (Apple Silicon optimized)
*   **Audio:** `sounddevice` (mic), `ScreenCaptureKit` via `pyobjc` (system)
*   **Dependency Management:** `uv`

## Setup & Installation

### Prerequisites
*   macOS 12.3+ (Required for `ScreenCaptureKit`)
*   Python 3.11+
*   `uv` (Universal Python Package Installer)

### Installation
```bash
# Install dependencies
uv sync
```

## Development Workflow

### Running the Application
To start the main TUI application:
```bash
uv run python meeting_assistant.py
```
*Note: The first run will download the Whisper model weights.*

### Running Tests
The project uses `pytest`. System audio components are mocked for cross-platform compatibility during testing.
```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest test_meeting_assistant.py
```

### Linting & Formatting
The project uses `ruff` for linting and formatting.
```bash
# Check for issues
uv run ruff check .

# Auto-format code
uv run ruff format .
```

## Architecture

### Core Components (`meeting_assistant.py`)
*   **`MeetingAssistantApp`:** The main Textual App class managing the UI and application state.
*   **`AudioEngine`:** Captures microphone input using `sounddevice`.
*   **`SystemAudioEngine`:** Captures system audio using macOS `ScreenCaptureKit`.
*   **`AudioMixer`:** Mixes multiple audio streams (mic + system) into a single mono 16kHz stream for the transcriber.
*   **`Transcriber`:** Wraps `lightning-whisper-mlx` to process audio buffers and generate text.
*   **`PermissionManager`:** Handles macOS screen recording permissions required for system audio capture.

### Configuration
User settings (API keys, model preferences) are stored in `~/.ttrans` (TOML format).

## Key Files
*   `meeting_assistant.py`: The core application logic.
*   `main.py`: Simple entry point wrapper.
*   `test_meeting_assistant.py`: Unit tests with mocking infrastructure.
*   `pyproject.toml`: Project dependencies and configuration.
*   `CLAUDE.md`: Existing context file (reference).

## Usage Tips
*   **Permissions:** The app requires "Screen Recording" permission to capture system audio.
*   **Key Bindings:**
    *   `r`: Start Recording
    *   `space`: Stop Recording
    *   `s`: Settings
    *   `a`: Audio Sources
    *   `t`: Transcript Browser
    *   `d`: Select Input Device
## Fidelity & Execution Rules  <!-- PREPOPULATED, TUNE PER PROJECT -->

These rules apply to fidelity-oriented workflows (PRDs/specs → tasks → implementation, simplification plans, etc.).

### Fidelity

- Treat the source document (user requirements, PRD, specification, or task file) as the single source of truth.
- Do not add requirements, tests, or security work beyond what is explicitly specified, unless this project section explicitly allows it.
- Do not broaden scope; when something is ambiguous or missing, ask for clarification instead of guessing.
- Preserve stated constraints and limitations unless this file explicitly authorizes changing them.

### Execution

- **Branches**
  - Do implementation work on a non-`main` branch.
  - Branch naming convention: `TODO` (e.g., `feature/<short-summary>`, `issue/<ticket-id>`).

- **Testing & Validation**
  - Primary test command(s): `TODO` (e.g., `npm test`, `pytest`, `cargo test`).
  - Additional checks (fill in as relevant):
    - Lint: `TODO` (e.g., `npm run lint`)
    - Typecheck: `TODO`
    - Build: `TODO`
    - Security / SAST: `TODO`
  - Before committing behavior changes, run the primary tests and any required additional checks for the touched area.

- **Task Lists & Plans**
  - When working from markdown task lists or simplification plans:
    - After completing a listed sub-task or step, immediately change its checkbox from `[ ]` to `[x]` in the same file.
    - Verify that the change is present in the file (avoid batching updates at the end).
    - Keep any “Relevant Files” / “Changed Files” sections accurate as files are created or modified.

## Security & Data Handling  <!-- PROJECT-SPECIFIC -->

- **Data classifications:** TODO (what data is sensitive, PII, etc.)
- **Forbidden behaviors:** TODO (e.g., never log secrets, never write to certain directories)
- **AuthN/AuthZ expectations:** TODO (e.g., always enforce permission checks in certain layers)
- **External services / secrets management:** TODO (e.g., how to access APIs, where secrets live)

## Testing Philosophy  <!-- PROJECT-SPECIFIC, WITH HINTS -->

- **Preferred test types:** TODO (unit vs integration vs e2e)
- **Coverage expectations:** TODO (e.g., “no new code without tests near 80%+ coverage in this module”)
- **Flaky / slow tests:** TODO (list known problematic suites, how to handle them)

## Git & Review Workflow  <!-- PROJECT-SPECIFIC -->

- **Branch protection rules:** TODO (what’s protected, and how)
- **Commit style:** TODO (e.g., Conventional Commits)
- **Review expectations:** TODO (e.g., when to request a human review, which files are high-risk)
- **CI / CD:** TODO (what pipelines run on PRs, what must be green before merge)

## Documentation & Task Files  <!-- PROJECT-SPECIFIC -->

- **Key docs:** TODO (e.g., `README.md`, `TESTING.md`, `ARCHITECTURE.md`, any API docs)
- **Task / PRD locations:** TODO (e.g., `/tasks/prd-*.md`, `/tasks/tasks-*.md`)
- **Doc update expectations:** TODO (e.g., “update README and API docs whenever public behavior changes”)

---

Agents should treat this `AGENTS.md` as authoritative for project-specific rules and combine it with any instructions in prompt files that are invoked from Codex. When in doubt, prefer the stricter rule (safer choice) and surface ambiguities to the human operator.


## Linear Integration (ltui)

`ltui` is the token-efficient Linear CLI for AI agents (replaces the legacy linear CLI/MCP). Use it for all Linear interactions.

### Setup
1. Get a Linear API key: https://linear.app/settings/api
2. Configure authentication:
   ```bash
   ltui auth add --name default --key <api-key>
   ltui auth list
   ltui teams list
   ```

### Project Alignment (.ltui.json)
Create a `.ltui.json` in the repo root so agents target the right team/project by default:
```json
{
  "profile": "default",
  "team": "ENG",
  "project": "Doc Thingy",
  "defaultIssueState": "Todo",
  "defaultLabels": ["bug"],
  "defaultAssignee": "me"
}
```
Commit this file so everyone shares the defaults.

### Common Commands
```bash
ltui issues view <ISSUE_KEY> --format detail
ltui issues create --team <TEAM> --project "Project Name" --title "Issue title" --description "Description" --state "Backlog" --label bug
ltui issues update <ISSUE_KEY> --state "In Review"
ltui issues comment <ISSUE_KEY> --body "Comment text"
ltui issues link <ISSUE_KEY> --url <pr-url> --title "PR #123"
```

For more, run `ltui --help` or see the ltui README in this configuration repo.

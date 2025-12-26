# Distributed Log Analysis & Threat Detection Engine

This project implements a distributed log analysis and threat detection engine with a Rust backend and an Astro frontend. It supports sequential, parallel, and distributed master-worker execution modes for log processing, along with AI-assisted explanation and rule generation.

## Project Structure

- `backend/`: Contains the Rust backend code.
  - `src/`: Rust source files for log parsing, threat detection, analysis modes, and utilities.
- `frontend/`: Contains the Astro frontend code.
  - `src/components/`: Astro and React components for the UI.
  - `src/layouts/`: Astro layouts.
  - `src/pages/`: Astro pages.
  - `public/data/`: Example log files and metrics data.
- `ai_modules/`: Python modules for AI-assisted functionalities.
  - `explanation_ai.py`: Generates natural language explanations for analysis results.
  - `rule_generation_ai.py`: Generates structured rules from natural language descriptions.
- `generate_logs.py`: Python script to generate example log data.
- `README.md`: This file.

## Features

### Backend (Rust)
- **Execution Modes**: Sequential, Parallel (using Rayon), and Distributed Master-Worker for scalable log processing.
- **Concurrency**: Utilizes Tokio for asynchronous networking and `Arc<Mutex>` for thread-safe shared state.
- **Modular Design**: Well-organized codebase with clear separation of concerns.
- **Threat Detection**: Stateful threat detection rules.
- **Error Handling**: Robust error handling using Rust's `Result` type.

### Frontend (Astro + React)
- **Modern UI**: Built with Astro for static content and React for interactive components (Astro Islands Architecture).
- **Log Analysis Dashboard**: Displays performance metrics (execution time, logs per second, alerts generated) and active rules.
- **Rule Input**: Allows manual rule creation and AI-assisted rule generation from natural language.
- **AI Explanation**: Provides natural language explanations and recommendations based on analysis results.

### AI Modules (Python)
- **Result Explanation**: `explanation_ai.py` takes JSON metrics as input and provides human-readable insights.
- **Rule Generation**: `rule_generation_ai.py` converts natural language rule descriptions into structured rule formats.

## Setup and Installation

### Prerequisites
- Rust (latest stable version)
- Node.js (LTS version) and npm/yarn
- Python 3.x

### 1. Clone the Repository

```bash
git clone <repository_url>
cd project
```

### 2. Generate Example Logs

First, generate a large example log file for testing:

```bash
python generate_logs.py
```
This will create `frontend/public/data/example_log.txt` with 500k-1M log entries.

### 3. Backend Setup (Rust)

Navigate to the `backend` directory and build the Rust project:

```bash
cd backend
cargo build --release
```

To run the backend (e.g., in sequential mode):

```bash
cargo run --release -- sequential
```

Replace `sequential` with `parallel` or `distributed` to run in different modes. The backend will expose an API for the frontend to interact with.

### 4. Frontend Setup (Astro)

Navigate to the `frontend` directory and install dependencies:

```bash
cd frontend
npm install
```

To start the Astro development server:

```bash
npm run dev
```

This will typically start the server at `http://localhost:4321`. Open this URL in your browser to access the dashboard.

### 5. AI Modules (Python)

The AI modules are designed to be called by the backend (or directly for testing). Ensure you have Python dependencies installed:

```bash
pip install -r requirements.txt # (You might need to create a requirements.txt if not present)
```

## Usage

1. **Start the Backend**: Run the Rust backend in your desired mode (sequential, parallel, or distributed).
2. **Start the Frontend**: Run the Astro development server.
3. **Interact with the Dashboard**: 
   - Use the buttons to run log analysis in different modes.
   - Add manual rules or generate rules using the AI-assisted feature.
   - Get AI explanations for the analysis results.

## Contributing

Feel free to fork the repository and contribute. Please follow standard coding practices and submit pull requests.

## License

[Specify your license here, e.g., MIT, Apache 2.0, etc.]

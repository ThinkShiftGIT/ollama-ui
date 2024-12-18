# Ollama UI

A beautiful and user-friendly interface for interacting with Ollama AI models on Windows.

## Features

- Clean, modern interface
- Support for multiple Ollama models
- Real-time model responses
- Responsive design
- Easy-to-use prompt interface

## Prerequisites

- Python 3.8 or higher
- Ollama installed and running on your system
- pip (Python package manager)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/ollama-ui.git
cd ollama-ui
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Make sure Ollama is running on your system
2. Start the Flask application:
```bash
python app.py
```
3. Open your web browser and navigate to `http://localhost:5000`
4. Select your desired model from the dropdown
5. Enter your prompt and click "Generate"

## Development

- The application uses Flask for the backend
- Frontend is built with HTML, CSS (Tailwind CSS), and vanilla JavaScript
- Styles can be customized in `static/style.css`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

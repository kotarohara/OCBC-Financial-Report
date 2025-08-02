# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python project focused on PDF to Markdown conversion and data extraction from financial documents. The project is organized with a backend/ directory containing the Python API service, preparing for future frontend integration.

## Directory Structure

```
/
├── backend/           # Python API service
│   ├── app.py        # Flask REST API
│   ├── pdf2markdown.py
│   ├── format_markdown.py
│   ├── requirements.txt
│   └── uploads/      # Temporary file storage
├── Dockerfile        # Docker configuration
├── docker-compose.yml
└── CLAUDE.md
```

## Key Files and Architecture

- `backend/pdf2markdown.py`: Handles PDF password removal and conversion to markdown using PyPDF2 and MarkItDown
- `backend/format_markdown.py`: Uses Anthropic's Claude API to extract and organize table data from markdown content
- `backend/app.py`: Flask REST API service providing endpoints for PDF processing

The workflow is typically:
1. Use `pdf2markdown.py` to convert protected PDF → unprotected PDF → markdown
2. Use `format_markdown.py` to organize extracted markdown content via Claude API

## Dependencies

The project requires:
- `PyPDF2` - for PDF manipulation and password removal
- `markitdown` - for PDF to markdown conversion
- `anthropic` - for Claude API integration
- `python-dotenv` - for environment variable management

## Environment Setup

- Set `ANTHROPIC_API_KEY` environment variable (loaded via dotenv)
- Ensure input PDF files are present in the project root

## Running the Tools

### PDF to Markdown Conversion
```bash
cd backend
python pdf2markdown.py
```
- Expects a file named 'Wealth Report-5728-Jun-25.pdf' in the backend directory
- Creates an unprotected PDF and corresponding .md file
- Update the `pdf_filename` variable for different input files

### Markdown Formatting and Data Extraction
```bash
cd backend
python format_markdown.py
```
- Processes 'Wealth Report-5728-Jun-25.md' by default
- Outputs organized tables to '_organized.md' file
- Update `input_file` and `output_file` variables for different files

## Dockerized Service

The project has been converted to a Flask-based REST API service that can be deployed with Docker.

### Building and Running the Service

```bash
# Build and run with docker-compose
docker-compose up --build

# Or build and run manually
docker build -t pdf-to-markdown .
docker run -p 5001:5001 --env-file .env pdf-to-markdown
```

### API Endpoints

- `GET /health` - Health check endpoint
- `POST /process-pdf` - Upload PDF, returns both raw and organized markdown
- `POST /process-pdf/raw` - Upload PDF, returns only raw markdown

### API Usage Examples

```bash
# Process PDF with both raw and organized output
curl -X POST -F "file=@document.pdf" http://localhost:5001/process-pdf

# Process password-protected PDF
curl -X POST -F "file=@document.pdf" -F "password=mypassword" http://localhost:5001/process-pdf

# Get only raw markdown
curl -X POST -F "file=@document.pdf" http://localhost:5001/process-pdf/raw
```

### Environment Configuration

Create a `.env` file with:
```
ANTHROPIC_API_KEY=your_api_key_here
```

## Code Conventions

- Uses Flask for REST API with proper error handling and validation
- Temporary file management for PDF processing security
- Claude API configured for data extraction with specific prompts for table preservation
- Uses UTF-8 encoding for all file operations
- Production-ready with gunicorn and health checks
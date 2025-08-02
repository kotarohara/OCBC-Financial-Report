# PDF to Markdown Service

A Dockerized REST API service that converts PDF files to markdown format with optional table extraction and organization using Claude AI.

## Features

- Convert PDF files to raw markdown
- Extract and organize tables using Claude AI
- Handle password-protected PDFs
- REST API with JSON responses
- Docker containerization for easy deployment
- Production-ready with gunicorn

## Quick Start

1. Clone the repository
2. Create a `.env` file with your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```
3. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

The service will be available at `http://localhost:5000`

## API Endpoints

### Health Check
```bash
GET /health
```

### Process PDF (Full)
Returns both raw markdown and organized tables:
```bash
POST /process-pdf
Content-Type: multipart/form-data

Parameters:
- file: PDF file (required)
- password: PDF password (optional)
```

### Process PDF (Raw Only)
Returns only raw markdown conversion:
```bash
POST /process-pdf/raw
Content-Type: multipart/form-data

Parameters:
- file: PDF file (required)
- password: PDF password (optional)
```

## Usage Examples

```bash
# Basic PDF processing
curl -X POST -F "file=@document.pdf" http://localhost:5000/process-pdf

# Password-protected PDF
curl -X POST -F "file=@document.pdf" -F "password=secret123" http://localhost:5000/process-pdf

# Raw markdown only
curl -X POST -F "file=@document.pdf" http://localhost:5000/process-pdf/raw
```

## Response Format

```json
{
  "success": true,
  "raw_markdown": "# Document Title\n\nContent...",
  "organized_markdown": "# Organized Tables\n\n## Table 1...",
  "filename": "document.pdf"
}
```

## Development

### Local Development
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key
python app.py
```

### Docker Build
```bash
docker build -t pdf-to-markdown .
docker run -p 5000:5000 --env-file .env pdf-to-markdown
```

## Dependencies

- Flask - Web framework
- PyPDF2 - PDF processing
- markitdown - PDF to markdown conversion
- anthropic - Claude AI integration
- gunicorn - Production WSGI server
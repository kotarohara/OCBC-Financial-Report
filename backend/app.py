from flask import Flask, request, jsonify
import os
import tempfile
import PyPDF2
from markitdown import MarkItDown
import anthropic
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Initialize clients
md = MarkItDown()
anthropic_client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

def process_pdf_to_markdown(pdf_file, password=None):
    """Convert PDF to markdown, handling password protection if needed."""
    try:
        # Create temporary files
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
            pdf_file.save(temp_pdf.name)
            
            # Check if PDF is password protected and handle it
            if password:
                with open(temp_pdf.name, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    if reader.is_encrypted:
                        reader.decrypt(password)
                        
                        # Create unprotected version
                        writer = PyPDF2.PdfWriter()
                        for page in reader.pages:
                            writer.add_page(page)
                        
                        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as unprotected_pdf:
                            with open(unprotected_pdf.name, 'wb') as output:
                                writer.write(output)
                            temp_pdf_path = unprotected_pdf.name
                    else:
                        temp_pdf_path = temp_pdf.name
            else:
                temp_pdf_path = temp_pdf.name
            
            # Convert to markdown
            result = md.convert(temp_pdf_path)
            
            # Cleanup temporary files
            try:
                os.unlink(temp_pdf.name)
                if password and temp_pdf_path != temp_pdf.name:
                    os.unlink(temp_pdf_path)
            except:
                pass
                
            return result.text_content
            
    except Exception as e:
        raise Exception(f"PDF processing failed: {str(e)}")

def organize_markdown_with_claude(markdown_content):
    """Use Claude API to organize and extract table data from markdown."""
    try:
        message = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            temperature=0,
            system="You are a data extraction specialist. Extract raw table data and preserve it in clean, structured table formats. Maintain data integrity and original values exactly as they appear.",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"""Extract and organize ALL tables from this document. For each table:

1. Preserve the exact raw data values (no summarization or modification)
2. Maintain the original column headers
3. Keep all rows of data
4. Format as clean markdown tables

Output format:
- Label each table clearly (e.g., "Table 1: [Original Table Title if available]")
- Present tables in the order they appear
- Include ALL numeric values exactly as shown
- Preserve dates in their original format
- Keep any reference numbers, transaction IDs, or codes intact

Do not summarize, analyze, or omit any data. I need the complete raw data from every table in the document.

{markdown_content}"""
                        }
                    ]
                }
            ]
        )
        
        return message.content[0].text
        
    except Exception as e:
        raise Exception(f"Claude API processing failed: {str(e)}")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "pdf-to-markdown"})

@app.route('/process-pdf', methods=['POST'])
def process_pdf():
    """Main endpoint to process PDF and return both raw and organized markdown."""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({"error": "File must be a PDF"}), 400
        
        # Get optional password
        password = request.form.get('password')
        
        # Process PDF to markdown
        raw_markdown = process_pdf_to_markdown(file, password)
        
        # Organize markdown with Claude (if API key is available)
        organized_markdown = None
        if os.environ.get("ANTHROPIC_API_KEY"):
            try:
                organized_markdown = organize_markdown_with_claude(raw_markdown)
            except Exception as e:
                # Continue without organized markdown if Claude API fails
                organized_markdown = f"Claude API processing failed: {str(e)}"
        else:
            organized_markdown = "Anthropic API key not configured"
        
        return jsonify({
            "success": True,
            "raw_markdown": raw_markdown,
            "organized_markdown": organized_markdown,
            "filename": file.filename
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/process-pdf/raw', methods=['POST'])
def process_pdf_raw_only():
    """Endpoint to process PDF and return only raw markdown."""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({"error": "File must be a PDF"}), 400
        
        password = request.form.get('password')
        raw_markdown = process_pdf_to_markdown(file, password)
        
        return jsonify({
            "success": True,
            "raw_markdown": raw_markdown,
            "filename": file.filename
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
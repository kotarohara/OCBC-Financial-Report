import anthropic
import os
from dotenv import load_dotenv

load_dotenv() 

# Initialize the client
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")  # Set your API key as environment variable
)

# Read the input markdown file
input_file = "Wealth Report-5728-Jun-25.md"  # Change this to your input file name
output_file = "Wealth Report-5728-Jun-25_organized.md"  # Change this to your desired output name

try:
    with open(input_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    print(f"Read {len(markdown_content)} characters from {input_file}")
    
    # Send to Claude API
    print("Sending to Claude for processing...")
    message = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=4000,
        temperature=0,
        system="You are a data extraction specialist. Extract raw table data and preserve it in clean, structured table formats. Maintain data integrity and original values exactly as they appear.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""Extract and organize ALL tables from this bank report. For each table:

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
    
    # Extract the response content
    response_content = message.content[0].text
    
    # Save to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(response_content)
    
    print(f"Successfully saved organized tables to {output_file}")
    
except FileNotFoundError:
    print(f"Error: Could not find input file '{input_file}'")
except Exception as e:
    print(f"Error occurred: {str(e)}")
# nubix-ai

AI library used for document processing and LLM calls.

## Installation

```bash
pip install nubix-ai
```

## Usage

```python
from pydantic import BaseModel
from nubix_ai import NubixAI

# Initialize the client
client = NubixAI(
    docling_api_key="your-docling-api-key",
    openai_api_key="your-openai-api-key"
)

# Process a document
markdown, metadata = client.call_docling_process_file("document.pdf")

# Extract structured data with LLM
class MySchema(BaseModel):
    field1: str
    field2: int

result = client.extract_with_llm(
    markdown_text=markdown,
    prompt_input="Extract the following information:",
    PydanticInput=MySchema
)
```

## License

MIT
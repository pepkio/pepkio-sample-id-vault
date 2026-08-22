# Pepkio Sample ID Vault

Python client for the Pepkio Sample ID Vault API (`sample-id-vault`).

## Installation

```bash
pip install pepkio-sample-id-vault
```

## Quick Start

```python
from pepkio_sample_id_vault import PepkioClient

with PepkioClient() as client:
    manifest = client.get_manifest()
    print("Tool Title:", manifest.get("title"))

    # Run tool with example input
    inp = client.get_example_input("generate_reversible")
    result = client.run(inp)
    print("Status:", result.status)
    print("Result:", result.result)
```

## CLI Usage

```bash
# Fetch tool manifest
pepkio-sample-id-vault manifest

# Run example input
pepkio-sample-id-vault run --example generate_reversible

# Run custom JSON input
pepkio-sample-id-vault run --input-json '{"action": "generate", "names_text": "Sample1\nSample2", "mode": "reversible"}'
```

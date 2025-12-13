# Caistro Python SDK

Official Python SDK for the Caistro API.

## Installation

```bash
pip install caistro
```

## Quick Start

```python
from caistro import Caistro, Message

client = Caistro(api_key="your-api-key")

response = client.chat(
    messages=[
        Message(role="user", content="Write a tagline for a coffee shop")
    ]
)

print(response.choices[0].message.content)
```

## Async Usage

```python
import asyncio
from caistro.client import AsyncCaistro
from caistro import Message

async def main():
    async with AsyncCaistro(api_key="your-api-key") as client:
        response = await client.chat(
            messages=[
                Message(role="user", content="Write a tagline for a coffee shop")
            ]
        )
        print(response.choices[0].message.content)

asyncio.run(main())
```

## Documentation

Full documentation: [docs.caistro.com](https://docs.caistro.com)

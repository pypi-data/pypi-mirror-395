# Vemmio Python Client

## Introduction

The Vemmio Python Client is a library for interacting with Vemmio Smart Home devices.

## Installation

```bash
pip install vemmio
```

## Usage

```python
import asyncio

import aiohttp
from vemmio import Vemmio


async def main():
    session = aiohttp.ClientSession()
    vemmio_host = "192.168.1.25"
    vemmio_provider = Vemmio(host=vemmio_host, session=session)

    device = await vemmio_provider.update()

    print("Vemmio Device Info: %s", device)

    # Don't forget to close the session
    await session.close()


if __name__ == "__main__":
    asyncio.run(main())

```

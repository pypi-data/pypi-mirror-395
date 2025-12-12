<div align="center">
    <a href="https://wrift.ai">
      <picture>
         <img alt="WriftAI Banner" src="./banner.png">
      </picture>
   </a>
   <h1 align="center">WriftAI Python Client</h1>
   <a href="https://wrift.ai/docs/clients/python">Docs</a>
    ·
   <a href="https://github.com/wriftai/wriftai-python/issues">Issues</a>
   <br />
   <br />

[![CI](https://github.com/wriftai/wriftai-python/actions/workflows/ci.yml/badge.svg)](https://github.com/wriftai/wriftai-python/actions/workflows/ci.yml)
![PyPI - Version](https://img.shields.io/pypi/v/wriftai)
[![License](https://img.shields.io/github/license/wriftai/wriftai-python)](https://img.shields.io/github/license/wriftai/wriftai-python)

</div>

The WriftAI Python Client provides convenient access to WriftAI's services. The library includes type definitions for all request params and response fields,
and offers both synchronous and asynchronous clients powered by [httpx](https://github.com/encode/httpx).

## Documentation
https://wrift.ai/docs/clients/python

## Requirements
- Python 3.10+

## Installation
```bash
pip install wriftai
```

## Basic Usage
```python
import os

from wriftai import Client

# Instantiate the WriftAI client
wriftai = Client(
    # This is the default and can be omitted
    access_token=os.environ.get("WRIFTAI_ACCESS_TOKEN"),
)

# Create a prediction against deepseek-ai/deepseek-r1 and wait for it to complete
prediction = wriftai.predictions.create(
    model="deepseek-ai/deepseek-r1",
    params={
        "input": {
            "prompt": "Summarize quantum computing.",
        }
    },
    wait=True,
)

print(prediction.output)
# Quantum computing uses quantum bits to solve problems...
```

## Contributing
Contributions are very welcome. To learn more, see the [Contributor Guide](./CONTRIBUTING.md).

## License
Copyright (c) Sych Inc. All rights reserved.

Distributed under the terms of the [Apache 2.0 license](./LICENSE).

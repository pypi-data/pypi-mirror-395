# Practiso SDK

> [!TIP]
> Check out [Practiso](https://github.com/PractisoDevelopers/Practiso), a local intelligent study utility.

To create Practiso archive for importing, use this Python SDK to

- create questions programmatically,
- parse other formats like Excel sheets or RTF documents,
- use generative AI to categorize the questions.

## Getting started

SDK is available via PyPi. To get it with pip, run:

```shell
pip install practiso-sdk
```

## Frames

Questions are composed of several frames, either representing its content
or the answerable sections. Following is a possible question model and its
Practiso rendering.

```python
from practiso_sdk import archive

archive.Text('This is Cat Walker')
archive.Image(filename='cat_walker.jpg', width=479, height=200, alt_text="People's favour cat DJ")
archive.Options([
    archive.OptionItem(archive.Text('pretty cool'), is_key=True)
])
```

![frames](assets/frames.png)

## Tag

Your categories will be the primary factor on which Practiso decides how to
recommend new questions or combinations. In Practiso, categorization is described in
dimensions, what knowledge point a question is related to and how much so,
so that the system can comprehend them in a hyper dimension line space.

## use generative AI

### 1. for tagging

Generative AI can be utilized to make decisions on how much a category a
question falls into.

Required extra: `googleai`. Install with:

```bash
pip install practiso-sdk[googleai]
```

Example code snippet:

```python
import os

import practiso_sdk

agent = practiso_sdk.google.ai.GeminiAgent(api_key=os.environ['GEMINI_API_KEY'])
dimensions = await agent.get_dimensions(quiz)
print(dimensions)
```

### 2. for generaing content

An MCP server is available at [PractisoDevelopers/mcp](https://github.com/PractisoDevelopers/mcp).

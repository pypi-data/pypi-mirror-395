# Research

Types:

```python
from happenstance_ai.types import ResearchCreateResponse, ResearchRetrieveResponse
```

Methods:

- <code title="post /v1/research">client.research.<a href="./src/happenstance_ai/resources/research.py">create</a>(\*\*<a href="src/happenstance_ai/types/research_create_params.py">params</a>) -> <a href="./src/happenstance_ai/types/research_create_response.py">ResearchCreateResponse</a></code>
- <code title="get /v1/research/{research_id}">client.research.<a href="./src/happenstance_ai/resources/research.py">retrieve</a>(research_id) -> <a href="./src/happenstance_ai/types/research_retrieve_response.py">ResearchRetrieveResponse</a></code>

# Usage

Types:

```python
from happenstance_ai.types import UsageRetrieveResponse
```

Methods:

- <code title="get /v1/usage">client.usage.<a href="./src/happenstance_ai/resources/usage.py">retrieve</a>() -> <a href="./src/happenstance_ai/types/usage_retrieve_response.py">UsageRetrieveResponse</a></code>

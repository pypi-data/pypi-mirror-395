1. Any theoretical section?...
2. Code structure:
    - We properly introduced the serving/interface layer by our MCP implementation
    - Note how everything else is completely independent from the MCP implementation. How we can take all the logic and infra and serve it using a completely different strategy such as FastMCP or a CLI script
    - Again a note on how we inject the infra stuff, such as the memory, only when initializing the workflow (app components)

- Video showing how this works when using Cursor...
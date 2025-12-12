1. Evaluator optimizer (workflows) vs Reflection (agents)
2. Explain more depth the article reviewer + editor prompts!!!
2. To clarify: Why we don't compute any score into the evaluator optimizer loop
3. Code structure:
    - We started introducing the app layer through the LangGraph workflows
    - And the infra layer through the memory
    - Note how we inject the infra stuff, such as the memory, only when initializing the workflow (app components)
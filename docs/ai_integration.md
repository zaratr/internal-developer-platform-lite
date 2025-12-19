# AI-Driven Platform Engineering

IDP-Lite explores how Generative AI can augment platform engineering by moving beyond static templates to dynamic, context-aware service generation.

## Current Capabilities
The CLI includes an `--ai-enhance` flag that performs a heuristic analysis of the generated service structure and provides initial optimization suggestions.

```bash
idp create service my-ai-service --ai-enhance
```

This generates an `AI_OPTIMIZATION.md` report alongside the service code, offering insights on:
- Performance bottlenecks
- Security gaps
- Scalability patterns

## Future Vision
In a production version of this platform, we would integrate with LLMs (Gemini, GPT-4) to:

1. **Dynamic Scaffolding**: Instead of choosing a static template, a user could describe their service: *"I need a Python service that consumes Kafka messages and writes to DynamoDB"* and the platform would generate a custom scaffold.
2. **Auto-Remediation**: CI pipelines could automatically suggest code fixes for linting errors or security vulnerabilities.
3. **Contextual Documentation**: Generate READMEs specific to the business logic added by developers, not just the boilerplate.

## Architecture for AI Integration
To add these features without bloating the CLI:
- **Agentic Workflow**: The CLI would send a prompt to a central Platform AI Agent.
- **RAG (Retrieval-Augmented Generation)**: The agent would have access to internal documentation (`docs/standards.md`) to ensure generated code complies with organization standards.

# Internal Developer Platform Lite

Internal Developer Platform Lite (IDP-Lite) is a deliberately small platform engineering portfolio project. It demonstrates how a platform team can standardize service delivery, enforce guardrails, and reduce operational burden without building a full control plane. The project answers a single interview question:

> **Can this engineer build systems that enable other engineers and reduce operational burden?**

## What this platform provides
- **Service template generator**: `idp create service <name>` scaffolds a FastAPI or Spring Boot backend that already has health checks, logging, metrics hooks, and config conventions.
- **Opinionated pipelines**: Shared GitHub Actions workflows run linting, tests, security scans, image builds, and promotion gates for dev → staging → prod.
- **Environment management**: Environments are represented by configuration overlays and Docker Compose profiles. Promotion requires passing checks and produces versioned artifacts.
- **Config & secrets abstraction**: Services consume configuration via a central provider interface. Local development uses `.env` and config files, but the interface is designed to swap in Vault or cloud secret managers.
- **Operational guardrails**: Readiness/liveness endpoints, structured JSON logging with correlation IDs, and rollback hooks in pipelines.
- **Control Plane Dashboard**: React-based UI for service management with real-time status and creation workflows.
- **AI-Enhanced Generation**: Optional AI optimization reports for generated services.
- **Production Observability**: Prometheus metrics, Grafana dashboards, and structured logging built-in.

## Repo structure
```
internal-developer-platform-lite/
  README.md
  platform/
    cli/
      idp.py
    templates/
      fastapi_service/
        app/
        tests/
        Dockerfile
        pyproject.toml
  pipelines/
    github-actions/
      service-ci.yml
      deploy.yml
  examples/
    sample-service/
  docs/
    architecture.md
    standards.md
```

## Quick start
1. Install dependencies for the CLI: `pip install -r platform/cli/requirements.txt`
2. Generate a service: `python -m platform.cli.idp create service user-profile`
3. Run the generated service locally: `cd examples/user-profile && docker compose --profile dev up`
4. Run platform tests: `pytest`

## Standards enforced
- Services must expose `/health/live` and `/health/ready`.
- Logging is JSON-formatted with correlation IDs propagated via `X-Request-ID`.
- Configuration is loaded through `platform.app.config_provider.ConfigProvider` only; direct `os.environ` access is banned for secrets.
- CI pipelines are source-of-truth; repos reuse the shared workflow via `workflow_call`.

## Scaling considerations
- **Extensibility**: Add templates under `platform/templates/` and register them in the CLI.
- **Secrets**: Swap `EnvConfigProvider` with a Vault-backed provider without changing services.
- **Rollbacks**: Deployment workflow retains previous image tags and can redeploy the last known good artifact.
- **Multi-language support**: The template generator is language-agnostic. Support includes Python (FastAPI) and Java (Spring Boot) out of the box.

## Trade-offs
- No control plane UI; everything is CLI + GitHub Actions to keep scope small.
- Security scanning is represented by `pip-audit` in CI; real orgs should integrate SAST/DAST.
- Deployment is simulated via Docker Compose; replace with your orchestrator of choice.
- Secrets are stored locally in `.env` for demo purposes; production must integrate a real secret manager.
- **Multi-Cloud Ready**: Deployment patterns for AWS, Azure, Google Cloud, and IBM Cloud are documented in [docs/multi_cloud.md](docs/multi_cloud.md).

## Example flow
```bash
# create a new service with platform defaults
python -m platform.cli.idp create service user-profile

# commit code and push; GitHub Actions runs CI
# on success, a dev image is built and tagged

# promotion
# staging promotion requires passing tests; prod promotion gates on staging success
```

## Who is this for?
Platform engineers who want a concise, demonstrable repo that shows platform thinking: standards, paved roads, and operational guardrails.

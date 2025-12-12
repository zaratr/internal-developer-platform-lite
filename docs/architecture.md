# Architecture Overview

IDP-Lite is intentionally simple: it provides a CLI that generates standardized services, shared CI/CD pipelines, and environment definitions that can be swapped for a real orchestrator. The goal is to showcase platform thinking rather than build a full product.

## Components
- **CLI (`platform/cli/idp.py`)**: Generates new services from templates and wires them to the shared workflows.
- **Templates (`platform/templates/`)**: Opinionated service blueprints. The FastAPI template includes health endpoints, logging, metrics hooks, config provider, Dockerfile, tests, and Docker Compose profiles.
- **Pipelines (`pipelines/github-actions`)**: Reusable workflows for CI (lint, test, security, build) and deployment/promotion (dev → staging → prod with rollback hooks).
- **Environment overlays**: `docker-compose.yml` and `config/*.yaml` in generated services represent dev/staging/prod. Promotions use tagged images and config overlays.
- **Config provider**: `platform.app.config_provider.ConfigProvider` enforces a single interface for configuration and secrets.

## Environment model
- **dev**: Runs locally via Docker Compose with live-reload. Pulls config from `.env` and `config/dev.yaml`.
- **staging**: Uses baked images and `config/staging.yaml`; promotion depends on CI success.
- **prod**: Promotion gated on staging success. Uses `config/prod.yaml`. Rollback is supported by redeploying the previous image tag.

## Deployment path
1. Developer scaffolds a service with `idp create service <name>`.
2. Commits/push triggers `service-ci` workflow via `workflow_call`.
3. On success, `deploy.yml` builds and tags Docker image as `ghcr.io/<org>/<service>:<gitsha>` and `:latest-dev`.
4. Promotion jobs gate staging and prod deployments; a `rollback` job can re-deploy the last successful tag.

## Operational guardrails
- **Health**: `/health/live` and `/health/ready` endpoints differentiate platform readiness from container liveness.
- **Logging**: JSON logging with correlation IDs. Each request sets `X-Request-ID` if missing.
- **Metrics hooks**: Placeholder hook in middleware to show where to emit metrics (exporter selection is left open).
- **Config**: Services must use the config provider abstraction, enabling secret manager swaps without code changes.

## Extending the platform
- Add new templates under `platform/templates/<stack>` and register them in `TEMPLATES` within `idp.py`.
- Swap out `EnvConfigProvider` with Vault or cloud-specific provider implementations.
- Replace Docker Compose deployment stages with Helm charts or Terraform modules while keeping the interface intact.

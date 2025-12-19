# Observability Strategy

IDP-Lite services are designed with observability as a first-class concern. Every generated service includes built-in instrumentation for metrics, logging, and tracing.

## Metrics

### Prometheus Integration
All FastAPI services automatically expose Prometheus metrics at `/metrics`.

**Key Metrics**:
- HTTP request duration (histogram)
- Request count by endpoint and status code
- Active requests (gauge)
- Application info (build version, environment)

**Example**:
```bash
curl http://localhost:8000/metrics
```

### Grafana Dashboards
We provide a reference Grafana dashboard configuration in `docs/grafana-dashboard.json` that visualizes:
- Request rate (RPS)
- P50, P95, P99 latency
- Error rate by endpoint
- Service health status

## Logging

### Structured JSON Logging
All services use `structlog` for structured logging with:
- Correlation IDs (propagated via `X-Request-ID` header)
- Timestamp in ISO format
- Log level
- Service name and version
- Contextual metadata

**Example Log Entry**:
```json
{
  "event": "request_completed",
  "timestamp": "2024-01-15T10:30:45.123Z",
  "level": "info",
  "service": "user-profile",
  "correlation_id": "abc-123",
  "method": "GET",
  "path": "/users/42",
  "status_code": 200,
  "duration_ms": 45
}
```

## Deployment Pattern

### Local Development
Services run standalone with metrics exposed on the same port.

### Production
- **Metrics Collection**: Prometheus scrapes `/metrics` every 15s
- **Log Aggregation**: Logs shipped to centralized system (e.g., Loki, CloudWatch)
- **Alerting**: Prometheus Alertmanager for SLO violations

## SLO Example
```yaml
# 99.9% of requests complete in < 500ms
- alert: HighLatency
  expr: histogram_quantile(0.999, http_request_duration_seconds_bucket) > 0.5
  for: 5m
```

This observability foundation ensures that platform users can debug issues quickly and maintain high service reliability.

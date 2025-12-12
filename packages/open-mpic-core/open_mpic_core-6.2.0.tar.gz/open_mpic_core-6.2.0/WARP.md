# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Tooling and common commands

This project is a Python 3.11+ library built and managed with [Hatch](https://hatch.pypa.io/). The main package lives under `src/open_mpic_core` with tests under `tests`.

### Environments

- Hatch will automatically create virtual environments on first use of `hatch run`, using the configuration in `pyproject.toml` (`[tool.hatch.envs.*]`).
- The default env uses a local `venv` directory; there are dedicated envs for `test` and `types`.

### Installing test dependencies

From the project root (this directory):

- Install Hatch (if not already available), mirroring CI:
  - `pipx install hatch`

### Running tests

Pytest is configured via `[tool.pytest.ini_options]` in `pyproject.toml` with:
- `pythonpath = ["src", "tests"]`
- `testpaths = ["tests/unit"]`
- Custom markers (`unit`, `integration`) and async settings.

Common commands (all from repo root):

- Run the main unit test suite (same as CI):
  - `hatch run test:unit`
- Run unit tests with HTML report:
  - `hatch run test:unit-html`
- Run integration tests (if/when `tests/integration` exists):
  - `hatch run test:integration`
- Run tests with coverage (HTML + terminal):
  - `hatch run test:coverage`

**Coverage in CI**

GitHub Actions (`.github/workflows/main.yml`) runs:
- `hatch run test:unit`
- Then parses coverage output and fails the build if total coverage is below 98%.

When modifying core logic, expect to maintain high coverage; use `hatch run test:coverage` locally to mirror CI behavior.

### Running a single test or subset of tests

The `test:unit` script is just a thin wrapper around `pytest -rp --disable-warnings`, so you can pass standard pytest selectors:

- Single test file:
  - `hatch run test:unit tests/unit/open_mpic_core/test_mpic_coordinator.py`
- Single test function within a file:
  - `hatch run test:unit tests/unit/open_mpic_core/test_mpic_coordinator.py::test_name_here`
- Tests matching a marker:
  - `hatch run test:unit -m unit`
  - `hatch run test:unit -m integration`

### Type checking

Mypy is configured via the `types` Hatch env in `pyproject.toml`:

- Run type checks:
  - `hatch run types:check`

This runs `mypy --install-types --non-interactive src/open_mpic_core tests`.

### Formatting

Black is configured via `[tool.black]` in `pyproject.toml` (line length 120). The library dependency list includes `black`.

Typical usage inside the Hatch environment:

- Format source and tests:
  - `hatch run python -m black src tests`

### Building the package

The project uses Hatchling as the build backend (`[build-system]` and `[tool.hatch]`):

- Build wheel and sdist into `dist/`:
  - `hatch build`

Tests under `tests/unit/test_util` are force-included in the wheel (`[tool.hatch.build.targets.wheel.force-include]`) under the `open_mpic_core_test.test_util` package to support downstream integration tests.

## High-level architecture

### Overview

This repository provides the core (transport-agnostic) implementation of Open MPIC (Multi-Perspective Issuance Corroboration) in Python. It is designed to be embedded into environment-specific wrappers (e.g., AWS Lambda handlers, FastAPI services, containers). The public API is surfaced via `open_mpic_core/__init__.py`, which re-exports the main domain types and orchestrators.

At a high level, there are three major functional areas:

1. **Common domain and utilities** (`open_mpic_core.common_domain`, `open_mpic_core.common_util`)
2. **MPIC Coordinator** (`open_mpic_core.mpic_coordinator`)
3. **Checker implementations** for CAA and DCV (`open_mpic_core.mpic_caa_checker`, `open_mpic_core.mpic_dcv_checker`)

### 1. Common domain models (`common_domain`)

The `common_domain` package defines Pydantic models and enums that codify the Open MPIC API specification; this layer is intentionally transport- and framework-agnostic.

Key pieces:

- **Check parameters** (`common_domain/check_parameters.py`)
  - `CaaCheckParameters`: configuration for CAA checks (certificate type, allowed CAA domains, whether lookup failures are tolerated).
  - A hierarchy of `Dcv*ValidationParameters` models, all discriminated by the `validation_method` field and collectively aliased as `DcvCheckParameters`.
    - Different subclasses model WEBSITE_CHANGE, DNS_CHANGE, ACME HTTP-01, ACME DNS-01, ACME TLS-ALPN-01, IP address checks, reverse lookups, and contact-email/phone flows.
    - Validators enforce constraints on allowed `DnsRecordType` values per method.

- **Requests** (`common_domain/check_request.py`)
  - `BaseCheckRequest` holds `domain_or_ip_target` and optional `trace_identifier`.
  - `CaaCheckRequest` and `DcvCheckRequest` extend this with their respective parameter types.
  - The `CheckRequest` union is used where generic handling is needed.

- **Responses & details**
  - `common_domain/check_response.py` defines `BaseCheckResponse` with `check_completed`, `check_passed`, `errors`, and `timestamp_ns`, and its two concrete variants:
    - `CaaCheckResponse` with `CaaCheckResponseDetails`.
    - `DcvCheckResponse` with `DcvCheckResponseDetails`.
  - `common_domain/check_response_details.py` models the detailed result payloads:
    - `CaaCheckResponseDetails`: where CAA was found and which records were seen.
    - HTTP DCV details (`DcvHttpCheckResponseDetails`): redirect chain, final URL/status, a base64-encoded snippet of the response body.
    - DNS DCV details (`DcvDnsCheckResponseDetails`): records seen, response code, AD flag, CNAME chain, and where it was found.
    - TLS-ALPN DCV details (`DcvTlsAlpnCheckResponseDetails`): fields specific to ACME TLS-ALPN.
    - `DcvCheckResponseDetailsBuilder.build_response_details(...)` is the central factory that maps a `DcvValidationMethod` to the correct details type.

- **Validation errors**
  - `MpicValidationError` (`common_domain/validation_error.py`) wraps error type keys and formatted messages. Error message templates live in `common_domain/messages/ErrorMessages.py` and are reused across coordinator/checkers.

- **Enums**
  - Various enums under `common_domain/enum/` (e.g., `CertificateType`, `CheckType`, `DcvValidationMethod`, `DnsRecordType`, `UrlScheme`) define the shared vocabulary across all components.

These domain models are the primary way environment-specific wrappers should exchange data with the core library.

### 2. Shared utilities (`common_util`)

- **DomainEncoder** (`common_util/domain_encoder.py`)
  - Normalizes `domain_or_ip_target` values for DNS queries:
    - Leaves valid IP addresses unchanged.
    - Detects and validates already-punycode labels.
    - Otherwise, encodes domains using IDNA (via `idna` and `dns.name`), raising `ValueError` on invalid input.
  - Both CAA and DCV checkers call this to safely handle IDNs and wildcard domains.

- **Trace-level logging** (`common_util/trace_level_logger.py`)
  - Defines a custom `TRACE` log level (numeric level 5) and augments `logging.Logger` with:
    - `.trace(...)` for fine-grained logging.
    - `.trace_timing(...)` async context manager to measure and log operation duration.
  - `get_logger(__name__)` is the canonical entry point. Most core classes keep a child logger named after the class for scoped tracing.
  - The coordinator and checkers rely heavily on `trace`/`trace_timing` for observability around DNS and HTTP calls.

### 3. MPIC Coordinator (`mpic_coordinator`)

The coordinator orchestrates multi-perspective issuance corroboration by delegating to remote “perspective” services and aggregating their results.

Key artifacts:

- **Configuration**
  - `MpicCoordinatorConfiguration` bundles:
    - `target_perspectives`: configured list of `RemotePerspective` objects (each representing a remote checker service in a particular RIR/region).
    - `default_perspective_count`: how many perspectives to include per request by default.
    - `global_max_attempts`: upper bound on retry attempts across cohorts.
    - `hash_secret`: secret used to deterministically shuffle perspective cohorts per target.

- **Coordinator class** (`mpic_coordinator/mpic_coordinator.py`)
  - `MpicCoordinator` is initialized with:
    - `call_remote_perspective_function`: an async-compatible function supplied by the environment that performs the actual RPC to a remote perspective. The core library treats it as a black box that takes `(RemotePerspective, CheckType, CheckRequest)` and returns a `CheckResponse`.
    - An `MpicCoordinatorConfiguration` instance.
    - Optional `log_level` used to set the internal logger level.
  - The main entrypoint is `coordinate_mpic(mpic_request: MpicRequest) -> MpicResponse`:
    - Validates the request using `MpicRequestValidator.is_request_valid(...)`, raising `MpicRequestValidationException` with structured notes if invalid.
    - Determines how many perspectives and attempts to use based on `mpic_request.orchestration_parameters`, while enforcing `global_max_attempts` and optional cohort selection.
    - Uses `CohortCreator` to shuffle perspectives (with a per-domain hash derived from `hash_secret` and `domain_or_ip_target`) and build cohorts that maximize RIR diversity.
    - For each attempt, calls `collect_checker_calls_to_issue(...)` to build `RemoteCheckCallConfiguration` instances and then `call_checkers_and_collect_responses(...)` to concurrently invoke `call_remote_perspective_function` for all selected perspectives.
    - Aggregates results into a single `MpicResponse` using `MpicResponseBuilder.build_response(...)` once a quorum is reached or attempts are exhausted.
    - Enforces additional diversity requirements when cohorts have more than two perspectives (e.g., requiring at least two distinct RIRs among successful perspectives).

- **Error handling and fallbacks**
  - `call_remote_perspective(...)` wraps the transport call and rethrows failures as `RemoteCheckException`, including the `RemoteCheckCallConfiguration` for context.
  - `build_error_perspective_response_from_exception(...)` converts transport-level failures into synthetic `PerspectiveResponse` objects with `MpicValidationError` entries and appropriate `CaaCheckResponse`/`DcvCheckResponse` defaults, ensuring the coordinator can always produce a well-structured response.
  - `call_checkers_and_collect_responses(...)` uses `asyncio.gather(..., return_exceptions=True)` and converts any `RemoteCheckException` instances into error responses while logging warnings.

Environment-specific wrappers are expected to:
- Configure `RemotePerspective` objects for their deployment topology.
- Provide the glue between their RPC mechanism (HTTP, queues, etc.) and `call_remote_perspective_function`.

### 4. CAA checker (`mpic_caa_checker`)

`MpicCaaChecker` encapsulates the logic for evaluating whether issuance is permitted based on DNS CAA records.

Highlights:

- Uses `dns.asyncresolver` for asynchronous lookups and walks up the domain hierarchy until it finds an RRset or hits the root.
- Respects `CaaCheckParameters`:
  - `caa_domains`: list of allowed issuer domains.
  - `allow_lookup_failure`: controls whether certain DNS failures (e.g., timeouts or no nameservers) are treated as soft-allow versus hard-fail.
  - `certificate_type`: distinguishes between TLS server certs and S/MIME (different CAA tags apply).
- Handles wildcard targets (`*.example.com`) specially when interpreting `issuewild` tags.
- `is_valid_for_issuance(...)` implements the RFC-compliant decision logic around `issue`, `issuewild`, `issuemail`, and unknown critical tags.
- `extract_domain_and_parameters_from_caa_value(...)` parses CAA parameter syntax (`tag=value`) and validates both tag and value formats, raising `ValueError` on malformed records.

This module is purely about protocol semantics and depends only on the common domain/util code and `dnspython`.

### 5. DCV checker (`mpic_dcv_checker`)

`MpicDcvChecker` encapsulates all Domain Control Validation flows supported by the spec, using DNS and HTTP clients.

Key responsibilities:

- **HTTP-based validations** (`perform_http_based_validation`)
  - WEBSITE_CHANGE
    - Builds a URL under `/.well-known/pki-validation/` with a provided `http_token_path`, optionally using a configurable `UrlScheme`.
    - Optionally applies a user-provided `match_regex` in addition to substring matching of the challenge value.
  - ACME_HTTP_01
    - Targets `/.well-known/acme-challenge/{token}`.
  - Uses an `aiohttp` client created via `get_async_http_client` with:
    - SSL verification control.
    - Disabled cookies (`DummyCookieJar`).
    - Per-request tracing via `logger.trace_timing`.
  - `evaluate_http_lookup_response(...)` inspects status codes, redirect history, and a truncated response body (base64-encoded in the details) to determine success.

- **DNS-based validations** (`perform_general_dns_validation` / `perform_dns_resolution` / `evaluate_dns_lookup_response`)
  - Supports multiple `DcvValidationMethod` variants including ACME_DNS_01, DNS_CHANGE, IP_ADDRESS, REVERSE_ADDRESS_LOOKUP, and contact-email/phone CAA/TXT methods.
  - Handles tree-walking for CAA-based contact lookups.
  - Populates rich `DcvDnsCheckResponseDetails` including AD flag, CNAME chain, and where the record was found.
  - Compares expected vs observed content with either exact-match or substring semantics, depending on method.
  - For IP address validation, compares canonicalized `ipaddress.ip_address` objects rather than strings.

- **TLS-ALPN validation**
  - Delegated to `DcvTlsAlpnValidator` (`mpic_dcv_checker/dcv_tls_alpn_validator.py`), used when `validation_method` is ACME_TLS_ALPN_01.

- **Error handling**
  - DNS exceptions are translated into structured `MpicValidationError` entries; some DNS errors mark the check as completed (e.g., NXDOMAIN) vs. hard infrastructure errors.
  - HTTP timeouts and transport errors are logged and recorded in the response, never leaking raw exceptions.

### 6. Tests

Tests are under `tests/`:

- `tests/unit/open_mpic_core/` contains focused unit tests for the coordinator, CAA/DCV checkers, and supporting domain logic (e.g., cohort creation, request validation, response building, domain encoder).
- `tests/unit/test_util/` provides helper utilities (`valid_mpic_request_creator`, `mock_dns_object_creator`, etc.), and is bundled into the wheel to support integration testing in downstream projects.

Pytest configuration in `pyproject.toml` sets the default test path to `tests/unit`, so any new tests under that tree will run automatically via `hatch run test:unit`.

### 7. API and specification versioning

The `[tool.api]` section in `pyproject.toml` documents the Open MPIC API specification version the library targets (e.g., `spec_version = "3.6.0"` and a `spec_repository` URL). When making changes that affect external behavior or data structures, keep this tight coupling in mind; environment-specific wrappers may rely on matching this version to the published spec.

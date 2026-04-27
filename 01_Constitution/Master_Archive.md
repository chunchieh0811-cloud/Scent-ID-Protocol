# Scent-ID Master Archive

This document is the canonical archive for the Scent-ID core standards.
All protocol updates must be appended through versioned change logs.

## 1) Constitution V2 (Foundational Layer)

- Principle 01: Scent is identifiable information, not only a sensory event.
- Principle 02: Every scent must have a unique, verifiable, and traceable digital identity.
- Principle 03: Scent-ID provides universal infrastructure for encoding, storage, exchange, and licensing.
- Principle 04: Every SID asset must preserve uniqueness, integrity, and consistency.
- Principle 05: The protocol remains open; value creation and services can be commercialized above the protocol.

## 2) V26 Specification Snapshot

- Version: V26
- Positioning: Transitional protocol baseline before V27 consolidation.
- Scope:
  - SID generation rule normalization.
  - Metadata schema unification.
  - Traceability field standardization.
- Mandatory metadata fields:
  - `sid`
  - `issuer`
  - `created_at`
  - `hash`
  - `protocol_version`
  - `integrity_signature`

## 3) V27 Specification Snapshot

- Version: V27
- Positioning: Current integrated baseline for production alignment.
- Core upgrades from V26:
  - Stronger interoperability requirements across application stacks.
  - Extended verification flow with deterministic hash checks.
  - Compatibility profile for API-driven identity exchange.
- Backward compatibility:
  - V27 readers MUST parse V26 payloads.
  - V27 writers SHOULD emit V27 by default unless compatibility override is explicitly enabled.

## 4) iOS Implementation Standard

- Target: iOS client and SDK implementations.
- Requirements:
  - UTF-8 payload support.
  - Stable SID rendering and copy-safe formatting.
  - Local verification capability without mandatory network access for basic checksum validation.
  - Secure storage for local secrets via platform keychain.
- Recommended:
  - Background sync retry with idempotent API requests.
  - Version pinning for protocol parsers.

## 5) Inkjet Standard (Physical Output Alignment)

- Target: inkjet output workflows for SID labels and certificates.
- Requirements:
  - Fixed SID print zone and machine-readable region.
  - Minimum print contrast threshold for scanner reliability.
  - Hash string and human-readable SID must match one-to-one.
  - Print template version must be embedded in output metadata.
- Quality gate:
  - Reject output if checksum text differs from encoded value.

## 6) API Protocol

- Transport: HTTPS only.
- Data format: JSON.
- Minimum endpoints:
  - `POST /sid/create`
  - `POST /sid/verify`
  - `GET /sid/{sid}`
  - `POST /sid/license`
- Security:
  - API key or token-based authentication.
  - Replay protection using timestamp + nonce.
  - Request integrity validation through content hash.
- Response contract:
  - `status`
  - `protocol_version`
  - `trace_id`
  - `data`
  - `error` (when applicable)

## 7) Change Control

- Owner: Scent-ID Command Authority.
- Every change MUST include:
  - semantic version bump
  - rationale
  - backward compatibility note
  - effective date
- Archive path:
  - Source archive: `01_Constitution/Master_Archive.md`
  - Locked export: `03_Application/ScentID_Master_Archive_LOCKED.pdf`

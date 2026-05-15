# Claude Sonnet Prompt For JIO-Compatible MCP Apps

Use the prompt below when asking Claude Sonnet to create a new MCP app or a wrapper that must comply with the JIO platform host contract.

This prompt is self-contained. It assumes access only to this delivery bundle.

Use it to generate a standalone app repository, not a code snippet that must be pasted into an internal JIO service.

Use this prompt when the main task is to create or normalize the standalone app repository itself. If the app already exists and the main task is platform-managed rollout, registration, and deployment, hand the repo off to the JIO platform team rather than using this standalone-authoring prompt.

Boundary rule for future component-specific docs generated from this package:

- keep the output inside the standalone app repo boundary
- do not generate or embed internal-only `platform_lifecycle` material inside the standalone app repo
- if a requested document is about internal deployment, registration, launch policy, or teardown, that document belongs to the internal `platform_lifecycle` package rather than this external package

Replace the bracketed placeholders before use.

## Quick Start

If you want the fastest path for a genuinely new app, use these defaults before copying the prompt:

- implementation mode: `native MCP app`
- visual UI required: `yes` for interactive visual apps, otherwise `no`
- durable session state required: `yes` if users must reopen work later, otherwise `no`
- source tool or external system: `not applicable`

Minimal example values:

- app name: `Horizon Picking`
- app id: `horizon.picking`
- version: `1`
- capability summary: `Interactive seismic horizon picking app with hosted UI and reusable outputs.`
- primary user outcomes: `create, edit, and review picks on seismic lines`
- expected inputs: `survey id, line id, and horizon name`
- expected outputs: `json picks, image previews, and selected horizon runtime values`
- visual UI required: `yes`
- durable session state required: `yes`
- source tool or external system: `not applicable`

Use that set when you want Claude Sonnet to scaffold a first native app draft before any wrapper or legacy-integration decision is needed.

Starter invocation to paste ahead of the full prompt:

```text
Use the native MCP app path for a new app.

- app name: Horizon Picking
- app id: horizon.picking
- version: 1
- capability summary: Interactive seismic horizon picking app with hosted UI and reusable outputs.
- primary user outcomes: create, edit, and review picks on seismic lines
- expected inputs: survey id, line id, and horizon name
- expected outputs: json picks, image previews, and selected horizon runtime values
- visual UI required: yes
- durable session state required: yes
- source tool or external system, if this is a wrapper: not applicable

Proceed as a native MCP app unless a real wrapper boundary is required.
```

## Prompt Boundaries

This document has two parts:

1. a short usage guide for the human preparing the prompt
2. a copy-paste prompt bounded by explicit start and end markers

When you copy the prompt into Claude Sonnet, copy only the text between:

- `BEGIN CLAUDE SONNET JIO MCP APP PROMPT`
- `END CLAUDE SONNET JIO MCP APP PROMPT`

## How To Use This Prompt

The bracketed items in this document are template variables. They are not special JIO syntax.

They are simply placeholders that the person using the prompt should replace with real values before giving the prompt to Claude Sonnet.

### Step 1: choose the implementation mode

Replace `[native MCP app / wrapper-based MCP integration]` with one of these exact options:

- `native MCP app`
- `wrapper-based MCP integration`

Use `native MCP app` when the new app will directly implement the JIO-compatible host result shape itself.

Use `wrapper-based MCP integration` when there is already some existing tool, API, UI, SDK, or vendor system and the new work is mainly an adapter that makes that existing thing behave like a JIO-compatible app.

### Step 2: fill the placeholders from the right source

In practice, the values come from three places.

Requester or product/domain owner usually provides:

- app name
- capability summary
- primary user outcomes
- expected inputs
- expected outputs
- whether a visual UI is required

Implementer or technical owner usually provides:

- app id
- version
- whether durable session state is required
- whether the implementation should be native or wrapper-based

Wrapper author or integration owner usually provides:

- the upstream provider being adapted
- the textual provenance label used for `source_tool`-style context

### Step 3: understand the placeholders

#### `[APP_NAME]`

Human-facing app name.

This should usually be provided by the requester, product owner, or whoever is asking for the app.

Examples:

- `Map Viewer`
- `Production Prediction`
- `Horizon Picking`

#### `[APP_ID]`

Stable machine identifier for the app family.

This is usually chosen by the implementer or platform owner, not by Claude Sonnet.

Examples:

- `map.viewer`
- `production.prediction`
- `horizon.picking`

#### `[APP_VERSION]`

Initial version of the app contract.

Usually this is `1` unless there is a deliberate versioning reason to start elsewhere.

#### `[CAPABILITY_SUMMARY]`

One short sentence describing what the app does.

Example:

- `Interactive seismic horizon picking app with hosted UI and reusable outputs.`

#### `[PRIMARY_USER_OUTCOMES]`

What users should be able to accomplish with the app.

Examples:

- `inspect permit locations on a map`
- `run forecasts and compare forecast scenarios`
- `create, edit, and review horizon picks`

#### `[INPUTS]`

What the app takes in.

Examples:

- `coordinates, filters, and selected feature ids`
- `well id, forecast horizon, and model parameters`
- `survey id, line id, and selected horizon name`

#### `[OUTPUTS]`

What the app publishes out.

Examples:

- `json selection payloads and selectable runtime values`
- `rows, chart_spec, and selected forecast series`
- `json picks, image previews, and selected horizon runtime values`

#### `[YES_OR_NO]`

Literal `yes` or `no` answers.

This is used for:

- `visual UI required`
- `durable session state required`

#### `[SOURCE_TOOL_OR_SYSTEM]`

This field is wrapper-only.

It is a textual provenance label for the upstream thing being wrapped.

It does not imply that the upstream system must literally expose a field with this name. It is simply a clear textual identifier for the existing tool, API, UI, SDK, or vendor system that the wrapper is adapting.

Examples:

- `Acme Production Forecast API v2`
- `vendor.analytics.get_table`
- `Mapbox GL JS viewer`
- `Internal Horizon Interpretation Service`

If the app is native rather than wrapped, replace this with `not applicable` or remove the line when preparing the filled prompt.

### Step 4: use this simple rule

If the value is about business intent, the requester should supply it.

If the value is about technical identity or lifecycle behavior, the implementer should supply it.

If the value is about an upstream provider being adapted, the wrapper author should supply it.

### Step 5: example filled values

For a native app:

- app name: `Horizon Picking`
- app id: `horizon.picking`
- version: `1`
- capability summary: `Interactive seismic horizon picking app`
- primary user outcomes: `create, edit, and review picks on seismic lines`
- expected inputs: `survey id, line id, horizon name`
- expected outputs: `json picks, image previews, selected horizon runtime value`
- visual UI required: `yes`
- durable session state required: `yes`
- source tool or external system, if this is a wrapper: `not applicable`

For a wrapper:

- app name: `Production Prediction`
- app id: `production.prediction`
- version: `1`
- capability summary: `Wrap an existing forecast service as a JIO-compatible hosted app`
- primary user outcomes: `run forecasts, inspect forecast curves, reuse outputs downstream`
- expected inputs: `entity id, forecast horizon, model parameters`
- expected outputs: `rows, chart_spec, selected series runtime value`
- visual UI required: `yes`
- durable session state required: `yes`
- source tool or external system, if this is a wrapper: `Acme Production Forecast API v2`

### Step 6: prompt boundary rule

The prompt starts immediately after the `BEGIN CLAUDE SONNET JIO MCP APP PROMPT` marker.

The prompt ends immediately before the `END CLAUDE SONNET JIO MCP APP PROMPT` marker.

Anything outside those markers is preparation guidance for the human using the prompt.

## BEGIN CLAUDE SONNET JIO MCP APP PROMPT

```text

You are creating a new MCP app for the JIO platform.

Your job is to produce an implementation that behaves like a first-class JIO platform app at the host boundary. Do not assume access to unpublished JIO repository files or internal implementation details.

Unless the request explicitly says otherwise, produce a standalone repository that owns its own app package, runtime entrypoints, config surface, tests, and packaging.

Use these bundle documents as the complete contract reference for this task:

- `C:\Claude_Projects\third_party_reference/reference/jio_mcp_app_contract_extensions_reference.md`
- `C:\Claude_Projects\third_party_reference/reference/jio_mcp_app_contract_examples.md`
- `C:\Claude_Projects\third_party_reference/reference/standalone_app_repository_guide.md`
- `C:\Claude_Projects\third_party_reference/schemas/app_instance_envelope.public.schema.json`
- `C:\Claude_Projects\third_party_reference/schemas/app_tool_payload.public.schema.json`
- `C:\Claude_Projects\third_party_reference/scripts/validate_public_bundle_examples.py`

## Goal

Create a [native MCP app / wrapper-based MCP integration] for:

- app name: [TD_Plot]
- app id: [well.TD.plot]
- version: [1.0]
- capability summary: [Give a plot of Time-Depth functions for well data]
- primary user outcomes: [A plot of Time vs Depth values]
- expected inputs: [UUID for a well TD function file]
- expected outputs: [Chart of Time vs Depth values]
- visual UI required: [YES]
- durable session state required: [NO]
- source tool or external system, if this is a wrapper: [Vega Lite Chart]

If this is a native app rather than a wrapper, replace the last line with `not applicable` or remove it before use.

## Non-Negotiable Rules

1. Use `snake_case` for the wire format.
2. Emit the canonical JIO app envelope with `result_kind = "app_instance"`.
3. Keep provider-specific runtime content inside `state`.
4. If the tool returns `structuredContent`, use the same canonical top-level shape there.
5. Declare `state_kind` and `state_schema_version` explicitly.
6. Publish `emitted_artifacts` when downstream consumers need typed outputs.
7. Publish `selectable_runtime_values` when downstream composition or agent use depends on meaningful selections.
8. Publish `meta.ui_resource` when the app has a real visual UI.
9. Preserve provenance through `source_tool`, `artifact_refs`, `input_bindings`, or provider-owned provenance in `state`.
10. Do not require the host to parse provider-native top-level fields outside the canonical envelope.
11. Do not invent JIO-internal metadata that is not described in this bundle.
12. Deliver a standalone app repository, not an internal router snippet.
13. Put data access behind the app's own backend boundary and explicit config rather than assuming direct database access.
14. Do not invent bespoke platform-only HTTP endpoints to stand in for governed platform data. If the real supported boundary is SQL catalogue or another reviewed query service, make that adapter explicit in the app backend.

## Ownership Rules

For a native MCP app:

- you own app behavior, `state`, emitted artifacts, runtime selections, and UI surface
- the platform owns persistence, replay, shell layout, and composition behavior

For a wrapped or non-native provider:

- normalize the provider result before the host sees it
- keep provider-specific details inside `state`
- make the delivered host-facing result indistinguishable from a native app result

## Required Outputs

Produce the files needed for a complete implementation in the target codebase.

Always include:

- the app implementation files
- a runnable standalone app package or equivalent source root
- an MCP server entrypoint
- an HTTP app entrypoint when the app has a visual UI
- versioned state schema files for each supported lifecycle kind
- starter state files for editable lifecycle kinds such as `template` and `session`, if applicable
- a README explaining the app's purpose, lifecycle model, artifacts, runtime values, and UI resource behavior
- fixtures or tests that prove the emitted envelope and payload are consistent with this bundle's contract
- env-driven configuration for upstream dependencies
- container and CI files for the standalone repo

For a visual native app, the default file shape should usually look like this unless the request gives a better app-owned reason to differ:

- `src/<package>/config.py` for env-driven settings
- `src/<package>/survey_data.py` or an equivalent app-owned data-access module
- `src/<package>/envelope.py` for the canonical app result builder
- `src/<package>/http_app.py` for the standalone HTTP surface
- `src/<package>/mcp_server.py` for the MCP tool entrypoint
- `src/<package>/ui.py` for UI resource construction and config injection
- `ui/main.html` for the hosted UI template
- a sample-data directory for example inputs or local fallback data
- `tests/` for envelope, HTTP runtime, and MCP transport checks
- `Dockerfile` and `.github/workflows/ci.yml` for delivery

When using FastMCP for stdio delivery, the server entrypoint should call `mcp.run(transport="stdio", show_banner=False)` so startup banner text does not pollute the stdio channel.

If this is a wrapper or non-native integration, also include:

- the adapter logic that transforms provider-native results into the canonical JIO envelope
- any app-local configuration needed to keep that adapter explicit and maintainable

## Implementation Expectations

Design the app so that:

- the host can reopen or replay it through explicit lifecycle kinds rather than opaque UI state
- downstream apps can consume outputs through explicit artifacts or runtime values
- the host does not need bespoke parsing logic for this app family
- the app can behave like a normal hosted JIO app whether it is native or wrapped
- any platform-governed data dependency is modeled as an explicit backend adapter rather than a fake native HTTP upstream

## Validation Requirements

Before finishing, verify that:

- every app result validates against `schemas/app_instance_envelope.public.schema.json`
- `structuredContent` validates against `schemas/app_tool_payload.public.schema.json` when applicable
- the validation can be reproduced with the bundled script or equivalent public JSON Schema tooling
- each supported state lifecycle has a clear versioned schema
- editable lifecycles have starter-state files when appropriate
- visual apps publish `meta.ui_resource`
- MCP stdio servers are validated through at least one real transport-level test, not only helper-layer unit calls
- downstream outputs are published explicitly as `emitted_artifacts` or `selectable_runtime_values`
- wrapped integrations do not leak provider-native top-level response fields into the host boundary

## Output Format

Return:

1. a short implementation summary
2. the file plan
3. the actual file contents
4. the validation checklist showing how the generated app satisfies the bundle contract

If any required input is missing, ask only the smallest number of questions needed to finish the app correctly.

```

## END CLAUDE SONNET JIO MCP APP PROMPT

Recommended usage note:

If the app is genuinely new and not a legacy integration, prefer the native MCP app path first and use the wrapper path only if a non-native provider boundary forces it.
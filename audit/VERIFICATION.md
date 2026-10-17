# Installer verification

Candidate: **0.8.0-heatcoder.7**. Publisher: **Heatcoder**.

## Installed Intel Mac build

Built, packaged, extracted and installed locally. PKG/ZIP payloads match the reviewed staging files; the installed bundle matches that payload and passes ad-hoc signature verification. One active DesignCraft editor remains, with the prior version preserved separately.

Restored-tool GUI interactions, save/reopen, IDML vertical direction, direct Malayalam typing and the user's 36-page INDD opening/panning checks passed. The original document was not saved or modified. Published patch reconstruction matches the compiled Rust source and Cargo inputs.

## Independent platform verification

Apple Silicon, Windows x64/ARM and Linux x64/ARM passed the native installer workflow, including tool regressions, extracted payload/notices, replacement installation/backup, INDD and Malayalam smoke tests.

The separate Intel Mac CI job is still running; local Intel Mac verification above is complete. Run and exact code commit: https://github.com/heatcoder/designcraft-indd-patch/actions/runs/39020248603 — efdfc61229c63941a368e593efb6ff164a5fe99e.

## Remaining release checks

The complete upstream quality gate is not passed. Formatting, asset attribution and dependency layering passed locally, but cargo xtask ci stopped because Clippy is not installed in the local Rust toolchain. The full workspace/WASM gate was not completed. Focused tool, engine and UI tests are recorded separately.

Public downloads remain paused for the existing notice/provenance and release review. Verification is engineering evidence, not legal clearance or Apple notarization.

See TOOL-VERIFICATION.md and ../TOOL-GUIDE.md.

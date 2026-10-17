# Heatcoder release-candidate verification

Candidate: **0.8.0-irajeev.4**. Publisher: **Heatcoder**. The “Malayalam (irajeev)” menu name and irajeev.com website remain unchanged.

## Local Intel Mac

- Fresh GUI/CLI compilation completed using Rust 1.95.0 and the pinned source/patch.
- PKG and ZIP extracted; every app file matched the staging tree by SHA-256. Exact collected notices and Typeit hash exclusions passed.
- Extracted CLI opened the hash-verified public CC0 INDD fixture and exported IDML. Malayalam replacement, undo/redo and InScript conversion passed.
- Extracted GUI passed direct keyboard-event tests for Manglish selection replacement, Backspace/retyping, undo/redo, InScript and Off. Queries were made after composition because the control API resets composition when running inspection commands.
- All six translation-catalog regression tests passed after removing unused promotional rows.
- The tested `.4` app was installed after verifying the existing app was closed; every installed file matches the extracted package. The previous app is retained for rollback.
- A page render was inspected. Window screenshot capture was unavailable because no frame was presented.
- GUI native imports reference Apple system frameworks/libraries; no Adobe or Typeit dynamic library is listed.
- Formatting, asset-attribution and dependency-layer checks passed. Full Clippy/workspace/WASM gates remain incomplete.

## Cross-platform build

Fresh six-platform run: https://github.com/heatcoder/designcraft-indd-patch/actions/runs/39010614389

Source commit: `607a0d0356371eb83ced1c9eb1f992369f8e8a2d`.

All six jobs completed successfully. Every platform passed the focused font, input/undo, direct-page input, translation, INDD routing, image-preview and quit-recovery tests, followed by actual installer extraction/installation and tests of the extracted CLI.

| Platform | Installer payload | INDD and Malayalam CLI |
|---|---|---|
| linux-aarch64 | PASS | PASS |
| linux-x86_64 | PASS | PASS |
| macos-aarch64 | PASS | PASS |
| macos-x86_64 | PASS | PASS |
| windows-aarch64 | PASS | PASS |
| windows-x86_64 | PASS | PASS |

Each downloaded Actions artifact matched GitHub's SHA-256 digest. Every contained installer matched its verification report. Per-platform reports and filtered test evidence are retained alongside this report. See `CI-SHA256SUMS.txt` for installer hashes. Earlier `.2`/`.3` candidates are superseded.

All six payloads contain identical collected third-party notices (SHA-256 `5c0e7ce8f61e1c27de54f419042d0c03aa53a98b534af058e4d6f6db31881b90`). Windows packages include the actual Inno Setup 6.7.1 notices; their runtime licence text was compared with the official 6.7.1 source. Native import checks ran on Mac/Linux; Windows PE import inspection is optional, so this is not a complete binary dependency audit.

The package verifier checks Heatcoder publisher text in the compiled GUI, rejects the four removed promotional phrases, compares payloads with staging, rejects the known restricted artwork and 49 Typeit file hashes, and rejects loose private documents, font files and VB6 components. These are concrete exclusion checks, not exhaustive decompilation or similarity proof.

## Release limits

Public downloads remain paused. The dispatch distributor notice includes the declared MIT terms and author attribution, but the original authoritative upstream notice is still missing. Reader provenance documents preserve the upstream attestations and their limits; no stolen Adobe code was identified. This review is not legal clearance. Installers remain unsigned/not notarized. Actual Windows/Linux desktop interaction has not been observed; their CI checks exercise direct-input code and the extracted CLI.

## Branding verification

Candidate `.4` removes the native Mac Help label and unused promotional translations, in addition to the rendered mark and About promotion. The compiled Mac GUI contains the Heatcoder publisher string and none of the four checked promotional phrases. Inspection of remaining ArtCraft strings found author credit and upstream-reference URLs. Required copyrights and author credits remain. The shared patch contains no restricted vector outline or promotional phrases. Every CI package verifier checks the compiled GUI too.

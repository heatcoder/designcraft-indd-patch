# Heatcoder toolbar restoration

Installed on this Mac: **0.8.0-heatcoder.7**, at Applications → DesignCraft.

Implemented Free Transform, Measure, Note, Color Theme and Vertical Type on a Path. Added an Apply Gradient fill button. Right-click tool groups to see their additional tools.

## Verification

- 60 tool tests; all catalogue tools have concrete implementations.
- 2 document interaction tests: transform gesture undo/redo and saved editable notes.
- 3 colour-theme tests: dominant image colours, read-only sampling and atomic swatch-group changes.
- 4 path-text tests including vertical orientation, editing and brackets.
- Dialog save/error handling, 7 toolbar layout/colour checks, direct Malayalam typing and pending-pan paper regression.
- Installed-app GUI: note creation, transform drag and undo/redo, palette save, path typing, measurement, save/reopen and vertical IDML export.
- Actual Apply Gradient toolbar click and Undo.
- User's 36-page INDD opened and panned at 189% without saving changes.
- Mac PKG/ZIP payloads match the reviewed staging files; installed bundle matches them and passes ad-hoc signature verification.
- One active DesignCraft editor; previous .6 copy retained in the separate rollback folder.

Other-platform run: https://github.com/heatcoder/designcraft-indd-patch/actions/runs/39020248603

Five independent CI targets passed: Apple Silicon, Windows x64/ARM and Linux x64/ARM. The additional Intel Mac CI run remains in progress; local Intel Mac verification is complete. These focused checks do not constitute the complete upstream quality gate. Public distribution remains paused for the existing notice/provenance review. The Mac package is not Apple-notarized.

See TOOL-GUIDE.md for use and limits. No new external dependencies or Typeit implementation were added.

The full upstream gate stopped at missing Clippy. Formatting, all 50 asset attributions and layering for 20 crates passed. Full workspace/WASM validation is not claimed.

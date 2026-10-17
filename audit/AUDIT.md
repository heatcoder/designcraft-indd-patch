# MalayalamPatch by iRajeev — distribution audit

**Publisher: iRajeev.** MalayalamPatch is a free enhancement for DesignCraft, adding INDD opening and Malayalam typing. It builds on open-source projects whose credits and licences accompany the software. In this report, “third-party components” means upstream libraries, fonts and other incorporated material.

Audit date: 17 October 2026. **Release decision: HOLD for completion of the release checks below.** This is a source/dependency and packaging audit, not a legal clearance certificate or a complete security audit. Generated code is not assumed cleared for redistribution.

## What was examined

DesignCraft 0.8.0 at `11a51d5b665aec8d6e675bd107a8a01514f10d00`, the local patch, INDD backports `a7c3e330ec626bfe8fba670d450d540b3d862831` and `82ffb692fccfbea83e0482693ed6aae597594387`, and `indd-utils` at `7f3060e5bce78d21ea70e0d5eacb96edce15dfbe`. Cargo fetches that converter from the **storytold/indd-utils** repository; its package metadata identifies **aiongg/indd-utils** as its project repository. These are not silently treated as interchangeable origins.

The installed earlier build, installer scripts, workflow configuration, upstream asset manifest, locally resolved Cargo graph, actual licence files, converter provenance documents, and new Malayalam code were reviewed. The new direct-typing version is a changed build and must be tested separately. Previous six-platform build success does not validate this version. Private test documents, document fonts and screenshots are excluded from distribution.

The inventory [dependencies.csv](dependencies.csv) lists **549 third-party package/version entries**, with declared licences, origins, scopes, manifest hashes and collected notice paths. The 20 local DesignCraft workspace packages are covered by the upstream MIT OR Apache-2.0 terms. A conservative traversal of normal dependencies from the GUI and CLI identifies 500 third-party entries; it unions target conditions, so it is not a claim that all 500 are linked into each executable. Remaining entries belong to build/dev/workspace tooling or other resolved features. Target-specific binary/SBOM reconciliation remains required. [dependencies.json](dependencies.json) contains the same inventory in machine-readable form.

## Exactly how INDD opening works

1. The app's File → Open routing recognizes `.indd` and `.indt`, or the INDD binary signature. `crates/engine/src/cmd/interchange.rs::open_idml` reads the file bytes (or receives caller-provided bytes).
2. It calls the statically linked Rust function `indd::convert(&bytes, &file)`. This is the `indd` crate from the pinned `indd-utils` source; its Cargo manifest has no external dependencies.
3. In `indd-utils/src/lib.rs::convert_with`, `Container::parse` reads the INDD container, `container.database()` exposes objects, and `model::Reader::document` reconstructs supported document properties. Optional XMP metadata is read from the document. `idml::write` writes an IDML ZIP package to an in-memory buffer. The converter also returns warnings and embedded graphic previews.
4. DesignCraft calls its own `import_report_with_previews` IDML importer, creating its native document model. It looks for linked assets and document-font folders, and uses previews where supported when original links are missing. The result is an unsaved DesignCraft document.
5. Edits are saved as `.designcraft`, or exported as IDML/PDF through DesignCraft. This patch does **not** implement native INDD writing or overwrite the original INDD with another format.

**InDesign is not required by this execution path.** It does not automate InDesign, call an Adobe conversion service, load an InDesign plug-in or require a Creative Cloud subscription to run the converter. The reviewed library conversion path has no subprocess launch or Adobe software call. It operates on the user's document bytes. Other ordinary app features can open external links or use platform services; this is not a claim that the whole app never accesses the network.

**It does not modify Adobe software.** The installer builds/installs a modified DesignCraft application. It does not patch an InDesign binary, Adobe plug-in, licence file, activation service or host-file entry. macOS ad-hoc signing signs this application's bundle, not Adobe software, and is not notarization. No Adobe activation bypass, subscription unlock, DRM-removal or protection-circumvention routine was found in the reviewed INDD conversion path or installer scripts. This is a code finding, not proof about every historical upstream contribution or every legal interpretation of format interoperability.

The project is a compiled DesignCraft fork/patch distribution, **not** an Adobe plug-in and not a generic binary plug-in that can be injected into arbitrary DesignCraft versions. Its new Window panel requires the matching patched build.

Conversion is partial and inferred from observed files. Unsupported properties may be omitted or approximated; linked images/fonts may be absent; line breaks, typography and page layout need checking. A successfully opened file is not proof of lossless InDesign compatibility.

## Adobe-origin material and uncertain provenance

| Component | Evidence and finding | Distribution action |
|---|---|---|
| INDD reader | `CLEANROOM.md`, `CONTRIBUTING.md`, format evidence in `docs/format/`. Authors state no InDesign binaries/SDK were used, no source from other INDD readers was copied, and samples were made by others. | Preserve provenance documents and MIT/Apache notices. These statements are author attestations, not independently verified chain-of-title evidence. |
| Adobe XMP Toolkit SDK reference | `indd-utils/third_party/README.md` identifies revision `7093513bd3ca`, `InDesign_Handler.cpp` as a container-layout reference and says no source code was copied. BSD 3-Clause notice is present. | Retain Adobe's notice and attribution conservatively. This is an open-source Adobe reference, not a proprietary InDesign runtime. Do not claim “no Adobe source was ever consulted.” |
| Source Sans 3 / Source Serif 4 | Adobe-authored open-source fonts in `assets/fonts`, SIL OFL 1.1. | Include their individual copyright/OFL texts. Adobe authorship alone does not make these proprietary. |
| Adobe CMap resources | `hayro-cmap 0.1.0/assets/cmaps.brotli` and `assets/LICENSE.txt`, copyright 1990–2023 Adobe, BSD-style three-clause terms. Used for PDF text mapping, not INDD activation. | Retain Adobe copyright, conditions, disclaimer and non-endorsement requirement. The blob-generation reference is LaurenzV/cmap-resources; verify generation provenance if requiring complete reproducibility. |
| IDML specification and validation schemas | Converter policy permits the public IDML specification. Schemas described as generated by InDesign and published elsewhere are used for local validation, not committed to the converter. | Do not bundle schemas/SDK documentation without checking their own terms. No proprietary Adobe SDK binaries or validation-schema files were identified in the reviewed installer payload construction. |
| AI-assisted INDD analysis | `CLEANROOM.md` explicitly says AI was used, training-data exposure cannot be disproved, some facts depend on non-public samples, and there was no separate analysis/implementation team. | **Provenance uncertainty remains.** Do not market this as legally certified clean-room work. Retain evidence and obtain independent IP review before broad public distribution. |
| New Malayalam implementation | Independently written mapping/transliteration and UI code; Microsoft published Malayalam InScript keyboard layout used as a functional reference. No Typeit! implementation was copied into the patch. | Keep reference attribution and review generated contributions normally; generation is not ownership/licensing evidence. It is a deterministic mapping, not Typeit!'s dictionary or predictive engine. |
| Typeit! in Downloads | Local VB6 sources and OCX/runtime material exist. No redistribution permission was established. | Excluded. Do not bundle its source, EXE, OCX, dictionary, fonts or copied routines without explicit applicable licences. |
| User fonts and documents | Legacy FML faces, Minion Pro and other document fonts are not licensed by this patch's MIT terms. | Excluded from installers. Users must have appropriate font rights. PDF embedding and document sharing may have separate font restrictions. |

The upstream claim of clean-room development is qualified by its own disclosures. A public repository and an MIT declaration do not establish that every contributed line has a verified origin. No exhaustive similarity, patent or jurisdiction-specific reverse-engineering review has been completed.

## Non-Cargo materials and toolchain components

The Cargo inventory is not the whole licence inventory. These also matter:

| Material | Licence / source | Treatment |
|---|---|---|
| DesignCraft core and original UI/icon code | MIT OR Apache-2.0; upstream LICENSE files, NOTICE, ASSETS | Preserve attribution, licence and relevant notices; identify the modified build. |
| Source Sans 3, Source Serif 4, Inter, JetBrains Mono | OFL-1.1, upstream individual font notices | Bundled. Include each copyright and licence; respect Reserved Font Names if modifying fonts. |
| Noto Sans Malayalam | OFL-1.1; Google Fonts revision `47d54ca1ebb14fd864695f1d39dc734f39017c33`, SHA-256 `312e0e7c3cc15fa09eb42a8f749eeb246b593ed420e3c81aafe8d910c3a6fb56` | Bundled unchanged through CRAFT_FONTS_DIR; include OFL and provenance. Japanese craft-fonts are not part of this selected font input. |
| egui default fonts | Hack: MIT plus Bitstream Vera terms / DejaVu public-domain contribution; Noto Emoji: OFL; Ubuntu Light: Ubuntu Font Licence 1.0; emoji-icon-font: MIT | `FontDefinitions::default()` retains these fallbacks. Cargo's top-level licence expression is insufficient by itself; collect `fonts/*.txt`, including Hack's separate terms and UFL. |
| PDF standard-14 substitute fonts | PDFium/Foxit BSD-style licence in `hayro-interpret/assets/LICENSE_FOXIT` | Bundled via embed-fonts feature; retain notice, not proprietary Adobe font files. |
| PDF CMYK profile / sRGB-v2-magic.icc | Compact ICC Profiles, CC0-1.0 | Retain provenance/CC0 text. Not an Adobe proprietary ICC profile. |
| English hyphenation | Moby Hyphenator II, Grady Ward public-domain grant; generated patterns CC0 | Preserve upstream provenance. Public-domain scope outside the stated jurisdiction may need review. |
| Spanish and Portuguese hyphenation | hypher embedded pattern data: Spanish MIT; Portuguese BSD 3-Clause | Include the full pattern notices in DesignCraft NOTICE, not just hypher's crate licence. |
| ArtCraft name/marks | **Not open source**, `docs/brand/LICENSE-brand.txt` | Modified distributions must remove marks and avoid endorsement. The earlier app painted the mark in code. Current source replaces it with neutral “DC” text and describes the build as independent. Verify final binaries and source packages contain no restricted mark assets. Plain attribution to the ArtCraft team is retained. |
| DesignCraft cat app icon | Separately declared MIT OR Apache-2.0 in assets/app-icon/LICENSE.txt | Distinct from the restricted ArtCraft mark; preserve its notice. |
| iRajeev branding | Publisher branding for this modified DesignCraft build. | Publisher identity is distinct from upstream component authorship. Trademark ownership and rights to any externally sourced logo assets were outside this audit’s verification scope. |
| Windows Inno Setup installer runtime | Inno Setup licence; preserve existing copyright/web addresses; bundled subcomponents have additional terms | Do not remove runtime acknowledgements. Pin and inventory the actual compiler version and inspect final EXE notices; current hosted-runner installation is not version-pinned. |
| Rust standard libraries/compiler support | MIT/Apache terms and Rust's own third-party notices | Version 1.95.0 pinned; compiler is a build tool, but linked standard/compiler-support code must be considered. Collect the toolchain's notices and compare final link outputs. |
| Host operating-system frameworks and shared libraries | macOS frameworks, Windows system DLLs, Linux distro libraries under their respective terms | Referenced system dependencies are not automatically bundled. Verify `otool -L`, PE imports and `ldd` on final artifacts. If shipping extra DLLs/shared objects, add their exact versions/licences and any source obligations. |
| Python/Git/GitHub Actions/build packages | Build tools, not copied as product payload by current scripts | Record for reproducibility; assess separately if shipping a build environment. Website uses project HTML/CSS/JS, without a third-party web framework. |

## Notices and source-code obligations

- **MIT/BSD/ISC and similar permissive components:** retain the applicable copyright, permission conditions and disclaimers. Binary distribution still has notice obligations. Do not substitute a generic MIT text for the package's copyright statement.
- **Apache-2.0 components:** include the licence, preserve relevant NOTICE/attribution material, and mark modified files as required. Apache does not generally require publishing all application source, and grants no general trademark permission. [Apache licence](https://www.apache.org/licenses/LICENSE-2.0).
- **OFL / Ubuntu / Bitstream font terms:** include the actual font notices; retain the font licences and observe naming/modified-font conditions. Fonts are bundled as part of the application, not sold separately. Font licensing does not automatically relicense user documents. [OFL text](https://openfontlicense.org/open-font-license-official-text/), [Ubuntu font licence](https://canonical.com/legal/font-licence).
- **`colored 2.2.0` (MPL-2.0):** appears through `dify`, used by screenshot/test tooling, outside the GUI/CLI normal-dependency closure. It is not evidence that the shipping app must be MPL. If its executable code or a tool containing it is distributed, provide the MPL-covered source (including changes) and tell recipients where to obtain it, under MPL; unrelated application files need not all become MPL. [Mozilla MPL guidance](https://www.mozilla.org/en-US/MPL/2.0/FAQ/).
- **`r-efi 5.3.0 / 6.0.0`:** `MIT OR Apache-2.0 OR LGPL-2.1-or-later`; elect and comply with a permissive alternative rather than assuming LGPL is mandatory. Target-conditioned entries are not proof of EFI code in desktop builds.
- **`self_cell 1.3.0`:** `Apache-2.0 OR GPL-2.0-only`; elect Apache-2.0. Its GPL alternative does not itself make the application GPL.
- **AND expressions require every applicable part:** e.g. BSD-3-Clause AND MIT, Apache-2.0 AND MIT, or Unicode/font terms alongside code licences. Slash-style older declarations are preserved verbatim in the inventory and must be checked against licence files rather than mechanically normalized.
- No compulsory GPL/AGPL/LGPL-only application dependency was identified in this resolved graph. That is not a blanket “no copyleft” statement: MPL test tooling, font terms, native runtime linkage and embedded materials require the scope checks above.
- Publishing the patch, pinned upstream revisions and build scripts is useful transparency and reconstruction support. It is not a replacement for licence notices, and it does not cure missing permission for uncertain-origin code or proprietary assets.

## Findings and release checks

1. **Earlier installers were incomplete for attribution.** Their `Notices` directory copied only a small subset of core/converter/Noto notices. It omitted many Cargo and embedded-material notices, including Adobe CMaps, default UI fonts and PDF substitute fonts. The collected notice set accompanies this audit; it must be included and verified in all final payloads.
2. **Earlier builds retained the restricted ArtCraft mark.** Current source removes the rendered mark. Public patch construction must not accidentally reproduce removed mark artwork in diff context. Reconstructed source and packaged binaries need checking.
3. **Origin uncertainty remains for the INDD reader and generated contributions.** Preserve the pinned source and provenance evidence; get independent review of the specific uncertainties before treating public distribution as cleared. Absence of detected proprietary Adobe binaries is not proof of legal clearance.
4. **Build provenance is incomplete.** Audit each final macOS/Windows/Linux architecture artifact, embedded assets, native imports and installer engine notices; archive hashes, source revisions, compiler version and licence choices. Older CI outputs are obsolete for direct typing.
5. **Testing is not the full upstream quality gate.** Earlier focused import/font/input/undo tests passed. `cargo xtask ci` stopped because the local Clippy component was unavailable; full workspace tests and WASM were not completed. Direct-page input passed real keyboard-event checks on the installed Intel Mac build (selection replacement, Backspace, undo/redo, Manglish, InScript and Off). Fresh installer verification is recorded separately. Builds are not developer-signed/notarized.
6. **No automatic publication on audit completion.** Keep public downloads disabled while the concrete blockers and provenance review remain open. Publish only artifacts matched to the reviewed source and notice set; do not reuse the earlier installers.

This audit separates observed implementation facts, licence declarations, and unresolved provenance. It makes no assertion that AI generation, a repository licence label, or successful compilation automatically clears redistribution.

## Notice collection exceptions

The previously missed `r-efi` notices were found in each published crate’s `AUTHORS` file, which includes actual copyright statements and full MIT terms; these are now collected. For `dispatch 0.2.0`, the manifest declares MIT and author Steven Sheldon. The installer now includes that manifest, author attribution and standard MIT terms in a clearly labelled distributor-assembled notice. No upstream full copyright notice was recovered; upstream issue #18 remains unanswered. This remaining evidence gap is not represented as resolved. All other inventory entries have at least one collected licence/notice file; embedded subcomponents still require package-level review.

## Target-filtered dependency check

`cargo metadata --locked --offline --filter-platform` was run for all six requested targets, followed by traversal of normal dependencies from the GUI and CLI. See [target-dependencies.json](target-dependencies.json). Both macOS architectures have 311 third-party entries, both Windows architectures 299, and both Linux architectures 367. These remain source-graph counts, not binary symbol evidence. `colored` and both `r-efi` versions are absent from all six normal-dependency closures. Thus the r-efi missing-notice records do not currently block those application payloads; they remain relevant to any broader source/toolchain redistribution. `dispatch 0.2.0` remains in the macOS closure; its declared terms and attribution are packaged, but authoritative upstream notice confirmation remains outstanding.


## Release-hardening update — 17 October 2026

- Release candidate `.2` adds the dispatch distributor notice, the actual r-efi AUTHORS notices, Rust standard-library copyright material and explicit reader provenance documentation.
- All platform packaging uses the same collected notice archive. Windows also collects the actual Inno Setup compiler/runtime licence files and compiler version.
- Native installer verification extracts macOS PKG/ZIP and Linux DEB/tar payloads, or installs Windows EXE into a disposable runner folder. It compares every staged app file by SHA-256, rejects unexpected files, checks restricted artwork hashes and rejects loose documents, private fonts and Typeit/VB6 payloads. It does not claim exhaustive decompilation or ownership clearance.
- The extracted CLI is tested with a hash-pinned CC0 INDD file, IDML export, Malayalam replacement, undo/redo and InScript conversion. Direct canvas keyboard-event regression tests remain separate.
- See [PROVENANCE.md](PROVENANCE.md). No stolen Adobe code was identified. Historical origin uncertainties remain qualified questions rather than findings of copying.
- Public release remains on hold; new per-platform verification reports must pass before describing the final artifacts as checked.

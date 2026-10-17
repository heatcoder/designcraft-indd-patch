# INDD reader provenance review — 17 October 2026

Publisher: Heatcoder. This is an evidence review, not legal clearance. **No stolen Adobe code was identified.** Outstanding questions concern independently verifying upstream attestations, not a finding of theft.

## Source chain

- Application: https://github.com/storytold/designcraft at `11a51d5b665aec8d6e675bd107a8a01514f10d00`, MIT OR Apache-2.0.
- Import integration backports: `a7c3e330ec626bfe8fba670d450d540b3d862831` and `82ffb692fccfbea83e0482693ed6aae597594387` from that repository.
- Reader: Cargo fetches https://github.com/storytold/indd-utils at `7f3060e5bce78d21ea70e0d5eacb96edce15dfbe`. Its manifest names https://github.com/aiongg/indd-utils as the project repository. The pinned source, not an unverified later branch, is the reviewed input.
- Reader licence files: MIT and Apache-2.0; MIT notice names aiongg and the indd-utils contributors. The reader crate declares no external dependencies.
- Local changes: independent Malayalam mapping, display fixes and UI integration, distributed as a source patch and reproducible customization script. Typeit! implementation was not used.

## Evidence and limits

The pinned reader's CLEANROOM.md describes learning the format from existing INDD/IDML pairs, recording observations in docs/format, and testing conversion against reference output. It states that InDesign binaries, SDK and incompatible readers were not used. These are upstream attestations; this review cannot independently prove every historical contribution's origin.

CLEANROOM.md discloses AI-assisted analysis, no separate analysis/implementation teams, and some facts supported only by non-public samples. These limit independent reproducibility. They do not establish infringement. The non-public samples are not distributed by this patch.

The reader explicitly consulted Adobe's BSD-3-Clause XMP Toolkit `InDesign_Handler.cpp` at revision `7093513bd3ca` for container structure. `third_party/README.md` says no source was copied. The Adobe BSD notice is included regardless. This is a permitted open-source reference, not a proprietary Adobe runtime.

IDML specifications and externally published validation schemas are references. Schema redistribution permission was not established by this review; no schemas or Adobe SDK files are included in installer payloads.

The open fixture manifest identifies CC0, MIT and BSD documents, URLs and hashes. The new extracted-app smoke test downloads the CC0 Heather Ryan flyer at a pinned revision and validates its hash. Test documents stay outside installer staging and are not published as package assets.

## Explicit exclusions

No Typeit! sources, VB6 controls/OCX, proprietary document fonts (including Minion Pro), private INDD files, user screenshots, Adobe applications or proprietary Adobe SDK binaries are selected by the installer payload. Runtime payloads are restricted to the freshly built executables, licensed app icon, notices and required platform metadata. An extraction verifier compares the actual installer payload with staging and rejects unexpected files. Source reconstruction removes restricted ArtCraft artwork; textual author credits remain. The About window’s upstream promotional section is also removed.

## Remaining decisions

- Independent IP review would be needed to resolve historical chain-of-title questions beyond the evidence available here. This audit does not provide that clearance.
- dispatch 0.2.0 explicitly declares MIT and names Steven Sheldon. The distributor includes those declarations and standard MIT terms. Upstream issue https://github.com/SSheldon/rust-dispatch/issues/18 remains unanswered: no original full copyright notice was recovered. Do not present the assembled notice as an upstream-authored licence file.
- Signing/notarization and platform UI testing are separate from source provenance.

## Typeit exclusion recheck

The local Typeit! folder contains 49 files. None is an exact-file match to the reviewed distribution source. The installer verifier also rejects their hashes and VB6/control payload extensions. See TYPEIT-EXCLUSION.json. This supplements the review of the independently implemented Rust Malayalam input; it is not an exhaustive similarity or legal ownership certificate.

# MalayalamPatch by iRajeev

A free enhancement for DesignCraft, adding INDD opening and Malayalam typing. Published by **iRajeev**, built on open-source projects; credits and licences are included.

**Downloads are temporarily paused while release checks are completed.** See [release notes](site/indd/release-notes.html) and the [technical audit](audit/AUDIT.md) for details.

This is a patched application build, not an Adobe plugin. It installs as **DesignCraft** alongside the official app. Open `.indd` or `.indt` with **File → Open**, drag and drop, or the command line. Conversion happens locally and in memory. Save edits as `.designcraft` or export `.idml`; INDD writing is not supported.

## Status

Experimental. Install only artifacts attached to a successful build/release. The native workflow checks INDD import, image previews, FML mappings, bundled Malayalam shaping, typing/Undo and quit recovery before packaging. These targeted automated checks are not exhaustive application testing or a guarantee of identical layouts. Interactive verification was performed on an Intel Mac; no Windows or Linux desktop UI verification is claimed. The download page is paused for the distribution audit, even if a release asset exists.

## Malayalam FML display compatibility

The patch resolves unsupported nonbreaking separators (U+2011) and curly quotation marks through the existing punctuation slots of legacy FML fonts. This removes missing-glyph boxes and the extra widths those boxes introduce. The original story text, UTF-8 offsets, line-breaking characters and existing encoded Malayalam conjuncts (including “ണ്ട”) are preserved. Fonts with their own glyphs and Unicode Malayalam fonts keep their original mappings.

The matching licensed FML fonts must already be installed or provided in the document’s `Document Fonts` folder. This is not a legacy-to-Unicode conversion, a font replacement, or a guarantee of identical text flow.

## MalayalamPatch (irajeev)

Open **Window → Malayalam (irajeev)** and choose **Manglish** or **InScript**. Select the Type tool (T), click in a text frame and type directly on the page using an English keyboard. Selected text is replaced. Space commits a Manglish word; Backspace revises the active word. Moving the cursor, changing modes or using Undo ends that composition. Choose Off or close the panel to return to normal typing. Paste is not transliterated.

Manglish uses deterministic, case-sensitive spelling: `namaskaaram` → നമസ്കാരം, `malayaaLam` → മലയാളം, `uNTu` → ഉണ്ടു. Use `T D N L R` for retroflex letters; `aa ee oo` for long vowels. It is not predictive transliteration. InScript uses the standard Malayalam keyboard positions; `vcmdkejx` produces നമസ്കാരം. Noto Sans Malayalam is bundled for new Unicode text. Existing legacy FML text is not converted. Typeit! is not required and its source is not included.

The macOS build also exits after preserving recovery data and settings to avoid a Touch Bar window-teardown crash.

## Installation

Download the matching file from [Releases](https://github.com/heatcoder/designcraft-indd-patch/releases).

- **macOS:** open the `.pkg` for Intel or Apple Silicon. Launch **Applications → MalayalamPatch → DesignCraft**. A `.zip` application is also provided.
- **Windows:** open the `.exe` for Intel/AMD x64 or ARM64. Launch **DesignCraft** from Start.
- **Linux (Debian/Ubuntu):** open the `.deb` using your software installer. A portable `.tar.gz` is provided for other distributions, where required system libraries must already be installed.

These independent builds are unsigned/not notarized unless the release explicitly says otherwise. Operating systems may block or warn about them. The installers do not disable security protections. Users distributing broadly should sign and notarize their builds with their own publisher certificates.

Keep your original document. Compare page breaks, text, styles and images before relying on the import for production. Missing linked graphics may show embedded low-resolution previews: relink the originals before printing. Use the original fonts where licensed and available. Place `Links` and `Document Fonts` beside the INDD document when possible.

To remove the patched edition, remove its application on macOS, use Installed apps on Windows, or uninstall `irajeev-designcraft-indd` on Debian/Ubuntu. The original DesignCraft installation remains separate.

## Build locally

Requires Git, Python 3, Rust **1.95.0**, and native platform development tools. Linux needs X11/Wayland, Vulkan, font, audio and device development libraries; see the workflow. Windows needs Visual Studio C++ build tools and Inno Setup 6. macOS needs Xcode Command Line Tools.

```sh
python3 scripts/prepare.py
export CRAFT_FONTS_DIR="$PWD/fonts"
export CRAFT_FONTS_REQUIRED=1
cd build/designcraft
cargo build --release --locked -p designcraft -p designcraft-cli
cargo test --release --locked -p designcraft-fonts legacy_fml
cargo test --release --locked -p designcraft-engine malayalam
cargo test --release --locked -p designcraft-engine indd
cargo test --release --locked -p designcraft-idml missing_linked_graphics_show_their_preview_and_keep_their_link
cd ../..
python3 scripts/package.py --source build/designcraft --bin-dir build/designcraft/target/release
```

On Windows use `python` instead of `python3`, and set `CRAFT_FONTS_DIR` to the absolute `fonts` directory and `CRAFT_FONTS_REQUIRED=1` using PowerShell environment variables. Run the build natively on the target OS/processor. `upstream.json` pins the exact base and converter revisions; `prepare.py` verifies the patch applies before changing source.

## Automated installers

Run **Actions → Build iRajeev installers → Run workflow**. The workflow builds separate macOS Intel/Apple Silicon, Windows x64/ARM64 and Linux x64/ARM64 installers. Artifacts are uploaded per platform. A `v*` tag builds all platforms and publishes a prerelease only if every build and its import regression tests succeed. No account secrets or signing certificates are bundled.

## Website

`site/indd/` is a static page intended for `/indd/` on an existing website. Upload only this directory's contents into the site's `indd` directory. Do not upload the whole source checkout or development archives into public web storage.

The page detects desktop OS and, where the browser exposes it, processor architecture. It looks up the exact release `v0.8.0-irajeev.1` and starts one matching download after a cancellable countdown. It asks for processor confirmation when detection is uncertain. Browsers can require a manual click. Unpublished/failed builds, mobile devices and unknown architectures never trigger a mismatched download.

## Credits and licensing

The importer was developed upstream by aiongg; embedded-preview support by Govinda Roy. This project packages/backports their work rather than claiming authorship of the INDD parser. See [NOTICE.md](NOTICE.md), the MIT and Apache licences, and the exact commits in `upstream.json`.

Not affiliated with Adobe or an official ArtCraft release. User documents and private test outputs must never be committed.

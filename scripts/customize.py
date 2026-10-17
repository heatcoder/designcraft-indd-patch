"""Remove restricted ArtCraft artwork from the independent modified build.

Uses source markers rather than redistributing the removed vector outline in a patch.
"""
from pathlib import Path
import shutil

def customize(source: Path):
    p=source/'crates/ui-egui/src/about.rs'
    s=p.read_text()
    start=s.index('/// The ArtCraft mark outline')
    end=s.index('/// The other ArtCraft apps',start)
    s=s[:start]+s[end:]
    start=s.index('/// Paint the ArtCraft mark')
    end=s.index('/// A speech-bubble glyph',start)
    s=s[:start]+'''/// Neutral text identifier for this independent modified build; no ArtCraft mark.
pub fn paint_mark(ui: &egui::Ui, rect: Rect, color: Color32) {
    ui.painter().text(rect.center(), egui::Align2::CENTER_CENTER, "DC", egui::FontId::monospace(rect.height() * 0.45), color);
}

'''+s[end:]
    s=s.replace('/// ArtCraft brand blue (from `docs/brand/artcraft-mark.svg`).','/// Accent colour for the independent build.').replace('Color32::from_rgb(0x4e, 0x7b, 0xfb)','Color32::from_rgb(0x35, 0x55, 0x48)').replace('Part of the ArtCraft suite of open creative tools.','Independent modified build, based on DesignCraft by the ArtCraft team.').replace('//! ArtCraft mark, version, and community links (Discord first and largest), plus the other ArtCraft','//! version and upstream community links, plus the other ArtCraft')
    p.write_text(s)
    # These are not included in binaries; also omit them from reconstructed distribution source.
    for p in (source/'docs/brand').glob('artcraft-*'):
        if p.is_file():p.unlink()

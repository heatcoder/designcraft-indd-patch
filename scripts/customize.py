"""Remove restricted ArtCraft artwork from the independent modified build.

Uses source markers rather than redistributing the removed vector outline in a patch.
"""
from pathlib import Path
import shutil
import re

def customize(source: Path):
    p=source/'crates/ui-egui/src/about.rs'
    s=p.read_text(encoding='utf-8')
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
    # Keep authorship credits without advertising upstream support for this fork.
    start=s.index('            if discord_button(ui, "Join the ArtCraft Discord"')
    end=s.index('            ui.add_space(12.0);',start)
    s=s[:start]+s[end:]
    start=s.index('/// A text link that opens `url`.')
    end=s.index('pub fn show(',start)
    s=s[:start]+s[end:]
    s=s.replace('use serde_json::json;\n','')
    s=s.replace("    let mut open: Option<&'static str> = None;\n",'')
    s=s.replace('    if let Some(k) = open {\n        let _ = app.run(&format!("help.{k}"), json!({}));\n    }\n','')
    p.write_text(s, encoding='utf-8')
    # These are not included in binaries; also omit them from reconstructed distribution source.
    for p in (source/'docs/brand').glob('artcraft-*'):
        if p.is_file():p.unlink()

    chrome=source/'crates/ui-egui/src/chrome.rs'
    c=chrome.read_text(encoding='utf-8').replace('Join the ArtCraft community','Independent DesignCraft build').replace('Get help, share your layouts and shape what we build next.','MalayalamPatch by Heatcoder. Based on open-source DesignCraft.').replace('Join our Discord','Upstream community').replace('discord_button(ui, "Discord", vec2(78.0, 22.0))','discord_button(ui, "Upstream", vec2(90.0, 22.0))')
    chrome.write_text(c, encoding='utf-8')
    menus=source/'crates/ui-egui/src/menus.rs'
    finish_branding(source)
    menus.write_text(menus.read_text(encoding='utf-8').replace('Join the ArtCraft Discord…','Upstream community…').replace('ArtCraft Website…','Upstream website…').replace('ArtCraft App Page…','Upstream app page…'), encoding='utf-8')


def finish_branding(source: Path):
    # Remove unused promotional translation rows, preserving attribution outside these tables.
    catalogs=[source/'crates/ui-egui/src/i18n.rs',*(source/'crates/ui-egui/src/i18n').glob('*.rs')]
    for p in catalogs:
        s=p.read_text(encoding='utf-8')
        marker='const TABLE:'
        if marker not in s: continue
        start=s.index('= &[',s.index(marker))+4
        end=s.index('\n];',start)
        rows=re.split(r'(?m)(?=^    \()',s[start:end])
        s=s[:start]+''.join(row for row in rows if 'artcraft' not in row.lower())+s[end:]
        p.write_text(s,encoding='utf-8')
    p=source/'apps/designcraft/src/native_menu.rs'
    p.write_text(p.read_text(encoding='utf-8').replace('Join the ArtCraft Discord…','Upstream community…'),encoding='utf-8')
    p=source/'crates/ui-egui/src/chrome.rs'
    p.write_text(p.read_text(encoding='utf-8').replace('("getartcraft.com", "help.website")','("Upstream website", "help.website")'),encoding='utf-8')
    p=source/'crates/engine/src/cmd/inspect.rs'
    p.write_text(p.read_text(encoding='utf-8').replace('(ArtCraft Discord, website, DesignCraft page and repository)','(upstream community, website, DesignCraft page and repository)'),encoding='utf-8')

"""Use format names in product copy; preserve protocol identifiers and notices."""
from pathlib import Path
import sys
REPLACEMENTS = {
    'DesignCraft, IDML or InDesign': 'DesignCraft, IDML or INDD',
    'InDesign Markup (IDML)': 'IDML',
    'InDesign document or template (INDD, INDT)': 'INDD document or INDT template',
    'InDesign .indd/.indt': 'INDD/INDT file',
    'InDesign document or template': 'INDD document or INDT template',
    'InDesign file': 'INDD file',
    'DesignCraft is a page-layout app (an InDesign clone).': 'DesignCraft is a page-layout app.',
}
FILES = [
    'apps/designcraft/src/main.rs', 'apps/designcraft-web/src/web.rs',
    'crates/ui-egui/src/menus.rs', 'crates/ui-egui/src/lib.rs',
    'crates/engine/src/cmd/file.rs', 'crates/engine/src/cmd/interchange.rs',
    'crates/mcp/src/server.rs',
]
def apply(source):
    changed = 0
    for name in FILES:
        p = source / name
        s = p.read_text(encoding='utf-8'); original = s
        for old, new in REPLACEMENTS.items():
            s = s.replace(old, new)
        if s != original:
            p.write_text(s, encoding='utf-8'); changed += 1
    return changed
if __name__ == '__main__':
    print(f'INDD product wording applied to {apply(Path(sys.argv[1]))} files')

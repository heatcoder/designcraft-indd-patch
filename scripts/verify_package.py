#!/usr/bin/env python3
"""Unpack native packages and compare all app files to the reviewed staging tree."""
from pathlib import Path
import argparse,hashlib,json,platform,subprocess,shutil,tarfile,zipfile,gzip
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,default=Path('dist'));a=p.parse_args()
root=Path(__file__).resolve().parents[1];out=a.output.resolve();system=platform.system();arch={'AMD64':'x86_64','ARM64':'aarch64','arm64':'aarch64'}.get(platform.machine(),platform.machine());stage=root/'build'/f'package-{system}-{arch}';review=stage/'verification';review.mkdir(exist_ok=True)
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
def run(*args):subprocess.run([str(x) for x in args],check=True)
def files(path):return {str(f.relative_to(path)):sha(f) for f in path.rglob('*') if f.is_file()}
def compare(expected,actual,allowed=()):
 e=files(expected);v=files(actual);assert e,'Empty staged payload'
 assert all(v.get(k)==h for k,h in e.items()),'Extracted payload differs from staging'
 unexpected=[k for k in v if k not in e and not any(Path(k).match(x) for x in allowed)]
 assert not unexpected,('Unexpected installer files',unexpected)
 return v
source=a.source.resolve();about=(source/'crates/ui-egui/src/about.rs').read_text(encoding='utf-8');patch=(root/'patches/designcraft-0.8.0-indd.patch').read_text(encoding='utf-8')
assert 'const MARK_PATH' not in about and '/// The ArtCraft mark outline' not in about
assert 'const MARK_PATH' not in patch and '/// The ArtCraft mark outline' not in patch
assert not list((source/'docs/brand').glob('artcraft-*')),'Restricted artwork remains in reconstructed source'
assert 'ArtCraft team' in about,'Required author credit missing'
assert 'Join the ArtCraft Discord' not in about and 'More ArtCraft apps' not in about,'Upstream promotional branding remains'
chrome=(source/'crates/ui-egui/src/chrome.rs').read_text(encoding='utf-8')
assert 'Join the ArtCraft community' not in chrome and 'Independent DesignCraft build' in chrome,'Welcome branding not customized'
# The shipped font input is deliberately limited to the pinned OFL font.
fonts={f.name:sha(f) for f in (root/'fonts').rglob('*') if f.suffix.lower() in ('.ttf','.otf','.ttc')}
assert list(fonts.values())==['312e0e7c3cc15fa09eb42a8f749eeb246b593ed420e3c81aafe8d910c3a6fb56'],fonts
if system=='Darwin':
 expected=stage/'root/MalayalamPatch/DesignCraft.app';pkg=next(out.glob('*macos-*.pkg'));expanded=review/'pkg';run('pkgutil','--expand-full',pkg,expanded)
 apps=list(expanded.rglob('DesignCraft.app'));assert len(apps)==1;inventory=compare(expected,apps[0]);binary=apps[0]/'Contents/MacOS/designcraft-cli';notices=apps[0]/'Contents/Resources/Notices'
 run('codesign','--verify','--deep','--strict',apps[0]);run('otool','-L',binary)
 z=review/'zip';run('ditto','-x','-k',next(out.glob('*macos-*.zip')),z);compare(expected,z/'DesignCraft.app')
elif system=='Linux':
 expected=stage/'root';expanded=review/'deb';run('dpkg-deb','-x',next(out.glob('*.deb')),expanded)
 # DEBIAN is package metadata, not installed payload.
 e=files(expected);e={k:v for k,v in e.items() if not k.startswith('DEBIAN/')};inventory=files(expanded);assert inventory==e,'DEB payload differs'
 binary=expanded/'opt/irajeev-designcraft/designcraft-cli';notices=expanded/'opt/irajeev-designcraft/Notices';run('ldd',binary)
 portable=review/'portable';portable.mkdir();run('tar','-xzf',next(out.glob('*.tar.gz')),'-C',portable);compare(expected/'opt/irajeev-designcraft',portable)
else:
 expected=stage/'payload';expanded=review/'installed';installer=next(out.glob('*.exe'))
 run(installer,'/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART','/SP-',f'/DIR={expanded}',f'/LOG={review / "install.log"}')
 inventory=compare(expected,expanded,('unins*.exe','unins*.dat'));binary=expanded/'designcraft-cli.exe';notices=expanded/'Notices'
 # Record imports if Visual Studio dumpbin is available on this runner.
 dumpbin=shutil.which('dumpbin')
 if dumpbin:run(dumpbin,'/DEPENDENTS',binary)
typeit_hashes=set(json.loads((root/'audit/TYPEIT-EXCLUSION.json').read_text(encoding='utf-8'))['excluded_file_sha256'])
assert not typeit_hashes.intersection(inventory.values()),'Typeit file detected in payload'
assert 'Heatcoder' in (notices/'NOTICE.md').read_text(encoding='utf-8'),'Publisher notice missing'
excluded={x['sha256'] for x in json.loads((root/'audit/excluded-brand-assets.json').read_text(encoding='utf-8'))}
assert not excluded.intersection(inventory.values()),'Restricted artwork file detected'
for path in inventory:
 name=Path(path).name.lower()
 assert not name.endswith(('.indd','.indt','.idml','.designcraft','.ocx','.vbp','.frm','.frx','.bas','.cls','.ttf','.otf','.ttc')),path
 assert not any(x in name for x in ('minion','typeit','artcraft-mark','artcraft-logo')),path
bundle=(notices/'THIRD-PARTY-NOTICES.txt').read_bytes();assert bundle==gzip.decompress((root/'audit/THIRD-PARTY-NOTICES.txt.gz').read_bytes())
for required in [b'dispatch-0.2.0/DISTRIBUTOR-NOTICE.txt',b'Steven Sheldon',b'r-efi-5.3.0/AUTHORS',b'Adobe-XMP',b'LICENSE_FOXIT']:
 assert required in bundle,required
report={'platform':system,'architecture':arch,'result':'PASS','scope':'Extracted native installer and portable archive match staged files; source artwork checks; approved external font input; forbidden loose payload files; exact notice archive. Does not establish legal chain of title or exhaustive binary decompilation.','files':inventory,'packages':{f.name:sha(f) for f in out.iterdir() if f.is_file() and f.suffix in ('.pkg','.zip','.exe','.deb','.gz')},'cli':str(binary)}
(out/f'verification-{system}-{arch}.json').write_text(json.dumps(report,indent=2), encoding='utf-8');print('PASS extracted installer verification')

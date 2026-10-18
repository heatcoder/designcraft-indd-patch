#!/usr/bin/env python3
"""Package already-built native binaries; never build or label a foreign binary."""
from pathlib import Path
import argparse, gzip, hashlib, html, json, os, platform, plistlib, shutil, subprocess
ROOT=Path(__file__).resolve().parents[1]
META=json.loads((ROOT/'upstream.json').read_text(encoding='utf-8'))
VERSION=META['patch_version']
p=argparse.ArgumentParser()
p.add_argument('--bin-dir',required=True,type=Path)
p.add_argument('--source',required=True,type=Path)
p.add_argument('--output',type=Path,default=ROOT/'dist')
a=p.parse_args(); bins=a.bin_dir.resolve(); source=a.source.resolve(); out=a.output.resolve()
out.mkdir(parents=True,exist_ok=True)
arch={'AMD64':'x86_64','ARM64':'aarch64','arm64':'aarch64'}.get(platform.machine(),platform.machine())
system=platform.system()
work=ROOT/'build'/f'package-{system}-{arch}'
if work.exists(): shutil.rmtree(work)
work.mkdir(parents=True)
def run(*args,**kw): subprocess.run([str(x) for x in args],check=True,**kw)
def copy(src,dst):
    dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst)
def notices(dst):
    for f in ['AUDIT.md','dependencies.csv','release-status.json']:
        copy(ROOT/'audit'/f,dst/f)
    copy(ROOT/'audit/PROVENANCE.md',dst/'PROVENANCE.md')
    copy(ROOT/'audit/TYPEIT-EXCLUSION.json',dst/'TYPEIT-EXCLUSION.json')
    copy(ROOT/'audit/notice-sources.json',dst/'notice-sources.json')
    (dst/'THIRD-PARTY-NOTICES.txt').write_bytes(gzip.decompress((ROOT/'audit/THIRD-PARTY-NOTICES.txt.gz').read_bytes()))
    copy(source/'NOTICE',dst/'DesignCraft-NOTICE.txt')
    copy(source/'assets/app-icon/LICENSE.txt',dst/'DesignCraft-icon-LICENSE.txt')
    for f in ['LICENSE-MIT','LICENSE-APACHE','NOTICE.md']: copy(ROOT/f,dst/f)
    copy(ROOT/'README.md',dst/'README.md')
    copy(ROOT/'fonts/OFL-NotoSansMalayalam.txt',dst/'OFL-NotoSansMalayalam.txt')
    copy(ROOT/'fonts/README.md',dst/'Malayalam-font-source.md')
    for f in ['LICENSE-MIT','LICENSE-APACHE']:
        found=list((Path(os.environ.get('CARGO_HOME',Path.home()/'.cargo'))/'git/checkouts').glob('indd-utils-*/*/'+f))
        if found: copy(found[0],dst/('indd-utils-'+f))
if system=='Darwin':
    for name in ['designcraft','designcraft-cli']:
        info=subprocess.check_output(['lipo','-archs',str(bins/name)],text=True).strip()
        expected='arm64' if arch=='aarch64' else 'x86_64'
        if info!=expected: raise SystemExit(f'Architecture mismatch: {name}: {info}, expected {expected}')
    app=work/'root/DesignCraft.app'; contents=app/'Contents'
    copy(bins/'designcraft',contents/'MacOS/DesignCraft')
    copy(bins/'designcraft-cli',contents/'MacOS/designcraft-cli')
    icon=source/'assets/app-icon/DesignCraft.icns'
    if not icon.exists():
        matches=list((source/'assets/app-icon').glob('*.icns')); icon=matches[0] if matches else None
    if icon: copy(icon,contents/'Resources/DesignCraft.icns')
    notices(contents/'Resources/Notices')
    info={'CFBundleExecutable':'DesignCraft','CFBundleIdentifier':'com.heatcoder.designcraft.indd','CFBundleName':'DesignCraft',
          'CFBundleDisplayName':'DesignCraft','CFBundlePackageType':'APPL','CFBundleShortVersionString':'0.8.0','CFBundleVersion':'0.8.7',
          'HeatcoderPatchVersion':VERSION,'LSMinimumSystemVersion':'11.0','NSHighResolutionCapable':True,'CFBundleIconFile':'DesignCraft',
          'NSHumanReadableCopyright':'DesignCraft authors. INDD patch distribution: Heatcoder.',
          'CFBundleDocumentTypes':[{'CFBundleTypeName':'DesignCraft, INDD and IDML documents','CFBundleTypeRole':'Editor','LSHandlerRank':'Alternate','CFBundleTypeExtensions':['designcraft','idml','indd','indt']}]}
    (contents/'Info.plist').write_bytes(plistlib.dumps(info))
    run('codesign','--force','--deep','--sign','-','--timestamp=none',app)
    run('codesign','--verify','--deep','--strict',app)
    component=work/'payload.pkg'
    # Disable bundle relocation: updates replace /Applications/DesignCraft.app.
    cp=work/'components.plist'
    run('pkgbuild','--analyze','--root',work/'root',cp)
    components=plistlib.loads(cp.read_bytes())
    for item in components:
        item['BundleIsRelocatable']=False
        item['BundleOverwriteAction']='upgrade'
    cp.write_bytes(plistlib.dumps(components))
    run('pkgbuild','--root',work/'root','--component-plist',cp,'--identifier','com.heatcoder.designcraft.indd','--version','0.8.7','--install-location','/Applications','--scripts',ROOT/'scripts/macos',component)
    resources=work/'resources';resources.mkdir()
    (resources/'welcome.html').write_text('''<html><body style="font-family:Helvetica;color:#273d37;background:#faf7f2;padding:20px"><h1 style="font-family:Georgia;font-size:44px;font-weight:normal">Heatcoder</h1><h2>DesignCraft · INDD opening</h2><p>Published by Heatcoder.</p><p>Update DesignCraft in Applications. Close DesignCraft first. Your previous app is backed up under /Library/Application Support/Heatcoder/DesignCraft Backups. Documents and settings are preserved.</p><p>Open INDD documents directly from File → Open. Save edits as DesignCraft or IDML.</p><p>This independent experimental build uses the DesignCraft and indd-utils open-source projects. Layout, fonts and linked images require review.</p></body></html>''', encoding='utf-8')
    (resources/'conclusion.html').write_text('''<html><body style="font-family:Helvetica;padding:20px"><h1>Ready to open INDD</h1><p>Open <b>Applications → DesignCraft</b>, then choose File → Open.</p><p>Your previous app is saved in /Library/Application Support/Heatcoder/DesignCraft Backups. Keep your original INDD documents and check imported layouts before production use.</p><p>Heatcoder</p></body></html>''', encoding='utf-8')
    copy(ROOT/'NOTICE.md',resources/'notice.txt')
    dist=work/'Distribution.xml'
    host='arm64' if arch=='aarch64' else 'x86_64'
    dist.write_text(f'''<?xml version="1.0"?><installer-gui-script minSpecVersion="2"><title>Heatcoder — DesignCraft INDD Patch</title><welcome file="welcome.html" mime-type="text/html"/><conclusion file="conclusion.html" mime-type="text/html"/><license file="notice.txt"/><options customize="never" require-scripts="true" hostArchitectures="{host}"/><domains enable_localSystem="true" enable_currentUserHome="false" enable_anywhere="false"/><choices-outline><line choice="main"/></choices-outline><choice id="main" visible="false" title="DesignCraft"><pkg-ref id="com.heatcoder.designcraft.indd"/></choice><pkg-ref id="com.heatcoder.designcraft.indd" version="0.8.7" onConclusion="none">payload.pkg</pkg-ref></installer-gui-script>''', encoding='utf-8')
    run('productbuild','--distribution',dist,'--resources',resources,'--package-path',work,out/f'heatcoder-designcraft-indd-{VERSION}-macos-{arch}.pkg')
    run('ditto','-c','-k','--sequesterRsrc','--keepParent',app,out/f'heatcoder-designcraft-indd-{VERSION}-macos-{arch}.zip')
elif system=='Windows':
    stage=work/'payload'; stage.mkdir()
    for name in ['designcraft.exe','designcraft-cli.exe']: copy(bins/name,stage/name)
    notices(stage/'Notices')
    # Prefer the real installation over Chocolatey's PATH shim. Notices live beside ISCC.
    candidates=[Path(r'C:\Program Files (x86)\Inno Setup 6\ISCC.exe'),Path(r'C:\Program Files\Inno Setup 6\ISCC.exe')]
    compiler=str(next((f for f in candidates if f.is_file()), Path(shutil.which('ISCC') or 'ISCC.exe')))
    compiler_root=Path(compiler).parent
    licence_files=[f for f in compiler_root.rglob('*') if f.is_file() and f.suffix.lower() in ('.txt','.rtf','.html') and any(word in f.name.lower() for word in ('license','licence','copying','copyright'))]
    if not licence_files: raise SystemExit(f'Inno Setup runtime licence files missing beside {compiler}; files: {[f.name for f in compiler_root.iterdir()]}')
    for f in licence_files: copy(f,stage/'Notices/InnoSetup'/f.relative_to(compiler_root))
    version=subprocess.run([compiler,'/?'],capture_output=True,text=True,encoding="utf-8",errors="replace").stdout
    (stage/'Notices/InnoSetup/compiler-version.txt').write_text(version, encoding='utf-8')
    run(compiler,f'/DBinDir={stage}',f'/DOutputDir={out}',f'/DArch={arch}',f'/DVersion={VERSION}',ROOT/'scripts/windows.iss')
elif system=='Linux':
    debarch={'x86_64':'amd64','aarch64':'arm64'}.get(arch)
    if not debarch: raise SystemExit(f'Unsupported package architecture {arch}')
    stage=work/'root'; app=stage/'usr/lib/heatcoder-designcraft'
    for name in ['designcraft','designcraft-cli']: copy(bins/name,app/name)
    notices(app/'Notices')
    for name in ['designcraft','designcraft-cli']:
        copy(bins/name,stage/'usr/bin'/name)
    copy(ROOT/'scripts/linux/preinst',stage/'DEBIAN/preinst')
    copy(ROOT/'branding/icon.png',stage/'usr/share/icons/hicolor/256x256/apps/heatcoder-designcraft.png')
    desktop=stage/'usr/share/applications/ai.storyteller.designcraft.desktop';desktop.parent.mkdir(parents=True)
    desktop.write_text('[Desktop Entry]\nType=Application\nName=DesignCraft\nComment=Direct INDD opening — Heatcoder\nExec=/usr/bin/designcraft %F\nIcon=heatcoder-designcraft\nTerminal=false\nCategories=Graphics;Publishing;\nMimeType=application/x-indesign;application/vnd.adobe.indesign-idml-package;\n', encoding='utf-8')
    control=stage/'DEBIAN/control';control.parent.mkdir(exist_ok=True)
    control.write_text(f'Package: designcraft\nVersion: 0.8.0-7\nArchitecture: {debarch}\nMaintainer: Heatcoder\nHomepage: https://github.com/heatcoder/designcraft-indd-patch\nDepends: libc6, libgcc-s1, libstdc++6, libx11-6, libxkbcommon0, libwayland-client0, libvulkan1, procps\nDescription: DesignCraft with direct INDD import\n DesignCraft upgrade distributed by Heatcoder.\n', encoding='utf-8')
    run('dpkg-deb','--root-owner-group','--build',stage,out/f'heatcoder-designcraft-indd-{VERSION}-linux-{arch}.deb')
    # Also provide a portable archive for other Linux distributions. No installer is claimed.
    run('tar','-C',app,'-czf',out/f'heatcoder-designcraft-indd-{VERSION}-linux-{arch}.tar.gz','.')
else: raise SystemExit(f'No installer implementation for {system}')
files=[f for f in out.iterdir() if f.is_file() and f.suffix in ['.pkg','.zip','.exe','.deb','.gz']]
(out/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.name+'\n' for f in sorted(files)), encoding='utf-8')
print(f'Packaged files in {out}')

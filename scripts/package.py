#!/usr/bin/env python3
"""Package already-built native binaries; never build or label a foreign binary."""
from pathlib import Path
import argparse, hashlib, html, json, os, platform, plistlib, shutil, subprocess
ROOT=Path(__file__).resolve().parents[1]
META=json.loads((ROOT/'upstream.json').read_text())
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
    for f in ['LICENSE-MIT','LICENSE-APACHE','NOTICE.md']: copy(ROOT/f,dst/f)
    copy(ROOT/'README.md',dst/'README.md')
    for f in ['LICENSE-MIT','LICENSE-APACHE']:
        found=list((Path(os.environ.get('CARGO_HOME',Path.home()/'.cargo'))/'git/checkouts').glob('indd-utils-*/*/'+f))
        if found: copy(found[0],dst/('indd-utils-'+f))
if system=='Darwin':
    for name in ['designcraft','designcraft-cli']:
        info=subprocess.check_output(['lipo','-archs',str(bins/name)],text=True).strip()
        expected='arm64' if arch=='aarch64' else 'x86_64'
        if info!=expected: raise SystemExit(f'Architecture mismatch: {name}: {info}, expected {expected}')
    app=work/'root/DesignCraft iRajeev.app'; contents=app/'Contents'
    copy(bins/'designcraft',contents/'MacOS/DesignCraft')
    copy(bins/'designcraft-cli',contents/'MacOS/designcraft-cli')
    icon=source/'assets/app-icon/DesignCraft.icns'
    if not icon.exists():
        matches=list((source/'assets/app-icon').glob('*.icns')); icon=matches[0] if matches else None
    if icon: copy(icon,contents/'Resources/DesignCraft.icns')
    notices(contents/'Resources/Notices')
    info={'CFBundleExecutable':'DesignCraft','CFBundleIdentifier':'com.irajeev.designcraft.indd','CFBundleName':'DesignCraft iRajeev',
          'CFBundleDisplayName':'DesignCraft iRajeev','CFBundlePackageType':'APPL','CFBundleShortVersionString':'0.8.0','CFBundleVersion':'0.8.1',
          'IRajeevPatchVersion':VERSION,'LSMinimumSystemVersion':'11.0','NSHighResolutionCapable':True,'CFBundleIconFile':'DesignCraft',
          'NSHumanReadableCopyright':'DesignCraft authors. INDD patch distribution: irajeev.com.',
          'CFBundleDocumentTypes':[{'CFBundleTypeName':'DesignCraft and InDesign documents','CFBundleTypeRole':'Editor','LSHandlerRank':'Alternate','CFBundleTypeExtensions':['designcraft','idml','indd','indt']}]}
    (contents/'Info.plist').write_bytes(plistlib.dumps(info))
    run('codesign','--force','--deep','--sign','-','--timestamp=none',app)
    run('codesign','--verify','--deep','--strict',app)
    component=work/'payload.pkg'
    # Disable bundle relocation: updates stay in the dedicated Applications folder.
    cp=work/'components.plist'
    run('pkgbuild','--analyze','--root',work/'root',cp)
    components=plistlib.loads(cp.read_bytes())
    for item in components: item['BundleIsRelocatable']=False
    cp.write_bytes(plistlib.dumps(components))
    run('pkgbuild','--root',work/'root','--component-plist',cp,'--identifier','com.irajeev.designcraft.indd','--version','0.8.1','--install-location','/Applications',component)
    resources=work/'resources';resources.mkdir()
    (resources/'welcome.html').write_text('''<html><body style="font-family:Helvetica;color:#273d37;background:#faf7f2;padding:20px"><h1 style="font-family:Georgia;font-size:44px;font-weight:normal">irajeev.com</h1><h2>DesignCraft · INDD opening</h2><p>Install DesignCraft iRajeev alongside your existing app.</p><p>Open InDesign documents directly from File → Open. Save edits as DesignCraft or IDML.</p><p>This independent experimental build uses the DesignCraft and indd-utils open-source projects. Layout, fonts and linked images require review.</p></body></html>''')
    (resources/'conclusion.html').write_text('''<html><body style="font-family:Helvetica;padding:20px"><h1>Ready to open INDD</h1><p>Open <b>Applications → DesignCraft iRajeev</b>, then choose File → Open.</p><p>Your original DesignCraft installation is still available. Keep your original INDD documents and check imported layouts before production use.</p><p>irajeev.com</p></body></html>''')
    copy(ROOT/'NOTICE.md',resources/'notice.txt')
    dist=work/'Distribution.xml'
    host='arm64' if arch=='aarch64' else 'x86_64'
    dist.write_text(f'''<?xml version="1.0"?><installer-gui-script minSpecVersion="2"><title>irajeev.com — DesignCraft INDD Patch</title><welcome file="welcome.html" mime-type="text/html"/><conclusion file="conclusion.html" mime-type="text/html"/><license file="notice.txt"/><options customize="never" require-scripts="false" hostArchitectures="{host}"/><domains enable_localSystem="true" enable_currentUserHome="false" enable_anywhere="false"/><choices-outline><line choice="main"/></choices-outline><choice id="main" visible="false" title="DesignCraft iRajeev"><pkg-ref id="com.irajeev.designcraft.indd"/></choice><pkg-ref id="com.irajeev.designcraft.indd" version="0.8.1" onConclusion="none">payload.pkg</pkg-ref></installer-gui-script>''')
    run('productbuild','--distribution',dist,'--resources',resources,'--package-path',work,out/f'irajeev-designcraft-indd-{VERSION}-macos-{arch}.pkg')
    run('ditto','-c','-k','--sequesterRsrc','--keepParent',app,out/f'irajeev-designcraft-indd-{VERSION}-macos-{arch}.zip')
elif system=='Windows':
    stage=work/'payload'; stage.mkdir()
    for name in ['designcraft.exe','designcraft-cli.exe']: copy(bins/name,stage/name)
    notices(stage/'Notices')
    compiler=shutil.which('ISCC') or r'C:\Program Files (x86)\Inno Setup 6\ISCC.exe'
    run(compiler,f'/DBinDir={stage}',f'/DOutputDir={out}',f'/DArch={arch}',f'/DVersion={VERSION}',ROOT/'scripts/windows.iss')
elif system=='Linux':
    debarch={'x86_64':'amd64','aarch64':'arm64'}.get(arch)
    if not debarch: raise SystemExit(f'Unsupported package architecture {arch}')
    stage=work/'root'; app=stage/'opt/irajeev-designcraft'
    for name in ['designcraft','designcraft-cli']: copy(bins/name,app/name)
    notices(app/'Notices')
    copy(ROOT/'branding/icon.png',stage/'usr/share/icons/hicolor/256x256/apps/irajeev-designcraft.png')
    desktop=stage/'usr/share/applications/irajeev-designcraft.desktop';desktop.parent.mkdir(parents=True)
    desktop.write_text('[Desktop Entry]\nType=Application\nName=DesignCraft iRajeev\nComment=Direct INDD opening — irajeev.com\nExec=/opt/irajeev-designcraft/designcraft %F\nIcon=irajeev-designcraft\nTerminal=false\nCategories=Graphics;Publishing;\nMimeType=application/x-indesign;application/vnd.adobe.indesign-idml-package;\n')
    control=stage/'DEBIAN/control';control.parent.mkdir()
    control.write_text(f'Package: irajeev-designcraft-indd\nVersion: 0.8.0-1\nArchitecture: {debarch}\nMaintainer: irajeev.com\nHomepage: https://irajeev.com\nDepends: libc6, libgcc-s1, libstdc++6, libx11-6, libxkbcommon0, libwayland-client0, libvulkan1\nDescription: DesignCraft with direct INDD import\n Independent side-by-side build distributed by irajeev.com.\n')
    run('dpkg-deb','--root-owner-group','--build',stage,out/f'irajeev-designcraft-indd-{VERSION}-linux-{arch}.deb')
    # Also provide a portable archive for other Linux distributions. No installer is claimed.
    run('tar','-C',app,'-czf',out/f'irajeev-designcraft-indd-{VERSION}-linux-{arch}.tar.gz','.')
else: raise SystemExit(f'No installer implementation for {system}')
files=[f for f in out.iterdir() if f.is_file() and f.suffix in ['.pkg','.zip','.exe','.deb','.gz']]
(out/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.name+'\n' for f in sorted(files)))
print(f'Packaged files in {out}')

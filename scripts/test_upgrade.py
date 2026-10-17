"""Native disposable-runner upgrade checks; never run against a user's installation."""
from pathlib import Path
import hashlib,json,os,platform,subprocess,sys,time,shutil
from xml.sax.saxutils import escape
root=Path(__file__).resolve().parents[1];out=root/'dist';system=platform.system()
assert os.environ.get('GITHUB_ACTIONS')=='true','Disposable CI runner only'
def run(*args):subprocess.run([str(x) for x in args],check=True)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if system=='Darwin':
 app=Path('/Applications/DesignCraft.app'); assert not app.exists()
 run('sudo','mkdir','-p',app/'Contents/MacOS');run('sudo','cp','/usr/bin/true',app/'Contents/MacOS/DesignCraft')
 old=digest(app/'Contents/MacOS/DesignCraft')
 legacy=Path('/Applications/MalayalamPatch/DesignCraft.app')
 run('sudo','mkdir','-p',legacy/'Contents/MacOS');run('sudo','cp','/usr/bin/true',legacy/'Contents/MacOS/DesignCraft')
 run('sudo','installer','-pkg',next(out.glob('*.pkg')),'-target','/')
 backups=list(Path('/Library/Application Support/Heatcoder/DesignCraft Backups').glob('*/DesignCraft.app/Contents/MacOS/DesignCraft'))
 assert any(digest(p)==old for p in backups),'Old app backup missing'
 stage=root/'build/package-Darwin'/ 'unused'
 expected=next((root/'build').glob('package-Darwin-*/root/DesignCraft.app/Contents/MacOS/DesignCraft'))
 assert digest(app/'Contents/MacOS/DesignCraft')==digest(expected)
 assert not (app/'Contents/MacOS/old-only').exists()
 assert not legacy.exists(),'Separate patch app still installed'
 retired=list(Path('/Library/Application Support/Heatcoder/DesignCraft Backups').glob('retired-*/DesignCraft.app/Contents/MacOS/DesignCraft'))
 assert any(digest(p)==old for p in retired),'Separate patch backup missing'
elif system=='Linux':
 # A real same-name Debian package upgrade, not just extraction.
 fixture=root/'build/old-package';(fixture/'DEBIAN').mkdir(parents=True)
 (fixture/'usr/bin').mkdir(parents=True)
 (fixture/'DEBIAN/control').write_text('Package: designcraft\nVersion: 0.8.0-1\nArchitecture: all\nMaintainer: Test\nDescription: upgrade test fixture\n')
 (fixture/'usr/bin/designcraft').write_text('old-test-binary\n')
 run('dpkg-deb','--build',fixture,root/'build/old.deb');run('sudo','dpkg','--unpack',root/'build/old.deb')
 run('sudo','dpkg','--unpack',next(out.glob('*.deb')))
 backups=list(Path('/var/backups/heatcoder-designcraft').glob('*/usr/bin/designcraft'))
 assert any(p.read_text(errors='ignore')=='old-test-binary\n' for p in backups)
 expected=next((root/'build').glob('package-Linux-*/root/usr/bin/designcraft'))
 assert digest(Path('/usr/bin/designcraft'))==digest(expected)
else:
 # Build and install a small MSI with the same registration structure as upstream.
 app=Path(os.environ['ProgramFiles'])/'HeatcoderUpgradeFixture'
 fixture=root/'build/msi-fixture';fixture.mkdir()
 old=fixture/'designcraft.exe';old.write_bytes(b'old-test-binary')
 wxs=fixture/'fixture.wxs'
 wxs.write_text(f'''<Wix xmlns="http://wixtoolset.org/schemas/v4/wxs"><Package Name="DesignCraft" Manufacturer="Upgrade test fixture" Version="0.8.0" UpgradeCode="49E87D30-BB68-4896-AA1D-F45C833CFC3C" Scope="perMachine"><MediaTemplate EmbedCab="yes"/><StandardDirectory Id="ProgramFiles6432Folder"><Directory Id="INSTALLFOLDER" Name="HeatcoderUpgradeFixture"><Component Id="App"><File Id="Exe" Source="{escape(str(old))}" KeyPath="yes"/><RegistryValue Root="HKLM" Key="Software\\Microsoft\\Windows\\CurrentVersion\\App Paths\\designcraft.exe" Value="[#Exe]" Type="string"/></Component></Directory></StandardDirectory><Feature Id="Main"><ComponentRef Id="App"/></Feature></Package></Wix>''')
 run('dotnet','tool','install','--tool-path',fixture/'tools','wix','--version','5.0.2')
 msi=fixture/'old.msi'
 arch='arm64' if platform.machine().lower() in ('arm64','aarch64') else 'x64'
 run(fixture/'tools/wix.exe','build',wxs,'-arch',arch,'-o',msi)
 run('msiexec.exe','/i',msi,'/qn','/norestart')
 assert (app/'designcraft.exe').read_bytes()==b'old-test-binary'
 installer=next(out.glob('*.exe'))
 # No /DIR override: exercise registration-based location discovery.
 run(installer,'/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART','/SP-',f'/LOG={out / "upgrade-install.log"}')
 backups=list((Path(os.environ['ProgramData'])/'Heatcoder/DesignCraft Backups').glob('*/designcraft.exe'))
 assert any(p.read_bytes()==b'old-test-binary' for p in backups)
 expected=next((root/'build').glob('package-Windows-*/payload/designcraft.exe'))
 assert digest(app/'designcraft.exe')==digest(expected)
(out/'upgrade-test.json').write_text(json.dumps({'result':'PASS','platform':system,'checks':['existing app backup','replacement executable hash'],'scope':'Disposable runner native upgrade; Windows synthetic MSI migration fixture using upstream registration structure; not every historical third-party installer.'},indent=2))
print('PASS native upgrade: previous app backed up and installed executable verified')

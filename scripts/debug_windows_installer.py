from pathlib import Path
import subprocess,hashlib,json,platform
r=Path(__file__).resolve().parents[1];incoming=r/'incoming';target=r/'build/debug-binaries';target.mkdir(parents=True)
arch='aarch64' if platform.machine().lower() in ('aarch64','arm64') else 'x86_64'
report=json.loads(next((r/'audit/verification-v4'/('windows-'+arch)).glob('verification-*.json')).read_text())
for name,h in report['packages'].items():assert hashlib.sha256((incoming/name).read_bytes()).hexdigest()==h
subprocess.run([str(next(incoming.glob('*.exe'))),'/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART','/SP-',f'/DIR={target}'],check=True)
subprocess.run(['python','scripts/package.py','--source','build/designcraft','--bin-dir',str(target)],check=True)
subprocess.run(['python','scripts/verify_package.py','--source','build/designcraft'],check=True)
subprocess.run(['python','scripts/test_upgrade.py'],check=True)

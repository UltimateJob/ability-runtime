import os, shutil, subprocess, zipfile, json
from pathlib import Path
root=Path.cwd(); out=root/'.output/payload'
asset=os.environ['COMPONENT']=='mujoco-asset'
allowed={'robot','scene','assets','asset-catalog.v1.json'} if asset else {'base-bundles'}
for name in subprocess.check_output(['git','ls-files','-z'],text=True).split('\0'):
 if not name or Path(name).parts[0] not in allowed:continue
 p=root/name
 if p.is_symlink():raise SystemExit('Unexpected symlink')
 if p.suffix=='.whl':
  with zipfile.ZipFile(p) as z:
   if z.testzip():raise SystemExit('Corrupt vendored wheel')
 target=out/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)

import os
from os.path import isdir

p="/Users/efaure/SeaFile/MorphoDeep/morphodeep"
d="/Users/efaure/Desktop/morphodeep"

if isdir(d):os.system(f"rm -rf {d}")
os.system(f"rm -rf {d}.tar.gz")

os.mkdir(d)
os.system(f"cp -r {p}/morphodeep {d}")
os.system(f"cp {p}/morphodeep.py {d}")
os.system(f"cp {p}/README.md {d}")
os.system(f"cp {p}/LICENSE {d}")
os.system(f"cp {p}/MANIFEST.in {d}")
os.system(f"cp {p}/pyproject.toml {d}")

os.system(f"rm -rf {d}/morphodeep/test")
os.system(f"rm -rf {d}/morphodeep/__pycache__")
os.system(f"rm -rf {d}/morphodeep/DataManagement/__pycache__")
os.system(f"rm -rf {d}/morphodeep/JobManagement/__pycache__")
os.system(f"rm -rf {d}/morphodeep/napari-plugin/__pycache__")
os.system(f"rm -rf {d}/morphodeep/networks/__pycache__")
os.system(f"rm -rf {d}/morphodeep/tools/__pycache__")

os.system(f"cd /Users/efaure/Desktop/ ;  tar -cf morphodeep.tar.gz morphodeep")
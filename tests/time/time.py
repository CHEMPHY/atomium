import os
import subprocess
import datetime
import sys
sys.path.insert(0, ".")
import atomium
import requests

here = dir_path = os.path.dirname(os.path.realpath(__file__))
version = atomium.__version__.replace(".", "-")
today = datetime.datetime.now().date().strftime("%Y-%m-%d")

pdbs = ["1LOL", "5XME"]
for pdb in pdbs:
    filestring = requests.get(
     "http://www.ebi.ac.uk/pdbe/entry-files/pdb{}.ent".format(pdb.lower())
    ).text
    with open("{}/{}.pdb".format(here, pdb), "w") as f:
        f.write(filestring)
    with open("{}/timescript.py".format(here)) as f:
        script = f.read().format(pdb)
    with open("{}/{}.py".format(here, pdb), "w") as f:
        f.write(script)
    try:
        subprocess.call(
         "python -m cProfile -o {}/profiles/{}-{}-{}.prof {}/{}.py".format(
          here, pdb, version, today, here, pdb
         ), shell=True
        )
    finally:
        os.remove("{}/{}.py".format(here, pdb))
        os.remove("{}/{}.pdb".format(here, pdb))
        os.remove("{}/temp.pdb".format(here))

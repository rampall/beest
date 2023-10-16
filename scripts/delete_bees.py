import os, glob, shutil
BEEST_DIR = os.path.expanduser("~/.beest")

print("Deleting config file...")
config_files = glob.glob(f"{BEEST_DIR}/config*")
for config_file in config_files:
    os.remove(config_file)

print("Deleting bee scripts...")
bee_scripts = glob.glob(f"{BEEST_DIR}/bees/scripts/*.sh")
for bee_script in bee_scripts:
    os.remove(bee_script)

os.system("pm2 delete beest -s")

print("Deleting bee datadirs...")
bee_datadirs = glob.glob(f"{BEEST_DIR}/bees/datadir/*")
for bee_datadir in bee_datadirs:
    shutil.rmtree(bee_datadir)

print("Done")
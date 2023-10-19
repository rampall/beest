import os, sys, glob, shutil

BEEST_DIR = os.path.expanduser("~/.beest")
PM2_DIR = os.path.expanduser("~/.pm2")

bee_scripts = glob.glob(f"{BEEST_DIR}/bees/scripts/*.sh")

print("Deleting config file...")
config_files = glob.glob(f"{BEEST_DIR}/config*")
for config_file in config_files:
    os.remove(config_file)

print("Deleting bee scripts...")
for bee_script in bee_scripts:
    os.remove(bee_script)

os.system("pm2 delete bees")
os.system("pm2 flush bees")
os.system(f"rm -rf {PM2_DIR}/logs/bee-*")

print("Deleting bee datadirs...")
bee_datadirs = glob.glob(f"{BEEST_DIR}/bees/datadir/*")
for bee_datadir in bee_datadirs:
    shutil.rmtree(bee_datadir)

print("Done")
import os, glob

BEEST_DIR = os.path.expanduser("~/.beest")

import subprocess
import json

def stop_all_bees():
    result = subprocess.run(['pm2', 'jlist'], capture_output=True, text=True)
    if result.returncode == 0:
        try:
            output = json.loads(result.stdout)
            return output
        except json.JSONDecodeError:
            print("Error: Failed to parse JSON output.")
    else:
        print(f"Error: Script execution failed with return code {result.returncode}.")

output = stop_all_bees()
os.system(f"pm2 stop bees")
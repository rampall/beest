import sys, os

# print(sys.argv)

bee_id = sys.argv[1]
BEEST_DIR = os.path.expanduser("~/.beest")

print("[cyan][/cyan]")
with open(f"{BEEST_DIR}/bees/scripts/{bee_id}.sh", "r") as file:
    contents = file.read()    
    print( " \\\n --".join(contents.split(' --')) )


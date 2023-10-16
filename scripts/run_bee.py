import os
import sys
import getopt
import asyncio
import subprocess
import secrets
import socket
import json
import sqlite3

from pupdb.core import PupDB


class i():
    @staticmethod
    def log(message):
        print(f"[green]INFO[/green] {message}")

    def info(message):
        # print(f"[cyan]INFO[/cyan] {message}")
        pass

    def err(message):
        print(f"[red]ERROR {message}[/red]")


BEEST_DIR = os.path.expanduser(f"~/.beest")
BEES_DIR = f"{BEEST_DIR}/bees"
BEES_SCRIPT_DIR = f"{BEEST_DIR}/bees/scripts"
BEES_DATA_DIR = f"{BEEST_DIR}/bees/datadir"

CONFIG = PupDB(f"{BEEST_DIR}/config.json")


def ensure_init(bee_id):
    BEE_DATA_DIR = f"{BEES_DATA_DIR}/{bee_id}"
    directories = {
        BEEST_DIR: f"Directory {BEEST_DIR} created.",
        BEES_DIR: f"Directory {BEES_DIR} created.",
        BEES_SCRIPT_DIR: f"Directory {BEES_SCRIPT_DIR} created.",
        BEES_DATA_DIR: f"Directory {BEES_DATA_DIR} created.",
        BEE_DATA_DIR: f"Directory {BEE_DATA_DIR} created."
    }
    for directory, message in directories.items():
        if not os.path.exists(directory):
            os.makedirs(directory)
            i.info(message)
        else:
            i.info(f"Directory'{directory}' already exists.")
    bee_passwd_file = f"{BEES_DIR}/.bee_password"
    if not os.path.exists(bee_passwd_file):
        with open(bee_passwd_file, "x") as file:
            file.write(secrets.token_hex(64 // 2))
    else:
        i.info(f"File '{bee_passwd_file}' already exists.")
    if not(CONFIG.get('start_port')):
        CONFIG.set('start_port', 6699)


def get_new_beeid():
    file_list = [file for file in os.listdir(
        BEES_SCRIPT_DIR) if os.path.isfile(os.path.join(BEES_SCRIPT_DIR, file))]
    # Count the number of files
    file_count = len(file_list)
    return file_count+1


def next_free_port(port, max_port=65535):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while port <= max_port:
        try:
            sock.bind(('', port))
            sock.close()
            return port
        except OSError:
            port += 1
    raise IOError('no free ports')


def add_bee_script(mode, verbosity, rpc):
    id = get_new_beeid()
    bee_id = f"bee_{str(id).zfill(4)}"
    ensure_init(bee_id)
    # print(CONFIG)
    # print(CONFIG.get('start_port'))
    bee_api_port = next_free_port(CONFIG.get('start_port'))
    bee_p2p_port = next_free_port(bee_api_port+1)
    bee_debug_port = next_free_port(bee_p2p_port+1)
    CONFIG.set('start_port', bee_debug_port+1)
    if rpc != "":
        rpc_list = CONFIG.get('rpc_list') or {}
        rpc_list[rpc] = rpc
    # print(CONFIG.get('start_port'))

    cmd = os.path.expanduser(
        f"{BEEST_DIR}/bin/bee/bee start --debug-api-enable=true" 
        + f" --api-addr :{bee_api_port} --p2p-addr :{bee_p2p_port} --debug-api-addr :{bee_debug_port}"
        + f" --verbosity {verbosity} --data-dir {BEEST_DIR}/bees/datadir/{bee_id} --password-file {BEEST_DIR}/bees/.bee_password" 
    )
    match mode:
        case "ultralight":
            cmd = cmd + " --full-node=false --swap-enable=false"
        case "light":
            cmd = cmd+f" --full-node=false --swap-enable=true --blockchain-rpc-endpoint {rpc}"
        case "full":
            cmd = cmd+f" --full-node=true --swap-enable=true --blockchain-rpc-endpoint {rpc}"

    with open(f"{BEES_SCRIPT_DIR}/{bee_id}.sh", "w") as file:
        file.write(cmd)
    print(f"[green]INFO[green] CREATED: {BEES_SCRIPT_DIR}/{bee_id}.sh")
    os.system(
        f"pm2 start {BEES_SCRIPT_DIR}/{bee_id}.sh --time --name {bee_id} --namespace bees")
    # os.system(f"pm2 log {bee_id}")


def main(argv):
    verbosity = 0
    mode = 'ultralight'
    rpc = ''
    opts, args = getopt.getopt(argv, "v:m:u:", ["verbosity=", "mode=", "rpc="])
    for opt, arg in opts:
        if opt in ("-v", "--verbosity"):
            verbosity = arg
        if opt in ("-m", "--mode"):
            mode = arg
        if opt in ("-r", "--rpc"):
            rpc = arg
    # print(f"verbosity : {verbosity}")
    # print(f"mode : {mode}")
    # print(f"rpc : {rpc}")
    add_bee_script(mode,verbosity,rpc)

if __name__ == "__main__":
    main(sys.argv[1:])

**Warning: This project is a WIP in early alpha. And is being actively developed. No guarantees can be made about its stability, efficiency, and security at this stage.**


# Beest
```
██████╗ ███████╗███████╗███████╗████████╗ 0.1.0
██╔══██╗██╔════╝██╔════╝██╔════╝╚══██╔══╝ 
██████╔╝█████╗  █████╗  ███████╗   ██║    
██╔══██╗██╔══╝  ██╔══╝  ╚════██║   ██║    
██████╔╝███████╗███████╗███████║   ██║    
╚═════╝ ╚══════╝╚══════╝╚══════╝   ╚═╝    

A swiss army knife for the Swarm ecosystem
```


Beest is a TUI app to install, run and manage multiple bee nodes. It also integrates with other developer tools in the Swarm ecosystem:

- https://github.com/ethersphere/etherproxy
- https://github.com/ethersphere/bee-factory
- https://github.com/fairDataSociety/fdp-play
- https://github.com/ethersphere/swarm-cli

## Running Beest

```
git clone https://github.com/rampall/beest.git
cd beest
pip install textual pupdb
python3 ./beest.py
```

## Screenshots
![image](https://github.com/rampall/beest/assets/520570/91b3c788-bfa6-4000-9c8a-ba5de203a8e7)
![image](https://github.com/rampall/beest/assets/520570/03b8a140-c603-44be-917d-40961c97702e)
![image](https://github.com/rampall/beest/assets/520570/42239999-d72a-463c-b793-0cb124027461)
![image](https://github.com/rampall/beest/assets/520570/fec70fd9-ffc4-4a43-92a3-ef2fe36a74f6)

## Features

- [x] Install multiple bee versions
- [x] Install PM2 + Swarm-CLI
- [x] Install etherproxy
- [x] Install Bee Factory
- [x] Install FDP Play
- [x] Run bee in Ultralight mode
- [x] Stop all bees
- [ ] Remove all bees (Backup and Soft Delete)
- [ ] Run Etherproxy
- [ ] Funding wallet + Automatic funding of full nodes
- [ ] Monitor Bees
- [ ] Run Gateway

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

Beest is a TUI app to install, run and manage multiple bee nodes. It also integrates with other tools in the Swarm ecosystem:

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

![image](https://github.com/rampall/beest/assets/520570/72bbe3ef-67e3-46a3-a107-46f7c5e9bbfa)
![image](https://github.com/rampall/beest/assets/520570/afcb7d5e-66de-43d2-94bf-29ee7490fea3)
![image](https://github.com/rampall/beest/assets/520570/aa18e06d-74fb-4246-885d-2cb7d3625794)

## Features

- [x] Install multiple bee versions
- [x] Install PM2 + Swarm-CLI
- [x] Install etherproxy
- [x] Install Bee Factory
- [x] Install FDP Play
- [x] Run bee in Ultralight, Light & Full mode
- [x] Stop all bees
- [x] Remove all bees
- [ ] Run Etherproxy
- [ ] Funding wallet + Automatic funding of full nodes
- [ ] Monitor Bees
- [ ] Run Gateway

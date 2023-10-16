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

## Screenshots

![image](https://github.com/rampall/beest/assets/520570/0f48e819-864e-485f-a8d2-754393cd5692)
![image](https://github.com/rampall/beest/assets/520570/16d1d3a4-6a54-4059-b480-a46af6da6a03)
![image](https://github.com/rampall/beest/assets/520570/e048c266-305f-4d29-9e13-6cbcab649cb2)

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

## Development

```
git clone https://github.com/rampall/beest.git
cd beest
pip install textual pupdb
python3 ./beest.py
```

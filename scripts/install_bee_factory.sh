#!/usr/bin/env bash
# packages=(etherproxy @ethersphere/swarm-cli @ethersphere/bee-factory @fairdatasociety/fdp-cli )
packages=(@ethersphere/bee-factory)

for package in "${packages[@]}"; do
      echo ""
      echo "[cyan]INSTALL $package:[/cyan]"
      echo ""
        # installed_version=$(npm list -g "$package" | grep -oP '(?<=@).*')
        # if [[ -z "$installed_version" ]]; then
            echo "Installing $package..."
            npm i --no-audit --no-fund -g "$package"
        # else
            installed_version=$(npm list -g "$package" | grep -oP '(?<=@).*')
            echo "$package is installed (version: $installed_version)"
        # fi
done
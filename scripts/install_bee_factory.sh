#!/usr/bin/env bash

packages=(@ethersphere/bee-factory)

for package in "${packages[@]}"; do
    echo ""
    echo "[cyan]INSTALL $package:[/cyan]"
    echo ""

    installed_version=$(npm list -g "$package" | grep -oP '(?<=@)[^@]*$')
    latest_version=$(npm show "$package" version)
    echo "[orange1]LATEST VERSION:[/orange1] $latest_version"
    echo "[orange1]INSTALLED VERSION:[/orange1] $installed_version"

    if [[ -z "$installed_version" ]]; then
        echo "Installing $package..."
        npm i --no-audit --no-fund -g "$package"
    elif [[ "$installed_version" != "$latest_version" ]]; then
        echo "Updating $package..."
        npm update -g "$package"
    else
        echo "$package is already installed (version: $installed_version)"
    fi
done
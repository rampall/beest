packages="etherproxy @ethersphere/swarm-cli @ethersphere/bee-factory @fairdatasociety/fdp-play"
echo "[cyan]INSTALLED:[/cyan]"
echo ""
npm list --depth=0 -g $packages
echo $installed
echo ""
echo "[cyan]OUTDATED:[/cyan]"
echo ""
outdated=$(npm outdated -g $packages)
if [[ -z "$installed_version" ]]; then
    echo "None"
else
    echo $outdated
fi

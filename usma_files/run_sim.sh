#!/bin/bash
cd
multi-sitl-start.bash -B -LRange11 -vArduCopter 1
fti.py -d sitl_bridge_1 -z &
gnome-terminal -e "bash -c 'echo network device sitl_bridge_1 | swarm_commander.py;$SHELL'"
~/usma_swarm/usma_files/serverSide/runServerSide.sh

#!/bin/bash
# Identify which shell is configured in execs.conf
EXECS="/home/linuxoed/.config/hypr/hyprland/execs.conf"

/home/linuxoed/Документы/scripts/kill_shell.sh

if grep -q "^exec-once = dms run" "$EXECS"; then
    dms run &
elif grep -q "^exec-once = quickshell -c noctalia-shell" "$EXECS"; then
    quickshell -c noctalia-shell &
fi

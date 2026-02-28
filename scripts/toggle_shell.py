#!/usr/bin/env python3
import sys
from pathlib import Path
import subprocess
import re

HOME = Path.home()
HYPR_DIR = HOME / ".config/hypr"
EXECS = HYPR_DIR / "hyprland/execs.conf"
KEYBINDS = HYPR_DIR / "hyprland/keybinds.conf"
VARS = HYPR_DIR / "variables.conf"
HYPR_CONF = HYPR_DIR / "hyprland.conf"

def toggle_block(path, start_marker, end_marker, enable):
    if not path.exists(): return
    content = path.read_text()
    pattern = re.compile(f"({re.escape(start_marker)}).*?({re.escape(end_marker)})", re.DOTALL)
    
    def replace_func(match):
        block_content = match.group(0)
        lines = block_content.splitlines()
        new_lines = []
        for i, line in enumerate(lines):
            if i == 0 or i == len(lines)-1: # Markers
                new_lines.append(line)
                continue
            
            if enable:
                # Uncomment
                if line.strip().startswith("#"):
                    new_lines.append(re.sub(r'^(\s*)#\s?', r'\1', line))
                else:
                    new_lines.append(line)
            else:
                # Comment
                if line.strip() and not line.strip().startswith("#"):
                    indent = re.match(r'^(\s*)', line).group(1)
                    new_lines.append(f"{indent}# {line.lstrip()}")
                else:
                    new_lines.append(line)
        return "\n".join(new_lines)

    new_content = pattern.sub(replace_func, content)
    path.write_text(new_content)

def main():
    if not EXECS.exists(): return
    content = EXECS.read_text()
    is_dms = any(line.strip() == "exec-once = dms run" for line in content.splitlines())

    if is_dms:
        print("Switching to Noctalia...")
        content = content.replace("exec-once = dms run", "# exec-once = dms run")
        content = content.replace("# exec-once = quickshell -c noctalia-shell", "exec-once = quickshell -c noctalia-shell")
        EXECS.write_text(content)
        
        toggle_block(KEYBINDS, "# [NOCTALIA_KB_START]", "# [NOCTALIA_KB_END]", True)
        toggle_block(KEYBINDS, "# [DMS_KB_START]", "# [DMS_KB_END]", False)
        
        toggle_block(VARS, "# [NOCTALIA_START]", "# [NOCTALIA_END]", True)
        toggle_block(VARS, "# [DMS_START]", "# [DMS_END]", False)
        
        hc = HYPR_CONF.read_text()
        hc = hc.replace("# source = /home/linuxoed/.config/hypr/noctalia/noctalia-colors.conf", "source = /home/linuxoed/.config/hypr/noctalia/noctalia-colors.conf")
        hc = hc.replace("source = /home/linuxoed/.config/hypr/dms/colors.conf", "# source = /home/linuxoed/.config/hypr/dms/colors.conf")
        HYPR_CONF.write_text(hc)
    else:
        print("Switching to DMS...")
        content = content.replace("exec-once = quickshell -c noctalia-shell", "# exec-once = quickshell -c noctalia-shell")
        content = content.replace("# exec-once = dms run", "exec-once = dms run")
        EXECS.write_text(content)

        toggle_block(KEYBINDS, "# [NOCTALIA_KB_START]", "# [NOCTALIA_KB_END]", False)
        toggle_block(KEYBINDS, "# [DMS_KB_START]", "# [DMS_KB_END]", True)

        toggle_block(VARS, "# [NOCTALIA_START]", "# [NOCTALIA_END]", False)
        toggle_block(VARS, "# [DMS_START]", "# [DMS_END]", True)

        hc = HYPR_CONF.read_text()
        hc = hc.replace("source = /home/linuxoed/.config/hypr/noctalia/noctalia-colors.conf", "# source = /home/linuxoed/.config/hypr/noctalia/noctalia-colors.conf")
        hc = hc.replace("# source = /home/linuxoed/.config/hypr/dms/colors.conf", "source = /home/linuxoed/.config/hypr/dms/colors.conf")
        HYPR_CONF.write_text(hc)

    subprocess.run(["/home/linuxoed/Документы/scripts/restart_shell.sh"])
    subprocess.run(["hyprctl", "reload"])
    subprocess.run(["notify-send", "Shell Switcher", "Configuration Updated"])

if __name__ == "__main__":
    main()

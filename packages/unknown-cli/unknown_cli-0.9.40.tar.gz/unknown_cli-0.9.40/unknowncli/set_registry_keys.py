"""
sets the s:/ subst command in registry, elevates access if needed.
Include the full value in quotes when calling this script. e.g. `set_registry_keys.py "subst S: [full path]"`
"""
import pyuac, winreg, sys
from os import getcwd

handler_name = "sn2"
key = f"{handler_name}\\shell\\open\\command"

@pyuac.main_requires_admin
def main(subst_cmd):
    try:
        run_key = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
        h = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, run_key)
        winreg.SetValueEx(h, "Perforce Work Drive", 0, winreg.REG_SZ, subst_cmd)

    except PermissionError as e:
        print(f"Unable to set subst command. Please open up your shell as Administrator (through shift-right click menu) and run this command again ({str(e)})")

if __name__ == "__main__":
    main(sys.argv[1])
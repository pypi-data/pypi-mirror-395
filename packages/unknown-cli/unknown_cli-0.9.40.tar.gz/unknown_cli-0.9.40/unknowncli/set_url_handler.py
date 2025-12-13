"""
sets the sn2:// url handler in registry, elevates access if needed.
Include the full path to the unk.exe executable when calling this script
"""
import pyuac, winreg, sys
from os import getcwd

handler_name = "sn2"
key = f"{handler_name}\\shell\\open\\command"

@pyuac.main_requires_admin
def main(exe):
    try:
        try:
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, handler_name)
        except:
            pass
        h = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, handler_name)
        winreg.SetValueEx(h, "URL Protocol", 0, winreg.REG_SZ, "")
        h = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key)
        cmd = f"{exe} unreal asset \"%1\""
        winreg.SetValueEx(h, "", 0, winreg.REG_SZ, cmd)
    except PermissionError as e:
        print(f"Unable to set url handler for sn2://. Please open up your shell as Administrator (through shift-right click menu) and run this command again ({str(e)})")

if __name__ == "__main__":
    main(sys.argv[1])
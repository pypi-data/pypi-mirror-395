import sys
import os
import json
import usb.core
from .core import FastbootProtocol

def output_json(success, message):
    if success:
        print(json.dumps({"success": message}))
    else:
        print(json.dumps({"error": message}))

def main():
    if len(sys.argv) < 2:
        output_json(False, "No arguments provided")
        sys.exit(1)

    args = sys.argv[1:]
    
    device = None
    if "USB_FD" in os.environ:
        device = usb.core.find(find_all=True, custom_match=lambda d: True)

    fb = FastbootProtocol(device)
    
    if not fb.connect():
        sys.exit(10)

    success = False
    result = ""

    try:
        cmd_type = args[0]

        if cmd_type == "product":
            success, result = fb.cmd("getvar:product")
            if success: 
                result = result.replace("product:", "").strip()

        elif cmd_type == "token":
            success_getvar, result_getvar = fb.cmd("getvar:token")
            if success_getvar:
                token = result_getvar.replace("token:", "").strip()
                result = {"model": "qualcomm", "token": token}
                success = True
            else:
                success_oem, result_oem = fb.cmd("oem get_token")
                if success_oem:
                    result = {"model": "mtk", "token": result_oem.strip()}
                    success = True
                else:
                    success = False
                    result = "Failed to get token"

        elif cmd_type == "unlock" and len(args) > 1:
            file_path = args[1]
            
            success_stage, result_stage = fb.stage(file_path)
            if not success_stage:
                success = False
                result = f"Failed to stage file: {result_stage}"
            else:
                success_unlock, result_unlock = fb.cmd("oem unlock")
                if success_unlock:
                    success = True
                    result = "unlock succeed"
                else:
                    success = False
                    result = f"Failed to unlock: {result_unlock}"

        else:
            success = False
            result = "Invalid command syntax"

    except Exception as e:
        success = False
        result = str(e)

    output_json(success, result)
    sys.exit(0)

if __name__ == "__main__":
    main()
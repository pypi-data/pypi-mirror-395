import usb.core
import usb.util
import os
import struct

VIDS = [0x18d1, 0x2717]
CLASS, SUBCLASS, PROTO = 0xff, 0x42, 0x03

class FastbootProtocol:
    def __init__(self, device=None):
        self.dev = device
        self.ep_in = None
        self.ep_out = None

    def connect(self):
        if not self.dev:
            self.dev = usb.core.find(find_all=True, custom_match=lambda d: d.idVendor in VIDS)
            if hasattr(self.dev, '__next__'):
                self.dev = next(self.dev, None)
            elif isinstance(self.dev, list) and self.dev:
                self.dev = self.dev[0]

        if not self.dev: return False

        try:
            if self.dev.is_kernel_driver_active(0):
                self.dev.detach_kernel_driver(0)
        except: pass

        try: self.dev.set_configuration()
        except: pass

        cfg = self.dev.get_active_configuration()
        intf = None
        for i in cfg:
            if i.bInterfaceClass == CLASS and i.bInterfaceSubClass == SUBCLASS and i.bInterfaceProtocol == PROTO:
                intf = i
                break
        
        if not intf: intf = cfg[(0,0)]

        for ep in intf:
            if usb.util.endpoint_direction(ep.bEndpointAddress) == usb.util.ENDPOINT_IN: self.ep_in = ep
            else: self.ep_out = ep
            
        return self.ep_in is not None and self.ep_out is not None

    def cmd(self, command):
        try:
            self.dev.write(self.ep_out, command.encode())
            resp_full = []
            while True:
                res = self.dev.read(self.ep_in, 1024, timeout=5000).tobytes().decode(errors='ignore')
                tag = res[:4]
                val = res[4:]
                if tag == "INFO": resp_full.append(val)
                elif tag == "OKAY": 
                    resp_full.append(val)
                    return True, "".join(resp_full)
                elif tag == "FAIL": return False, val
        except Exception as e:
            return False, str(e)

    def stage(self, path):
        if not os.path.exists(path): return False, "File not found"
        size = os.path.getsize(path)
        
        try:
            self.dev.write(self.ep_out, f"download:{size:08x}".encode())
            res = self.dev.read(self.ep_in, 64).tobytes().decode()
            if not res.startswith("DATA"): return False, f"Unexpected response: {res}"

            with open(path, 'rb') as f:
                while True:
                    chunk = f.read(16384)
                    if not chunk: break
                    self.dev.write(self.ep_out, chunk)
            
            res = self.dev.read(self.ep_in, 64).tobytes().decode()
            if "OKAY" in res: return True, "File staged successfully"
            return False, res
        except Exception as e:
            return False, str(e)
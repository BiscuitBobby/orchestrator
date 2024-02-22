import re
import subprocess

def peripherals():
    device_re = re.compile(b"Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
    df = subprocess.check_output("lsusb")
    devices = []
    for i in df.split(b'\n'):
        if i:
            info = device_re.match(i)
            if info:
                info = info.groupdict()
                for j in info:
                    info[j] = info[j].decode("utf-8")
                info['device'] = '/dev/bus/usb/%s/%s' % (info.pop('bus'), info.pop('device'))
                devices.append(info)

    return devices

for i in (peripherals()):
    print(i)

import serial


def main():
    try:
        from serial.tools.list_ports import comports
    except ImportError:
        return None
    if comports:
        for port in comports():

            # It's a USB port on a platform that supports the extended info
            # Do something with it.
            print("Port={},VID={:#06x},PID={:#06x}".format(
                port.device, port.vid, port.pid))


if __name__ == "__main__":
    main()

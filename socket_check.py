import socket
from time import time, sleep


def socket_check(ip, port=22, socket_timeout=1, scan_timeout=400, retry=1):
    '''
    Socket Check

    This function will continually check an ip and port to see if it is
    responding.

    Args:
        ip(str): IP of the device
        port(int): Port to check. Default to 22.
        socket_timeout(int): Amount of time in seconds to wait for socket
                             to respond.
        scan_timeout(int): Amount of time in seconds to scan the device.
        retry(int): Amount of time in seconds to wait before trying to
                    scan the device again.
    Returns:
        Boolean. True if port becomes responsive during the scan_timeout.
                 False is scan_timeout is reached and device is still
                   unresponsive.

    Outputs:
        None
    '''
    end_time = time() + scan_timeout
    while end_time > time():
        try:
            a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            a_socket.settimeout(socket_timeout)
            a_socket.connect((ip, port))
            return True
        except ConnectionRefusedError:
            print(f"{ip}:{port} not open..sleep for {retry} seconds")
            sleep(retry)
        finally:
            a_socket.close()
    return False


def main():
    ip = '127.0.0.1'
    port = 9000
    response = socket_check(ip, port, scan_timeout=10)
    if response:
        print(f"{ip}:{port} is responsive")
    else:
        print(f"{ip}:{port} is unresponsive")


if __name__ == "__main__":
    main()

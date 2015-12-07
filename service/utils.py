import socket


def get_ip_address():
    """
    Returns IP4 address of host.

    :return: str
    """
    return socket.gethostbyname(socket.gethostname())


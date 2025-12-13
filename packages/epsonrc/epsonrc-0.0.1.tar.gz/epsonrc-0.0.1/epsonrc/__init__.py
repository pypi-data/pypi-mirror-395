from .commands import connect, send, command, go, move, go_here, move_here, begin

__all__ = ['connect','send','command','go','move','go_here','move_here','begin']

def __version__():
    return "0.0.1"

def describe():
    description = (
        "EPSON RC Library for Python\n"
        "Version: {}\n"
        "Allows the control of every EPSONRC+ robot controller connected by Ethernet Remote. The existing commands are:\n"
        "  - connect\n"
        "  - send\n"
        "  - command\n"
        "  - go\n"
        "  - move"
        "  - go_here\n"
        "  - move_here\n"
        "  - begin\n"
    ).format(__version__())
    print(description)
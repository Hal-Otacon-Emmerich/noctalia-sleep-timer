"""Pointer layer for the sleep timer dial.

Noctalia only reports press / drag / release / wheel to a plugin through ui.pixelStream,
and a pixel stream needs a companion process that serves frames over a Unix socket.
This companion serves a single fully transparent 1x1 frame, so the dial image under
the stream stays visible and the panel script gets the pointer events.

Usage: python3 companion.py <socket path>
Exits a few seconds after Noctalia stops connecting (the panel was closed).
Protocol: docs/user/plugins/development/declarative-ui.mdx, "Companion protocol".
"""

import fcntl
import os
import socket
import struct
import sys

IDLE_EXIT_SECONDS = 5


def transparent_buffer():
    fd = os.memfd_create("sleep-timer-dial", os.MFD_ALLOW_SEALING)
    os.write(fd, b"\0\0\0\0")  # one RGBA pixel, alpha 0
    fcntl.fcntl(fd, fcntl.F_ADD_SEALS, fcntl.F_SEAL_SHRINK)
    return fd


def already_running(path):
    probe = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)
    try:
        probe.connect(path)
        return True
    except OSError:
        return False
    finally:
        probe.close()


def serve(conn, buffer_fd):
    sent = False
    while True:
        msg = conn.recv(64)
        if len(msg) < 8:
            return  # closed, or a probe from a second companion
        kind, value = struct.unpack_from("<II", msg)
        if kind == 1 and value != 1:
            return  # HELLO with a protocol version we do not speak
        # The frame never changes, so only the first REQUEST of a connection gets one
        if kind == 2 and not sent:
            socket.send_fds(conn, [struct.pack("<IIII", 1, 0, 1, 1)], [buffer_fd])
            conn.send(struct.pack("<II", 2, 0))
            sent = True


def main():
    path = sys.argv[1]
    if already_running(path):
        return
    try:
        os.unlink(path)
    except FileNotFoundError:
        pass

    server = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)
    server.bind(path)
    os.chmod(path, 0o600)
    server.listen(2)
    server.settimeout(IDLE_EXIT_SECONDS)
    buffer_fd = transparent_buffer()
    try:
        while True:
            try:
                conn, _ = server.accept()
            except socket.timeout:
                return
            with conn:
                conn.settimeout(None)
                try:
                    serve(conn, buffer_fd)
                except OSError:
                    pass
    finally:
        server.close()
        try:
            os.unlink(path)
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    main()

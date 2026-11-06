#!/usr/bin/env python3
"""Check, from the server machine, that the community master is reachable and lists this server.

    python3 check-master.py [--master 51.68.190.110] [--port 7779] [--settings path/to/ServerSettings.ini]

--port is the listed port: your game port + 2. Exit code 0 when everything checked passes.
"""
import argparse, os, socket, struct, sys


def recv_all(s, limit=4 << 20):
    data = b''
    while len(data) < limit:
        chunk = s.recv(65536)
        if not chunk:
            break
        data += chunk
    return data


def request(host, port, payload):
    with socket.create_connection((host, port), timeout=8) as s:
        s.sendall(payload)
        s.shutdown(socket.SHUT_WR)
        return recv_all(s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--master', default='51.68.190.110')
    ap.add_argument('--port', type=int, default=7779, help='listed port (game port + 2)')
    ap.add_argument('--settings', default='SCUM/Saved/Config/WindowsServer/ServerSettings.ini')
    a = ap.parse_args()
    ok = True

    def report(name, good, detail=''):
        nonlocal ok
        ok &= good
        print('%-34s %s %s' % (name, 'OK  ' if good else 'FAIL', detail))

    if os.path.exists(a.settings):
        text = open(a.settings, encoding='utf-8', errors='replace').read()
        want = 'Endpoint=%s:31337' % a.master
        report('ServerSettings.ini points here', '[SCUM.MasterServer]' in text and want in text,
               '' if want in text else '(add [SCUM.MasterServer] Endpoint=%s:31337)' % a.master)
    else:
        print('%-34s skip (no %s; run from the server root or pass --settings)' % ('ServerSettings.ini', a.settings))

    try:
        bans = request(a.master, 31330, b'\x02\x05')
        report('ban list port 31330', len(bans) >= 2, '%d entries' % struct.unpack_from('<H', bans)[0] if len(bans) >= 2 else '')
    except OSError as e:
        report('ban list port 31330', False, str(e))

    listed = None
    try:
        data = request(a.master, 31337, b'\x02\x03\x00\x00')
        n = struct.unpack_from('<H', data)[0] if len(data) >= 2 else 0
        report('server list port 31337', len(data) >= 2, '%d servers listed' % n)
        for i in range(n):
            rec = data[2 + 127 * i: 2 + 127 * (i + 1)]
            if len(rec) == 127 and struct.unpack_from('<H', rec, 4)[0] == a.port:
                ip = socket.inet_ntoa(struct.pack('>I', struct.unpack_from('<I', rec)[0]))
                name = rec[6:107].split(b'\0')[0].decode('utf-8', 'replace')
                listed = (ip, name, rec[107], rec[108])
    except OSError as e:
        report('server list port 31337', False, str(e))

    if listed:
        report('this server is listed', True, '%s:%d "%s" %d/%d players' % (listed[0], a.port, listed[1], listed[2], listed[3]))
    else:
        report('this server is listed', False, '(no server with port %d; is it running and enrolled?)' % a.port)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())

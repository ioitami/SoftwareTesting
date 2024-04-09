
import signal
import sys
import os
import afl

def main(s):
    if not s:
        print('Hum?')
        sys.exit(1)
    s.encode('ASCII')
    if s[0] == '0':
        print('Looks like a zero to me!')
    else:
        print('A non-zero value? How quaint!')

if __name__ == '__main__':
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)  # this should have no effect on the forkserver
    afl.init()
    s = sys.stdin.read()
    main(s)
    os._exit(0)

# vim:ts=4 sts=4 sw=4 et

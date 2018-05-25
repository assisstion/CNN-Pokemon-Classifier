import os, sys

def stop_server(num):
    import signal
    os.kill(num, signal.SIGKILL)

if __name__ == '__main__':
    port = 8080
    if len(sys.argv) >= 2:
        port = sys.argv[1]
    num = os.fork()
    if num == 0:
        import server
        t = server.MultiWebApp(port)
        t.run()
    else:
        import client
        import atexit
        atexit.register(stop_server, num)
        client.start_client('127.0.0.1', port, True)
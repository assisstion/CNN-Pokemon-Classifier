import os

def stop_server(num):
    import signal
    os.kill(num, signal.SIGKILL)

if __name__ == '__main__':
    num = os.fork()
    if num == 0:
        import server
        t = server.MultiWebApp()
        t.run()
    else:
        import client
        import atexit
        atexit.register(stop_server, num)
        client.start_client('127.0.0.1', 8080, True)
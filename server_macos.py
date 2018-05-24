import os

if __name__ == '__main__':
    if os.fork() == 0:
        import server
        server.start_child()
    else:
        import client
        client.start_client('127.0.0.1', 8080, True)
   

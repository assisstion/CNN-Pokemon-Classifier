from socketIO_client import SocketIO, BaseNamespace
import multi
import threading
import sys
import guidata
import asyncio

class Namespace(BaseNamespace):

    #Pass in a multiclient
    def bind(self, pd):
        self.pd = pd

    def on_connect(self):
        print('[Connected]')

    def on_reconnect(self):
        print('[Reconnected]')

    def on_disconnect(self):
        print('[Disconnected]')

    def on_reply(self, *args):
        print('reply', args)

    def on_request_response(self, *args):
        print('on_request_response', args)
        self.pd.net.round_num = args[0]
        last_item = (args[1], args[2])
        self.pd.net.last_item = last_item
        multi.push_event('set_timer', [args[3]])
        multi.push_event('set_pokemon', last_item)
        multi.push_event('labels')
        #GUI.set_pokemon(args[0], args[1])
        #GUI.labels()

    def on_update_score(self, *args):
        print('on_update_score', args)
        scores = args[0]
        multi.push_event('set_scores', [scores])


class MultiClient(threading.Thread):
    def __init__(self, pd, host, port, local_server):
        threading.Thread.__init__(self)
        self.pd = pd
        self.pd.hook = self
        self.host = host
        self.port = port
        self.local_server = local_server

    def run(self):
        print("client started")

        socketIO = SocketIO('http://' + str(self.host), self.port)
        chat_namespace = socketIO.define(Namespace, '/chat')
        chat_namespace.bind(self.pd)
        socketIO.on('reply', chat_namespace.on_reply)
        socketIO.on('request_item', chat_namespace.on_request_response)
        socketIO.on('update_score', chat_namespace.on_update_score)
        if self.local_server:
            chat_namespace.emit('game_start', None)
            #socketIO.wait(seconds=1)
        #chat_namespace.emit('request_item', None)
        #socketIO.wait(seconds=1)

        while True:
            chat_namespace.emit('chat message', "helloworld")
            #s = input('Send message: ')
            #chat_namespace.emit("chat message", s)
            #socketIO.wait(seconds=0.1)
            while self.pd.net.queue.empty():
                socketIO.wait(seconds=0.1)
            event = self.pd.net.queue.get()
            #chat_namespace.emit('request_item', self.pd.net.last_item)
            chat_namespace.emit('submit_answer', event)

class MultiGUI(threading.Thread):
    def __init__(self, local_server, loop):
        threading.Thread.__init__(self)
        self.local_server = local_server
        self.loop = loop

    def run(self):
        import GUI
        GUI.gui()
        if self.local_server:
            print("start cd loop")
            guidata.pd.window.after(100, self.start_cd_loop(self.loop))
        guidata.pd.window.mainloop()

    def start_cd_loop(self, loop):  
        t = threading.Thread(target=self.await_cd_loop, args=(loop,))
        t.daemon = True
        t.start()

    def await_cd_loop(self, async_loop):
        #import server
        #loop = asyncio.new_event_loop()
        #asyncio.set_event_loop(loop)
        #asyncio.ensure_future(server.db.countdown_loop())
        #loop.run_forever()
        #async_loop.run_until_complete(server.db.countdown_loop())
        pass

def start_client(host, port, local_server):
    guidata.pd.multi = True
    #guidata.setup()
    t = MultiClient(guidata.pd, host, port, local_server)
    t.daemon = True
    t.start()
    loop = asyncio.get_event_loop()
    t2 = MultiGUI(local_server, loop)
    #t2.daemon = True
    #t2.start()
    t2.run()

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080
    if len(sys.argv) >= 2:
        host = sys.argv[1]
    if len(sys.argv) >= 3:
        port = int(sys.argv[2])
    loop = asyncio.get_event_loop()
    start_client(host, port, False, loop)

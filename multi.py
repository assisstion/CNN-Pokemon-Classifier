import events
import guidata
from queue import Queue
import asyncio
from aiohttp.web import *

def start_event_queue():
    guidata.pd.net.event_queue = Queue()
    event_queue()

def event_queue():
    events.tick_update()
    process_event()
    guidata.pd.window.after(100, event_queue)

def process_event():
    while not guidata.pd.net.event_queue.empty():
        event = guidata.pd.net.event_queue.get()
        method = getattr(events, event.name)
        method(*event.args)

class GUIEvent:
    def __init__(self, name, args):
        self.name = name
        self.args = args

def push_event(name, args=[]):
    guidata.pd.net.event_queue.put(GUIEvent(name, args))


#Adapted from https://github.com/aio-libs/aiohttp/blob/master/aiohttp/web.py
def run_app(app, loop, *, host=None, port=None, path=None, sock=None,
            shutdown_timeout=60.0, ssl_context=None,
            print=print, backlog=128,
            reuse_address=None, reuse_port=None):
    """Run an app locally"""
    if asyncio.iscoroutine(app):
        app = loop.run_until_complete(app)

    runner = AppRunner(app)

    loop.run_until_complete(runner.setup())

    sites = []

    try:
        if host is not None:
            if isinstance(host, (str, bytes, bytearray, memoryview)):
                sites.append(TCPSite(runner, host, port,
                                     shutdown_timeout=shutdown_timeout,
                                     ssl_context=ssl_context,
                                     backlog=backlog,
                                     reuse_address=reuse_address,
                                     reuse_port=reuse_port))
            else:
                for h in host:
                    sites.append(TCPSite(runner, h, port,
                                         shutdown_timeout=shutdown_timeout,
                                         ssl_context=ssl_context,
                                         backlog=backlog,
                                         reuse_address=reuse_address,
                                         reuse_port=reuse_port))
        elif path is None and sock is None or port is not None:
            sites.append(TCPSite(runner, port=port,
                                 shutdown_timeout=shutdown_timeout,
                                 ssl_context=ssl_context, backlog=backlog,
                                 reuse_address=reuse_address,
                                 reuse_port=reuse_port))

        if path is not None:
            if isinstance(path, (str, bytes, bytearray, memoryview)):
                sites.append(UnixSite(runner, path,
                                      shutdown_timeout=shutdown_timeout,
                                      ssl_context=ssl_context,
                                      backlog=backlog))
            else:
                for p in path:
                    sites.append(UnixSite(runner, p,
                                          shutdown_timeout=shutdown_timeout,
                                          ssl_context=ssl_context,
                                          backlog=backlog))

        if sock is not None:
            if not isinstance(sock, Iterable):
                sites.append(SockSite(runner, sock,
                                      shutdown_timeout=shutdown_timeout,
                                      ssl_context=ssl_context,
                                      backlog=backlog))
            else:
                for s in sock:
                    sites.append(SockSite(runner, s,
                                          shutdown_timeout=shutdown_timeout,
                                          ssl_context=ssl_context,
                                          backlog=backlog))
        for site in sites:
            print("starting")
            loop.run_until_complete(site.start())
            loop.run_forever()
        #try:
        #    if print:  # pragma: no branch
        #        names = sorted(str(s.name) for s in runner.sites)
        #        print("======== Running on {} ========\n"
        #              "(Press CTRL+C to quit)".format(', '.join(names)))
        #    loop.run_forever()
        #except (GracefulExit, KeyboardInterrupt):  # pragma: no cover
        #    pass
    finally:
        pass
    #    loop.run_until_complete(runner.cleanup())
    #if hasattr(loop, 'shutdown_asyncgens'):
    #    loop.run_until_complete(loop.shutdown_asyncgens())
    #loop.close()
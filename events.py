import GUI
import time
import server
import asyncio

def current_time():
    return int(round(time.time() * 1000))

def tick_update():
    if hasattr(GUI.pd.net, 'end_time'):
        time_diff = GUI.pd.net.end_time - current_time()
        if time_diff < 0:
            time_diff = 0
        GUI.pd.net.time_txt.set(int(time_diff / 100) / 10)

def set_timer(millis):
    time = current_time()
    GUI.pd.net.start_time = time
    GUI.pd.net.end_time = time + millis

def labels():
    GUI.labels()

def set_pokemon(file_name, img):
    GUI.set_pokemon(file_name, img)

def set_scores(scores):
    print("update score")
    GUI.pd.player_counter.configure(text="Player score: " + str(scores["self"]))
    GUI.pd.AI_counter.configure(text="Opponent score: " + str(scores["high"]))


def emit_room(name, item, room_id):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(emit_async(name, item, room_id))

def emit(name, item):
    emit_room(name, item, None)

async def emit_async(name, item, room_id):
    print("emit async", name, item, room_id)
    if room_id is None:
        await server.sio.emit(name, item)
    else:
        await server.sio.emit(name, item, room=room_id)

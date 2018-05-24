import os, random
from queue import Queue

class GUIData:
    #Attrs:
    #pd.AI_answer
    #pd.AI_counter
    #pd.classifier
    #pd.name_txt
    #pd.player_counter
    #pd.pokemon_id
    #pd.prediction
    #pd.test_set
    #pd.type_labels
    #pd.window
    #pd.multi
    #pd.net
    pass

class NetData:
    #pd.net.queue
    #pd.net.last_item
    pass

pd = GUIData()
pd.net = NetData()
pd.net.queue = Queue()

def random_sprite():
    path = "data/main-sprites/"

    game_vers = random.choice(os.listdir(path))
    while str(game_vers).endswith('.DS_Store'):
        game_vers = random.choice(os.listdir(path))
    img = random.choice(os.listdir(path + game_vers))
    while not str(img).endswith('png'):
        img = random.choice(os.listdir(path + game_vers))
    return (path + game_vers + '/' + img, img)
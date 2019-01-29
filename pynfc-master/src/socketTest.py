from socketIO_client import SocketIO, LoggingNamespace

socketIO = SocketIO('localhost', 3000, LoggingNamespace)

#socketIO = SocketIO('localhost', 3000)
#socketIO.emit('replaceAndPlay', {"uri":"live_playlists_random_50", "title":"50 random tracks", "service":"live_playlists"})


def mute():
    socketIO.emit('mute', '')
    socketIO.wait(seconds=1)

def on_push_state(*args):
    print('state', args)
    global status
    status = args[0]['status'].encode('ascii', 'ignore')
    print status

def getState():
     socketIO.on('pushState', on_push_state)
     #get initial state
     socketIO.emit('getState', '', on_push_state)

def random():
     print 'random'
     socketIO.emit('replaceAndPlay', {"uri":"live_playlists_random_50", "title":"50 random tracks", "service":"live_playlists"})

def on_search(*args):
    print('search',args)
    # how do I print out all the uri's which start with albums://


def search():
    print 'search'
    socketIO.on('pushBrowseLibrary', on_search)
    #socketIO.emit('search', {"value":'lion king'}, on_search);
    socketIO.emit('search', {"value":'trainor'}, on_search);

def replaceAndPlay():
    print 'replace and play'
    #socketIO.emit('replaceAndPlay', {"uri":"music-library/USB/Lexar/music/Mike Gibbens/Mike's Album/For You (Tracy Chapman).m4a"})
    #socketIO.emit('replaceAndPlay', {"uri":"albums://Various%20artists/The%20Lion%20King%3A%20Special%20Edition%20Original%20Soundtrack%20(English%20Version)"})
    socketIO.emit('replaceAndPlay', {"uri":"artists://Meghan%20Trainor"})

#mute()

# get initial state
#getState()

#random()

search()

replaceAndPlay()

try:
	socketIO.wait()
except KeyboardInterrupt:
	pass

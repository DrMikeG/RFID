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

#mute()

# get initial state
getState()

try:
	socketIO.wait()
except KeyboardInterrupt:
	pass

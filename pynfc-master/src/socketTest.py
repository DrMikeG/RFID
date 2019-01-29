from socketIO_client import SocketIO, LoggingNamespace

#socketIO = SocketIO('localhost', 3000)
#socketIO.emit('replaceAndPlay', {"uri":"live_playlists_random_50", "title":"50 random tracks", "service":"live_playlists"})


def mute():
    with SocketIO('localhost', 3000, LoggingNamespace) as socketIO:
        socketIO.emit('mute', '')
        socketIO.wait(seconds=1)
#   socketIO.on('pushState', on_push_state)

# get initial state
#socketIO.emit('getState', '', on_push_state)

#try:
#	socketIO.wait()
#except KeyboardInterrupt:
#	pass

mute()

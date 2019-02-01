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
    #socketIO.emit('replaceAndPlay', {"uri":"artists://Meghan%20Trainor"})
    #socketIO.emit('replaceAndPlay', {"uri":"albums:///My%20Universe"})
    #socketIO.emit('replaceAndPlay', {"uri":"albums://Various%20artists/BBC%20Radio%202%3A%20Sounds%20of%20the%2080s"})
	#socketIO.emit('replaceAndPlay', {"uri":"albums://Kacey%20Musgraves/Same%20Trailer%20Different%20Park"})
	#socketIO.emit('replaceAndPlay', {"uri":"albums://Various%20Artists/Keep%20Calm%20And%20Stay%20Cosy"})
	#socketIO.emit('replaceAndPlay', {"uri":"albums:///This%20House%20Is%20Not%20For%20Sale"})
	#socketIO.emit('replaceAndPlay', {"uri":"albums:///Jupiter%20Calling"})
    #socketIO.emit('replaceAndPlay', {"uri":"albums://Queen//Platinum%20Collection"})
	#socketIO.emit('replaceAndPlay', {"uri":"albums://Barenaked%20Ladies/Disc%20One%3A%20%20All%20Their%20Greatest%20Hits%201991-2001"})
	#socketIO.emit('replaceAndPlay', {"uri":"albums:///Swing%20When%20You're%20Winning"})
	#socketIO.emit('replaceAndPlay', {"uri":"albums://Various%20Artists/100%20Rock%20n%20Roll%20Hits%20%26%20Jukebox%20Classics%20-%20The%20Very%20Best%2050s%20%26%2060s%20Rock%20and%20Roll%20Collection%20from%20the%20Greatest%20Legends"})
    #socketIO.emit('replaceAndPlay', {"uri":"artists://Barenaked%20Ladies/Disc%20One%3A%20%20All%20Their%20Greatest%20Hits%201991-2001"})
#    socketIO.emit('replaceAndPlay', {"uri":"music-library/USB/Lexar/music/The Corrs/Jupiter Calling"})

def stop():
	print 'stop'
	socketIO.emit('stop',{});
#mute()

# get initial state
#getState()

#random()

#search()

replaceAndPlay()

#stop()

try:
	socketIO.wait()
except KeyboardInterrupt:
	pass

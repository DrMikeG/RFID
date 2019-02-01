import os
import sys
from socketIO_client import SocketIO, LoggingNamespace

socketIO = SocketIO('localhost', 3000, LoggingNamespace)

#socketIO = SocketIO('localhost', 3000)
#socketIO.emit('replaceAndPlay', {"uri":"live_playlists_random_50", "title":"50 random tracks", "service":"live_playlists"})


def on_search(args):
    print('search',args)
    # how do I print out all the uri's which start with albums://
    if 'navigation' in args:
    	result = args['navigation']
	if 'isSearchResult' in result and result['isSearchResult']:
		if 'lists' in result:
			list = result['lists']
			#print list
			#print type(list)
			#print len(list)
			for v in list:
				#print type(v)
				if 'items' in v:
					it = v['items']	
					for d in it:
						if 'uri' in d:
							print d['uri']
			
    

def search(args):
    print 'search'
    socketIO.on('pushBrowseLibrary', on_search)
    #socketIO.emit('search', {"value":'lion king'}, on_search);
    socketIO.emit('search', {"type":"album","value":args[1],"service":"mpd"}, on_search)

if __name__ == '__main__':
    search(sys.argv)

try:
	socketIO.wait()
except KeyboardInterrupt:
	pass

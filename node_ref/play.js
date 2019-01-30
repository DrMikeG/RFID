var io = require('socket.io-client');
var socket = io.connect('http://localhost:3000');
socket.emit('getState', '');
socket.on('pushState', function(data) {
  switch (data.status) {
    case 'play':
      socket.emit('pause');
      break;
    default:
      socket.emit('play');
      break;
  }
  socket.removeAllListeners('pushState');
  socket.on('pushState', function() { socket.disconnect(); } );
} );

setTimeout(function() { socket.disconnect(); }, 3000);
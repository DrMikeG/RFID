var RandomOrg = require('random-org');
var io = require('socket.io-client');
var random = new RandomOrg({'apiKey':'#########################'});
var socket = io.connect('http://localhost:3000');
socket.emit('browseLibrary', {'uri':'albums://'});
socket.on('pushBrowseLibrary',function(data) {
    var list = data.navigation.lists[0].items;
    random.generateIntegers({'min':0, 'max':list.length-1, 'n':1})
    .then(function(result) {
        select = list[result.random.data[0]];
        socket.emit('clearQueue');
        socket.emit('addToQueue', {'uri':select.uri});
    });
  }
);
socket.on('pushQueue', function(data) { if (data.length > 0) { socket.disconnect(); } } );

setTimeout(function() { socket.disconnect(); }, 5000);
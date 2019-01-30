var io = io('http://raspi1');

io.on('pushBrowseLibrary', function (data) {
var items = data.navigation.lists[0].items;
var albums = [];

items.forEach(function(entry) {
if (albums.indexOf(entry.title) === -1) {
albums.push(entry.title);
io.emit('addToPlaylist', {"name": entry.artist + ' - ' + entry.title, "service": entry.service, "uri": entry.uri});
}
});
alert(albums.length + ' playlists created')
});

io.on('pushState', function (data) {
console.log(data);
});

io.emit('browseLibrary', {'uri':'albums://'});
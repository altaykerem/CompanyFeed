var http = require('http'); 

var fs = require('fs'),
    path = require('path'),    
    filePath = path.join(__dirname, '/DBServer/index.html');

http.createServer(function (req, res) {
	fs.readFile(filePath, {encoding: 'utf-8'}, function(err,data){
	    if (!err) {
	        console.log('received data: ' + data);
	        res.writeHead(200, {'Content-Type': 'text/html'});
	        res.write(data);
	        res.end();
	    } else {
	        console.log(err);
	    }
	});
}).listen(5000);
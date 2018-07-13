var express = require('express')
var app = express()

app.use(express.static('DBServer'));

var server = app.listen(process.env.PORT || 5000, function () {

    var port = server.address().port

    console.log('Express app listening at port %s', port)

});
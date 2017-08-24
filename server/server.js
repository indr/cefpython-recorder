var express = require('express');
var path = require('path');
var serveStatic = require('serve-static');

app = express();
app.use(serveStatic(__dirname));

var port = process.env.PORT || 8082;
app.listen(port);

console.log('Server started ' + port);


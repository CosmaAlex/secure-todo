const express = require('express');
const fs = require('fs');
const path = require('path');
const https = require('https');
const morgan = require('morgan');
const bodyParser = require('body-parser');
const helmet = require('helmet');

const filename = "todo.txt";

const opts = {
	key: fs.readFileSync('certs/server_key.pem'),
	cert: fs.readFileSync('certs/server_cert.pem'),
	requestCert: true,
	rejectUnauthorized: false,
	ca: [ fs.readFileSync('certs/server_cert.pem') ]
}

const app = express();

app.use(helmet());
app.use(morgan('dev'));
app.use(bodyParser.raw({type: 'application/octet-stream', limit: '10mb'}));

app.get('/', (req, res) => { res.send('<a href="todos">Log in</a>');});

app.get('/todos', (req, res) => {
	const cert = req.connection.getPeerCertificate();
	if (req.client.authorized) {
		// absolute path to the file
    		let p = path.join(__dirname, filename);

		// Send the todos file
    		res.sendFile(p);
	} else if (cert.subject) {
		// Not accepted certificate
		res.status(403).send(`Sorry, no access`);
	} else {
		res.status(401).send(`Sorry, no access. Client certifcate required.`);
	}
});

app.post('/todos', (req, res) => {
	const cert = req.connection.getPeerCertificate();
	if (req.client.authorized) {
		// Update the TODO file
		try {
			var filePath = path.join(__dirname, filename)
			fs.open(filePath, 'w', function(err, fd) {  
				fs.write(fd, req.body, 0, req.body.length, null, function(err) {
					if (err) throw 'error writing file: ' + err;
					fs.close(fd, function() {
						console.log('wrote the file successfully');
						res.status(200).end();
					});
				});
			});
		} catch (err) {
			console.log('Error while writing to file ' + err);
			res.status(501).send('There has been a problem while writing to file');
		}
	} else if (cert.subject) {
		// Not accepted certificate
		res.status(403).send(`Sorry, no access`);
	} else {
		res.status(401).send(`Sorry, no access. Client certifcate required.`);
	}
});

https.createServer(opts, app).listen(9999);

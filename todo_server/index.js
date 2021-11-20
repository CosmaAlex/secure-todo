const express = require('express');
const fs = require('fs');
const path = require('path');
const https = require('https');

const opts = {
	key: fs.readFileSync('certs/server_key.pem'),
	cert: fs.readFileSync('certs/server_cert.pem'),
	requestCert: true,
	rejectUnauthorized: false,
	ca: [ fs.readFileSync('certs/server_cert.pem') ]
}

const app = express();

app.get('/', (req, res) => { res.send('<a href="todos">Log in</a>');});

app.get('/todos', (req, res) => {
	const cert = req.connection.getPeerCertificate();
	if (req.client.authorized) {
		// absolute path to the file
    		let p = path.join(__dirname, 'todo.txt');

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
	} else if (cert.subject) {
		// Not accepted certificate
		res.status(403).send(`Sorry, no access`);
	} else {
		res.status(401).send(`Sorry, no access. Client certifcate required.`);
	}
});

https.createServer(opts, app).listen(9999);

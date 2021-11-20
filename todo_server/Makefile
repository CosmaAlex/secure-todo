get:
	. ../env_vars.env; curl --insecure --cert-type p12 --cert ../$${CLIENT_CERT} https://localhost:9999/todos

post:
	. ../env_vars.env; curl --insecure --cert-type p12 --cert ../$${CLIENT_CERT} -X POST -H "Content-Type: application/octet-stream" -d 'AAAAA' https://localhost:9999/todos

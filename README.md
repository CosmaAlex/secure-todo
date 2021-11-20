# Secure-TODO

Deploy on your server an API endpoint to which you can POST a file to store it on the server, and GET to obtain it back. In this case it is a text file containing all my personal todos, which I personally manage using [todo.txt](https://github.com/todotxt/todo.txt-cli) (check it out, it's very cool). But your usage may vary, and it's easily customizable.

The authentication happens at connection level using TLS mutual authentication on **public key crypto** on PKCS12 certificates.
The server signs all the client certificates that can be used to access the endpoint, and this is used as a proof of an authorized user.
The signature process of a client certificate must be done manually: this is not scalable, but for now this project doesn't aim to achieve this goal.

To add a further level of protection, you may store on the server an encrypted version of your todos using AES, and distribute the key to your other machines manually to let them all decrypt successfully.

Further details on the certificates creation and signature process will come along the way...

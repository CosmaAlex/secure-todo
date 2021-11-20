# Idea

The idea is to provide an API from which I can send a POST to update my encrypted file containing all TODOs and a GET to obtain it. The key to encrypt is saved locally on my machines and distributed manually. THe algo is AES-256-CTR.

All requests are authenticated using elliptic curves on both server and client.

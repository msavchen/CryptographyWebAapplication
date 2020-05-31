# CryptographyWebApplication
Web site in Django which provides with some cryptographic functions from java library. Connected via RabbitMQ.

This project consists of some parts:
* Java server which provides some basic functionality from Package javax.crypto;
* Django client which gets input and tasks from a user and calls for Java server to perform them;
* To communicate between Java Server and Python client RabbitMQ is used. Pattern Remote procedure call (RPC) is implemented for this purpose. The client sends a request and waits for a response, the server gets a basic acknowledge.

### To run:
#### Server
Import cryptoAppServer as Maven project, JRE 1.8 and above is required.  
Run 'cryptoAppServer\src\main\java\com\rabbitmq\cryptoAppServer\RPCServer.java'

#### Client 
RabbitMQ Service, Django are required.  
Go to CryptographyWebClient and run 'python manage.py runserver'.  
Open home page: http://127.0.0.1:8000/cryptoApp/

## Current possibilities:
* MAC (Message authentication code);   
After a user provides input, a client sends a request to the server to generate a key with a chosen algorithm and size. After this server sends a request to create mac using a specified algorithm and created key. After the server answers - client shows Message authentication code and generated key.
* Encrypt text;  
After a user provides input, a client sends a request to the server to generate a key with a chosen algorithm and size. After this server sends a request to encode text using a specified algorithm and created key. After the server answers - client shows encrypted text and generated key.
* Hash text;  
After a user provides input, a client sends a request to the server to hash a text with a chosen algorithm. After the server answers - client shows hashed text.
* Generate key;  
After a user provides input, a client sends a request to the server to generate a key with a chosen algorithm and size. After the server answers - client shows generated key.
* Decrypt text - doesn't work properly;  
After a user provides input, a client sends a request to the server to create a key object with a chosen algorithm and key text. After this server sends a request to decode text using a specified algorithm and generated key. After the server answers - client shows decrypted.


## Further improvements:
* Improve frontend;
* Add file encoding;
* Fix text decoding.

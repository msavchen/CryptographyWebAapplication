# CryptographyWebApplication
Web site in Django which provides with some cryptographic functions from java library. Connected via RabbitMQ.

This project consists of some parts:
* Java server which provides some basic functionality from Package javax.crypto;
* Django client which gets input and tasks from a user and calls for Java server to perform them;
* RabbitMQ is used to communicate between the client in Python and the server in Java;

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
* Encrypt text;
* Hash text;
* Generate key;
* Decrypt text - doesn't work properly.


## Further improvements:
* Improve frontend;
* Add file encoding;
* Fix text decoding.

import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from constants import PUBLIC_SERVER_KEY
 
class ClientError(Exception):
   pass

key = RSA.generate(1024)
private_key_cl =  key
public_key_cl = key.publickey()
 
 
class Client:
   def __init__(self, host, port, timeout=None):
       self._host = host
       self._port = port
       self._timeout = timeout
       self._client_pub_key = public_key_cl
       self._client_private_key = private_key_cl
       self._server_public_key = PUBLIC_SERVER_KEY
       try:
           self._sock = socket.create_connection((self._host, self._port))
       except socket.error as err:
           raise ClientError(err)

   def decrypt(self, msg):
    pass

   def encrypt(self):

        self._sock.sendall(public_key_cl)
        print("Sending your public_key_cl")
        response = self._sock.recv(2048)
        if "ok" in response.decode('utf8'):
            print("all communication now will be super secure")

   def get(self, command):


       send_data = f'{command}'.encode('utf8')
       try:
           self._sock.sendall(send_data)
           response = self._sock.recv(1024)
           print("\n" + response.decode('utf8'))
      
 
       except Exception as err:
           print(err)
          
    
   def start_client(self):
       self.get(command=f'welcome_new_client {self._client_pub_key}')

       while True:
           command = input('\033[92mtype in word to search\033[0m\n')
           self.get(command)
           if command == "exit":
               break
 
   def close(self):
       self._sock.close()
 
if __name__ == '__main__':
   client = Client('127.0.0.1', 8888)
   client.start_client()
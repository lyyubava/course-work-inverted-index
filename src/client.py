import socket
 
 
class ClientError(Exception):
   pass
 
 
class Client:
   def __init__(self, host, port, timeout=None):
       self._host = host
       self._port = port
       self._timeout = timeout
       try:
           self._sock = socket.create_connection((self._host, self._port))
       except socket.error as err:
           raise ClientError(err)
 
#
   def get(self, command):
       send_data = f'{command}'.encode('utf8')
       try:
           self._sock.sendall(send_data)
           response = self._sock.recv(40960000)
           if not "client_data" in response.decode('utf8'):
                print("\n" + response.decode('utf8'))
           else:
                with(open(response.decode('utf8'))) as f:
                    data = f.read()
                print(data)
 
       except Exception as err:
           print(err)
          
 
   def start_client(self):
       self.get(command='welcome_new_client')
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
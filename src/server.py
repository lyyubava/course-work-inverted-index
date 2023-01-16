import socket
import _thread
from inverted_index_parallel_another_try import InvertedIndex as ii_parallel
import json
from storage import Storage

storage = Storage(16, "test/neg", "test/pos", "train/neg", "train/pos", "train/unsup")
inverted_index = ii_parallel(storage)
inverted_index.create_index_parallel(5)
class Server:
 
    def __init__(self, host, port, timeout=None):
        self._host = host
        self._port = port
        self._timeout = timeout
        self.commands = {
           "welcome_new_client": self._welcome_new_client,
           "exit": self._bye,
           "options": self._options
 
       }

    def _options(self):
       options = {
                  "exit": "exit",
                  "word": "search word in index"
                   }
 
       opts = []
       for opt, opt_descr in options.items():
           t = opt + "  " + opt_descr
           opts.append(t)
       return "\n".join(opts)

    @staticmethod
    def _welcome_new_client():
            return "\033[96mYou are now connected to the index server\033[0m \n"\
                  "Type 'word' to search \n"\
                  "Use 'exit' to exit \n"\
                  "Or see 'options'"
 
 
    @staticmethod
    def _bye():
        return "good bye, thanks for searching"
    
    def _search_word(self, word):
        return json.dumps(inverted_index.search(word))

    def reply(self, message):
        if message in self.commands:
           reply = self.commands[message]()
           return reply


        reply = self._search_word(message)
        return reply
 
    def handle(self, connection):
       
        while True:
           data = connection.recv(2048)
           message = data.decode('utf-8')
           rep = self.reply(message)
           connection.sendall(str.encode(rep))


    def get(self, sock):
        cl, addr = sock.accept()
        _thread.start_new_thread(self.handle,(cl, ) )
 
  
    def start_server(self):
        server_sock = socket.socket()
        try:
            server_sock.bind((self._host, self._port))
        except socket.error as e:
            print(str(e))
            
        server_sock.listen()
    
        while True:
            self.get(server_sock)
 
if __name__ == "__main__":
   server = Server("127.0.0.1", 8888)
   server.start_server()

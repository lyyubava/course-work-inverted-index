from importlib.resources import path
import socket
import _thread
import pathlib
import threading
from inverted_index_serial import InvertedIndex, Storage
import re
import json
from constants import PRIVATE_SERVER_KEY
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from aes import AESCipher
import os
import base64

 
WELCOME_MSG = "You are now connected to the lab server"
LIST_OF_STUDENTS = "/tmp/list_of_students"
COMMANDS = ["add", "fetch", "welcome_new_client"]
LOG_FILE = "/tmp/logs"
k = "СмаглюкЛюбовІгорівна0000"
key = k.encode("cp1251")
#  
# def add_logs(info):
#    with open(LOG_FILE, "a") as log_file:
#        log_file.write(info)


storage = Storage("pos/", "index")
inverted_index = InvertedIndex(storage)

class Server:
 
    def __init__(self, host, port, timeout=None):
        self._host = host
        self._port = port
        self._timeout = timeout
        self.server_private_key = PRIVATE_SERVER_KEY
        self.commands = {
           "welcome_new_client": self._welcome_new_client,
           "exit": self._bye
 
       }

    


    def session_key(self, client_pub):
           print(client_pub)
           encryptor = PKCS1_OAEP.new(client_pub)
           encrypted_with_client_pub = bytearray()
           encrypted_with_client_pub += encryptor.encrypt(pad(key, 16))

           encryptor_server = PKCS1_OAEP.new(self.server_private_key)
           encrypted_with_server_private = bytearray()
           encrypted_with_server_private += encryptor_server.encrypt(pad(encrypted_with_client_pub, 16))

           return base64.b64encode(encrypted_with_server_private)
    
    def get_aes_key_from_session_key(self, session_key, client_pub):
           decryptor = PKCS1_OAEP.new(client_pub)
           encrypted_aes_key =  base64.b64decode(session_key)
           decrypted_with_client_pub = bytearray()
           decrypted_with_client_pub +=  decryptor.decrypt(encrypted_aes_key)
        
           decryptor = PKCS1_OAEP.new(self.server_private_key)
           decrypted_with_server_private = bytearray()
           decrypted_with_server_private +=  decryptor.decrypt(decrypted_with_client_pub)
        
           return decrypted_with_server_private

    @staticmethod
    def encrypt_data(data):
        aes = AESCipher(key)
        return aes.encrypt(data)
    
    # def decrypt_data(self, session_key, data):
        
        



    def _welcome_new_client(self, client_pub_key):
            return self.session_key(client_pub_key)
            return "\033[96mYou are now connected to the server\033[0m \n"\
                  "Type 'word' to search \n"\
                  "Use 'exit' to exit \n"\
                  "Or see 'options'"
 
 
    @staticmethod
    def _bye():
        return "good bye, thanks for searching"
    
    def _highlight_term(id, term, text):
        replaced_text = text.replace(term, "\033[1;32;40m {term} \033[0;0m".format(term=term))
        return "--- document {id}: {replaced}".format(id=id, replaced=replaced_text)

    
    def _search_word(self, word):
        entries = inverted_index.search(word)
        #print(entries)
        # msg = f"Wow, word {word} was founded in {len(entries)} document/s" 
        # msg_list = list(msg)
        # for entry in entries:
        #     with open(entry["docID"], "r") as f:
        #         data = f.read()
        #         msg_list.append(entry["docID"])
        #         msg_list.append(re.sub(word, f"\033[1;32;40m {word} \033[0;0m", data, flags=re.IGNORECASE))
        # 
        # highlightened_text_fn = storage.copy_data_to_client_docs("\n".join(msg_list))
        return json.dumps(entries)
        #return msg
        # for entry in entries:
        #     m

    def reply(self, message, *args):
         if message not in self.commands:
           reply = f"{message} unknown option for me, don't know what to do"\
                   "See 'options'"
           return reply
         if message == "welcome_new_client":
           reply = self.commands[message](args[0])
           return reply
        
         return reply 

 
 
 
    def handle(self, connection):
       
        while True:
            data = connection.recv(2048)
            message = data.decode('utf-8')
            message = message.split()
            if not message:
               continue
            if len(message) == 1:
               self.reply(message[0])
            message, options = message[0], message[1:]
            rep = self.reply(message, options)
            connection.sendall(rep)
            connection.sendall(rep)
 
  
 
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

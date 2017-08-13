import sys
import select
import socket as sc
from threading import Thread

class Client():
    def __init__(self, host=sys.argv[1], port=int(sys.argv[2])):
        #if(len(sys.argv) < 3):
            #host = 'localhost'
            #port = 5555
        self.c_name = ''
        self.host = host
        self.port = port
        self.socket = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
        self.socket.settimeout(180)
        # sys.stdout.write('[' + sc.gethostname() + '@ Me]: '); sys.stdout.flush()

    def send(self):
        while True:
            # print(('[' + sc.gethostname() + '@ Me]: '))
            # print(self.c_name + ' => ')
            # sys.stdout.write('[' + self.c_name + '] => '); sys.stdout.flush()
            msg = input()
            msg = self.c_name + ' => ' + msg
            # self.socket.send(msg)
            self.socket.send(msg.encode('utf-8'))
            # sys.stdout.write('[' + sc.gethostname() + '@ Me]: '); sys.stdout.flush()

    def recv(self):
        while True:
            data = self.socket.recv(1024).decode('utf-8')
            print(str(data))

    def recv_old(self):
        while True:
            name = self.socket.recv(1024)
            payload = self.socket.recv(1024)
            if not payload :
                print('\nDisconnected from chat server')
                sys.exit()
            else:
                print('\t' + str(data))
                # sys.stdout.write(payload)
                # sys.stdout.write('[' + sc.gethostname() + '@ Me]: '); sys.stdout.flush()

    def run(self):
        self.c_name = input("Please enter your name: ")
        try :
            self.socket.connect((self.host, self.port))
        except :
            print("[-] Connection to server failed.")
            sys.exit()
        print('Connection established!')
        self.socket.send(self.c_name.encode('utf-8'))
        thr_snd = Thread(target=self.send, args=())
        # thr_snd.daemon = True
        thr_snd.start()
        thr_rcv = Thread(target=self.recv, args=())
        # thr_rcv.daemon = True
        thr_rcv.start()



if __name__ == "__main__":
    sys.exit(Client().run())

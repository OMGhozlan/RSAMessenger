import sys
import select
import socket as sc
from threading import Thread

class Server():
    # sc.gethostname()
    def __init__(self, host="localhost", buffer=1024, port=5555):
        self.users = []
        self.conn_list = []
        self.buffer = buffer
        self.srv_soc = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
        self.srv_soc.setsockopt(sc.SOL_SOCKET, sc.SO_REUSEADDR, 1)
        self.srv_soc.bind((host, port))
        self.srv_soc.listen(5) # 5 connections
        self.conn_list.append(self.srv_soc)  # Add server to existing connection
        print("[+] Server (%s) started on port (%s)" % (str(host), str(port)))

    def reg_old(self):
        while True:
            r2r, r2w , err = select.select(self.conn_list,[],[],0)
            for sock in r2r:
                if sock == self.srv_soc:
                    conn, addr = self.srv_soc.accept()
                    try:
                        name = conn.recv(self.buffer).strip()
                    except sc.error:
                        continue
                    if name in self.users:
                        conn.send("[*] Name entered is already in use.\n")
                    elif name:
                        conn.setblocking(False)
                        self.users.append(name)
                        self.conn_list.append(conn)
                        print("[+] Client (%s, %s) connected\n" % addr)
                        # self.broadcast(conn, "[+] %s entered the room\n" % name)
                        print
                        thr_svc = Thread(target=self.serve, args=[name, conn])
                        break

    def reg(self):
        while True:
            conn, addr = self.srv_soc.accept()
            name = conn.recv(self.buffer).decode('utf-8')
            print(name)
            self.users.append(name)
            self.conn_list.append(conn)
            # print("[+] Client (%s, %s) connected\n" % addr)
            print("[+] Client "+ str(addr) +" connected as " + name + "\n")
            # self.broadcast(conn, "[+] %s entered the room\n" % name)
            thr_svc = Thread(target=self.serve, args=[name, conn, addr])
            thr_svc.start()

    def serve(self, name, sock, addr):
        while True:
            try:
                data = sock.recv(1024)
                if data:
                    print('[*] %s said something..' % name)
                    for socket in self.conn_list:
                        if socket != self.srv_soc and socket != sock: # Send message to designated clients
                            try :
                                socket.send(data)
                            except :
                                socket.close() # Close dead connection and remove it
                                if socket in self.conn_list:
                                    self.conn_list.remove(socket)
            except Exception as exp:
                print('[*] %s has disconnected.' % name)
                break

    def run(self):
        thr_reg = Thread(target=self.reg, args=())
        thr_reg.start()

    def run_old(self):
        while True:
            r2r, r2w , err = select.select(self.conn_list,[],[],0)
            for sock in r2r:
                if sock == self.srv_soc:
                    conn, addr = self.srv_soc.accept()
                    self.conn_list.append(conn)
                    print("[+] Client (%s, %s) connected\n" % addr)
                    self.broadcast(conn, "[+] (%s:%s) entered the room\n" % addr)
                else: # Receiving and processing message
                    try:
                        payload = sock.recv(buffer)
                        if data:
                            self.broadcast(sock, "\r" + '[' + str(sock.getpeername()) + '] ' + payload)
                        else: # Remove dead connection
                            if sock in SOCKET_LIST:
                                # del self.users[]
                                self.conn_list.remove(sock)
                            self.broadcast(sock, "[-] Client (%s, %s) is offline\n" % addr)
                    except:
                        self.broadcast(sock, "[-] Client (%s, %s) is offline\n" % addr)
                        continue
        self.srv_soc.close()


    def broadcast (self, sock, message):
        for socket in self.conn_list:
            if socket != self.srv_soc and socket != sock: # Send message to designated clients
                try :
                    socket.send(message)
                except :
                    socket.close() # Close dead connection and remove it
                    if socket in self.conn_list:
                        self.conn_list.remove(socket)

if __name__ == "__main__":
    sys.exit(Server().run())

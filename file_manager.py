from __future__ import print_function
import socket
import time
from threading import Thread
import os

import Pyro4
import Pyro4.core
import Pyro4.naming
import Pyro4.socketutil


@Pyro4.expose
@Pyro4.callback
class File_Manager(object):
    def __init__(self):
        print("Bem vindo ao gerenciador de arquivos distribuidos")

        # Local URI list and logical name dictionary.
        # In case naming server fails (local backup)
        self.uri_list = []
        # Dictonary key = URI, value = logical_name
        self.logical_names = {}

        # Gets own IP address
        self.my_ip = Pyro4.socketutil.getIpAddress(None, workaround127=True)
        
        # RMI Daemon
        with Pyro4.Daemon(host=self.my_ip) as daemon:
            self.daemon = daemon

        # Locating naming_server
        self.naming_server = None
        self.recover_naming_server()

        # Pinging naming server to see if it's still up
        thread_ping_ns = Thread(target = self.ping_naming_server, daemon=True)
        thread_ping_ns.start()

    def store_file(self, local_file, logic_name=''):
        """
        Register a file of your computer on the network, so that other computers can access it
        """
        if ('' == logic_name):
            logic_name = str(os.path.basename(local_file.name))

        # Give logical name to Pyro to register the object on the network
        # Gets local_file URI
        local_file_uri = self.daemon.register(local_file)

        # Adds uri and logical name to local list (in case of naming server failure)
        self.uri_list.append(local_file_uri)
        self.logical_names[local_file_uri] = logic_name

        # Try 3 times to register on naming server
        attempts = 0
        while (attempts < 3):
            try:
                self.naming_server.register(logic_name, local_file_uri)
                print("Arquivo armazenado! " + logic_name )
                break;
            except:
                self.recover_naming_server()
                attempts += 1

        if (3 == attempts):
            print(":( Nao foi possivel registrar o arquivo. Tente novamente mais tarde.")
 
        return 

    def search_file(self, logical_name):
        """
        Receives a logical_name of a file and return a list of lists.
        Lists contain [file_name, proxy_object] for possible results
        URI contains file location. User then proceeds to open files and check which he wants
        """
        
        files = []

        try:
            print(self.naming_server)
            for file_name, file_uri in self.naming_server.list(prefix=logical_name).items():
                print("Encontrado arquivo: " + file_name)
                finding = [file_name, Pyro4.Proxy(file_uri)]
                files.append(finding)
        except:
            print("Naming server nao encontrado. Tente novamente")
            self.recover_naming_server()

        print("Returning: " + str(files))
        return files

    @Pyro4.expose
    @Pyro4.callback
    def download_file(self, remote_file):
        """
        Receives a [file_name, proxy_object] object to be downloaded. Downloads
        """
        # Define name of new file. MISSING FILE EXTENSION!
        name = remote_file[0] + "_downloaded"

        # Open new file to be downloaded
        with open(name, 'wb') as local_file:
            
            # Reads whole file, 1024 bytes at a time.
            while (True):
                data = remote_file[1].get(1024)
                if ('' == data): break
                local_file.write(data)

    @Pyro4.expose
    @Pyro4.callback
    def remove_file(self, remote_file):
        """
        Receives a [file_name, proxy_object] object to be removed
        """
        
        # Removes files from remote computer
        os.remove(os.path.realpath(remote_file[1].name) )

        # Remove name from naming server
        self.naming_server.remove(remote_file[0])

        # Remove URI from daemon
        self.naming_server.remove(remote_file[1])

    def recover_naming_server(self):
        """
        If there isn't a naming server, creates one and send info.
        If there is, connects to it and send all previous information.
        """
        # Tries to locate Naming Server
        try:        
            with Pyro4.locateNS() as ns:
                self.naming_server = ns
                if self.uri_list:
                    for uri in uri_list:
                        # Register on new naming server
                        ns.register(self.logic_names[uri], uri)

        # If no naming server was found, create one
        except:
            thread_start_ns = Thread(target = start_naming_server, daemon=True)
            thread_start_ns.start()
            self.recover_naming_server()

        return 

    def ping_naming_server(self, timer=30):
        """
        Check if naming server still on every such seconds (received in argument)
        """
        while (True):
            time.sleep(timer)
            try:
                self.naming_server.ping()
            except:
                self.recover_naming_server()


    def get(self, number):
        return self.remote_file.read(number)

    def remove(self, remote_file):
        return os.remove(os.path.realpath(remote_file[1].name) )
        

def start_naming_server():
    Pyro4.config.SERVERTYPE = "multiplex"
    Pyro4.config.POLLTIMEOUT = 3


    hostname = socket.gethostname()
    my_ip = Pyro4.socketutil.getIpAddress(None, workaround127=True)


    @Pyro4.expose
    class EmbeddedServer(object):
        def multiply(self, x, y):
            return x * y


    print("MULTIPLEXED server type. Initializing services...")
    print("Make sure that you don't have a name server running already!\n")
    # start a name server with broadcast server
    nameserverUri, nameserverDaemon, broadcastServer = Pyro4.naming.startNS(host=my_ip)
    assert broadcastServer is not None, "expect a broadcast server to be created"
    print("got a Nameserver, uri=%s" % nameserverUri)

    # create a Pyro daemon
    pyrodaemon = Pyro4.core.Daemon(host=hostname)
    serveruri = pyrodaemon.register(EmbeddedServer())
    print("server uri=%s" % serveruri)

    # register it with the embedded nameserver
    nameserverDaemon.nameserver.register("example.embedded.server", serveruri)

    print("")

    # Because this server runs the different daemons using the "multiplex" server type,
    # we can use the built in support (since Pyro 4.44) to combine multiple daemon event loops.
    # We can then simply run the event loop of the 'master daemon'. It will dispatch correctly.

    pyrodaemon.combine(nameserverDaemon)
    pyrodaemon.combine(broadcastServer)

    def loopcondition():
        #print(time.asctime(), "Waiting for requests...")
        return True
    pyrodaemon.requestLoop(loopcondition)

    # clean up
    nameserverDaemon.close()
    broadcastServer.close()
    pyrodaemon.close()
    print("done")    
#
#def main():
#    Pyro4.Daemon.serveSimple(
#            {
#                File_Manager: "example.file_manager"
#            },
#            ns = True)
#
#if __name__=="__main__":
#    main()


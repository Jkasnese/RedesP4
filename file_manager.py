from __future__ import print_function
import socket
import time

import Pyro4
import Pyro4.core
import Pyro4.naming
import Pyro4.socketutil


@Pyro4.expose
class File_Manager(object):
    def __init__(self):
        print("Bem vindo ao gerenciador de arquivos distribuidos")

    def choose_file(self):
        """
        Chooses a file from your computer
        """
        # Opens local directory

        return local_file

    def store_file(self, local_file):
        """
        Register a file of your computer on the network, so that other computers can access it
        """

        # Hash file to get logical name. Is it really necessary?

        # Give logical name to Pyro to register the object on the network
        with Pyro4.Daemon() as daemon:
            # Gets local_file URI
            local_file_uri = daemon.register(local_file)
            with Pyro4.locateNS() as naming_server:
                # Register on naming server
                naming_server.register(local_file.name, local_file_uri)            
            
        return local_file_uri

    def search_file(self, logical_name):
        """
        Receives a logical_name of a file and return a list of possible URIs results
        URI contains file location. User then proceeds to open files and check which he wants
        """
        
        files = []

        with Pyro4.locateNS() as naming_server:
            for file_name, file_uri in naming_server.list(prefix=logical_name).items():
                print("Encontrado arquivo: " + file_name)
                files.append(Pyro4.Proxy(file_uri))

        # If no file was found
        if not files:
            raise ValueError("Não foi encontrado arquivo com este nome!")

        return files

    def pick_file(self, files):
        """
        Receive a list of possible files with that name
        """

    def remove_file_from_network(self, logical_name):

        uri = self.search_file(logical_name)

        # Remove URI from name server

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
        print(time.asctime(), "Waiting for requests...")
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

start_naming_server()

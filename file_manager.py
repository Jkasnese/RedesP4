import Pyro4

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

def main():
    Pyro4.Daemon.serveSimple(
            {
                File_Manager: "example.file_manager"
            },
            ns = True)

if __name__=="__main__":
    main()

import Pyro4

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class File_Manager(object):
    def __init__(self):
        print("Bem vindo ao gerenciador de arquivos distribuidos")

    def store_file(self):
        """
        Register a file of your computer on the network, so that other computers can access it
        """

        # Choose file

        # Hash file to get logical name

        # Give logical name to Pyro to register the object on the network

        return uri

    def search_file(self, logical_name):
        """
        Receives a logical_name of a file and return it's URI, which contains the precise location
        """

        return uri

    def remove_file_from_network(self, logical_name):

        uri = self.search_file(logical_name)

        # Remove URI from name server

def main():
    Pyro4.Daemon.serveSimple(
            {
                Warehouse: "example.warehouse"
            },
            ns = False)

if __name__=="__main__":
    main()

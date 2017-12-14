from file_manager import *
import Pyro4

app = File_Manager()
with open('arquivo_teste.txt', 'r') as local_file:
    app.store_file(local_file)
    app.search_file('arquivo_teste.txt')

from tkinter import Tk, Label, Button, LEFT, RIGHT, W, IntVar, Entry, Toplevel
from tkinter.filedialog import askopenfilename
from file_manager import *
from threading import Thread
from functools import partial

class Manager_GUI:
    def __init__(self, master):
        self.master = master
        master.title("Gerenciador de arquivos distribuidos")

        # # # # # GRID # # # # # # # # # # # # # # # # #
        # Armazenar  [BOTAO]                           #
        # Baixar [CAIXA PARA DIGITAR NOME] [BOTÃO]     #
        # Buscar [CAIXA PARA DIGITAR NOME] [BOTÃO]     #
        # Remover [CAIXA PARA DIGITAR NOME] [BOTÃO]    # 
        # # # # # GRID # # # # # # # # # # # # # # # # #

        # File manager per se
        self.file_manager = File_Manager()

        # # # # # FIRST ROW: STORAGE # # # # # 

        # Store file Label
        self.store_file_label = Label(master, text="Armazenar um arquivo:")
        self.store_file_label.grid(row=0, column=1, columnspan=1)
    
        # Store file button
        self.store_file_button = Button(master, text="Selecione o arquivo", command=self.store)
        self.store_file_button.grid(row=0, column=2)


        # # # # # SECOND ROW: DOWNLOAD # # # # # 

        # Download file Label
        self.download_file_label = Label(master, text="Baixar um arquivo. Informe o nome:")
        self.download_file_label.grid(row=1, column=1, columnspan=1)
    
        # Input download file name
        self.download_input = Entry(master, text="Text", textvariable="Text variable")
        self.download_input.grid(row=1, column=2)

        # Download file button
        self.download_file_button = Button(master, text="Baixar", command=self.download)
        self.download_file_button.grid(row=1, column=3)


        # # # # # THIRD ROW: SEARCH # # # # # 

        # Search file Label
        self.search_file_label = Label(master, text="Buscar arquivo. Informe nome:")
        self.search_file_label.grid(row=2, column=1, columnspan=1)

        # Input search file name
        self.search_input = Entry(master)
        self.search_input.grid(row=2, column=2)
    
        # Store file button
        self.search_file_button = Button(master, text="Buscar", command=self.search)
        self.search_file_button.grid(row=2, column=3)


        # # # # # FOURTH ROW: REMOVE # # # # # 

        # Search file Label
        self.remove_file_label = Label(master, text="Remover arquivo. Informe nome:")
        self.remove_file_label.grid(row=3, column=1, columnspan=1)

        # Input remove file name
        self.remove_input = Entry(master)
        self.remove_input.grid(row=3, column=2)
    
        # Store file button
        self.remove_file_button = Button(master, text="Remover", command=self.remove)
        self.remove_file_button.grid(row=3, column=3)
        
        # # # # # # # # # # # # # # # # # # # 


    # # # # # CLASS FUNCTIONS # # # # #

    def store(self):
        path = askopenfilename()
        with open(path) as local_file:
            self.file_manager.store_file(local_file)

    def download(self):
        user_input = self.download_input.get()
        if (self.check_valid_input(user_input)):
            self.search_results_window(self.file_manager.search_file(user_input), self.file_manager.download_file, "baixar")
        else:
            self.invalid_input_msg()
        return

    def search(self):
        user_input = self.search_input.get()
        if (self.check_valid_input(user_input)):
            self.search_results_window(self.file_manager.search_file(user_input), self.file_manager.download_file, "baixar")
        else:
            self.invalid_input_msg()
        return

    def remove(self):
        user_input = self.remove_input.get()
        if (self.check_valid_input(user_input)):
            self.search_results_window(self.file_manager.search_file(user_input), self.file_manager.remove_file, "remover")
        else:
            self.invalid_input_msg()
        return

    def check_valid_input(self, user_input):
        if ('' != user_input):
            return True
        return False

    def search_results_window(self, results, function, function_name):
        """
        Receives a list of lists (each list is a possible result), function to execute and it's name
        Each possible result contains [file_name, proxy_object]
        Shows the user the file_names and user can download the file through a button
        """

        # Opens new window
        results_window = Toplevel(self.master)
        results_window.title("Resultados da busca")
        
        # If there is any results:
        if results:

            # Show instructions
            instrucao = "Clique no botao ao lado do arquivo para " + function_name
            instrucao_label = Label(results_window, text=instrucao)
            instrucao_label.grid(row=0, column=0)

            # Positioning the results
            file_row=1

            # Shows the user the file names and button to perform certain action (argument)
            for result in results:
                file_label = Label(results_window, text=result[0])
                file_label.grid(row=file_row, column=0)
                file_action = Button(results_window, text=function_name, command=partial(function, result[1]) )
                file_action.grid(row=file_row, column=1)
        
        # If there's no results
        else: 
            no_results_label= Label(results_window, text="Nao foram encontrados resultados :(")
            no_results_label.grid(row=0, column=0)

    def invalid_input_msg(self):
        """
        Shows the user a message to fill the input box
        """

        # Creates window
        invalid_input_window = Toplevel(self.master)
        invalid_input_window.title("Erro")    

        error_label = Label(invalid_input_window, text="Por favor, preencha o campo!")
        error_label.grid(row=0, column=0)



# Rodando
root = Tk()
my_gui = Manager_GUI(root)
root.mainloop()

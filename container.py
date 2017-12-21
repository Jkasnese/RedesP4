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
class Container(object):
    def __init__(self):
        with open() as file_object:
            self.remote_file = file_object

    def get(self, number):
        return self.remote_file.read(number)

    def rem(self):
        

from threading import Thread
import threading
from controllers.ControllerRequests import ControllerRequests
import _thread
import time
from datetime import datetime, timezone
from entities.User import User
from random import randint
from util.PrettyPrint import PrettyPrint
from util.Colors import Colors
import os
import shutil


class ControllerConnections(Thread):
    def __init__(self, server):
        Thread.__init__(self)
        self.server = server
        self.width = os.get_terminal_size().columns
        self.terminal_size = shutil.get_terminal_size(fallback=(120, 50))

    def run(self):
        while True:
            connectionSocket, addr = self.server.serverSocket.accept()
            connectionSocket.send(('\n' +
                                   (PrettyPrint.pretty_print("CONCORD".center(self.width), Colors.TITLE))).encode())

            connectionSocket.send((f"\n\nSeja bem vindo ao concord!\n\nDeseja se registrar ou logar?\n"
                                   + f"Para logar execute "
                                     f"{PrettyPrint.pretty_print('/login <user> <passw>', Colors.WARNING)} \n"
                                   + f"Para registrar execute "
                                     f"{PrettyPrint.pretty_print('/register <name> <user> <passw>', Colors.WARNING)}"
                                     f"\n\n").encode())

            user = User("UserRandom", "random" + str(randint(0, 10000)), "", connectionSocket)

            self.server.activeUser.append(connectionSocket)
            t = ControllerRequests(connectionSocket, self.server, user)
            t.start()

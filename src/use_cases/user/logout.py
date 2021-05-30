import sys

from util import *
from entities.ent_user import *
from entities.resources import *
from use_cases import *
from random import randint

__all__ = ['Logout']


class Logout:
    @staticmethod
    def response(user: User, server, args) -> User:
        try:
            if not user.is_logged:
                raise Exception("Not logged")

            if user.status_room != 'lobby':
                Leave.response(user, server)

            user.toggle_log()

            user_random = UserFactory.create(connection_socket=user.connection_socket)

            # remove obj with log true and save with log false
            for users in server.registered_users:
                if users.nickname == user.nickname:
                    server.active_users.remove(users)
                    server.active_users.append(user)

            # the obj in server is random now
            for users in server.active_users:
                if users.nickname == user.nickname:
                    server.active_users.remove(users)
                    server.active_users.append(user_random)

            user.connection_socket.send(
                (PrettyPrint.pretty_print("You logged out successfully!\n\n", Colors.OKGREEN)).encode())

            return user_random

        except Exception as exp:
            print(exp.with_traceback(sys.exc_info()[2]))
            user.connection_socket.send((PrettyPrint.pretty_print(
                "Error in logging client out\n\n", Colors.FAIL
            )).encode())

            return user

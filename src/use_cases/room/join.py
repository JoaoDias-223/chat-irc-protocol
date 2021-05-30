from util import *
from entities.ent_user import *
from dtos.dto_participants import Participants as dtoParticipants

__all__ = ['Join']


class Join:
    @staticmethod
    def response(user: User, server, args: list) -> User:
        if user.status_room != 'lobby':
            user.connection_socket.send(
                (PrettyPrint.pretty_print("Você já está em uma sala \n\n", Colors.FAIL)).encode())
            return user

        if not user.is_logged:
            user.connection_socket.send(
                (PrettyPrint.pretty_print("Você não está logado amigo \n\n", Colors.FAIL)).encode())
            return user

        room_name = args[0]

        for room in server.registered_rooms:
            if room.name == room_name:
                if room.add(user):
                    user.status_room = room_name
                    server.participants_repository.put(dtoParticipants(nickname=user.nickname, room_id=room.id))
                    return user

        user.connection_socket.send(
            (PrettyPrint.pretty_print("Error in join to room '" + str(room_name) + "' \n\n", Colors.FAIL)).encode())

        return user

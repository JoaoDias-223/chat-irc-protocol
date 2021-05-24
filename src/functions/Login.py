from Interface.PrettyPrint import PrettyPrint
from Interface.Colors import Colors


class Login:
    @staticmethod
    def response(user, server, nick, password) -> None:
        try:
            if nick == '' or password == '':
                raise Exception("Invalid command")

            nick_ok = False
            pass_ok = False
            logged_ok = False
            user_found = None

            for userRegistered in server.registeredUsers:
                if userRegistered.nick == nick and userRegistered.password == password and not userRegistered.isLogged:
                    user_found = userRegistered
                    nick_ok = True
                    pass_ok = True
                    break
                if userRegistered.isLogged:
                    logged_ok = True
                if userRegistered.nick == nick:
                    nick_ok = True
                if userRegistered.password == password:
                    pass_ok = True

            if nick_ok and pass_ok and not logged_ok:
                user_found.toggleLog()
                user_found.setSocket(user.connectionSkt)
                user.connectionSkt.send(
                    (PrettyPrint.pretty_print("Client " + str(nick) + " successfully log\n\n", Colors.OKGREEN)).encode())
                return user_found
            elif logged_ok:
                user.connectionSkt.send(
                    (PrettyPrint.pretty_print("Client '" + str(nick) + "' already logged\n\n", Colors.FAIL)).encode())
            elif not nick_ok:
                user.connectionSkt.send(
                    (PrettyPrint.pretty_print("Client '" + str(nick) + "' not found\n\n", Colors.FAIL)).encode())
            elif not pass_ok:
                user.connectionSkt.send(
                    (PrettyPrint.pretty_print("Wrong password\n\n", Colors.FAIL)).encode())

            return user

        except:
            user.connectionSkt.send(
                (PrettyPrint.pretty_print("Error in login client '" + str(nick) + "'\n\n", Colors.FAIL)).encode())

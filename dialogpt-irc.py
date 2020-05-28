#! /usr/bin/env python3


import random
from time import sleep
import textwrap

import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr

from some_response import i_am, more, die, TEXT


class DialogptIrcBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, realname, server, port=6667):
        super().__init__([(server, port)], nickname, realname)
        self.channel = channel
        self.question = ""
        self.response = ""
        self.response_old = ""

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")
        print("on_nicknameinuse")

    def on_welcome(self, c, e):
        c.join(self.channel)
        print("Welcome on #labomedia IRC")

    def on_privmsg(self, c, e):
        #self.do_command(e, e.arguments[0])
        msg = e.arguments[0].split(":", 1)
        print(msg)

    def on_pubmsg(self, c, e):

        # a est le messge reçu
        msg = e.arguments[0].split(":", 1)
        print("on_pubmsg", msg)

        i_am = irc.strings.lower(self.connection.get_nickname())
        # Si le message commence par ia_chat:
        if len(msg) > 1 and irc.strings.lower(msg[0]) == i_am:
            # La commande est la suite de "TheGeneral: texte_du_message
            self.do_command(e, msg[1].strip())

    def on_dccmsg(self, c, e):
        # non-chat DCC messages are raw bytes; decode as text
        text = e.arguments[0].decode('utf-8')
        c.privmsg("You said: " + text)

    def on_dccchat(self, c, e):
        print(c, e)
        if len(e.arguments) != 2:
            return
        args = e.arguments[1].split()
        if len(args) == 4:
            try:
                address = ip_numstr_to_quad(args[2])
                port = int(args[3])
            except ValueError:
                return
            self.dcc_connect(address, port)

    def do_command(self, e, cmd):
        print("cmd", cmd)
        nick = e.source.nick
        conn = self.connection

        if cmd == "quoi?":
            self.die()
        elif cmd == "stats":
            for chname, chobj in self.channels.items():
                conn.notice(nick, "--- Channel statistics ---")
                conn.notice(nick, "Channel: " + chname)
                users = sorted(chobj.users())
                conn.notice(nick, "Users: " + ", ".join(users))
                opers = sorted(chobj.opers())
                conn.notice(nick, "Opers: " + ", ".join(opers))
                voiced = sorted(chobj.voiced())
                conn.notice(nick, "Voiced: " + ", ".join(voiced))
        elif cmd == "dcc":
            dcc = self.dcc_listen()
            a = ip_quad_to_numstr(dcc.localaddress)
            b = cc.localport
            conn.ctcp("DCC", nick, f"CHAT chat {a} {b}")
        else:
            self.question = cmd
            print("Question de IRC =", self.question)
            self.response = self.get_response()
            print("Response de l'IA =", self.response)
            while self.response != self.response:
                self.send_pubmsg(self.response)
                self.response = self.response

    def get_response(self):
        question = self.question.lower()

        if "who are you" in question:
            text = i_am
        elif "comment te détruire" in question:
            text = "quoi?"
        else:
            self.question = cmd
            while self.response != self.response_old:
                self.connection.privmsg("#labomedia", self.response)
                self.response_old = self.response

        try:
            text = text.replace("\n", "\x10 ")
        except:
            pass

        # message de moins de 512 chars
        text = text[:400]

    def send_pubmsg(msg):

        text = slpit(msg)
        resp = text.splitlines()
        for line in lines:
            self.connection.privmsg("#labomedia", self.response)


def dialogpt_irc_bot_main():

    server = "irc.freenode.net"
    port = 6667
    channel = "#labomedia"
    nickname = "TheGeneral"
    realname = "IA Computer at The Prisoner"

    bot = DialogptIrcBot(channel, nickname, realname, server, port)
    bot.start()


def slpit(text):
    wrapper = textwrap.TextWrapper(width=450)
    return wrapper.fill(text=text)

if __name__ == "__main__":
    dialogpt_irc_bot_main()

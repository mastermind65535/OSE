from Engine.Parser.SearchEngine import Google
from Engine.Parser.SearchEngine import Bing
from Engine.Parser.SearchEngine import Yahoo
from Engine.Parser.SearchEngine import Yandex
from Engine.Parser.SearchEngine import DuckDuckGo
from Engine.Parser.SearchEngine import BraveSearch
from Engine.Parser.SearchEngine import Baidu

from Engine.Parser.Services import Youtube
from Engine.Parser.Services import Instagram
from Engine.Parser.Services import Facebook
from Engine.Parser.Services import Discord
from Engine.Parser.Services import Pinterest
from Engine.Parser.Services import Snapchat
from Engine.Parser.Services import TikTok
from Engine.Parser.Services import Reddit
from Engine.Parser.Services import LinkedIn
from Engine.Parser.Services import Twitter
from Engine.Parser.Services import WeChat
from Engine.Parser.Services import Telegram

import traceback
import requests
import socket
import socks
import os

ORIGIN_SOCKET = socket.socket
Local_Version = "2.0.0"
settings = {}

class Setting:
    def __init__(self):
        self.Settings = {
            "dns.subdomains.proto": "",
        }
        self.run()
    def run(self):
        for setting in self.Settings:
            settings[setting] = self.Settings[setting]

class Shell:
    class proxy:
        def set(*args):
            if len(args) > 0 and args[0] == "help":
                return ['''Set proxy server''', ["SERVER", "PORT"]]
            try:
                PROXY_HOST = str(args[0])
                PROXY_PORT = int(args[1])
                socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, PROXY_HOST, PROXY_PORT, rdns=True)
                socket.socket = socks.socksocket
                
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("ifconfig.me", 80))
                s.sendall(b"GET / HTTP/1.1\r\nHost: ifconfig.me\r\nConnection: close\r\n\r\n")
                response = s.recv(4096).decode()
                s.close()

                ipv4_address = response.split("\r\n\r\n")[1].strip()
                print(f"Your IP address is (SOCKET): {ipv4_address}")
                print(f"Your IP address is (REQUEST): {requests.get('https://api.ipify.org').text}")
            except:
                raise

        def unset(*args):
            if len(args) > 0 and args[0] == "help":
                return ['''Unset proxy server''', ["N/A"]]
            try:
                socket.socket = ORIGIN_SOCKET
            except:
                raise

        def test(*args):
            if len(args) > 0 and args[0] == "help":
                return ['''Test proxy connection''', ["N/A"]]
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("ifconfig.me", 80))
                s.sendall(b"GET / HTTP/1.1\r\nHost: ifconfig.me\r\nConnection: close\r\n\r\n")
                response = s.recv(4096).decode()
                s.close()

                ipv4_address = response.split("\r\n\r\n")[1].strip()
                print(f"Your IP address is (SOCKET): {ipv4_address}")
                print(f"Your IP address is (REQUEST): {requests.get('https://api.ipify.org').text}")
            except:
                raise
            
    class var:
        def set(*args):
            if len(args) > 0 and args[0] == "help":
                return ['''Set local variable''', ["KEY", "VALUE"]]
            try:
                target = str(args[0])
                value = str(args[1])
                if target in settings:
                    old = settings[target]
                    settings[target] = value
                    print(f"[+] Variable successfully changed: {old} --> {value}")
                elif not target in settings:
                    print(f"[-] Variable change failed: variable not exists")
                else:
                    print(f"[-] Variable change failed: Unknown")
            except:
                raise
        def print(*args):
            if len(args) > 0 and args[0] == "help":
                return ['''print local variable.\nType 'all' to see all local variables''', ["KEY"]]
            try:
                target = str(args[0])
                if target in settings:
                    print(f"{target}{' ' * (32 - len(str(target)))}: {settings[target]}")
                elif target == "all":
                    for key in settings:
                        print(f"{key}{' ' * (32 - len(str(key)))}: {settings[key]}")
                elif not target in settings:
                    print(f"[-] Variable print failed: variable not exists")
                else:
                    print(f"[-] Variable print failed: Unknown")
            except:
                raise
        def reset(*args):
            if len(args) > 0 and args[0] == "help":
                return ['''Reset local variables''', ["N/A"]]
            Setting()

class Handler:
    def __init__(self, command):
        self.COMMAND = str(command)
        self.ObjectSplit = "."
        self.ArgumentsSplit = " "
        self.arguments = []
        self.object = Shell
    def execute(self):
        Type = self.COMMAND.split(self.ObjectSplit)[0]
        Func = self.COMMAND.split(self.ObjectSplit)[1].split(self.ArgumentsSplit)[0]
        arguments = self.COMMAND.split(self.ArgumentsSplit)[1:]
        getattr(getattr(self.object, Type), Func)(*arguments)

if __name__ == "__main__":
    Setting()
    while True:
        try:
            command = str(input(f"OSE {Local_Version} > "))
            if command == "clear" or command == "cls": os.system("cls" if os.name == "nt" else "clear")
            elif command == "exit": break
            elif command == "": continue
            elif command == "help":
                for Type in Shell.__dict__:
                    if not Type.startswith("__"):
                        print(f"[{Type}]")
                        commands = getattr(Shell, Type).__dict__
                        for func in commands:
                            if not func.startswith("__"):
                                help_object = getattr(getattr(Shell, Type), func)('help')
                                helptext = help_object[0]
                                help_args = help_object[1]

                                help_command = f"{f'{Type}.{func}':<30}"
                                if "\n" in helptext:
                                    helptext += ''.rjust(60-len(helptext.split("\n")[-1]), " ")
                                    helptext = str(helptext).replace("\n", f"\n{' ' * 30}")
                                else:
                                    helptext = f"{helptext:<60}"
                                print(f"{help_command}{helptext}{' '.join(help_args)}")
                        print("")
            else:
                obj = Handler(command=command)
                obj.execute()
                print("")
        except:
            print(f"{traceback.format_exc()}")
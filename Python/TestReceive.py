from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server

dispatcher = Dispatcher()
dispatcher.map("/spacemouse/all", print)

ip = "127.0.0.1"
port = 12000
server = osc_server.ThreadingOSCUDPServer(
      (ip, port), dispatcher)

server.serve_forever()

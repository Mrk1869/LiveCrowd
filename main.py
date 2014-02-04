import time
import datetime
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado import websocket
import os
from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)
define("debug", default=0, help="1:watch in real time (debug mode)", type=bool)

class DataWebSocket(websocket.WebSocketHandler):
    def open(self):
        self.send_data()

    def send_data(self):
        nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        val_a = datetime.datetime.now().strftime("%S")
        val_b = datetime.datetime.now().strftime("%M")
        self.write_message({'date':nowtime, 'val_a':val_a, 'val_b':val_b})
        tornado.ioloop.IOLoop.instance().add_timeout(time.time() + 1, self.send_data)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html', url="", title="sample")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
            debug=options.debug,
            handlers=[(r"/", IndexHandler),
                (r"/data", DataWebSocket)],
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static")
            )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

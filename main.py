import time
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado import websocket
import os
import MySQLdb
import json
import threading
import socket
from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)
define("debug", default=0, help="1:watch in real time (debug mode)", type=bool)

froyer_count = 0
showroom_count = 0

class SQLThread(threading.Thread):
    import MySQLdb

    def __init__(self):
        threading.Thread.__init__(self)

        print ">> Connecting to MySQL database.."

        self.config = {}
        file = open('./config.json')
        self.config = json.load(file)
        file.close()

        self.ignore_device_list = []
        file = open('./ignore.txt')
        lines = file.readlines()
        for line in lines:
            self.ignore_device_list.append(line.rstrip('\n'))
        file.close()

        self.connection_foyer = MySQLdb.connect(
            db=self.config['foyer']['db'],
            host=self.config['foyer']['host'],
            port=int(self.config['foyer']['port']),
            user=self.config['foyer']['user'],
            passwd=self.config['foyer']['passwd'])
        self.cursor_foyer = self.connection_foyer.cursor()
        self.connection_showroom = self.MySQLdb.connect(
                db=self.config['showroom']['db'],
                host=self.config['showroom']['host'],
                port=int(self.config['showroom']['port']),
                user=self.config['showroom']['user'],
                passwd=self.config['showroom']['passwd'])
        self.cursor_showroom = self.connection_showroom.cursor()
        self.query = "SELECT * FROM "+self.config['foyer']['table']+" WHERE TimeStamp > TIMESTAMPADD(SECOND, -120, CURRENT_TIMESTAMP())"

    def run(self):
        while self.isRunning:
            self.cursor_foyer.execute(self.query)
            result = self.cursor_foyer.fetchall()
            global froyer_count
            froyer_count = self.count("Froyer", result)
            time.sleep(2)

            self.cursor_showroom.execute(self.query)
            result = self.cursor_showroom.fetchall()
            global showroom_count
            showroom_count = self.count("showroom", result)
            time.sleep(2)

    def count(self, name, result):
        print "--"+name+"--"
        dict = {}
        last_device = ""
        for row in result:
            device = row[2]
            if device not in self.ignore_device_list and device != last_device:
                res = ""
                dict.update({row[2]:"dummy"})
                for val in row:
                    res+= str(val)+" "
                print res
            last_device = device
        return len(dict)


class DataWebSocket(websocket.WebSocketHandler):
    def open(self):
        self.send_data()

    def send_data(self):
        self.write_message({'froyer':froyer_count, 'showroom':showroom_count})
        tornado.ioloop.IOLoop.instance().add_timeout(time.time() + 5, self.send_data)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html', url="", title="Live Crowd Density Visualization")

if __name__ == "__main__":

    print ">> LiveCrowd is running. Please access to http://" + socket.gethostbyname(socket.gethostname()) + ":" + str(options.port)

    th = SQLThread()
    th.isRunning = True
    th.start()

    try:
        tornado.options.parse_command_line()
        app = tornado.web.Application(
                debug=options.debug,
                handlers=[
                    (r"/", IndexHandler),
                    (r"/data/", DataWebSocket)],
                template_path=os.path.join(os.path.dirname(__file__), "templates"),
                static_path=os.path.join(os.path.dirname(__file__), "static")
                )
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(options.port)
        tornado.ioloop.IOLoop.instance().start()

    except KeyboardInterrupt:
        print ">> Wait a minute. Stop running.."
        th.isRunning = False

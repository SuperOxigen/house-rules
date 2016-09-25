#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard Library
import os
import sys
import signal


# Standard utilities
import argparse
import logging
logging.basicConfig(format="%(asctime)-15s - [%(levelname)6s] %(message)s")
logger = logging.getLogger("house-rules")

# Tornado Library
import tornado.httpserver as httpserver
import tornado.web as web
import tornado.ioloop as ioloop
getcloop = lambda: ioloop.IOLoop.current()

from controllers import HomeController
from models.layout import Header, Link, Footer

ONE_SECOND = 1.0
SERVER_KILL_COUNTDOWN = 5.0 * ONE_SECOND

class HRules(web.Application):
    def __init__(self, debug: bool=True):
        header = Header()
        header.links.append(Link("/view", "View"))
        header.links.append(Link("/edit", "Edit"))
        layoutData = {
            "header": header,
            "footer": Footer(),
        }
        super().__init__([
                (r"/?", HomeController, layoutData, "home"),
                (r"/css/(.*)", web.StaticFileHandler, { "path": "static/css" }, "css"),
                (r"/js/(.*)", web.StaticFileHandler, { "path": "static/js"}, "js")
                # (r"/article(?:/(?P<article>\w*))?", ArticleHandler),
            ],
            debug=debug,
            serve_traceback=debug,
            template_path="templates",
        )
        logger.info("Application setting initialized")

def parse_args(*argv):
    parser = argparse.ArgumentParser(description="Blog server.  Serves blog posts from Git.",
                                     epilog="Copyright (c) 2016 Alex Dale - See LICENCE")

    parser.add_argument("-p", "--port", type=int, dest="port", default=None,
                           help="Server listening port.  "
                                "Default port 8080 non-debug, 8888 debug.")
    parser.add_argument("--debug", action="store_true", dest="debug",
                           help="Runs server in debug mode.  "
                                "Extra logs, and traceback on server error.")
    # parser.add_argument("-c", "--config", dest="config", required=True,
    #                        help="JSON server configuration file.")

    return parser.parse_args(args=argv)

def run_server(options):
    serverPort = options.port

    logger.setLevel(logging.DEBUG if options.debug else logging.INFO)
    if serverPort is None:
        serverPort = 8888 if options.debug else 8080

    logger.debug("Initializing server")
    blog = HRules(debug=options.debug)
    ruleServer = httpserver.HTTPServer(blog)

    def sig_handler(sig, frame):
        logger.warning("Signal recieved {0}".format(sig))
        if sig == signal.SIGINT:
            getcloop().add_callback(shutdown_handler)
            stopSent = True

    logger.debug("Setting signal handlers")
    signal.signal(signal.SIGINT, sig_handler)

    def shutdown_handler():
        logger.info("Shutting down server in {0} seconds".format(int(SERVER_KILL_COUNTDOWN)))
        logger.debug("Stop listening")
        ruleServer.stop()
        secondCountDown = SERVER_KILL_COUNTDOWN
        def shutdown_callback(secondCountDown):
            logger.debug("Tick {0:02d}".format(int(secondCountDown)))
            secondCountDown -= 1
            if secondCountDown > 0:
                getcloop().call_later(ONE_SECOND, shutdown_callback, secondCountDown)
            else:
                getcloop().stop()
        shutdown_callback(secondCountDown)

    logger.info("Start listening on port {0:04}".format(serverPort))
    ruleServer.listen(serverPort)

    logger.debug("Starting IO loop")
    getcloop().start()

    return 0

def main(*argv):
    options = parse_args(*argv)
    run_server(options)

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))

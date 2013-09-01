#!/usr/bin/env python

import SimpleHTTPServer
import SocketServer


def main(host='localhost', port=4040):
	Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
	httpd = SocketServer.TCPServer((host, port), Handler)
	print "serving at port", port
	return httpd

if __name__ == '__main__':
	httpd = main()
	httpd.serve_forever()
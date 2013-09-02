#!/usr/bin/env python

import SimpleHTTPServer
import SocketServer
from walkdir import filtered_walk, dir_paths, all_paths, file_paths

class ChromeCastServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

	def __init__(self, request, client_address, server):
		print(request)
		super(ChromeCastServerHandler, self).__init__(request, client_address, server)

def index_podcasts():
	files = file_paths(filtered_walk('podcasts', included_files=['*.mp3', '*.mp4'], ))
	return files


def main(host='localhost', port=4041):
	Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
	httpd = SocketServer.TCPServer((host, port), Handler)
	#files = index_podcasts()
	return httpd

if __name__ == '__main__':

	httpd = main()
	httpd.serve_forever()

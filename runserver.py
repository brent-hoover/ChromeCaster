#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gevent.wsgi import WSGIServer
from chromecaster import caster
app = caster.run()
http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()

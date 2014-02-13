#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mimetypes
import os
import re

from flask import request, send_file, Response


def send_file_partial(path):
    """
        Simple wrapper around send_file which handles HTTP 206 Partial Content
        (byte ranges)
        TODO: handle all send_file args, mirror send_file's error handling
        (if it has any)
    """
    range_header = request.headers.get('Range', None)
    if not range_header:
        return send_file(path)

    size = os.path.getsize(path)
    byte1, byte2 = 0, None

    range_match = re.search(r'(\d+)-(\d*)', range_header)
    match_groups = range_match.groups()

    if match_groups[0]:
        byte1 = int(match_groups[0])

    if match_groups[1]:
        byte2 = int(match_groups[1])

    length = size - byte1
    if byte2 is not None:
        length = byte2 - byte1

    data = None
    with open(path, 'rb') as current_file:
        current_file.seek(byte1)
        data = current_file.read(length)
    content_range = 'bytes {0}-{1}/{2}'.format(byte1, byte1 + length - 1, size)
    if content_range == 'bytes=0-':
        status_code = 200
    else:
        status_code = 206
    partial_response = Response(data,
                                status_code,
                                mimetype=mimetypes.guess_type(path)[0],
                                direct_passthrough=True)

    partial_response.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(byte1, byte1 + length - 1, size))
    return partial_response


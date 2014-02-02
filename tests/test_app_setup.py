#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import unittest


class TestAppSetup(unittest.TestCase):

    def test_config_find_content(self):
        from chromecaster.chromecaster import config_app, app
        config_app()
        self.assertEqual(app.config['CHROMECAST_CONTENT'], 'static/podcasts')

    def test_index_mp3(self):
        from chromecaster.chromecaster import index_podcasts
        content_dir= os.path.join('.', 'test_content')
        files = [x for x in index_podcasts(content_dir)]
        self.assertEqual(files[0], './test_content/plang.ogg')

    def test_index_mp4(self):
        from chromecaster.chromecaster import index_videos
        content_dir= os.path.join('.', 'test_content')
        files = [x for x in index_videos(content_dir)]
        self.assertEqual(files[0], './test_content/quickcast-compressed.mp4')



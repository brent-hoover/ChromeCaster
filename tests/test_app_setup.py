#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import unittest


class TestAppSetup(unittest.TestCase):

    def setUp(self):
        self.test_root_dir = os.path.abspath(os.path.dirname(__file__))
        self.test_content_dir = os.path.join(self.test_root_dir, 'test_content')

    def test_config_find_content(self):
        from chromecaster.chromecaster import config_app, app
        config_app()
        self.assertEqual(app.config['CHROMECAST_CONTENT'], 'static/podcasts')

    def test_index_mp3(self):
        from chromecaster.chromecaster import index_podcasts
        files = [x for x in index_podcasts(self.test_content_dir)]
        self.assertEqual(os.path.split(files[0])[1], 'plang.ogg')

    def test_index_mp4(self):
        from chromecaster.chromecaster import index_videos
        files = [x for x in index_videos(self.test_content_dir)]
        self.assertEqual(os.path.split(files[0])[1], 'quickcast-compressed.mp4')

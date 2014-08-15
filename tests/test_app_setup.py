#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest


class TestAppSetup(unittest.TestCase):

    def setUp(self):
        self.test_root_dir = os.path.abspath(os.path.dirname(__file__))
        self.test_content_dir = os.path.join(self.test_root_dir, 'test_content/content_subdirectory')
        self.local_dir = os.path.relpath(self.test_content_dir, self.test_root_dir)
        self.config_file = 'config_for_test.py'

    def test_config_find_content(self):
        from chromecaster.caster import config_app, app
        config_app(filename=self.config_file, project_root=self.test_root_dir, app_instance=app)
        self.assertEqual(app.config['CHROMECAST_CONTENT'], 'test_content/content_subdirectory')

    def test_index_mp3(self):
        from chromecaster.caster import index_content, config_app, app
        config_app(filename=self.config_file, project_root=self.test_root_dir, app_instance=app)

    def test_index_mp4(self):
        from chromecaster.caster import index_content, config_app, app
        config_app(filename=self.config_file, project_root=self.test_root_dir, app_instance=app)
        index_content(self.test_root_dir, ['*.mp4'], 'video')

    def test_index(self):
        from chromecaster.caster import index, config_app, app
        config_app(filename=self.config_file, project_root=self.test_root_dir, app_instance=app)
        index(self.test_root_dir)

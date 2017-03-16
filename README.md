## ChromeCaster

It's just a local web server that serves local audio and video files so you can view them on ChromeCast.

### Quick Start

 * Symlink your content into /static/podcasts
 * Install flask
 * Run ```python chomecaster.py```
 * Visit localhost:5000
 * Browse to your audio or video file and click to watch
 * Chromecast your Tab

Ripe for improvements but so far I haven't really needed any. It's the app you could have written yourself but why do it now?

Requires:

 * Flask
 * walkdir
 * Chrome
 * ChromeCast
 * local Content

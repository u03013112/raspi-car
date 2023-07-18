import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject

class TestRtspMediaFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self):
        GstRtspServer.RTSPMediaFactory.__init__(self)

    def do_create_element(self, url):
        spec = '( udpsrc port=5000 caps="application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264" ! rtph264depay ! decodebin ! x264enc ! rtph264pay name=pay0 pt=96 )'
        return Gst.parse_launch(spec)

class GstreamerRtspServer():
    def __init__(self):
        self.server = GstRtspServer.RTSPServer()
        f = TestRtspMediaFactory()
        f.set_shared(True)
        m = self.server.get_mount_points()
        m.add_factory("/test", f)
        self.server.attach(None)

if __name__ == '__main__':
    s = GstreamerRtspServer()
    loop = GObject.MainLoop()
    loop.run()

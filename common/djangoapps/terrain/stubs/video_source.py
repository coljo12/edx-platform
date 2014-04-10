"""
Serve HTML5 video sources for acceptance tests
"""
from SimpleHTTPServer import SimpleHTTPRequestHandler
from .http import StubHttpService
import os

from logging import getLogger
LOGGER = getLogger(__name__)


class VideoSourceRequestHandler(SimpleHTTPRequestHandler):
    """
    Request handler for serving video sources locally.
    """
    def translate_path(self, path):
        """
        Remove any extra parameters from the path.
        For example /gizmo.mp4?1397160769634
        becomes /gizmo.mp4
        """
        root_dir = self.server.config.get('root_dir')
        path = '{}{}'.format(root_dir, path)
        return path.split('?')[0]


class VideoSourceHttpService(StubHttpService):
    """
    Simple HTTP server for serving HTML5 Video sources locally for tests
    """
    HANDLER_CLASS = VideoSourceRequestHandler

    def __init__(self, port_num=0):
        """
        Configure the server to listen on localhost.
        Default is to choose an arbitrary open port.
        """
        # Files are automatically served from the current directory
        # so we need to change it, start the server, then set it back.
        orig_wd = os.getcwd()

        # Set the path to root, which we will add on to with a setting
        # for root_dir when we start it up.
        os.chdir('/')

        # Set up a dict for config, which will be used to set the
        # root directory we are serving files from.
        self.config = dict()

        # Start the server in a separate thread
        StubHttpService.__init__(self, port_num=port_num)

        # Reset the current working directory
        os.chdir(orig_wd)

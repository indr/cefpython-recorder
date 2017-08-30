"""
Example of using CEF browser in off-screen rendering mode
(windowless) to create a screenshot of a web page. This
example doesn't depend on any third party GUI framework.
This example is discussed in Tutorial in the Off-screen
rendering section.

With optionl arguments to this script you can resize viewport
so that screenshot includes whole page with height like 5000px
which would be an equivalent of scrolling down multiple pages.
By default when no arguments are provided will load cefpython
project page on Github with 5000px height.

Usage:
    python capture.py
    python capture.py https://github.com/cztomczak/cefpython 1024 5000 25
    python capture.py https://www.google.com/ncr 1024 768 25

Tested configurations:
- CEF Python v57.0+
"""

from cefpython3 import cefpython as cef
import os
import platform
import signal
import subprocess
import sys
import time


# Config
URL = "https://github.com/cztomczak/cefpython"
VIEWPORT_SIZE = (1024, 5000)
FPS = 25
SCREENSHOT_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "fifo.bgra")


def main():
    check_versions()
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    command_line_arguments()
    # Off-screen-rendering requires setting "windowless_rendering_enabled"
    # option, so that RenderHandler callbacks are called.
    cef.Initialize(settings={"windowless_rendering_enabled": True},
                   commandLineSwitches={"disable-gpu": ""})
    print("[capture.py] Open write {}".format(SCREENSHOT_PATH))
    global fifo
    fifo = open(SCREENSHOT_PATH, 'w')
    global browser
    browser = create_browser()
    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)
    cef.MessageLoop()
    print("[capture.py] Shutting down")
    cef.Shutdown()


def exit_gracefully(signum, frame):
    global browser
    print("")
    # print(os.linesep) # "[capture.py] Signal " + str(signum))
    cef.PostTask(cef.TID_UI, exit_app, browser)


def check_versions():
    print("[capture.py] CEF Python {ver}".format(ver=cef.__version__))
    print("[capture.py] Python {ver} {arch}".format(
          ver=platform.python_version(), arch=platform.architecture()[0]))
    assert cef.__version__ >= "57.0", "CEF Python v57.0+ required to run this"


def command_line_arguments():
    if len(sys.argv) == 5:
        url = sys.argv[1]
        width = int(sys.argv[2])
        height = int(sys.argv[3])
        fps = int(sys.argv[4])
        if url.startswith("http://") or url.startswith("https://"):
            global URL
            URL = url
        else:
            print("[capture.py] Error: Invalid url argument")
            sys.exit(1)
        if width > 0 and height > 0:
            global VIEWPORT_SIZE
            VIEWPORT_SIZE = (width, height)
        else:
            print("[capture.py] Error: Invalid width and height")
            sys.exit(1)
        if fps > 0:
            global FPS
            FPS = fps
        else:
            print("[capture.py] Error: invalid fps")

    elif len(sys.argv) > 1:
        print("[capture.py] Error: Expected arguments: url width height fps")
        sys.exit(1)


def create_browser():
    # Create browser in off-screen-rendering mode (windowless mode)
    # by calling SetAsOffscreen method. In such mode parent window
    # handle can be NULL (0).
    parent_window_handle = 0
    window_info = cef.WindowInfo()
    window_info.SetAsOffscreen(parent_window_handle)
    print("[capture.py] Viewport size: {size}"
          .format(size=str(VIEWPORT_SIZE)))
    print("[capture.py] Max frames per second: {fps}"
          .format(fps=FPS))
    print("[capture.py] Loading url: {url}"
          .format(url=URL))
    browser = cef.CreateBrowserSync(window_info=window_info,
                                    settings={"windowless_frame_rate": FPS},
                                    url=URL)
    browser.SetClientHandler(LoadHandler())
    browser.SetClientHandler(RenderHandler())
    browser.SendFocusEvent(True)
    # You must call WasResized at least once to let know CEF that
    # viewport size is available and that OnPaint may be called.
    browser.WasResized()
    return browser


def exit_app(browser):
    # Important note:
    #   Do not close browser nor exit app from OnLoadingStateChange
    #   OnLoadError or OnPaint events. Closing browser during these
    #   events may result in unexpected behavior. Use cef.PostTask
    #   function to call exit_app from these events.
    print("[capture.py] Close browser and exit app")
    browser.CloseBrowser()
    cef.QuitMessageLoop()
    global fifo
    if fifo:
        fifo.close()


class LoadHandler(object):
    def OnLoadingStateChange(self, browser, is_loading, **_):
        """Called when the loading state has changed."""
        if not is_loading:
            # Loading is complete
            # sys.stdout.write(os.linesep)
            print("[capture.py] Web page loading is complete")
            # See comments in exit_app() why PostTask must be used
            # cef.PostTask(cef.TID_UI, exit_app, browser)

    def OnLoadError(self, browser, frame, error_code, failed_url, **_):
        """Called when the resource load for a navigation fails
        or is canceled."""
        if not frame.IsMain():
            # We are interested only in loading main url.
            # Ignore any errors during loading of other frames.
            return
        print("[capture.py] ERROR: Failed to load url: {url}"
              .format(url=failed_url))
        print("[capture.py] Error code: {code}"
              .format(code=error_code))
        # See comments in exit_app() why PostTask must be used
        cef.PostTask(cef.TID_UI, exit_app, browser)


current_milli_time = lambda: int(round(time.time() * 1000))


class RenderHandler(object):
    def __init__(self):
        self.frameCount = 0
        self.lastTime = current_milli_time()

    def GetViewRect(self, rect_out, **_):
        """Called to retrieve the view rectangle which is relative
        to screen coordinates. Return True if the rectangle was
        provided."""
        # rect_out --> [x, y, width, height]
        rect_out.extend([0, 0, VIEWPORT_SIZE[0], VIEWPORT_SIZE[1]])
        return True

    def OnPaint(self, browser, element_type, paint_buffer, **_):
        """Called when an element should be painted."""
        self.frameCount = self.frameCount + 1
        time = current_milli_time()
        fps = 1000.0 / (time - self.lastTime)
        self.lastTime = time

        sys.stdout.write("[capture.py] frame={number: >5} fps={fps: >6.2f}\r"
                .format(number=self.frameCount, fps=fps))
        # sys.stdout.flush()

        if element_type == cef.PET_VIEW:
            try:
                global fifo
                fifo.write(paint_buffer.GetString())
                fifo.flush()
            except Exception as ex:
                print("[capture.py] Error {0}".format(str(ex)))
                # See comments in exit_app() why PostTask must be used
                cef.PostTask(cef.TID_UI, exit_app, browser)
        else:
            raise Exception("Unsupported element_type in OnPaint")

    
if __name__ == '__main__':
    main()

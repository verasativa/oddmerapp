from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from datetime import timedelta
import PIL, time
from plyer import gps, uniqueid
from kivy.clock import mainthread
from kivy.utils import platform
from queue import LifoQueue
from kivy.config import ConfigParser

config = ConfigParser()
config.read('config.ini')

class CameraClick(FloatLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timer = timedelta(seconds=config.getint('camera', 'interval'))
        Clock.schedule_interval(self.tick, 1)

    def save_img(self):
        texture = self.ids['camera'].texture
        image_data = texture.pixels
        size = texture.size
        fmt = texture.colorfmt.upper()
        pil_image = PIL.Image.frombytes(mode=fmt, size=size, data=image_data)
        time_str = time.strftime("%Y.%m.%d.%H.%M.%S")
        filename = f'{uniqueid.id.decode()}.{time_str}.jpg'
        pil_image.convert('RGB').save(filename)

    def tick(self, *args):
        self.timer = self.timer - timedelta(seconds=1)
        counter = self.ids['counter']
        counter.text = str(self.timer)
        if self.timer == timedelta(0):
            counter.text = f'[color=#FF0000]{str(self.timer)}[/color]'
            self.save_img()
            self.ids['camera'].play = False
            self.timer = timedelta(seconds=config.getint('camera', 'interval'))

        elif self.timer == (timedelta(seconds=config.getint('camera', 'interval')) - timedelta(seconds=1)):
            self.ids['camera'].play = True

class OddmerappApp(App):
    """Basic kivy app

    Edit oddmerapp.kv to get started.
    """
    def request_android_permissions(self):
        """
        Since API 23, Android requires permission to be requested at runtime.
        This function requests permission and handles the response via a
        callback.
        The request will produce a popup if permissions have not already been
        been granted, otherwise it will do nothing.
        """
        from android.permissions import request_permissions, Permission

        def callback(permissions, results):
            """
            Defines the callback to be fired when runtime permission
            has been granted or denied. This is not strictly required,
            but added for the sake of completeness.
            """
            if all([res for res in results]):
                print("callback. All permissions granted.")
            else:
                print("callback. Some permissions refused.")

        request_permissions([Permission.ACCESS_COARSE_LOCATION,
                             Permission.ACCESS_FINE_LOCATION], callback)

    def build(self):
        try:
            gps.configure(on_location=self.on_location,  on_status=self.on_status)
        except NotImplementedError:
            import traceback
            traceback.print_exc()
            self.gps_status = 'GPS is not implemented for your platform'

        if platform == "android":
            print("gps.py: Android detected. Requesting permissions")
            self.request_android_permissions()

        return CameraClick()


    def start(self, minTime, minDistance):
        gps.start(minTime, minDistance)


    def stop(self):
        gps.stop()


    @mainthread
    def on_location(self, **kwargs):
        self.gps_location = '\n'.join([
            '{}={}'.format(k, v) for k, v in kwargs.items()])


    @mainthread
    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)


    def on_pause(self):
        gps.stop()
        return True


    def on_resume(self):
        gps.start(1000, 0)
        pass
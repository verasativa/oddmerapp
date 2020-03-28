from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.clock import Clock
from  oddmerapp import settings
from datetime import timedelta
import PIL, time


class CameraClick(AnchorLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timer = timedelta(seconds=settings.interval)
        Clock.schedule_interval(self.tick, 1)

    def save_img(self):
        texture = self.ids['camera'].texture
        image_data = texture.pixels
        size = texture.size
        fmt = texture.colorfmt.upper()
        pil_image = PIL.Image.frombytes(mode=fmt, size=size, data=image_data)
        timestr = time.strftime("%Y%m%d_%H%M%S")
        pil_image.convert('RGB').save(f'IMG_{timestr}.jpg')

    def tick(self, *args):
        self.timer = self.timer - timedelta(seconds=1)
        counter = self.ids['counter']
        counter.text = str(self.timer)
        if self.timer == timedelta(0):
            counter.text = f'[color=#FF0000]{str(self.timer)}[/color]'
            self.save_img()
            self.ids['camera'].play = False
            self.timer = timedelta(seconds=settings.interval)

        elif self.timer == (timedelta(seconds=settings.interval) - timedelta(seconds=1)):
            self.ids['camera'].play = True

class OddmerappApp(App):
    """Basic kivy app

    Edit oddmerapp.kv to get started.
    """

    def build(self):
        return CameraClick()
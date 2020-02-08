import sys
from unittest.mock import MagicMock
from PIL import Image

picamera = MagicMock()


class PiCameraMock:
    def capture(self, stream, test, test2):
        img = Image.new("RGBA", (50, 50), (256, 0, 0))
        img.save(stream, "png")


picamera.PiCamera = PiCameraMock

sys.modules["picamera"] = picamera

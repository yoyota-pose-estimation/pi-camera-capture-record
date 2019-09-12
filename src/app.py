import os
import datetime
from picamera import PiCamera
from flask import Flask, request

picture_dir = '/home/pi/Pictures'
app = Flask(__name__)


@app.route("/<section>")
def main(section):
    section_dir = os.path.join(picture_dir, section)
    if not os.path.exists(section_dir):
        os.mkdir(section_dir)

    with PiCamera() as camera:
        camera.rotation = 180
        today = str(datetime.datetime.today()) + '.jpg'
        save_path = os.path.join(section_dir, today)
        camera.capture(save_path)
        return 'ok'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

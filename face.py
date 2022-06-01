from __future__ import print_function

from Queue import Queue, Empty
import logging
from threading import Thread
import time

import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))


PIN_A = 2
PIN_B = 3
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_A, GPIO.OUT)
GPIO.setup(PIN_B, GPIO.OUT)
GPIO.output(PIN_A, GPIO.LOW)
GPIO.output(PIN_B, GPIO.LOW)


def tick(tick_pin):
    logging.info(tick_pin)
    GPIO.output(tick_pin, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(tick_pin, GPIO.LOW)
    time.sleep(0.1)


def face_recognizer(q):
    time.sleep(1)  # camera warmup
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE,
        )
        has_face = faces != ()
        if has_face:
            logging.info('Found face!')
        q.put(has_face)
        rawCapture.truncate(0)


def main():
    start = int(time.time())
    ticks = 0
    tick_pin = PIN_A

    q = Queue(maxsize=1)
    has_face = False

    worker = Thread(target=face_recognizer, args=(q,))
    worker.setDaemon(True)
    worker.start()

    while True:
        try:
            has_face = q.get_nowait()
        except Empty:
            pass  # use last value

        elapsed = int(time.time() - start)
        if ticks < elapsed and not has_face:
            tick(tick_pin)
            ticks += 1
            tick_pin = PIN_A if tick_pin == PIN_B else PIN_B


if __name__ == '__main__':
    main()

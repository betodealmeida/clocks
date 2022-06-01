# clocks

These are the files from an art project I worked on at Facebook, with an artist in residence (Elana Schlenker) back in 2016. It's a wall clock that stops ticking when someone looks at it; when the person looks away it ticks 2.5x faster until it catches up to the correct time.

You can see a video [here](https://youtu.be/wTJTtdlqP4g):

[![Clock video](https://img.youtube.com/vi/wTJTtdlqP4g/0.jpg)](http://www.youtube.com/watch?v=wTJTtdlqP4g)

It works by running a Python script (`face.py`) on a Raspberry Pi, processing frames from the camera to identify faces. Without any faces the Raspberry Pi will send a voltage signal every second to the clock mechanism, making it tick. When a face is detected the signals accumulate, being sent when there's no longer a face.

The circuit is pretty simple: two wires (A and B) from the Raspberry Pi are connected to 4 transitors. A signal on wire A makes the current flow through the clock in one direction, and a signal on wire B makes it flow on the opposite direction. To make the clock tick we need to send alternating signals to pins A and B, one per second (ie: A, 1 second, B, 1 second, A, etc.).

I don't have photos of the interior of the clock mechanism, but you want to solder the 2 wires to the coil. Figure `mechanism.jpg` shows how to do this.

The model I used (`haarcascade_frontalface_default.xml`) detects faces, so the clock will stop whenever someone is facing the clock, even if their eyes are closed. It should be possible to use a differnet model to detect that the person is actually looking at the clock/camera.

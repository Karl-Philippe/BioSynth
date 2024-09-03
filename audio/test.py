from pyo import *

# Initialize the Pyo server with the desired audio backend
s = Server(audio="portaudio").boot()
s.start()

f = Fader(fadein=0.1, fadeout=0.5, dur=1, mul=0.3)
a = Sine(freq=440, mul=f)
lfo = LFO(freq=4, mul=0.5, add=0.2)
d = Delay(a, delay=lfo, feedback=lfo).out()
p = Pattern(f.play, time=2).play()

s.gui(locals())

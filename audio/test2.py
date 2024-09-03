from pyo import *
import time 

s = Server().boot()
s.start()

wav = SquareTable()

beat = Metro(time=0.125, poly=7).play()

envelope = CosTable([(0,0),(100,1),(500,0.3), (8191,0)])

amplitude = TrigEnv(beat, table=envelope, dur=0.25, mul=0.7)

pitch = TrigXnoiseMidi(beat, dist=3, scale=0, mrange=(24,48))

oscillator = Osc(table=wav, freq=pitch, mul=amplitude).out()

time.sleep(5)
from pyo import *
from time import sleep

class Synth:
    def __init__(self):
        self.server = Server().boot()
        self.server.start()

        self.freqfactor = 1
        self.freq = 440
        self.setup_synth()
        
    def setup_synth(self):
        self.wav = SquareTable()
        self.beat = Metro(time=0.125, poly=7).play()
        self.envelope = CosTable([(0,0),(100,1),(500,0.3), (8191,0)])
        self.amplitude = TrigEnv(self.beat, table=self.envelope, dur=0.25, mul=0.7)
        self.pitch = TrigXnoiseMidi(self.beat, dist=3, scale=0, mrange=(24,48))
        self.oscillator = Osc(table=self.wav, freq=self.pitch*self.freqfactor, mul=self.amplitude).out()
        
        #self.wav = SincTable()
        #self.oscillator = Osc(table=self.wav, freq=self.freq, mul=0.1).out()  

    def update_sound(self, heart_rate, hand_positions):
        self.freq = 330
        self.setup_synth()
        
    def play_sound(self):
        self.oscillator.out()
        
    def stop_sound(self):
        self.oscillator.stop()

    def cleanup(self):
        # Clean up resources if needed
        pass

if __name__ == "__main__":
    # If you run supercollider_controller.py as a standalone script for testing
    synth_controller = Synth()
    sleep(10)

    # Test update synth
    synth_controller.update_sound(240, [0.5, 0.7])
    
    sleep(10)
    
    #synth_controller.stop_sound()

    # Cleanup and close the controller
    #synth_controller.cleanup()




from pyo import *

class SynthController:
    def __init__(self):
        self.server = Server().boot()
        self.server.amp = 0.1

        # Initialize sine wave oscillators
        self.sound = Sine(freq=440, mul=0.5).out()

    def update_sound(self, heart_rate, hand_positions):
        # Update the frequency of sine wave oscillators
        self.freq = heart_rate
        for i, osc in enumerate(self.sine_oscillators):
            osc.setFreq(self.freq * (2 * (i + 1) - 1))
        print(hand_positions)

    def cleanup(self):
        self.server.stop()
        self.server.shutdown()

if __name__ == "__main__":
    synth_controller = SynthController()
    print(synth_controller.freq)

    # Test update synth
    synth_controller.update_sound(240, [0.5, 0.7])
    print(synth_controller.freq)

    # Cleanup and close the controller
    synth_controller.cleanup()

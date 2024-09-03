from pythonosc import osc_message_builder
from pythonosc import udp_client

class SuperColliderController:
    def __init__(self, sc_ip='localhost', sc_port=57110):
        self.sc_ip = sc_ip
        self.sc_port = sc_port
        self.client = udp_client.UDPClient(address=sc_ip, port=sc_port)

    def update_sound(self, heart_rate, hand_positions, trigger_synth=False):
        # Create and send OSC messages to control SuperCollider
        self.send_osc_message("/heart_rate", heart_rate)
        self.send_osc_message("/hand_positions", hand_positions)
        
        if trigger_synth:
            self.send_osc_message("/trigger_synth", 1)  # Trigger the synth

    def send_osc_message(self, address, value):
        msg = osc_message_builder.OscMessageBuilder(address=address)
        msg.add_arg(value)
        msg = msg.build()
        self.client.send(msg)

    def cleanup(self):
        # Clean up resources if needed
        pass

if __name__ == "__main__":
    # If you run supercollider_controller.py as a standalone script for testing
    sc_controller = SuperColliderController()

    # Simulate sending OSC messages (for testing purposes)
    sc_controller.update_sound(160, [0.5, 0.7], trigger_synth=True)  # Trigger the synth

    # Cleanup and close the controller
    sc_controller.cleanup()

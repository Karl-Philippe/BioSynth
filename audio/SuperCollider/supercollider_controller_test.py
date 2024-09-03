from pythonosc import udp_client

# Create an OSC client to send messages to SuperCollider's default OSC port (57110)
client = udp_client.SimpleUDPClient("127.0.0.1", 57110)

# Send a message to start the synth with custom parameters
client.send_message("/s_new", ["mySynth", 1001, 1, 1, "freq", 220, "dur", 2])

# Sleep for a duration to hear the sound
import time
time.sleep(2)

# Send a message to free the synth
client.send_message("/n_free", [1001])

import sounddevice as sd
import numpy as np
import threading
import soundfile  # For saving audio files

fs = 44100  # Sampling frequency
channels = 2  # Number of channels

audio_data = []  # Initialize empty list to store recorded data
stream = None  # Initialize the stream variable globally

recording = False  # Flag to indicate recording status

def callback(indata, frames, time, status):
    global audio_data
    if recording:  # Only append data if recording is active
        audio_data.append(indata.copy())

def start_recording():
    global recording
    global stream

    # Attempt to create an input stream directly using sounddevice
    stream = sd.InputStream(device="BlackHole 2ch", channels=channels, samplerate=fs, callback=callback, blocksize=1024)

    try:
        recording = True  # Set the recording flag to True
        stream.start()  # Start the stream
        threading.Thread(target=_recording_loop, args=(stream,)).start()  # Start the recording loop in a separate thread
    except sd.PortAudioError:
        print("Failed to create input stream using sounddevice. PyAudio might be required for hardware access.")
        return  # Exit if stream creation fails

def stop_recording():
    global recording
    global stream

    try:
        recording = False  # Stop appending data to the list
        stream.stop()  # Now accessible since stream is global
        stream.close()  # Close the stream after stopping
    except sd.PortAudioError:
        print("Failed to stop or close the stream.")

    # Concatenate the recorded data into a single NumPy array
    recorded_audio = np.concatenate(audio_data)

    # Save the recording as a WAV file using soundfile
    soundfile.write('output.wav', recorded_audio, fs)

    # Reset the audio data list for future recordings
    audio_data.clear()

def _recording_loop(stream):
    while recording:
        sd.sleep(10000)  # Effectively infinite sleep to keep the stream running

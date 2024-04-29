import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter

recording_duration = 5
def record_audio(filename, duration=recording_duration, rate=10000, chunk=1024, channels=1, format=pyaudio.paInt16):
    audio = pyaudio.PyAudio()

    # Open the microphone
    stream = audio.open(format=format,
                        channels=channels,

                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)

    print("Recording...")

    frames = []
    for i in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("Finished recording.")

    # Stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio to a file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(audio.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

def play_audio(filename):
    # Open the audio file
    wf = wave.open(filename, 'rb')
    print(wf)

    audio = pyaudio.PyAudio()

    # Open stream to play audio
    stream = audio.open(format=audio.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
    print("Playing back...")

    # Read data in chunks and play
    data = wf.readframes(1024)
    while data:
        stream.write(data)
        data = wf.readframes(1024)

    # Stop Playback
    stream.stop_stream()
    stream.close()
    audio.terminate()

    print("Playback finished.")

def plot_waveform(filename):
    # Open the audio file
    wf = wave.open(filename, 'rb')

    # Read the audio frames
    signal = wf.readframes(-1)
    print('length sig level 1: '+str(len(signal)))
    signal = np.frombuffer(signal, dtype=np.int16)
    print('length sig level 2: ' + str(len(signal)))

    # Get the time axis for the waveform
    time = np.linspace(0, len(signal) / wf.getframerate(), num=len(signal))

    # Plot the waveform
    plt.figure(figsize=(10, 3))
    plt.plot(time, signal, color='b')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Recorded Audio Waveform')
    plt.grid(True)
    plt.show()

def apply_lowpass_filter(filename, cutoff_freq):
    wf = wave.open(filename, 'rb')
    # Read the audio frames
    signal = wf.readframes(-1)
    signal = np.frombuffer(signal, dtype=np.int16)
    sample_rate = wf.getframerate()
    nyquist_freq = 0.5 * sample_rate
    normal_cutoff = cutoff_freq / nyquist_freq
    b, a = butter(6, normal_cutoff, btype='low', analog=False)
    filtered_signal = lfilter(b, a, signal)
    return filtered_signal

if __name__ == "__main__":
    filename = "recorded_audio.wav"
    record_audio(filename)
    play_audio(filename)
    plot_waveform(filename)

    # Define filter parameters
    cutoff_frequency = 4000  # Adjust this according to your needs
    # Apply low-pass filter
    filtered_signal = apply_lowpass_filter(filename, cutoff_frequency)
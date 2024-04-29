import pyaudio
import wave



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

if __name__ == "__main__":
    filename = "recorded_audio.wav"
    play_audio(filename)
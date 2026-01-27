import librosa
import soundfile as sf
import sys

# usage: python convert_to_mono.py input.wav output.wav

input_path = sys.argv[1]
output_path = sys.argv[2]

audio, sr = librosa.load(input_path, sr=None, mono=True)
sf.write(output_path, audio, sr)

print("Saved mono file to:", output_path)

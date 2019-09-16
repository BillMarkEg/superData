import pyaudio
import wave
import subprocess
import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('output.avi',fourcc, 30.0, (640,480))

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 7
WAVE_OUTPUT_FILENAME = "voice.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
    _, frame = cap.read()

    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # frame = cv2.flip(frame, 1)

    # write the flipped frame
    out.write(frame)
    print(time.clock())
    #cv2.imshow('ana', frame)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

#p=subprocess.Popen('python' , shell=True, stdout=subprocess.PIPE)


#print(p.communicate()[0])
#cmd = 'avconv -v debug -i audio.wav -i ouput.mp4 -c:a libmp3lame -qscale 20 -shortest output.mov'
## ffmpeg -i voice.wav -i output.avi -acodec copy -vcodec copy -f avi output22.avi
subprocess.Popen('ffmpeg -i voice.wav -i output.avi -acodec copy -vcodec copy -f avi output22.avi' ,  stdout=subprocess.PIPE, shell=True)         # Muxing Done
print('Muxing Done')

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
cap.release()
out.release()
cv2.destroyAllWindows()
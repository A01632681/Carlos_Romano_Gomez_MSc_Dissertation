import sounddevice as sd
import soundfile as sf
import pyzed.sl as sl
import os
import CameraRecordingStoring as zt
from threading import Thread

recnum = 1
test_num = input('Insert test number: ')

sd.default.device=24

def record_audio(recording_file, duration):
    print('Start Audio')
    sample_rate = 44100  # Adjust this to match your desired sample rate
    frames = int(duration * sample_rate)
    audio = sd.rec(frames, channels=2, dtype='float32')
    print('Flag 1')
    sd.wait()
    print('Flag 2')
    sf.write(recording_file, audio, sample_rate)
    print('Finish audio')

if __name__ == "__main__":
    try:
        while True:
            filepath = '/home/nvidia/Downloads/AudioVideo/Runs/{0}'.format(test_num)
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            
            audio_file = filepath + '/{0}.wav'.format(recnum)
            video_file = filepath + '/{0}.svo'.format(recnum)

            record_duration = 5.0  # Duration to record in seconds

            threads = [Thread(target = zt.Recording, args = (video_file,record_duration), daemon=True, name='Video'), 
                       Thread(target = record_audio, args = (audio_file, record_duration), daemon=True, name='Audio')]
            
            # Func1 and Func2 run in separate threads
            for thread in threads:
                print(thread.name)
                thread.start()

            # Wait until both Func1 and Func2 have finished
            for thread in threads:
                print(thread.name)
                thread.join()
                            
            print('Finish Both!')
            recnum += 1

    except KeyboardInterrupt:
        print('interrupted!')
        exit()
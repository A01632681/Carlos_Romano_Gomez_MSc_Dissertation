import pyzed.sl as sl
import os
import CameraRecordingStoring as zt

key = ''
seconds=5
flag = True
recnum = 1

test_num = input('Insert test number: ')

try:
    while True:
        filepath = '/home/nvidia/Downloads/rectest/{0}'.format(test_num)
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        filepath += '/rec{0}.svo'.format(recnum)
        print("SVO file path set to: {0}".format(filepath))
        zt.Recording(filepath,seconds)
        recnum += 1
except KeyboardInterrupt:
    print('interrupted!')


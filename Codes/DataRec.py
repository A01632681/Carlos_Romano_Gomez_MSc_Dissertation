import pyzed.sl as sl
import os
import zedtests as zt

# Create init variables
seconds=1000
recnum = 1

test_num = input('Insert test number: ')

try:
    while True: # Record until the user presses ctrl-c
        # Create a new folder for each recording
        filepath = '/home/nvidia/Downloads/rectest/{0}'.format(test_num)
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        filepath += '/rec{0}.svo'.format(recnum)
        print("SVO file path set to: {0}".format(filepath))
        zt.Recording(filepath,seconds) # Record
        recnum += 1
except KeyboardInterrupt: # If the user presses ctrl-c exit
    print('interrupted!')
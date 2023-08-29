import numpy as np
import pyzed.sl as sl
import os

directory = '/home/nvidia/Downloads/rectest/path3incomplete/'

for file in os.listdir(directory):
    filename = os.fsdecode(file)

    print(filename)

    # Check if the file is an SVO file
    if filename.endswith(".svo"):
        foldername = filename[:-4] + '/'
        path = directory+foldername
        if not os.path.exists(path):
            os.makedirs(path)

        # Create a ZED camera object
        zed = sl.Camera()

        # Set configuration parameters
        input_type = sl.InputType()
        input_type.set_from_svo_file(directory+filename)
        init = sl.InitParameters(input_t=input_type, svo_real_time_mode=False)
        init.depth_minimum_distance = 0.15 # Set the minimum depth perception distance to 15cm
        init.depth_maximum_distance = 10       # Set the maximum depth perception distance to 10 m
        init.coordinate_units = sl.UNIT.METER

        # Open the camera
        status = zed.open(init)
        # Check camera
        if status != sl.ERROR_CODE.SUCCESS:
            print(repr(status))
            print('Exiting')
            exit()

        # Get image and depth image
        runtime = sl.RuntimeParameters()
        image = sl.Mat()
        depth = sl.Mat()
        frames = zed.get_svo_number_of_frames()
        zed.set_svo_position(0)
        frame_num = 1

        while frame_num<=frames:
            err = zed.grab(runtime)
            if err == sl.ERROR_CODE.SUCCESS:
                # Get images
                zed.retrieve_image(image, sl.VIEW.LEFT)
                zed.retrieve_image(depth, sl.VIEW.DEPTH)

                img = sl.ERROR_CODE.FAILURE
                while img != sl.ERROR_CODE.SUCCESS:
                    # Save image
                    imgpath = path + "Img_{0}.png".format(frame_num)
                    img = image.write(imgpath, compression_level = 100)
                
                    # Save depth image
                    depthpath = path + "Dep_{0}.png".format(frame_num)
                    dep = depth.write(depthpath, compression_level = 100)
                    
                    print("Saving {2} image: {0} and depth: {1}".format(repr(img),repr(dep),frame_num))
                    if img == sl.ERROR_CODE.SUCCESS:
                        break
            frame_num+=1 # Increment frame count
            if frame_num == frames+1: # If the frame count is equal to the number of frames
                break

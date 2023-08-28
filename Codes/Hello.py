import pyzed.sl as sl
from time import process_time
import math
import os
import numpy as np
import cv2

exit_signal = False
seconds = 45

# -----------------------------Recording PNG---------------------------------------------
def Recording(filepath,frames):
    # Create a ZED camera object
    zed = sl.Camera()

    # Set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.VGA # Use VGA video mode
    init_params.camera_fps = 60  # Set fps at 60
    init_params.depth_mode = sl.DEPTH_MODE.PERFORMANCE  # Use PERFORMANCE depth mode
    init_params.depth_minimum_distance = 0.15 # Set the minimum depth perception distance to 15cm
    init_params.depth_maximum_distance = 10       # Set the maximum depth perception distance to 10 m
    init_params.coordinate_units = sl.UNIT.METER

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print(repr(err))
        exit(1)

    # Enable recording with the filename specified in argument
    recordingParameters = sl.RecordingParameters()
    recordingParameters.compression_mode = sl.SVO_COMPRESSION_MODE.LOSSLESS
    recordingParameters.video_filename = filepath
    err = zed.enable_recording(recordingParameters)
    if err != sl.ERROR_CODE.SUCCESS:
        print(repr(err))
        exit(1)

    # Start SVO recording
    runtime = sl.RuntimeParameters()
    print("SVO is Recording.")
    frames_recorded = 0

    t1 = process_time()

    # Record SUPPOSEDLY for 3 seconds
    while frames_recorded<frames:
        if zed.grab(runtime) == sl.ERROR_CODE.SUCCESS:
            frames_recorded += 1
            print("Frame count: " + str(frames_recorded), end="\r")

    t2 = process_time()
    print("Time elapsed: " + str(t2-t1) + ' Frames: ' + str(frames_recorded))
# --------------------------------Storing PNG---------------------------------------------
def storing(filepath,filesave):
    # Create a ZED camera object
    zed = sl.Camera()

    # Set configuration parameters
    input_type = sl.InputType()
    input_type.set_from_svo_file(filepath)
    init = sl.InitParameters(input_t=input_type, svo_real_time_mode=False)
    init.depth_minimum_distance = 0.15 # Set the minimum depth perception distance to 15cm
    init.depth_maximum_distance = 10       # Set the maximum depth perception distance to 10 m
    init.coordinate_units = sl.UNIT.METER

    # Open the camera
    status = zed.open(init)
    # Check camera
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit()

    # Get image and depth image
    runtime = sl.RuntimeParameters()
    image = sl.Mat()
    depth = sl.Mat()
    point_cloud = sl.Mat()
    global t1, t2, v1
    t2 = []
    v1 = []

    frame_num = 1
    frames = zed.get_svo_number_of_frames()
    zed.set_svo_position(0)

    # Start SVO reading thread
    while frame_num<=frames:
        err = zed.grab(runtime)
        if err == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_image(image, sl.VIEW.LEFT)
            zed.retrieve_image(depth, sl.VIEW.DEPTH)
            x2=[]

            # Get the 3D point cloud values for pixel (i, j)
            zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA)
            time1 = process_time()
            tensor_building(depth,point_cloud,x2)
            time2 = process_time()
            print('Tensor building time: ', time2-time1)
            print(np.shape(t2))

            time5 = process_time()
            saving_image(image,depth,point_cloud,frame_num,filesave) # Save image and depth image
            time6 = process_time()
            print('Saving image time: ', time6-time5)

            time3 = process_time()
            depthtensor(frame_num,filesave,zed)
            time4 = process_time()
            print('Depth tensor time: ', time4-time3)
            print('')
            frame_num+=1
        else:
            print(repr(err))

    zed.close()
    print("\nFINISH")
 
def saving_image(mat,depthmat,point,frame,path):
    img = sl.ERROR_CODE.FAILURE
    while img != sl.ERROR_CODE.SUCCESS:
       
        # Save image
        imgpath = path + "Img_{0}.png".format(frame)
        img = mat.write(imgpath, compression_level = 100)
       
        # Save depth image
        depthpath = path + "Dep_{0}.png".format(frame)
        dep = depthmat.write(depthpath, compression_level = 100)

        # #Save PCD file
        pcdpath = path + "PC_{0}.pcd".format(frame)
        point.write(pcdpath, compression_level = 100)

        print("Saving {2} image: {0} and depth: {1}".format(repr(img),repr(dep),frame))
       
        if img == sl.ERROR_CODE.SUCCESS:
            break
# ----------------------------------------------------------------------------
def depthtensor(frame,filesave,zed):
    path = filesave + "Dep_{0}.png".format(frame)
    print("Depth min and max range values: {0}, {1}".format(zed.get_init_parameters().depth_minimum_distance, zed.get_init_parameters().depth_maximum_distance))
    depth_img = cv2.imread(path)
    depth_img = cv2.cvtColor(depth_img, cv2.COLOR_BGR2GRAY)
    print('Min: ',depth_img.min(),' Max: ',depth_img.max())
    depth_norm = (depth_img - depth_img.min())/(depth_img.max() - depth_img.min())
    v1.append(depth_norm)
    print(depth_img)
    print(depth_norm)
# -----------------------------Tensor Building---------------------------------------------
def tensor_building(image,point,x2):
    for i in range(image.get_height()):
        for j in range(image.get_width()):
            # # Tensor building
            point3D = point.get_value(i, j)
            x2.append(point3D)
    t2.append(x2)
# --------------------------------Main---------------------------------------------
def main():
    # Create a svo file name and path
    name = input("Enter the name of the SVO file: ")
    name = name + ".svo"
    path = input("Do you want to use the default path (/home/nvidia/Downloads/test/) [y/n]?: ")
    if path == "y":
        filepath = '/home/nvidia/Downloads/test/'
    elif path == "n":
        filepath = input("Enter the path to the SVO file: ")
        if not os.path.exists(filepath):
            os.makedirs(filepath)

    # Set the filepath
    filesave = filepath
    filepath = filepath + name
    print()
    print("SVO file path set to: {0}".format(filepath))
    print()

    # Recording and storing
    option = input("Do you want to record or store [r/s]?: ")
    if option == "r":
        print("Recording will now start, use Ctrl-C to stop recording.")
        Recording(filepath,seconds)
        print("Recording complete.")
    elif option == "s":
        print("Converting SVO to PNG.")
        storing(filepath,filesave)
        print("Conversion complete.")
        print('T1: {0}, T2: {1}'.format(t1,t2))

if __name__ == "__main__":
    main()
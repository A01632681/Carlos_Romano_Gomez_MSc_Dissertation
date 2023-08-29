import pyzed.sl as sl
from time import process_time

exit_signal = False

# -----------------------------Recording PNG---------------------------------------------
def Recording(filepath):
    """
    This function records a SVO file for SUPPOSEDLY 3 seconds and stores it
    in the filepath specified.    
    """

    # Create a ZED camera object
    zed = sl.Camera()

    # Set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.VGA # Use VGA video mode
    init_params.camera_fps = 15  # Set fps at 15
    init_params.depth_mode = sl.DEPTH_MODE.PERFORMANCE  # Use PERFORMANCE depth mode
    init_params.coordinate_units = sl.UNIT.METER # Set units in meters

    # Open the camera
    err = zed.open(init_params)
    # Check camera status
    if err != sl.ERROR_CODE.SUCCESS: # If unsuccessful exit
        print(repr(err))
        exit(1)

    # Enable recording with the filename specified in argument
    recordingParameters = sl.RecordingParameters()
    recordingParameters.compression_mode = sl.SVO_COMPRESSION_MODE.LOSSLESS # Set lossless compression (As is the only one that works)
    recordingParameters.video_filename = filepath # Set the filepath
    err = zed.enable_recording(recordingParameters)
    if err != sl.ERROR_CODE.SUCCESS:
        print(repr(err))
        exit(1)

    # Start SVO recording
    runtime = sl.RuntimeParameters()
    print("SVO is Recording.")
    frames_recorded = 0

    # Start timing the recording
    t1 = process_time()

    # Record SUPPOSEDLY for 3 seconds
    while frames_recorded<180:
        if zed.grab(runtime) == sl.ERROR_CODE.SUCCESS:
            frames_recorded += 1
            print("Frame count: " + str(frames_recorded), end="\r")

    # Finish timing the recording
    t2 = process_time()
    print("Time elapsed: " + str(t2-t1) + ' Frames: ' + str(frames_recorded))
# --------------------------------Storing PNG---------------------------------------------
def storing(filepath,filesave):
    """
    This function converts a SVO file to PNG and depth images and stores them in the
    filepath specified.
    """

    # Create a ZED camera object
    zed = sl.Camera()

    # Set configuration parameters
    input_type = sl.InputType()
    input_type.set_from_svo_file(filepath)
    init = sl.InitParameters(input_t=input_type, svo_real_time_mode=False)

    # Open the camera
    status = zed.open(init)

    # Check camera status
    if status != sl.ERROR_CODE.SUCCESS: # If unsuccessful exit
        print(repr(status))
        exit()

    # Get image, depth and distance values
    runtime = sl.RuntimeParameters()
    image = sl.Mat()
    depth = sl.Mat()
    point_cloud = sl.Mat() 

    frame_num = 1
    zed.set_svo_position(0) # Set the SVO position to the first frame

    # Start SVO reading thread
    while not exit_signal:
        err = zed.grab(runtime) # Grab an image
        if err == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_image(image, sl.VIEW.LEFT) # Retrieve the left image
            zed.retrieve_image(depth, sl.VIEW.DEPTH) # Retrieve the depth image
            saving_image(image,depth,frame_num,filesave) # Save the image and depth
            frame_num+=1
        else:
            print(repr(err))

    zed.close()
    print("\nFINISH")
 
def saving_image(mat,depthmat,frame,path):
    '''
    This function saves the image and depth image in the path specified.
    '''

    img = sl.ERROR_CODE.FAILURE # Set the image error code to failure
    while img != sl.ERROR_CODE.SUCCESS: # While the image error code is not success
        
        # Save image
        imgpath = path = "/Img_{0}.png".format(frame)
        img = mat.write(imgpath)
        
        # Save depth image
        depthpath = path + "/Dep_{0}.png".format(frame)
        dep = depthmat.write(depthpath)
        print("Saving image: {0} and depth: {1}".format(repr(img),repr(dep)))
        
        if img == sl.ERROR_CODE.SUCCESS:
            break
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

    # Set the filepath 
    filesave = filepath
    filepath = filepath + name
    print("SVO file path set to: {0}".format(filepath))

    # Recording and storing
    option = input("Do you want to record or store [r/s]?: ")
    if option == "r":
        print("Recording will now start, use Ctrl-C to stop recording.")
        Recording(filepath)
        print("Recording complete.")
    elif option == "s":
        print("Converting SVO to PNG.")
        storing(filepath,filesave)
        print("Conversion complete.")

if __name__ == "__main__":
    main()
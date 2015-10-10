"""
An example that shows how to use the motorized tilt
"""

import time
from pykinect import nui

WAIT_INTERVAL = 1.35

def post_frame(frame):
    print 'New elevation angle: ' + `cam.elevation_angle`
    
def main():
    with nui.Runtime() as kinect:
        cam = nui.Camera(kinect)

        while True:
            kinect.skeleton_engine.enabled = True
            kinect.skeleton_frame_ready += post_frame
          
            x = skeleton.Joints[JointID.HandRight].Position.X              

                    # wait before moving tilt again
            time.sleep(WAIT_INTERVAL)


if __name__ == '__main__':
    main()

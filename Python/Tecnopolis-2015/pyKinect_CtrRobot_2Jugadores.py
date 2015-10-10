import itertools
import pygame
import pygame.color
import serial
import time

from pygame.color import THECOLORS
from pykinect import nui
from pykinect.nui import JointId
from pykinect.nui import SkeletonTrackingState
from pykinect.nui.structs import TransformSmoothParameters

KINECTEVENT = pygame.USEREVENT
WINDOW_SIZE = 640, 480

SKELETON_COLORS = [THECOLORS["red"], 
                   THECOLORS["blue"], 
                   THECOLORS["green"], 
                   THECOLORS["orange"], 
                   THECOLORS["purple"], 
                   THECOLORS["yellow"], 
                   THECOLORS["violet"]]

LEFT_ARM = (JointId.ShoulderCenter, 
            JointId.ShoulderLeft, 
            JointId.ElbowLeft, 
            JointId.WristLeft, 
            JointId.HandLeft)
RIGHT_ARM = (JointId.ShoulderCenter, 
             JointId.ShoulderRight, 
             JointId.ElbowRight, 
             JointId.WristRight, 
             JointId.HandRight)
LEFT_LEG = (JointId.HipCenter, 
            JointId.HipLeft, 
            JointId.KneeLeft, 
            JointId.AnkleLeft, 
            JointId.FootLeft)
RIGHT_LEG = (JointId.HipCenter, 
             JointId.HipRight, 
             JointId.KneeRight, 
             JointId.AnkleRight, 
             JointId.FootRight)
SPINE = (JointId.HipCenter, 
         JointId.Spine, 
         JointId.ShoulderCenter, 
         JointId.Head)

SMOOTH_PARAMS_SMOOTHING = 0.7
SMOOTH_PARAMS_CORRECTION = 0.4
SMOOTH_PARAMS_PREDICTION = 0.7
SMOOTH_PARAMS_JITTER_RADIUS = 0.1
SMOOTH_PARAMS_MAX_DEVIATION_RADIUS = 0.1
SMOOTH_PARAMS = TransformSmoothParameters(SMOOTH_PARAMS_SMOOTHING,
                                          SMOOTH_PARAMS_CORRECTION,
                                          SMOOTH_PARAMS_PREDICTION,
                                          SMOOTH_PARAMS_JITTER_RADIUS,
                                          SMOOTH_PARAMS_MAX_DEVIATION_RADIUS)

skeleton_to_depth_image = nui.SkeletonEngine.skeleton_to_depth_image



def post_frame(frame):
    """Get skeleton events from the Kinect device and post them into the PyGame
    event queue."""
    try:
        pygame.event.post(
            pygame.event.Event(KINECTEVENT, skeleton_frame=frame)
        )
    except:
        # event queue full
        pass

def draw_skeleton_data(dispInfo, screen, pSkelton, index, positions, width = 4):
    start = pSkelton.SkeletonPositions[positions[0]]
       
    for position in itertools.islice(positions, 1, None):
        next = pSkelton.SkeletonPositions[position.value]
        
        curstart = skeleton_to_depth_image(start, dispInfo.current_w, dispInfo.current_h) 
        curend = skeleton_to_depth_image(next, dispInfo.current_w, dispInfo.current_h)

        pygame.draw.line(screen, SKELETON_COLORS[index], curstart, curend, width)
        
        start = next

def Hablar(sPalabra):
####    pygame.mixer.init(42100)
    pygame.mixer.music.load(sPalabra + ".wav")
    pygame.mixer.music.play()
    time.sleep(1)

def draw_skeletons(dispInfo, screen, skeletons):
    sDataTX = "0"
    iIndex = 0
    # clean the screen
    screen.fill(pygame.color.THECOLORS["black"])

    for index, skeleton_info in enumerate(skeletons):
        # test if the current skeleton is tracked or not
        if skeleton_info.eTrackingState == SkeletonTrackingState.TRACKED:
            # draw the Head
            HeadPos = skeleton_to_depth_image(skeleton_info.SkeletonPositions[JointId.Head], dispInfo.current_w, dispInfo.current_h) 
            draw_skeleton_data(dispInfo, screen, skeleton_info, index, SPINE, 10)
            pygame.draw.circle(screen, SKELETON_COLORS[index], (int(HeadPos[0]), int(HeadPos[1])), 20, 0)
    
            # drawing the limbs
            draw_skeleton_data(dispInfo, screen, skeleton_info, index, LEFT_ARM)
            draw_skeleton_data(dispInfo, screen, skeleton_info, index, RIGHT_ARM)
            draw_skeleton_data(dispInfo, screen, skeleton_info, index, LEFT_LEG)
            draw_skeleton_data(dispInfo, screen, skeleton_info, index, RIGHT_LEG)

            ##Manos
            Mano_RightPos = skeleton_info.SkeletonPositions[JointId.HandRight]
            Mano_LeftPos = skeleton_info.SkeletonPositions[JointId.HandLeft]
            ##Hombros
            Hombro_RightPos = skeleton_info.SkeletonPositions[JointId.ShoulderRight]
            Hombro_LeftPos = skeleton_info.SkeletonPositions[JointId.ShoulderLeft]
            Hombro_CenterPos = skeleton_info.SkeletonPositions[JointId.ShoulderCenter]
            ##Cabeza
            Cabeza_Pos = skeleton_info.SkeletonPositions[JointId.Head]
            ##Cintura
            Cintura_RightPos = skeleton_info.SkeletonPositions[JointId.HipRight]
            Cintura_LeftPos = skeleton_info.SkeletonPositions[JointId.HipLeft]
            Cintura_CenterPos = skeleton_info.SkeletonPositions[JointId.HipCenter]
            ##espina
            Espina_Pos = skeleton_info.SkeletonPositions[JointId.Spine]
            
            Mano_RightPos_Y = Mano_RightPos.y * 1000
            Mano_LeftPos_Y = Mano_LeftPos.y * 1000
            Cintura_CenterPos_Y = Cintura_CenterPos.y * 1000
            Hombro_CenterPos_Y = Hombro_CenterPos.y * 1000
            Cabeza_Pos_Y = Cabeza_Pos.y * 1000
            Espina_Pos_Y = Espina_Pos.y * 1000

            Medio =  Cabeza_Pos_Y - Espina_Pos_Y
            Tolerancia = 30
            Dife_Manos = abs(Mano_RightPos_Y - Mano_LeftPos_Y)

            
##            print "Mano derecha  : "
##            print HandRightPos
##            print "Mano izquierda: "
##            print int(Mano_LeftPos.y*1000)
##            print "Cabeza: "
##            print Cabeza_Pos
##            print "Hombroz: "
##            print Hombro_LeftPos
##            print Dife_Manos
            print index
           
            iIndex = index
            ## con las dos manos arriba para de la cabeza o por debajo de la cintura para
            if  Mano_RightPos_Y  > Cabeza_Pos_Y and Mano_LeftPos_Y  > Cabeza_Pos_Y:
                 print "Detener"
            elif Mano_RightPos_Y < Cintura_CenterPos_Y and Mano_LeftPos_Y < Cintura_CenterPos_Y:
                   print "Detener"
            elif Dife_Manos >= Tolerancia:
                 if Mano_RightPos_Y > Mano_LeftPos_Y:
                     print "Giro a la derecha"
                     sDataTX = "4"
##                     Hablar("derecha")
                 else:
                     print "Giro a la izquierda"
                     sDataTX = "3"
##                     Hablar("izquierda")
            elif Mano_RightPos_Y > Espina_Pos_Y+10:
                 print "Avanzar"
                 sDataTX = "2"
##                 Hablar("Adelante")
            else:
                 print "Retroceder"
                 sDataTX = "1"
####                 Hablar("retroceder")
                 
##            elif Mano_RightPos.y > Mano_LeftPos.y:
##                print "Girar a la derecha"
##            elif Mano_RightPos.y < Mano_LeftPos.y:
##                print "Girar a la izquierda"

    return sDataTX
            

            
def main():
    """Initialize and run the game."""
    pygame.init()

    # Initialize PyGame
    screen = pygame.display.set_mode(WINDOW_SIZE, 0, 16)
    pygame.display.set_caption('Robot Tecnopolis - Control Gestual')
    screen.fill(pygame.color.THECOLORS["black"])

##    iport = 6
##    s = serial.Serial(int(iport),9600)
##    serial.timeout=1

    print "Enviando comando de inicio al Robot Amigo"
##    s.write ("e")
##    
##    sDataTX  = "0"
    with nui.Runtime() as kinect:
        kinect.skeleton_engine.enabled = True
        kinect.skeleton_frame_ready += post_frame
        ##kinect.SkeletonFrame.TrackingMode = 
            ## Main game loop
        while True:

##            if sDataTX!="0":
##                s.write (sDataTX)
##                print sDataTX
                
            event = pygame.event.wait()

            if event.type == pygame.QUIT:
                break
            elif event.type == KINECTEVENT:
                # apply joint filtering
                kinect._nui.NuiTransformSmooth(event.skeleton_frame, SMOOTH_PARAMS)

                sDataTX = draw_skeletons(pygame.display.Info(), screen, event.skeleton_frame.SkeletonData)
                print sDataTX
                
                pygame.display.update()
                pass

if __name__ == '__main__':
    main()

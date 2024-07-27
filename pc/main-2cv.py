import cv2
import serial
import tomllib
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--serial", default="/dev/ttyUSB0")
parser.add_argument("--triggers", default="triggers.toml")
parser.add_argument("--v1", default="v1.m4v")
parser.add_argument("--v2", default="v2.m4v")

if __name__ == "__main__":
    args = parser.parse_args(sys.argv[1:])
else:
    args = parser.parse_args()

serial = serial.Serial(args.serial)

def set_red():
    serial.write('0\n'.encode())

def set_yellow():
    serial.write('1\n'.encode())

def set_double_yellow():
    serial.write('2\n'.encode())

def set_green():
    serial.write('3\n'.encode())

def set_flashing_yellow():
    serial.write('4\n'.encode())

def set_flashing_double_yellow():
    serial.write('5\n'.encode())

with open(args.triggers, "rb") as f:
    triggers = tomllib.load(f)['triggers']

for key, val in triggers.items():
    triggers[key] = globals()[val]

cv2.namedWindow("viewer1", flags = cv2.WINDOW_NORMAL)
cv2.setWindowProperty("viewer1", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN);

cv2.namedWindow("viewer2", flags = cv2.WINDOW_NORMAL)
cv2.moveWindow("viewer2", 1024, 0)
cv2.setWindowProperty("viewer2", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN);

cap1 = cv2.VideoCapture(args.v1)
cap2 = cv2.VideoCapture(args.v2)
fps = cap1.get(cv2.CAP_PROP_FPS)
frame_count = int(cap1.get(cv2.CAP_PROP_FRAME_COUNT))

# Read until video is completed
while(cap1.isOpened()):
      
# Capture frame-by-frame
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    if ret1 == True:
    # Display the resulting frame
        fn = int(cap1.get(cv2.CAP_PROP_POS_FRAMES))
        frames_left = frame_count-fn
        secs_left = int(frames_left/fps)
        try:
            triggers[str(int(float(fn)))]()
        except:
            pass
        #cv2.putText(
        #    img = frame,
        #    text = "Video restarts in {} seconds".format(str(secs_left)),
        #    org = (10, 30),
        #    fontFace = cv2.FONT_HERSHEY_DUPLEX,
        #    fontScale = 1.0,
        #    color = (255, 255, 255),
        #    thickness = 1
        #)
        cv2.imshow('viewer1', frame1)
        cv2.imshow('viewer2', frame2)
        
    # Press Q on keyboard to exit
        if cv2.waitKey(40) & 0xFF == ord('q'):
            break

# Break the loop
    else:
        cap1.set(cv2.CAP_PROP_POS_FRAMES, 0)
        cap2.set(cv2.CAP_PROP_POS_FRAMES, 0)
  
# When everything done, release
# the video capture object
cap1.release()
cap2.release()
  
# Closes all the frames
cv2.destroyAllWindows()

serial.close()
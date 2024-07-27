import cv2
import serial
import tomllib
import argparse
import sys
from tkinter import *
from PIL import Image, ImageTk
from pytictoc import TicToc

parser = argparse.ArgumentParser()
parser.add_argument("--serial", default="/dev/ttyUSB0")
parser.add_argument("--triggers", default="triggers.toml")
parser.add_argument("--video", default="video.mp4")

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

window = Tk()  #Makes main window
window.overrideredirect(True)
window.wm_attributes("-topmost", True)
display1 = Label(window, borderwidth=0, highlightthickness=0)
display1.grid(row=1, column=0, padx=0, pady=0)  #Display 1

def close_win(e):
   window.destroy()

window.bind('<Escape>', lambda e: close_win(e))

#cv2.namedWindow("viewer", flags = cv2.WINDOW_AUTOSIZE)
#cv2.setWindowProperty("viewer", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN);

cap = cv2.VideoCapture(args.video)
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Read until video is completed
#while(cap.isOpened()):
      
def show_frame():
# Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:
    # Display the resulting frame
        fn = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
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
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(master = display1, image=img)
        display1.imgtk = imgtk #Shows frame for display 1
        display1.configure(image=imgtk)
        #cv2.imshow('viewer', frame)
        
    # Press Q on keyboard to exit
        #if cv2.waitKey(40) & 0xFF == ord('q'):
            #break

# Break the loop
    else:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    tm = t.tocvalue(restart=True)
    window.after(max(1, int(40.0-tm*1000)), show_frame)

t = TicToc()
t.tic()
show_frame()
window.mainloop()
  
# When everything done, release
# the video capture object
cap.release()
  
# Closes all the frames
cv2.destroyAllWindows()

serial.close()
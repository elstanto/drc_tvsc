The Arduino sketch goes on the NodeMCU in the junction box on the wall. There should be a spare unit in there already programmed.
The pc folder has a python program which runs the video and sends serial commands to the Arduino at certain frames. This changes the signal aspect.
I use pyinstaller to make a windows exe from the python code. I forget the command to compile but it is straightforward, you just need to remember to include the video file.

import cv2


class ReadCAM:
    vid = None  # video capture object

    @classmethod
    def setup(cls):
        # ref to use camera with opencv: https://www.geeksforgeeks.org/python-opencv-capture-video-from-camera/
        # define a video capture object
        cls.vid = cv2.VideoCapture(0) #starts capturing video when this setup is called

    @classmethod
    def run(cls):
        ret, frame = cls.vid.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #reads the video and returns the frame. 
        return frame

    @classmethod
    def stop(cls):
        cls.vid.release() #deletes therecorded video. 

from parameters import cv2
import numpy as np

# output of subsystem


class markers_status:
    corners = []
    ids = []
    all_tvecs = {}
    all_rvecs = {}


# subsystem
class MarkersDetected:

    PARAM_DRAW_MARKERS = True
    camdata = np.matrix([[457.9243469, 0.0000, 342.5554546
],[0.00000, 456.24218, 233.3466135
],[0.00000, 0.0000000, 1.000000
]])
    camdist = np.matrix([-0.292971622, 0.10770688, 
                   0.0013103841, -0.00003110,
                   0.0434799801])

    @classmethod
    def setup(cls):
        pass

    @classmethod
    def run(cls, frame):
        cp_frame = frame.copy() #takes the frame from the subsys_read_cam file.
        corners, ids = cls.__find_markers(cp_frame)
        if cls.PARAM_DRAW_MARKERS and ids is not None:
            cls.__draw_markers(cp_frame, corners, ids)
            all_tvecs, all_rvecs = cls.__get_marker_pos(corners, ids)
#=============================================================================
            markers_status.all_tvecs = all_tvecs
            markers_status.all_rvecs = all_rvecs
#=============================================================================
        markers_status.ids = ids
        markers_status.corners = corners 
        return markers_status, cp_frame

    @classmethod
    def stop(cls):
        pass

    @classmethod
    def __find_markers(cls, frame):
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_100)
        parameters = cv2.aruco.DetectorParameters_create()
        corners, ids, _ = cv2.aruco.detectMarkers(
            gray, aruco_dict, parameters=parameters
        )
        
# =============================================================================
#         if ids is None: 
#             print(".")
#         else:
#             if markers_status.all_ids is None:
#                 markers_status.all_ids.extend([item for sublist in ids for item in sublist])
#             else:
#                 markers_status.all_ids.extend(list(set(markers_status.all_ids) - set([item for sublist in ids for item in sublist])))
# =============================================================================

        return corners, ids

    @classmethod
    def __draw_markers(cls, frame, corners, ids):
        cv2.aruco.drawDetectedMarkers(
            frame, corners, ids, borderColor=(100, 0, 240))
# =============================================================================
#         for i in range(len(corners)): 
#             rvec1, tvec1, _ = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.37, cls.camdata, cls.camdist)
# =============================================================================
# =============================================================================
#             print("rvec:", rvec1)
#             print("tvec:", tvec1)
#             print("id:",ids[i])
# =============================================================================
#=============================================================================
    @classmethod
    def __get_marker_pos(cls, corners, ids):
        all_tvecs = markers_status.all_tvecs.copy()
        all_rvecs = markers_status.all_tvecs.copy()
        for i in range(len(corners)):
            rvec1, tvec1, _ = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.37, cls.camdata, cls.camdist)
            all_tvecs[ids[i][0]] = tvec1
            all_rvecs[ids[i][0]] = rvec1
        return all_tvecs, all_rvecs
#=============================================================================

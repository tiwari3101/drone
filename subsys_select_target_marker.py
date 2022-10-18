from parameters import RED, cv2, np
# output of subsystem


class marker_status:
    camdata = np.matrix([[457.9243469, 0.0000, 342.5554546
],[0.00000, 456.24218, 233.3466135
],[0.00000, 0.0000000, 1.000000
]])
    camdist = np.matrix([-0.292971622, 0.10770688, 
                   0.0013103841, -0.00003110,
                   0.0434799801])
    
    available_id = []
    available_corners = []
    
    next_id = -1
    next_corner = []
    next_rotation = 1
    next_height = 0
    
    all_tvecs = {}
    all_rvecs = {}
    
    id = -1
    corners = []
    # Origin axis
    center_pt = (0, 0)
    # Horizontal axis
    top_pt = (0, 0)
    bottom_pt = (0, 0)
    # Vertical axis
    left_pt = (0, 0)
    right_pt = (0, 0)

    # Horizontal angle
    h_angle = 0
    # Vertical angle
    v_angle = 0
    # angle and distance between marker and drone
    m_angle = 0
    m_distance = 0
    
    drone_pos = []
    marker_pos = []

    height = 0
    width = 0

    @classmethod
    def reset(cls): # to reset the marker
        cls.id = -1
        cls.corners = []
        cls.center_pt = (0, 0)
        cls.top_pt = (0, 0)
        cls.bottom_pt = (0, 0)
        cls.left_pt = (0, 0)
        cls.right_pt = (0, 0)
        cls.h_angle = 0
        cls.v_angle = 0
        cls.m_angle = 0
        cls.m_distance = 0
        cls.height = 0
        cls.width = 0
        cls.marker_pos = []
        cls.drone_pos = []

# subsystem


class SelectTargetMarker:
    @classmethod
    def setup(cls):
        marker_status.reset()

    @classmethod
    def stop(cls):
        pass

    @classmethod
    def run(cls, frame, markers, drone_pos, offset=(0, 0)):

        cls.drone_pos = drone_pos
        id, corners = cls._get_marker_with_min_id(markers)

#         for i in available_id:
#             if i not in cls.available_id:
# =============================================================================
                
        marker_status.available_id, marker_status.available_corners= cls._get_sorted_markers(id, corners, markers)
        #marker_status.all_tvecs, marker_status.all_rvecs = cls._get_sorted_markers_info(frame)
        marker_status.all_tvecs, marker_status.all_rvecs = markers.all_tvecs, markers.all_rvecs
        #print("all_tvecs", marker_status.all_tvecs)    
        
# =============================================================================
#         print("available_id:", marker_status.available_id)
#         print("available_corners:", marker_status.available_corners)
# =============================================================================
# =============================================================================
#         print("all_tvecs:", marker_status.all_tvecs)
#         print("all_rvecs:", marker_status.all_rvecs)
# =============================================================================
# =============================================================================
#         print("available id:", marker_status.available_id)
#         print("available corners:", marker_status.available_corners)
# =============================================================================
        print("target:", id)
        
        
        if len(marker_status.available_id) >= 2:
            if(id != -1):
                index = marker_status.available_id.index(id)
                if index < len(marker_status.available_id) - 1:
                    marker_status.next_id = marker_status.available_id[index+1]
            
                    print("next id:", marker_status.next_id)
                    print("next id pos:", marker_status.all_tvecs[marker_status.next_id][0][0][0])
                
                    print("id pos:", marker_status.all_tvecs[id][0][0][0])
                    print("id depth:", marker_status.all_tvecs[id][0][0][2])
                    
                    marker_status.next_height = marker_status.all_tvecs[marker_status.next_id][0][0][1]
                    if(marker_status.all_tvecs[marker_status.next_id][0][0][0] > marker_status.all_tvecs[id][0][0][0]):
                        marker_status.next_rotation = 1
                        print("clockwise")
                    else:
                        marker_status.next_rotation = -1
                
# =============================================================================
#         print(id, corners)
#         print(available_id, available_corners)
# =============================================================================
        if id == -1:
            marker_status.reset()
            return marker_status

        br, bl, tl, tr = corners[0], corners[1], corners[2], corners[3]
        center_pt = cls._get_midpoint([br, bl, tl, tr])
        # get symmetry axes
        left_pt = cls._get_midpoint([bl, tl])
        right_pt = cls._get_midpoint([br, tr])
        bottom_pt = cls._get_midpoint([br, bl])
        top_pt = cls._get_midpoint([tl, tr])

        height = cls._length_segment(bottom_pt, top_pt)
        width = cls._length_segment(left_pt,   right_pt)

        h_angle = cls._angle_between(left_pt, right_pt)
        v_angle = cls._angle_between(top_pt, bottom_pt, vertical=True)

        cls.offset = (int(offset[0]*width), int(offset[1]*height))
        cls.marker_pos = (center_pt[0] + cls.offset[0],
                          center_pt[1] + cls.offset[1])
        m_angle = cls._angle_between(drone_pos,  cls.marker_pos, vertical=True)
        m_distance = cls._length_segment(drone_pos, cls.marker_pos)

        cls.draw(frame)
        #cls.marker_distance(corners, height)

        # update output
        marker_status.id = id
        marker_status.corners = corners
        #marker_status.available_id = cls.available_id
        #marker_status.available_corners = cls.available_corners
        marker_status.center_pt = center_pt
        marker_status.left_pt = left_pt
        marker_status.right_pt = right_pt
        marker_status.bottom_pt = bottom_pt
        marker_status.top_pt = top_pt
        marker_status.h_angle = h_angle
        marker_status.v_angle = v_angle
        marker_status.m_angle = m_angle
        marker_status.m_distance = m_distance
        marker_status.height = height
        marker_status.width = width
        marker_status.drone_pos = drone_pos
        marker_status.marker_pos = cls.marker_pos
        
# =============================================================================
#         marker_status.all_ids = cls.all_ids
#         marker_status.all_corners = cls.all_corners
# =============================================================================
        return marker_status

    @staticmethod
    def _get_marker_with_min_id(markers):
        target_id = -1
        target_corners = []
# =============================================================================
#         available_id = []
#         available_corners = []
# =============================================================================

        if markers.ids is None:
            return target_id, target_corners
        
        #print(markers.ids)
        #print(markers.all_ids)
        for i in range(len(markers.ids)):
            id = markers.ids[i][0]
            if target_id == -1:
                target_id = id
                target_corners = markers.corners[i][0]
            elif markers.all_tvecs[id][0][0][2] < markers.all_tvecs[target_id][0][0][2]:
                target_id = id
                target_corners = markers.corners[i][0]
            
                
                
# =============================================================================
#         for i in range(len(markers.ids)):
#             id = markers.ids[i][0]
#             if id < target_id or target_id == -1:
#                 target_id = id
#                 target_corners = markers.corners[i][0]
# =============================================================================
# =============================================================================
#         if target_id != -1: #available ids will not be made if none available
#             for i in range(len(markers.ids)):
#                 id = markers.ids[i][0]
#                 if id != target_id:
#                     available_id.append(id)
#                     available_corners.append(markers.corners[i][0])
#         print(available_id, available_corners)
# =============================================================================
        # target_id, target_corners, available_id, available_corners
        return target_id, target_corners
    
# =============================================================================
# =============================================================================
#     @staticmethod
#     def _get_sorted_markers_info(frame):
#          all_tvecs = marker_status.all_tvecs.copy()
#          all_rvecs = marker_status.all_rvecs.copy()
#          gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#  
#          aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_100)
#          parameters = cv2.aruco.DetectorParameters_create()
#          corners, ids, _ = cv2.aruco.detectMarkers(
#              gray, aruco_dict, parameters=parameters
#          )
#          cv2.aruco.drawDetectedMarkers(frame, corners, ids, borderColor=(100, 0, 240))
#          print(ids)
#          for i in range(len(corners)):
#              
#              rvec1, tvec1, _ = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.37, marker_status.camdata, marker_status.camdist)
#              print(ids)
#              id1 = ids[i][0]
#              all_tvecs[id1] = tvec1
#              all_rvecs[id1] = rvec1
#          return all_tvecs, all_rvecs
# =============================================================================
         
# =============================================================================
    @staticmethod
    def _get_sorted_markers(id, corners, markers):
        available_id = marker_status.available_id[:]
        available_corners = marker_status.available_corners[:]
        
        if id != -1: 
            for i in range(len(markers.ids)):
                if markers.ids[i][0] not in available_id:
                    available_id.append(markers.ids[i][0])
                    available_corners.append(markers.corners[i][0])
            updated_available_corners = []
            updated_available_id = []
            least = -1
            if len(available_id) != 0:
                while len(available_id) != 0 :
                    for i in range(len(available_id)):
                        #print(a[i])
                        if available_id[i] < least or least == -1:
                            least = available_id[i]
                            index = i
                    updated_available_id.append(least)
                    updated_available_corners.append(available_corners[index])
                    available_id.remove(least)
                    if len(available_id) != 0:
                        least = available_id[0]
                
            return updated_available_id, updated_available_corners
        else:
            return available_id, available_corners
    
# =============================================================================
#     def _get_marker_position(id, frame):
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# 
#         aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_100)
#         parameters = cv2.aruco.DetectorParameters_create()
#         corners, ids, _ = cv2.aruco.detectMarkers(
#             gray, aruco_dict, parameters=parameters
#         )
#         data = {}
#         if ids is not None:
#             ids = list(ids)
#             index = ids.index(id)
#             rvec1, tvec1, _ = cv2.aruco.estimatePoseSingleMarkers(corners[index], 0.37, marker_status.camdata, marker_status.camdist)
#             data[id] = [rvec1, tvec1]
#             return data
#         else:
#             return data
# =============================================================================
    
    @staticmethod
    def _get_midpoint(corners):
        # corners = [p1,p2,p3,p4] with pi = (xi, yi)
        xc = yc = 0
        n = len(corners)
        for x, y in corners:
            xc += x
            yc += y
        xc = int(xc/n)
        yc = int(yc/n)
        return (xc, yc)

    @staticmethod
    def _angle_between(p1, p2, vertical=False):
        dx = p1[0]-p2[0]
        dy = p1[1]-p2[1]
        if not vertical:  # angle betwenn Horizantal axis and segment (p1,p2)
            return np.arctan(-dy/(dx+0.000001))
        else:  # angle betwenn vertical axis and segment (p1,p2)
            return np.arctan(-dx/(dy+0.000001))

    @staticmethod
    def _length_segment(p1, p2):
        return int(np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2))

    @classmethod
    def draw(cls, frame):
        if marker_status.id == -1:
            return
        cv2.aruco.drawDetectedMarkers(frame, np.array([[marker_status.corners]]), np.array([
            [marker_status.id]]), borderColor=RED)

        cv2.line(frame, marker_status.top_pt,
                 marker_status.bottom_pt, (255, 0, 0), 2)
        cv2.line(frame, marker_status.left_pt,
                 marker_status.right_pt, (255, 0, 0), 2)
        top_pt_with_offset = tuple(
            np.array(marker_status.top_pt) + np.array(cls.offset))
        bottom_pt_with_offset = tuple(
            np.array(marker_status.bottom_pt) + np.array(cls.offset))
        left_pt_with_offset = tuple(
            np.array(marker_status.left_pt) + np.array(cls.offset))
        right_pt_with_offset = tuple(
            np.array(marker_status.right_pt) + np.array(cls.offset))
        cv2.line(frame,
                 top_pt_with_offset,
                 bottom_pt_with_offset,
                 (255, 0, 0), 2)
        cv2.line(frame,
                 left_pt_with_offset,
                 right_pt_with_offset,
                 (255, 0, 0), 2)

        if cls.drone_pos[0] != 0:
            cv2.line(frame,
                     cls.drone_pos,
                     cls.marker_pos,
                     (0, 0, 255), 2)
    
    #def marker_distance(corners, height):
        #for corner in np.array([[marker_status.corners]]):
# =============================================================================
#             print(np.array([[marker_status.corners]]))
#             print(corner)
#             if corner is not None:
#                 
#                 rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corner, 0.375,marker_status.camdata, marker_status.camdist)
#                 
#                 print(rvecs, tvecs)
#             else:
#                 continue
# =============================================================================

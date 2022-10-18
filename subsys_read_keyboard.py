from parameters import run_status, RUN, MODE, pygame


# output of subsystem


class key_status:
    is_pressed = False
    type_pressed = None


class rc_status: #indicates the direction of the drone
    a = 0 # right/left
    b = 0 # forward/backward
    c = 0 # up/down 
    d = 0 # clockwis/counter-clockwise


class mode_status:
    value = MODE.LAND

# Subsystem


class ReadKeyboard:
    """Maintains the Tello display and moves it through the keyboard keys.
    Press escape key to quit.
    The controls are:
        - T: Takeoff
        - L: Land
        - Space: Emergency 
        - Arrow keys: Forward, backward, left and right.
        - Q and D: Counter clockwise and clockwise rotations (yaw)
        - Z and S: Up and down.
    """
    @classmethod
    def setup(cls):
        run_status.value = RUN.START
        mode_status.value = -1

    @classmethod
    def run(cls, rc_threshold):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run_status.value = RUN.STOP

            elif event.type == pygame.KEYDOWN:
                key_status.is_pressed = True
                key_status.type_pressed = event.key

                if event.key == pygame.K_ESCAPE:
                    run_status.value = RUN.STOP

                elif event.key == pygame.K_SPACE:
                    mode_status.value = MODE.EMERGENCY
                elif event.key == pygame.K_t:
                    mode_status.value = MODE.TAKEOFF
                elif event.key == pygame.K_l:
                    mode_status.value = MODE.LAND

                else:
                    cls.__key_down(event.key, rc_threshold)

            elif event.type == pygame.KEYUP:

                key_status.is_pressed = False
                key_status.type_pressed = None
                cls.__key_up(event.key)
        return rc_status, key_status, mode_status

    # inter functions
    @classmethod
    def __key_down(cls, key, rc_threshold): # key is pressed
        """
        Update velocities based on key pressed
        Arguments:
            key: pygame key
        """
        # left_right_velocity
        if key == pygame.K_RIGHT:
            rc_status.a = rc_threshold
        elif key == pygame.K_LEFT:
            rc_status.a = - rc_threshold

        # for_back_velocity
        elif key == pygame.K_UP:
            rc_status.b = rc_threshold
        elif key == pygame.K_DOWN:
            rc_status.b = -rc_threshold

        # up_down_velocity
        elif key == pygame.K_z:
            rc_status.c = rc_threshold
        elif key == pygame.K_s:
            rc_status.c = -rc_threshold

        # yaw_velocity
        elif key == pygame.K_d:
            rc_status.d = rc_threshold
        elif key == pygame.K_q:
            rc_status.d = -rc_threshold

    @classmethod
    def __key_up(cls, key): # key is unpressed/ finger lifted
        """
        Update velocities based on key released
        Arguments:
            key: pygame key

        """
        # left_right_velocity
        if (key == pygame.K_RIGHT or key == pygame.K_LEFT):
            rc_status.a = 0
        # for_back_velocity
        elif(key == pygame.K_UP or key == pygame.K_DOWN):
            rc_status.b = 0
        # up_down_velocity
        elif(key == pygame.K_z or key == pygame.K_s):
            rc_status.c = 0
        # yaw_velocity
        elif(key == pygame.K_d or key == pygame.K_q):
            rc_status.d = 0

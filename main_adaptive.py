import sys
sys.path.append('/Clone')

import time
from camera_setup import setup_camera
from image_processing import process_image
from channel_detection_modified import detect_channel, calculate_reference_mean, analyze_segments, draw_results
from state_machine import StateMachine, STATE_INIT, STATE_DETECT, STATE_CALCULATE, STATE_ANALYZE, STATE_DRAW, STATE_FINISH
from logging_setup import logger  # Import the logger

def main():
    logger.debug("=================BEGIIIIIIIIIIIIIIIIIIIIIIN=================")
    sensor_width, sensor_height= setup_camera()
    #img = process_image()
    state_machine = StateMachine()
    number = 20
    manual_threshold = 1.0
    clock = time.clock()
    old_x = 1000 #initializing old_min_x
    initial_bounding = None  # Initial value set to None
    initial_x = None
    initial_width = None



     # add a counter that it allowes the state machine to go back to reset every 10 frames.
    while True:

        current_state = state_machine.get_state()

        if current_state == STATE_INIT:
            frame_counter = 50
            img = process_image()
            state_machine.next_state()

        elif current_state == STATE_DETECT:
            logger.debug("DETECT STATE")
            #channel_roi = (0, 0, 240, 320) all channel
            channel_roi = (100,0,93,320)
            changed, old_x, channel_detected, lines_found, new_min_x, min_y, channel_width, channel_height, initial_bounding,initial_x,initial_width = detect_channel(img, sensor_width, sensor_height, channel_roi, old_x, initial_bounding,initial_x,initial_width)

            #logger.warning(f"lines_found = {lines_found}, min_x = {new_min_x}, min_y = {min_y}, channel_width = {channel_width}, channel_height = {channel_height}")

            #time.sleep(2)

            if channel_detected == True:
                logger.debug("=================0- DETECT STATE=================")
                if changed == False:

#                    logger.error(f"the channeldid not change = {initial_bounding}")
#                    logger.error(f"the channeldid not change = {initial_x}")
#                    logger.error(f"the channeldid not change = {initial_width}")

                    logger.debug("Going to Next state")

                    state_machine.next_state()
                elif changed:
                    logger.warning("Channel's position has changed")
                    state_machine.reset()
                else:
                    logger.error("It is impossible to print error")
            elif channel_detected == False:
                logger.warning(f"Channel is too narrow = {channel_width}, Reseting...")
                state_machine.reset()

            else:
                logger.warning("Detection failed, Reseting...")

                state_machine.reset()

        elif current_state == STATE_CALCULATE:
            img = process_image()
            logger.info(f"Processing complete. FPS: {clock.fps()}")

            ref_mean = calculate_reference_mean(img, initial_width, channel_height, number)
            logger.debug("=================1- Calculate STATE=================")
            state_machine.next_state()

        elif current_state == STATE_ANALYZE:
            segments_mean_array, ratio_array = analyze_segments(img, initial_x, initial_width, channel_height, ref_mean, number)
            logger.debug("=================2- Analyze STATE=================")
            state_machine.next_state()

        elif current_state == STATE_DRAW:
            draw_results(img, initial_x, initial_width, number, ratio_array, manual_threshold)
            logger.debug("=================3- Draw STATE=================")
            state_machine.next_state()

        elif current_state == STATE_FINISH:

            logger.info("=================4- Finished=================")
            if frame_counter != 0:
                state_machine.calculate_state()
                frame_counter -=1
                logger.error(f"frame_counter = {frame_counter}")
            else:
                state_machine.reset()
                #state_machine.detect_state()

if __name__ == "__main__":
    main()

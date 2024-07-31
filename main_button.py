import time
from camera_setup import setup_camera
from image_processing import process_image
from channel_detection import detect_channel, calculate_reference_mean, analyze_segments, draw_results
from state_machine import StateMachine, STATE_INIT, STATE_DETECT, STATE_CALCULATE, STATE_ANALYZE, STATE_DRAW, STATE_FINISH
from logging_setup import logger  # Import the logger

from pyb import Pin

button = Pin('PA9',Pin.IN,Pin.PULL_UP)

def main():
    logger.debug("=================BEGIIIIIIIIIIIIIIIIIIIIIIN=================")
    sensor_width, sensor_height= setup_camera()
    img = process_image()
    state_machine = StateMachine()
    number = 20
    manual_threshold = 1.0
    clock = time.clock()

    while True:
        current_state = state_machine.get_state()

        if current_state == STATE_INIT:
            img = process_image()
            state_machine.next_state()

        if current_state == STATE_DETECT:
            logger.debug("DETECT STATE")
            #channel_roi = (0, 0, 240, 320) all channel
            channel_roi = (100,0,93,320)
            channel_detected,lines_found, min_x, min_y, channel_width, channel_height = detect_channel(img, sensor_width, sensor_height, channel_roi)
            logger.info(f"lines_found = {lines_found}, min_x = {min_x}, min_y = {min_y}, channel_width = {channel_width}, channel_height = {channel_height}")


            if channel_detected == True:
                logger.debug("=================0- DETECT STATE=================")
                logger.warning("Channel was detected!")
                state_machine.next_state()
            elif channel_detected == False:
                #logger.warning(f"Channel is too narrow = {channel_width}, Reseting...")
                state_machine.reset()
            else:
                logger.warning("Detection failed, Reseting...")
                time.sleep(1)

                state_machine.reset()

        elif current_state == STATE_CALCULATE:
            img = process_image()
            logger.info(f"Processing complete. FPS: {clock.fps()}")

            ref_mean = calculate_reference_mean(img, min_x, channel_width, channel_height, number)
            logger.debug("=================1- Calculate STATE=================")
            state_machine.next_state()

        elif current_state == STATE_ANALYZE:
            segments_mean_array, ratio_array = analyze_segments(img, min_x, channel_width, channel_height, ref_mean, number)
            logger.debug("=================2- Analyze STATE=================")
            state_machine.next_state()

        elif current_state == STATE_DRAW:
            draw_results(img, min_x, channel_width, number, ratio_array, manual_threshold)
            logger.debug("=================3- Draw STATE=================")
            state_machine.next_state()

        elif current_state == STATE_FINISH:

            logger.info("=================4- Finished=================")

            if button.value() == 0:
                state_machine.reset()
                logger.warning("The reset button is pressed")
                time.sleep(1)
            else:
                state_machine.calculate_state()

if __name__ == "__main__":
    main()

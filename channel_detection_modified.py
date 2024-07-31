import sensor, time
from logging_setup import logger  # Import the logger

# Add a new parameter to keep track of the initial bounding box
def detect_channel(img, sensor_width, sensor_height, channel_roi, old_x, initial_bounding=None,initial_x=None,initial_width = None):
    new_min_x = sensor_width
    min_y = sensor_height
    max_x = 0
    max_y = 0
    lines_found = False
    channel_detected = False
    channel_width = 0
    channel_height = 0
    changed = False

    for l in img.find_lines(roi=channel_roi, threshold=250, theta_margin=1, rho_margin=1): # 250
        if abs(l.theta()) < 1.0 or abs(l.theta() - 180) < 1.0:
            lines_found = True
            new_min_x = min(new_min_x, l.x1(), l.x2())
            max_x = max(max_x, l.x1(), l.x2())
            min_y = min(min_y, l.y1(), l.y2())
            max_y = max(max_y, l.y1(), l.y2())

    difference = old_x - new_min_x  # comparing previous_x with new_x

    if lines_found:
        channel_width = max((max_x - new_min_x) + 1, 0)
        channel_height = max((max_y - min_y) + 1, 0)
        if 21 <= channel_width < 40:
            channel_detected = True
            logger.info(f"Width is {channel_width}")

            if old_x == 1000:
                changed = True
                logger.info("First value.")
                old_x = new_min_x
                initial_bounding = (new_min_x, max_x, min_y, max_y) # values go there ONLY IN THE FIRST LOOP
                initial_x = new_min_x
                initial_width = (max_x - new_min_x) + 1

                return changed, old_x, False, lines_found, 0, 0, 0, 0, initial_bounding,initial_x,initial_width

            elif -2 <= difference <= 2:
                changed = False
                logger.error(f"Didn't move, old_x = {old_x}, new_min_x = {new_min_x}")
                # Keep returning the initial bounding box values
                return changed, old_x, channel_detected, lines_found, new_min_x, min_y, channel_width, channel_height, initial_bounding,initial_x,initial_width #IF NO CHANGE, VALUES STAY THE SAME FROM THE FIRST LOOP

            elif difference > 2:
                changed = True
                logger.error(f"Moved to the left, old_x = {old_x}, new_min_x = {new_min_x}")
                time.sleep(1)
                old_x = new_min_x
                initial_bounding = (new_min_x, max_x, min_y, max_y) # VALUES UPDATE UPON CHANGE
                initial_x = new_min_x
                initial_width = (max_x - new_min_x) + 1
                return changed, old_x, False, lines_found, 0, 0, 0, 0, initial_bounding,initial_x,initial_width

            elif difference < -2:
                changed = True
                logger.error(f"Moved to the right, old_x = {old_x}, new_min_x = {new_min_x}")
                time.sleep(1)
                old_x = new_min_x
                initial_bounding = (new_min_x, max_x, min_y, max_y) # VALUES UPDATE UPON CHANGE
                initial_x = new_min_x
                initial_width = (max_x - new_min_x) + 1
                return changed, old_x, False, lines_found, 0, 0, 0, 0, initial_bounding,initial_x,initial_width

            else:
                changed = True
                print("Did not meet any conditions")
                print(f"Old_x = {old_x} and New_x = {new_min_x}")
                time.sleep(1)
                old_x = new_min_x
                initial_bounding = (new_min_x, max_x, min_y, max_y) # VALUES UPDATE UPON CHANGE
                initial_x = new_min_x
                initial_width = (max_x - new_min_x) + 1

                return changed, old_x, False, lines_found, 0, 0, 0, 0, initial_bounding,initial_x,initial_width
        elif channel_width < 15:
            logger.warning(f"Channel is too narrow = {channel_width}")
            return changed, old_x, False, lines_found, 0, 0, 0, 0, initial_bounding,initial_x,initial_width
        else:
            logger.error("FATAL ERROR")
            return changed, old_x, False, lines_found, 0, 0, 0, 0, initial_bounding,initial_x,initial_width

    else:
        logger.warning("No lines were detected")

    return changed, old_x, channel_detected, lines_found, 0, 0, 0, 0, initial_bounding,initial_x,initial_width

def calculate_reference_mean(img, initial_width, channel_height, number):
    empty_block_roi = (5, int(channel_height / 2), int(initial_width), number)
    img.draw_rectangle(empty_block_roi, color=(255), thickness=1)
    ref_stats = img.get_statistics(roi=empty_block_roi)
    ref_mean = ref_stats[0]
    logger.info(f"Mean of Reference Block: {ref_mean}")
    return ref_mean

def analyze_segments(img, initial_x, initial_width, channel_height, ref_mean, number):
    segments_mean_array = []
    ratio_array = []
    start = 0
    end = number

    for i in range(0, channel_height, number):
        img.draw_line((0, start - 1, sensor.width(), start - 1), color=(0), thickness=1)
        segment_roi = (initial_x + 2, start - 1, initial_width - 2, end - start)
        segment_stats = img.get_statistics(roi=segment_roi)
        segment_mean = segment_stats[0]
        difference = segment_mean / ref_mean
        ratio_array.append(difference)
        segments_mean_array.append([segment_mean])
        start = end
        end = min(start + number, channel_height)

    logger.info(f"Segment Ratio Array  = {ratio_array}")
    return segments_mean_array, ratio_array

def draw_results(img, initial_x, initial_width, number, ratio_array, manual_threshold):
    y_position = 3
    for ratio in ratio_array:
        if ratio > manual_threshold:  # Empty -> white
            img.draw_circle(initial_x - 20, int(y_position - 3 + (number / 2)), 5, color=(255), thickness=1, fill=True)
            img.draw_rectangle((initial_x, y_position - 3, initial_width, number), color=(255), thickness=1)
        else:  # Full -> Black
            img.draw_circle(initial_x - 20, y_position + 5, 5, color=(0), thickness=1, fill=True)
            img.draw_rectangle((initial_x, y_position - 3, initial_width, number), color=(0), thickness=1)
        y_position += number

import sensor,time
from logging_setup import logger  # Import the logger

def detect_channel(img, sensor_width, sensor_height, channel_roi):
    min_x = sensor_width
    min_y = sensor_height
    max_x = 0
    max_y = 0
    lines_found = False
    channel_detected = False
    channel_width = 0
    channel_height = 0

    for l in img.find_lines(roi=channel_roi, threshold=250, theta_margin=1, rho_margin=1):
        if abs(l.theta()) < 1.0 or abs(l.theta() - 180) < 1.0:
            lines_found = True
            min_x = min(min_x, l.x1(), l.x2())
            max_x = max(max_x, l.x1(), l.x2())
            min_y = min(min_y, l.y1(), l.y2())
            max_y = max(max_y, l.y1(), l.y2())

    if lines_found:
        channel_width = max((max_x - min_x) + 1, 0)
        channel_height = max((max_y - min_y) + 1, 0)
        if channel_width >= 21 and channel_width < 40:
            channel_detected = True
            img.draw_rectangle(min_x, min_y, channel_width, channel_height, color=(0), thickness=1)
            logger.info(f"Width is {channel_width}")
            return channel_detected, lines_found, min_x, min_y, channel_width, channel_height

        elif channel_width < 15:
            channel_detected = False
            min_x = 0
            min_y = 0
            channel_width = 0
            channel_height = 0
            return channel_detected, lines_found, min_x, min_y, channel_width, channel_height

        else:
            #logger.error("FATAL ERROR")
            channel_detected = False
            min_x = 0
            min_y = 0
            channel_width = 0
            channel_height = 0
            return channel_detected, lines_found, min_x, min_y, channel_width, channel_height


    else:
        logger.warning("No lines were detected")
        channel_detected = False
        lines_found = False
        min_x = 0
        min_y = 0
        channel_width = 0
        channel_height = 0
        return channel_detected,lines_found, min_x, min_y, channel_width, channel_height

def calculate_reference_mean(img, min_x, channel_width, channel_height, number):
    empty_block_roi = (5, int(channel_height / 2), int(channel_width), number)
    img.draw_rectangle(empty_block_roi, color=(255), thickness=1)
    ref_stats = img.get_statistics(roi=empty_block_roi)
    ref_mean = ref_stats[0]
    logger.info(f"Mean of Reference Block: {ref_mean}")
    return ref_mean

def analyze_segments(img, min_x, channel_width, channel_height, ref_mean, number):
    segments_mean_array = []
    ratio_array = []
    start = 0
    end = number

    for i in range(0, channel_height, number):
        img.draw_line((0, start - 1, sensor.width(), start - 1), color=(0), thickness=1)
        segment_roi = (min_x + 2, start - 1, channel_width - 2, end - start)
        segment_stats = img.get_statistics(roi=segment_roi)
        segment_mean = segment_stats[0]
        difference = segment_mean / ref_mean
        ratio_array.append(difference)
        segments_mean_array.append([segment_mean])
        start = end
        end = min(start + number, channel_height)

    logger.info(f"Segment Ratio Array  = {ratio_array}")
    return segments_mean_array, ratio_array

def draw_results(img, min_x, channel_width, number, ratio_array, manual_threshold):
    y_position = 3
    for ratio in ratio_array:
        if ratio > manual_threshold:  # Empty -> white
            img.draw_circle(min_x - 20, int(y_position - 3 + (number / 2)), 5, color=(255), thickness=1, fill=True)
            img.draw_rectangle((min_x, y_position - 3, channel_width, number), color=(255), thickness=1)
        else:  # Full -> Black
            img.draw_circle(min_x - 20, y_position + 5, 5, color=(0), thickness=1, fill=True)
            img.draw_rectangle((min_x, y_position - 3, channel_width, number), color=(0), thickness=1)
        y_position += number

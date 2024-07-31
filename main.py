import time

from camera_setup import setup_camera
from image_processing import process_image
from channel_detection import detect_channel, calculate_reference_mean, analyze_segments, draw_results

def main():
    #return values of height and width
    sensor_height, sensor_width = setup_camera()
    number = 20
    manual_threshold = 1.4
    clock = time.clock()

    while True:
        clock.tick()
        img = process_image()
        channel_roi = (106, 0, 63, 320)
        lines_found, min_x, min_y, channel_width, channel_height = detect_channel(img, sensor_width, sensor_height, channel_roi)

        if lines_found and channel_width >= 21 and channel_width < 40:
            ref_mean = calculate_reference_mean(img, min_x, channel_width, channel_height, number)
            segments_mean_array, ratio_array = analyze_segments(img, min_x, channel_width, channel_height, ref_mean, number)
            draw_results(img, min_x, channel_width, number, ratio_array, manual_threshold)

        print("FPS:", clock.fps())

if __name__ == "__main__":
    main()

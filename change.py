import time
from logging_setup import logger
# function that checks for lines,
# 1- checks the minimum x position of the leftmost line in new fun
# 2- compare the previous function with the new function



#def detect_change(img, min_x,sensor_width,change_roi):
#    min_x_new = sensor_width
#    lines = False
#    for l in img.find_lines(threshold=250, theta_margin=1, rho_margin=1):
#        if abs(l.theta()) < 1.0 or abs(l.theta() - 180) < 1.0:
#            lines = True
#            min_x_new = min(min_x_new, l.x1(), l.x2())
#            img.draw_line(l.x1(), l.y1(), l.x2(), l.y2(), color=(255), thickness=5)  # Adjust color and thickness as needed

#        if lines:
#            logger.info("found")
#            return min_x_new

#        else:
#            logger.warning("No lines were detected")
#            min_x_new = 0
#            return min_x_new


def change(img, sensor_width, change_roi):
    min_xn = sensor_width

    lines_found = False
    channel_detected = False

    for l in img.find_lines(roi=change_roi, threshold=250, theta_margin=1, rho_margin=1):
        #img.draw_line(l.x1(), l.y1(), l.x2(), l.y2(), color=(0), thickness=1)  # Adjust color and thickness as needed
        if abs(l.theta()) < 1.0 or abs(l.theta() - 180) < 1.0:
            lines_found = True
            min_xn = min(min_xn, l.x1(), l.x2())
            img.draw_line(l.x1(), l.y1(), l.x2(), l.y2(), color=(255), thickness=5)  # Adjust color and thickness as needed

            print(f"min_xn={min_xn}")
            #time.sleep(1)
            return min_xn



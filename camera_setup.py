import sensor

def setup_camera():
    sensor.reset()
    sensor.set_pixformat(sensor.GRAYSCALE)
    sensor.set_framesize(sensor.QVGA)
    sensor.set_auto_exposure(True)
    sensor.set_transpose(True)
    #sensor.skip_frames(time=2000)
    return sensor.height(), sensor.width()

import sensor

def process_image():
    img = sensor.snapshot().rotation_corr(x_rotation=0, y_rotation=0, z_rotation=1, x_translation=0, y_translation=0, zoom=1.1)
    img.histeq(True, 3)
    img.laplacian(1, sharpen=True)
    return img

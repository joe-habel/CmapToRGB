import numpy as np
import matplotlib.pyplot as plt

FIG_HEIGHT = 36
FIG_WIDTH = 36
PIXEL_SPACING = 0.75

STRIP_LOC = [3, 8, 11, 14, 18, 20, 23, 26, 32, 35]

def fractional_centers(locations, height, width, pixel_spacing):
    pixels_per_strip = float(width)/pixel_spacing

    fracs = []
    for i, vert_pos in enumerate(locations):
        row = []
        for j in range(int(pixels_per_strip)):
            row.append((vert_pos/float(height), j/float(pixels_per_strip)))
        fracs.append(row)

    return fracs

def bin_image(image, fractional_centers):
    size = image.shape[:2]
    max_h, max_w = size[0] - 1, size[1] - 1

    bin_slices = []

    rows = len(fractional_centers)
    pixels = len(fractional_centers[0])
    rescaled_image = np.zeros((rows, pixels, image.shape[2]))

    for i, row in enumerate(fractional_centers):
        row_slices = []
        if i == 0:
            height_start = 0
        else:
            prev_row = fractional_centers[i-1]
            height_start = (row[0][0] + prev_row[0][0])/2.*max_h
        if i == rows - 1:
            height_end = max_h
        else:
            next_row = fractional_centers[i+1]
            height_end = (row[0][0] + next_row[0][0])/2.*max_h

        height_slice = (int(height_start), int(height_end))
        #print "Row %s, Height Bounds: %s, %s"%(i, height_slice[0], height_slice[1])
        pixels = len(row)
        for j, pixel in enumerate(row):
            if j == 0:
                width_start = 0
            else:
                prev_pixel = row[j-1]
                width_start = (pixel[1] + prev_pixel[1])/2.*max_w
            if j == pixels - 1:
                width_end = max_w
            else:
                next_pixel = row[j+1]
                width_end = (pixel[1] + next_pixel[1])/2.*max_w

            width_slice = (int(width_start), int(width_end))
            #print "... Column %s, Width Bounds: %s, %s"%(j, width_slice[0], width_slice[1])
            row_slices.append((slice(*height_slice), slice(*width_slice)))

        bin_slices.append(row_slices)

    for i, row in enumerate(bin_slices):
        for j, pixel in enumerate(row):
            h_slice, w_slice = pixel
            #print slice(*h_slice), slice(*w_slice)
            sub_image = image[h_slice , w_slice]
            rescaled_image[i, j, :] = sub_image.mean(axis=(0, 1))

    return rescaled_image

def create_test_gradient(size, direction='h', colors='rg'):
    if direction == 'h':
        grad_index = 0
        tile_index = 1
    elif direction == 'v':
        grad_index = 1
        tile_index = 0

    gradient = np.linspace(0, 255, size[grad_index])
    if direction == 'h':
        gradient = gradient.T
        gradient = np.tile(gradient, (size[tile_index], 1))
        print gradient[0]
    elif direction == 'v':
        gradient = np.tile(gradient, (size[tile_index], 1))
        gradient = gradient.T


    all_colors = ['r', 'g', 'b']
    frames = []
    for i, color in enumerate(all_colors):
        if color in colors:
            frame = np.ones(size)*gradient
        else:
            frame = np.zeros(size)
        frames.append(frame)

    test_image = np.dstack(tuple(frames))
    return test_image.astype(int)

def generate_arduino_map(downsampled, output_location='arduino/static_cmap/Colormap.h'):
    start = '#ifndef Colormap\n#define Colormap\n'
    end = '#endif'

    pixels = downsampled.flatten()
    pixel_count = len(pixels)/3
    colormap_def = 'uint8_t cmap[%s][3] = {'%pixel_count
    pixel_total = '#define CALC_PIXELS %s\n'%pixel_count
    color_vals = ','.join(pixels)
    color_map = colormap_def + color_vals + '};\n'

    with open(output_location, 'w') as header:
        header.write(start)
        header.write(pixel_total)
        header.write(color_map)
        header.write(end)

#test_image = create_test_gradient((512,512))
test_image = plt.imread('jet.png')


fracs = fractional_centers(STRIP_LOC, FIG_HEIGHT, FIG_WIDTH, PIXEL_SPACING)
image = bin_image(test_image, fracs)
plt.imsave('map.png', image)
image *= 255
image = image.astype(int)
image = image.astype('S3')
generate_arduino_map(image)



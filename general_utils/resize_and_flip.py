import sys
import os
from os import walk, listdir
from os.path import isfile, join
from PIL import Image
import numpy

NEW_SIZE = (256, 256)
RESIZE_METHOD = Image.NEAREST


def main(sourceDir, destinationDir):
    subdirs = listdir(sourceDir)
    assert (('color' in subdirs) and ('mask' in subdirs) and ('normal' in subdirs),
            "Not all expected subdirectories are present!")

    colordir = join(sourceDir, 'color/')
    maskdir = join(sourceDir, 'mask/')
    normsdir = join(sourceDir, 'normal/')

    # Check if normals directory is empty
    normsdirNotEmpty = 1
    if not os.listdir(normsdir):
        normsdirNotEmpty = 0

    # Walk through the color directory
    for (dirpath, dirnames, filenames) in walk(colordir):

        tot = len(filenames)
        print("Starting to process {} images".format(tot))

        for idx, filename in enumerate(filenames):

            # Display progress
            print("image {} of {} ...".format(idx+1, tot))

            # Colored image
            coloredIm = getResized(colordir, filename)
            colordest = join(destinationDir, filename[:-4] + '_color.png')
            coloredIm.save(colordest, coloredIm.format)
            # Save rotated color
            coloredIm = coloredIm.rotate(180)
            colordest = join(destinationDir, filename[:-4] + 'f_color.png')
            coloredIm.save(colordest, coloredIm.format)

            # Mask image
            maskIm = getResized(maskdir, filename)
            maskdest = join(destinationDir, filename[:-4] + '_valid.png')
            maskIm.save(maskdest, maskIm.format)
            # Save rotated mask
            maskIm = maskIm.rotate(180)
            maskdest = join(destinationDir, filename[:-4] + 'f_valid.png')
            maskIm.save(maskdest, maskIm.format)

            # Resize respective normal
            if normsdirNotEmpty:
                normIm = getResized(normsdir, filename)
                normdest = join(destinationDir, filename[:-4] + '_normal_camera.png')
                normIm.save(normdest, normIm.format)
                # Save rotated normal
                normIm = normIm.rotate(180)
                pix = numpy.array(normIm.getdata())
                pix[:, 0] = -pix[:, 0]+254
                pix[:, 1] = -pix[:, 1]+254
                data = list(tuple(pixel) for pixel in pix)
                normIm.putdata(data)
                normdest = join(destinationDir, filename[:-4] + 'f_normal_camera.png')
                normIm.save(normdest, normIm.format)


def getResized(directory, filename):
    # Resize images
    imdir = join(os.getcwd(), directory, filename)
    im = Image.open(imdir)
    return im.resize(NEW_SIZE, RESIZE_METHOD)


if __name__ == '__main__':
    if not len(sys.argv) == 3:
        print("ERROR: need to pass the images directory and destination")

    print("Processing images from directory: {}".format(sys.argv[1]))
    print("Destination directory:            {}".format(sys.argv[2]))
    print('\n')

    main(sys.argv[1], sys.argv[2])

    # # Hardcoded directories for testing
    # source = "/home/baldeeb/Documents/EECS442/data/train"
    # destination = '/home/baldeeb/Documents/EECS442/output'
    # main(source, destination)


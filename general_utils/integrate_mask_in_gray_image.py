import sys
import os
from os import walk, listdir
from os.path import isfile, join
from PIL import Image

NEW_SIZE = (256, 256)
RESIZE_METHOD = Image.NEAREST


def main(sourceDir, destinationDir):
    subdirs = listdir(sourceDir)
    assert (('color' in subdirs) and ('mask' in subdirs) and ('normal' in subdirs),
            "Not all expected subdirectories are present!")

    colordir = join(sourceDir, 'color/')
    maskdir = join(sourceDir, 'mask/')
    normsdir = join(sourceDir, 'normal/')

    # Walk through the color directory
    for (dirpath, dirnames, filenames) in walk(colordir):

        tot = len(filenames)
        print("Starting to process {} images".format(tot))

        for idx, filename in enumerate(filenames):

            # Display progress
            print("image {} of {} ...".format(idx+1, tot))

            # Resize colored images
            imdir = join(os.getcwd(), colordir, filename)
            coloredIm = Image.open(imdir)
            coloredIm = coloredIm.resize(NEW_SIZE, RESIZE_METHOD)

            # Resize respective masks
            imdir = join(os.getcwd(), maskdir, filename)
            maskIm = Image.open(imdir)
            maskIm = maskIm.resize(NEW_SIZE, RESIZE_METHOD)

            # Resize respective normal
            imdir = join(os.getcwd(), normsdir, filename)
            normIm = Image.open(imdir)
            normIm = normIm.resize(NEW_SIZE, RESIZE_METHOD)

            # Combine image layers
            c1, c2, c3 = coloredIm.split()[0], maskIm.split()[0], coloredIm.split()[2]
            merged_im = Image.merge('RGB', [c1, c2, c3])

            # Save images
            colordest = join(os.getcwd(), 'temp', filename[:-4] + '_color.png')
            merged_im.save(colordest, merged_im.format)

            normdest = join(os.getcwd(), 'temp', filename[:-4] + '_normal_camera.png')
            normIm.save(normdest, normIm.format)

            maskdest = join(os.getcwd(), 'temp', filename[:-4] + '_valid.png')
            maskIm.save(maskdest, maskIm.format)


if __name__ == '__main__':
    if not len(sys.argv) == 3:
        print("ERROR: need to pass the images directory and destination")

    print("Processing images from directory: {}".format(sys.argv[1]))
    print("Destination directory:            {}".format(sys.argv[2]))
    print('\n')
    
    # # Hardcoded directories for testing
    # source = "/home/baldeeb/Documents/EECS442/eecs442challenge/train"
    # destination = './temp/'
    # main(source, destination)

    main(sys.argv[1], sys.argv[2])

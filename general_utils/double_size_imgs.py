import sys
import os
from os import walk
from os.path import isfile, join
from PIL import Image


def main(imsdir, imdestination):
    for (dirpath, dirnames, filenames) in walk(imsdir):
        for filename in filenames:
            imdir = join(os.getcwd(), dirpath, filename)

            if (not isfile(imdir)) or (imdir.split('.')[-1] != 'png'):
                continue

            with Image.open(imdir) as image:
                imcategory = dirpath.split('/')[-1]
		if imcategory == 'color':
                    filename = filename[:-4] + '_color.png'
                elif imcategory == 'mask':
                    filename = filename[:-4] + '_valid.png'
                elif imcategory == 'normal':
                    filename = filename[:-4] + '_normal_camera.png'

                print("original     :   {}".format(imdir))
                print("destination  :   {}\n".format(join(os.getcwd(), imdestination, filename)))

                cover = image.resize((256, 256), Image.NEAREST)
                cover.save(join(os.getcwd(), imdestination, filename), image.format)


if __name__ == '__main__':
    if not len(sys.argv) == 3:
        print("ERROR: need to pass the images directory and destination")

    main(sys.argv[1], sys.argv[2])

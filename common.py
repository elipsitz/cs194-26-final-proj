import numpy as np
import skimage.io as skio
import skimage as sk
import IPython
import PIL.Image
import IPython.display
import scipy.ndimage
import scipy
import skimage.transform
import matplotlib.pyplot as plt
import cv2

import io
import os

def load_images_from_directory(directory, scale=1.0):
    filenames = sorted(os.listdir(directory))
    filenames = [x for x in filenames if any(x.endswith(y) for y in ('jpg', 'jpeg', 'png'))]
    filenames = ["{}/{}".format(directory, x) for x in filenames]
    print("{} images".format(len(filenames)))

    imgs = []
    for i, filename in enumerate(filenames):
        print("Loading {} / {}...".format(i + 1, len(filenames)))
        imgs.append(imread(filename, scale))
    return imgs

def imread(filename, scale=1.0):
    im = skio.imread(filename)
    im = sk.img_as_float(im)
    if scale != 1.0:
        im = sk.transform.rescale(im, scale)
    return im

def imsave(filename, im):
    im = np.clip(im, -1, 1)
    skio.imsave(filename, im)

def showimage(im, clip=True, quality=80):
    if np.max(im) > 50:
        im = im / 255.0
    if clip:
        im = np.clip(im, 0, 1)
    im = sk.img_as_ubyte(im)
    f = io.BytesIO()
    PIL.Image.fromarray(im).save(f, 'jpeg' if quality < 100 else 'png', quality=quality)
    IPython.display.display(IPython.display.Image(data=f.getvalue()))

def videosave(filename, ims, fps=60):
    height, width = ims[0].shape[0], ims[0].shape[1]
    video = cv2.VideoWriter(filename, -1, 1, (width,height), fps)
    for im in ims:
        video.write(im)
    cv2.destroyAllWindows()
    video.release()

def vecdist(a, b):
    return np.sum((a - b) ** 2.0) ** 0.5

# ffmpeg -framerate 60 -i '%2d.png' -pix_fmt yuv420p -r 60 -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" out.mp4

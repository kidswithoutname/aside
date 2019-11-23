import os
import numpy as np
import tensorflow as tf
from matplotlib import pyplot as plt
from PIL import Image
import re
import cv2
import glob

import models

# RUN WITH
# python36 predicts.py models/NYU_FCRN.ckpt images3
#
#

# Default input size
height = 228
width = 304
channels = 3
batch_size = 1
j=0

# Drone
linewidth=960

# Webcam
linewidth=1280
    
def contruct_net():
    # Create a placeholder for the input image
    input_node = tf.placeholder(tf.float32, shape=(None, height, width, channels))
    # Construct the network
    net = models.ResNet50UpProj({'data': input_node}, batch_size, 1, False)
    return input_node,net


def threshold(imageArray):

    balanceAr = []
    newAr = imageArray
    from statistics import mean
    for eachRow in imageArray:
        for eachPix in eachRow:
            avgNum = mean(eachPix[:3])
            balanceAr.append(avgNum)

    balance = mean(balanceAr)
    for eachRow in newAr:
        for eachPix in eachRow:
            if mean(eachPix[:3]) > balance:
                eachPix[0] = 255
                eachPix[1] = 255
                eachPix[2] = 255
                eachPix[3] = 255
            else:
                eachPix[0] = 0
                eachPix[1] = 0
                eachPix[2] = 0
                eachPix[3] = 255
    return newAr


def np_multi_tofile(data, frame_number=1, prefix=None):
    # https://stackoverflow.com/questions/3685265/how-to-write-a-multidimensional-array-to-a-text-file
    if prefix:
        outname = str(prefix) + str(frame_number) + ".txt"
    else:
        outname = str(frame_number) + ".txt"

    # Write the array to disk
    with open(outname, 'w') as outfile:
        # I'm writing a header here just for the sake of readability
        # Any line starting with "#" will be ignored by numpy.loadtxt
        outfile.write('# Array shape: {0}\n'.format(data.shape))
        print(data.shape)
        # Iterating through a ndimensional array produces slices along
        # the last axis. This is equivalent to data[i,:,:] in this case
        for data_slice in data:
            # The formatting string indicates that I'm writing out
            # the values in left-justified columns 7 characters in width
            # with 2 decimal places.
            np.savetxt(outfile, data_slice, fmt='%-7.2f')

            # Writing out a break to indicate different slices...
            outfile.write('# New slice\n')
    return outname


def np_multi_fromfile(filename):
    new_data = np.loadtxt(filename)
    fline = open(filename).readline().rstrip()
    # kk = re.findall(r'\d+', fline)
    newstr = ''.join((ch if ch in '0123456789' else ' ') for ch in fline)
    shape = [int(i) for i in newstr.split()]
    new_data = new_data.reshape(shape)
    return new_data


def save_sample(frame_number, pred, frame):
    if args.save_session:
        cv2.imwrite("{}/tellocap{}.jpg".format(ddir, imgCount), frameRet)


    if frame_number == 3:
        myfile = open("sample_pred_" + str(frame_number) + ".txt", 'w')
        np.set_printoptions(threshold=np.inf, linewidth=linewidth)
        myfile.write(np.array2string(pred, formatter={'float_kind': lambda x: "%.3f" % x}, precision=2, separator=',',suppress_small=True).replace(',\n', '').replace('   ', '\t').replace('[','').replace(']', ''))
        myfile.close()

        myfile = open("sample_frame_" + str(frame_number) + ".txt", 'w')
        np.set_printoptions(threshold=np.inf, linewidth=linewidth)
        myfile.write(np.array2string(frame, formatter={'float_kind': lambda x: "%.3f" % x}, precision=2, separator=',',suppress_small=True).replace(',\n', '').replace('   ', '\t').replace('[','').replace(']', ''))
        myfile.close()
    return


# def predict_frame(model_data_path, frame, frame_number, input_node, net, output_dir):
def predict_frame(sess, frame, frame_number, input_node, net, output_dir):

    # Save multi array to file
    # filenma = np_multi_tofile(frame, frame_number)
    # new = np_multi_fromfile(filenma)
    # # Just to check that they're the same...
    # assert np.all(frame == new)


    img = Image.fromarray(frame)
    img = img.resize([width,height], Image.ANTIALIAS)
    img = np.array(img).astype('float32')
    img = np.expand_dims(np.asarray(img), axis = 0)

    # with tf.Session() as sess:
    # Load the converted parameters
    # print('Loading the model')
    # saver = tf.train.Saver()
    # saver.restore(sess, model_data_path)

    # Use to load from npy file
    #net.load(model_data_path, sess)

    # Evalute the network for the given image
    pred = sess.run(net.get_output(), feed_dict={input_node: img})

    # Save prediction into file
    # np_multi_tofile(pred[0,:,:,0], 19)

    # Plot result
    fig = plt.figure()
    ii = plt.imshow(pred[0,:,:,0], interpolation='nearest')

    # if save_example:
    #     save_sample(frame_number, pred, frame)

    # Set lateral color bar
    # fig.colorbar(ii)

    outname=str(frame_number) + ".jpg"
    plt.savefig(output_dir+"/"+outname)
    plt.close(fig)
        
    return pred


def next_path(path_pattern):
    """
    Finds the next free path in an sequentially named list of files

    e.g. path_pattern = 'file-%s.txt':

    file-1.txt
    file-2.txt
    file-3.txt

    Runs in log(n) time where n is the number of existing files in sequence
    """
    i = 1

    # First do an exponential search
    while os.path.exists(path_pattern % i):
        i = i * 2

    # Result lies somewhere in the interval (i/2..i]
    # We call this interval (a..b] and narrow it down until a + 1 = b
    a, b = (i / 2, i)
    while a + 1 < b:
        c = (a + b) / 2 # interval midpoint
        a, b = (c, b) if os.path.exists(path_pattern % c) else (a, c)

    return path_pattern % b


def clear_directory(directory):
    if os.path.exists(directory):
        os.rename(directory,next_path(directory + '-%s'))
    os.makedirs(directory)


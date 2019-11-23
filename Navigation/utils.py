import matplotlib.patches as patches
import numpy as np
from predictf import predict_frame, contruct_net, clear_directory


def rect(box):
    y_min, y_max, x_min, x_max = box
    r_w = x_max - x_min
    r_h = y_max - y_min
    rect = patches.Rectangle((x_min, y_min), r_w, r_h, linewidth=1, edgecolor='r', facecolor='none')
    return rect


def circle(centerm, radius=2):
    x_cen, y_cen = centerm
    circle = patches.Circle((x_cen, y_cen), radius, color='r')
    return circle


def center(rectm):
    y_min, y_max, x_min, x_max = rectm
    centerm = x_min + (x_max - x_min) / 2, y_min + (y_max - y_min) / 2
    return centerm


def bbox2(img):
    rows = np.any(img, axis=1)
    cols = np.any(img, axis=0)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    return rmin, rmax, cmin, cmax


def bbox1(img):
    a = np.where(img != 0)
    bbox = np.min(a[0]), np.max(a[0]), np.min(a[1]), np.max(a[1])
    return bbox


def rescale_center(frame_shape, pred_shape, centerm):
    x_cen, y_cen = centerm
    w_frame, h_frame, _ = frame_shape
    w_pred, h_pred = pred_shape

    coord_x = w_frame * x_cen / w_pred
    coord_y = h_frame * y_cen / h_pred

    return coord_x, coord_y


def rescale_box(frame_shape, pred_shape, rectm):
    y_min, y_max, x_min, x_max = rectm
    w_frame, h_frame, _ = frame_shape
    w_pred, h_pred = pred_shape

    coord_x_min = w_frame * x_min / w_pred
    coord_x_max = w_frame * x_max / w_pred

    coord_y_min = h_frame * y_min / h_pred
    coord_y_max = h_frame * y_max / h_pred

    return coord_y_min, coord_y_max, coord_x_min, coord_x_max


def save_as_csv(thresh):
    filename = "sample_frame.txt"
    myfile = open(filename, 'w')
    np.set_printoptions(threshold=np.inf, linewidth=960)
    myfile.write(np.array2string(thresh, formatter={'float_kind': lambda x: "%.3f" % x}, precision=2, separator=',',suppress_small=True).replace(',\n', '').replace('   ', '\t').replace('[','').replace(']', ''))
    myfile.close()
    return filename


def simple_save(thresh):
    filename = 'test.csv'
    np.savetxt(filename, thresh, delimiter=',')
    return filename


def np_multi_tofile(data, frame_number, dir, prefix):
    # https://stackoverflow.com/questions/3685265/how-to-write-a-multidimensional-array-to-a-text-file
    outname = "{}/{}_{}.txt".format(dir, prefix, frame_number)
    # Write the array to disk
    with open(outname, 'w') as outfile:
        # I'm writing a header here just for the sake of readability
        # Any line starting with "#" will be ignored by numpy.loadtxt
        outfile.write('# Array shape: {0}\n'.format(data.shape))
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


# def do_depth_prediction(frameRet, imgCount, input_node, net, ddird, saveses, ddirp):
def do_depth_prediction(frameRet, imgCount, input_node, net, ddird, saveses, ddirp, sess):
    #  ------------------------------- BEGIN Depth Prediction ADDED ------------------------------------------ #
    # pred = predict_frame('models/NYU_FCRN.ckpt', frameRet, imgCount, input_node, net, ddird)
    pred = predict_frame(sess, frameRet, imgCount, input_node, net, ddird)

    if saveses:
        #  Save prediction into file
        np_multi_tofile(pred[0, :, :, 0], imgCount, ddirp, 'pred')
        np_multi_tofile(frameRet, imgCount, ddirp, 'frame')

    frame_pred = pred[0, :, :, 0]
    thresh = (frame_pred.astype('float32') > np.percentile(frame_pred, 95)) * frame_pred.astype('float32')

    box = bbox2(thresh)
    pred_center = center(bbox2(thresh))
    res_center = rescale_center(frameRet.shape, frame_pred.shape, pred_center)
    res_box = rescale_box(frameRet.shape, frame_pred.shape, bbox2(thresh))

    print("Frame shape:", frameRet.shape)
    print("Center:", res_center)
    print("BBox:", res_box)

    print("Pred shape:", frame_pred.shape)
    print("Center:", pred_center)
    print("BBox:", box)

    # cv2.circle(frameRet, (int(res_center[0]), int(res_center[1])), 10, (0, 255, 0), 2)

    x_face = res_box[2]
    y_face = res_box[0]
    w_face = res_box[3] - res_box[2]
    h_face = res_box[1] - res_box[0]

    faces = x_face, y_face, w_face, h_face
    return faces, res_center
    #  ------------------------------- END Depth Prediction ADDED ------------------------------------------- #
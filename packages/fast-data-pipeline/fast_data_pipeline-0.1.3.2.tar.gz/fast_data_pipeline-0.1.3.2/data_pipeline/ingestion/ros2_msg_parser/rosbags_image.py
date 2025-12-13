import sys
from array import array
from time import perf_counter_ns

import cv2
import numpy as np

name_to_dtypes = {
    "rgb8": (np.uint8, 3),
    "rgba8": (np.uint8, 4),
    "rgb16": (np.uint16, 3),
    "rgba16": (np.uint16, 4),
    "bgr8": (np.uint8, 3),
    "bgra8": (np.uint8, 4),
    "bgr16": (np.uint16, 3),
    "bgra16": (np.uint16, 4),
    "mono8": (np.uint8, 1),
    "mono16": (np.uint16, 1),
    # for bayer image (based on cv_bridge.cpp)
    "bayer_rggb8": (np.uint8, 1),
    "bayer_bggr8": (np.uint8, 1),
    "bayer_gbrg8": (np.uint8, 1),
    "bayer_grbg8": (np.uint8, 1),
    "bayer_rggb16": (np.uint16, 1),
    "bayer_bggr16": (np.uint16, 1),
    "bayer_gbrg16": (np.uint16, 1),
    "bayer_grbg16": (np.uint16, 1),
    # OpenCV CvMat types
    "8UC1": (np.uint8, 1),
    "8UC2": (np.uint8, 2),
    "8UC3": (np.uint8, 3),
    "8UC4": (np.uint8, 4),
    "8SC1": (np.int8, 1),
    "8SC2": (np.int8, 2),
    "8SC3": (np.int8, 3),
    "8SC4": (np.int8, 4),
    "16UC1": (np.uint16, 1),
    "16UC2": (np.uint16, 2),
    "16UC3": (np.uint16, 3),
    "16UC4": (np.uint16, 4),
    "16SC1": (np.int16, 1),
    "16SC2": (np.int16, 2),
    "16SC3": (np.int16, 3),
    "16SC4": (np.int16, 4),
    "32SC1": (np.int32, 1),
    "32SC2": (np.int32, 2),
    "32SC3": (np.int32, 3),
    "32SC4": (np.int32, 4),
    "32FC1": (np.float32, 1),
    "32FC2": (np.float32, 2),
    "32FC3": (np.float32, 3),
    "32FC4": (np.float32, 4),
    "64FC1": (np.float64, 1),
    "64FC2": (np.float64, 2),
    "64FC3": (np.float64, 3),
    "64FC4": (np.float64, 4),
}

NAME_TO_CVTYPE = {
    "rgb8": "RGB",
    "rgba8": "RGBA",
    "rgb16": "RGB",
    "rgba16": "RGBA",
    "bgr8": "BGR",
    "bgra8": "BGRA",
    "bgr16": "BGR",
    "bgra16": "BGRA",
    "mono8": "GRAY",
    "mono16": "GRAY",
    "bayer_rggb8": "BayerRGGB",
    "bayer_bggr8": "BayerBGGR",
    "bayer_gbrg8": "BayerGBRG",
    "bayer_grbg8": "BayerGRBG",
    "bayer_rggb16": "BayerRGGB",
    "bayer_bggr16": "BayerBGGR",
    "bayer_gbrg16": "BayerGBRG",
    "bayer_grbg16": "BayerGRBG",
}


def get_cv_type(src_encoding: str, dst_encoding: str):
    if src_encoding == dst_encoding:
        return None
    if NAME_TO_CVTYPE.get(src_encoding) is None:
        raise NotImplementedError(f"`src_encoding` `{src_encoding}` not implemented.")
    if NAME_TO_CVTYPE.get(dst_encoding) is None:
        raise NotImplementedError(f"`dst_encoding` `{dst_encoding}` not implemented.")

    return getattr(cv2, f"COLOR_{NAME_TO_CVTYPE[src_encoding]}2{NAME_TO_CVTYPE[dst_encoding]}")


def convert_color(img: np.ndarray, src_encoding: str, dst_encoding: str):
    return cv2.cvtColor(img, get_cv_type(src_encoding, dst_encoding))


def image_to_numpy_rosbags(msg):
    """
    Convert a rosbags Image message directly to numpy array without converting to native ROS message.
    
    Args:
        msg: Rosbags Image message (with attributes: encoding, is_bigendian, height, width, step, data)
        
    Returns:
        numpy array with the image data
    """
    if not msg.encoding in name_to_dtypes:
        raise TypeError("Unrecognized encoding {}".format(msg.encoding))

    dtype_class, channels = name_to_dtypes[msg.encoding]
    dtype = np.dtype(dtype_class)
    dtype = dtype.newbyteorder(">" if msg.is_bigendian else "<")
    shape = (msg.height, msg.width, channels)

    if isinstance(msg.data, list):
        image_data = bytes(msg.data)
    else:
        image_data = msg.data

    data = np.frombuffer(image_data, dtype=dtype).reshape(shape)
    data.strides = (msg.step, dtype.itemsize * channels, dtype.itemsize)

    if channels == 1:
        data = data[..., 0]
    return data
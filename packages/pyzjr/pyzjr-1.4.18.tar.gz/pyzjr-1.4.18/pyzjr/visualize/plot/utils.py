"""
Copyright (c) 2023, Auorui.
All rights reserved.
"""
import cv2
import numpy as np

def OverlayPng(imgBack, imgFront, pos=(0, 0), alpha_gain=1.0):
    """
    Overlay display image with proper alpha blending
    :param imgBack: Background image, no format requirement, 3 channels
    :param imgFront: PNG pre image, must be read using cv2.IMREAD_UNCHANGED=-1
    :param pos: Placement position

    Examples:
    '''
        background = cv2.imread(background_path)
        overlay = cv2.imread(overlay_path, cv2.IMREAD_UNCHANGED)
        fused_image = pyzjr.OverlayPng(background, overlay, alpha_gain=1.5)
    '''
    """
    img_back = imgBack.copy()
    hf, wf, cf = imgFront.shape
    hb, wb, cb = imgBack.shape
    y_pos, x_pos = pos
    y_end = y_pos + hf
    x_end = x_pos + wf

    # Ensure we don't go beyond the background boundaries
    if y_end > hb:
        y_end = hb
    if x_end > wb:
        x_end = wb

    # Resize overlay to fit the background (optional but good practice)
    overlay_resized = cv2.resize(imgFront, (x_end - x_pos, y_end - y_pos))

    overlay_alpha = overlay_resized[:, :, 3].astype(float) / 255.0
    overlay_alpha = np.clip(overlay_alpha * alpha_gain, 0, 1)
    background_alpha = 1.0 - overlay_alpha

    result = overlay_resized[:, :, :3] * overlay_alpha[..., np.newaxis] + img_back[y_pos:y_end, x_pos:x_end, :3] * background_alpha[..., np.newaxis]
    img_back[y_pos:y_end, x_pos:x_end, :3] = result.astype(np.uint8)

    return img_back


def norm_to_abs(cx_norm, cy_norm, w_norm, h_norm, img_w, img_h):
    """
    Convert normalized bounding box coordinates to absolute pixel coordinates.

    This function transforms bounding box parameters from normalized [0,1] range
    (common in machine learning datasets) to absolute pixel values based on image dimensions.

    :param cx_norm: Normalized x-coordinate of bounding box center [0,1]
    :param cy_norm: Normalized y-coordinate of bounding box center [0,1]
    :param w_norm: Normalized width of bounding box [0,1]
    :param h_norm: Normalized height of bounding box [0,1]
    :param img_w: Width of the image in pixels
    :param img_h: Height of the image in pixels
    :return: list: [x_min, y_min, x_max, y_max] absolute coordinates (pixels) representing:
                                                x_min: Left boundary of bounding box
                                                y_min: Top boundary of bounding box
                                                x_max: Right boundary of bounding box
                                                y_max: Bottom boundary of bounding box
    """
    cx = cx_norm * img_w
    cy = cy_norm * img_h
    w = w_norm * img_w
    h = h_norm * img_h
    x_min = cx - w/2
    y_min = cy - h/2
    x_max = cx + w/2
    y_max = cy + h/2
    return [x_min, y_min, x_max, y_max]


def abs_to_norm(x_min, y_min, x_max, y_max, img_w, img_h):
    """
    Convert absolute pixel coordinates to normalized bounding box coordinates.

    This function transforms bounding box parameters from absolute pixel values
    to normalized [0,1] range (common in machine learning datasets).

    :param x_min: Left boundary of bounding box in pixels
    :param y_min: Top boundary of bounding box in pixels
    :param x_max: Right boundary of bounding box in pixels
    :param y_max: Bottom boundary of bounding box in pixels
    :param img_w: Width of the image in pixels
    :param img_h: Height of the image in pixels
    :return: list: [cx_norm, cy_norm, w_norm, h_norm] normalized coordinates representing:
                    cx_norm: Normalized x-coordinate of bounding box center [0,1]
                    cy_norm: Normalized y-coordinate of bounding box center [0,1]
                    w_norm: Normalized width of bounding box [0,1]
                    h_norm: Normalized height of bounding box [0,1]
    """
    w = x_max - x_min
    h = y_max - y_min
    cx = x_min + w / 2
    cy = y_min + h / 2
    cx_norm = cx / img_w
    cy_norm = cy / img_h
    w_norm = w / img_w
    h_norm = h / img_h
    return [cx_norm, cy_norm, w_norm, h_norm]
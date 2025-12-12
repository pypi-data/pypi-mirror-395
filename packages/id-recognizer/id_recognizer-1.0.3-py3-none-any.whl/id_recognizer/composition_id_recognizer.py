import collections
import dataclasses
import functools
import enum
import logging
import os
import hashlib
import requests
import json
import re
import time
import uuid
import math
from logging import Logger, StreamHandler
import base64
import typing as _typing
import cv2
from cv2.typing import MatLike as _MatLike, Rect as _Rect, Size as _Size
import numpy as np
from numpy.typing import NDArray
import zxingcpp
from zxingcpp import TextMode

_logger = Logger(name="CIR", level=logging.DEBUG)
_logger.addHandler(StreamHandler())


############################################
#               basic types
############################################
@dataclasses.dataclass
class CtInfo:
    rect: _Rect
    ct: _MatLike | NDArray = None
    area: float = 0
    zone_area: float = 0
    hull: _MatLike | NDArray = None
    sides: int = 0


@dataclasses.dataclass
class ImParam(object):
    blur_size: int = 0
    dilate_size: int = 0
    auto_binary: bool = False
    zone_auto_bin: bool = False
    zone_block_size: int = 101
    zone_c: int = 2
    zone_max: int = 255
    thresh: int = 90


class StatusCode(int, enum.Enum):
    OK = 200
    ERR_UNKNOWN = 500
    ERR_IM_NOT_EXIST = 1000
    ERR_DECODE_FAIL = 1001
    ERR_LAYOUT_ANALYSIS_FAIL = 1002
    ERR_OCR_FAIL = 1003
    ERR_OCR_AUTH_FAIL = 1004


class CardDirection(int, enum.Enum):
    NORMAL = 1
    INVERTED = 2
    ROTATED_90_CW = 3
    ROTATED_90_CCW = 4


class IdSource(int, enum.Enum):
    UNKNOWN = 0
    QR_CODE = 1
    BAR_CODE = 2
    OCR = 3


@dataclasses.dataclass
class RecognitionResult:
    status: StatusCode = StatusCode.ERR_IM_NOT_EXIST
    sid: str = ""  # 读取到的学号
    raw_qr_code: str = ""  # 二维码中的信息
    raw_bar_code: str = ""  # 条形码中的信息
    b64_response: str = ""  # 处理后的图像的base64编码
    original_direction: CardDirection = CardDirection.NORMAL  # 图像的原始方向, 若原始方向为`NORMAL`, 外部可不使用`b64_response`
    id_source: IdSource = IdSource.UNKNOWN  # sid的来源

    def __repr__(self) -> str:
        fields = []
        for field in dataclasses.fields(self):
            name = field.name
            value = getattr(self, name)
            if name == "b64_response":
                if len(value) > 20:
                    value_repr = f"<b64_response len={len(value)}>"
                else:
                    value_repr = repr(value)
            elif name == "status" or name == "original_direction" or name == "id_source":
                value_repr = value.name if isinstance(value, enum.Enum) else repr(value)
            else:
                value_repr = repr(value)
            fields.append(f"{name}={value_repr}")
        return f"{self.__class__.__name__}({', '.join(fields)})"


_QueryInfo = _typing.Tuple[bool, _typing.List[CtInfo]]
_Callable = _typing.Callable[[_typing.List[CtInfo]], _typing.Tuple[bool, _typing.List[CtInfo]]] | None
_ContextCategory = _typing.Literal['id', 'side', 'container', 'dot']
_Orientation = _typing.Literal['ttt', 'ttl', 'ttb', 'ttr', 'unknown']
_OCRRunUnit = _typing.Tuple[_typing.List[_typing.List[int]], str, int]
RecInputType = str | bytes | _MatLike


############################################
#       basic image process function
############################################
def do_draw(im: _MatLike, cts: _typing.List[CtInfo], thickness: int = 4, bounding: bool = True):
    if im is None or cts is None:
        return
    for ct in cts:
        cv2.drawContours(image=im, contourIdx=-1, contours=[ct.ct], thickness=thickness, color=(0, 0, 255))
        if bounding:
            cv2.rectangle(img=im, rec=ct.rect, thickness=6, color=(100, 255, 0))


def do_show(title: str, im: _MatLike):
    if im is None:
        return
    cv2.imshow(title, im)


def do_erode(im: _MatLike, k: _typing.Sequence[int]) -> _MatLike:
    if 0 in k:
        return im
    kernel = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=k)
    return cv2.erode(src=im, kernel=kernel)


def do_open(im: _MatLike, k: _typing.Sequence[int]) -> _MatLike:
    if 0 in k:
        return im
    kernel = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=k)
    return cv2.morphologyEx(im, op=cv2.MORPH_OPEN, kernel=kernel)


def do_dilate(im: _MatLike, k: _typing.Sequence[int]) -> _MatLike:
    if 0 in k:
        return im
    kernel = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=k)
    return cv2.dilate(src=im, kernel=kernel)


def do_sharpen(im: _MatLike, sigma: float = 1.5, strength: float = 1.0) -> _MatLike:
    if sigma == 0:
        return im
    blurred = cv2.GaussianBlur(im, ksize=(0, 0), sigmaX=sigma)
    weighted = cv2.addWeighted(im, 1.0 + strength, blurred, -strength, 0)
    weighted = np.clip(weighted, 0, 255).astype(np.uint8)
    return weighted


def do_clahe(im: _MatLike, limit: float = 2.0, size: _typing.Sequence[int] = (8, 8)) -> _MatLike:
    if limit == 0:
        return im
    lab = cv2.cvtColor(im, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=limit, tileGridSize=size)
    l_channel = clahe.apply(l_channel)
    lab = cv2.merge((l_channel, a, b))
    bright_image = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    return bright_image


def do_binary(
        im: _MatLike,
        blur_size: _Size,
        auto: bool = True,
        zone_auto: bool = False,
        zone_auto_max: int = 255,
        zone_auto_c: int = 2,
        zone_auto_block_size: int = 101,
        bin_thresh: int = 90
) -> _MatLike:
    blur = cv2.GaussianBlur(im, ksize=blur_size, sigmaX=0)
    if auto:
        _, binary = cv2.threshold(blur, thresh=0, maxval=255, type=cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    elif zone_auto:
        b_size = zone_auto_block_size if zone_auto_block_size >= 0 else min(im.shape[:2]) // 30
        b_size = b_size if b_size % 2 == 1 else b_size + 1
        binary = cv2.adaptiveThreshold(
            src=blur,
            maxValue=zone_auto_max,
            adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            thresholdType=cv2.THRESH_BINARY_INV,
            C=zone_auto_c,
            blockSize=b_size
        )
    else:
        _, binary = cv2.threshold(blur, thresh=bin_thresh, maxval=255, type=cv2.THRESH_BINARY_INV)

    return binary


def do_rotate(im: _MatLike, code: int) -> _MatLike | None:
    if im is None:
        return im
    return cv2.rotate(im, rotateCode=code)


def do_find_point(ct: _MatLike, op: int) -> _typing.Sequence[int]:
    if ct is None:
        return []
    dots = ct.copy().squeeze()
    target = None
    for d in dots:
        if op == 0:
            if target is None or (target[0] + target[1]) > (d[0] + d[1]):
                target = d
        if op == 1:
            if target is None or (target[0] - target[1]) < (d[0] - d[1]):
                target = d
        if op == 2:
            if target is None or (target[0] + target[1]) < (d[0] + d[1]):
                target = d
        if op == 3:
            if target is None or (target[0] - target[1]) > (d[0] - d[1]):
                target = d
    return target


def do_warp(
        full_im: _MatLike,
        ct: CtInfo,
        whr: float
) -> _typing.Tuple[bool, _MatLike | None]:
    if full_im is None or ct is None:
        return False, None
    x, y, w, h = ct.rect
    im = full_im[y:y + h, x:x + w]
    im_h, im_w = im.shape[:2]
    im_h = im_h if whr <= 0 else int(im_w / whr)
    ct_bk = ct.ct.copy().reshape((-1, 2)) - ct.rect[:2]
    ct_bk = ct_bk.reshape((-1, 1, 2))
    left_top = do_find_point(ct=ct_bk, op=0)
    right_top = do_find_point(ct=ct_bk, op=1)
    right_bottom = do_find_point(ct=ct_bk, op=2)
    left_bottom = do_find_point(ct=ct_bk, op=3)
    src_pts = np.float32([left_top, right_top, right_bottom, left_bottom])
    dst_pts = np.float32([[0, 0], [im_w, 0], [im_w, im_h], [0, im_h]])
    matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
    dst = cv2.warpPerspective(src=im, M=matrix, dsize=[im_w, im_h])
    return True, dst


def do_find_cts(
        im: _MatLike,
        mode: int = cv2.RETR_EXTERNAL,
        min_size: _typing.Tuple[float, float] = (0, 0),
        max_size: _typing.Tuple[float, float] = (999999, 999999),
        min_whr: float | None = None,
        max_whr: float | None = None,
        sort_type: _typing.Literal["x", "y", "area"] | None = None
) -> _typing.List[CtInfo]:
    cts, _ = cv2.findContours(image=im, mode=mode, method=cv2.CHAIN_APPROX_SIMPLE)
    target_cts = []
    for c in cts:
        rect_ = cv2.boundingRect(c)
        if min_size[0] <= rect_[2] <= max_size[0] and min_size[1] <= rect_[3] <= max_size[1]:
            h = rect_[3] if rect_[3] > 0 else 1e6
            whr = rect_[2] / h
            whr1 = min_whr if min_whr is not None else 0
            whr2 = max_whr if max_whr is not None else 1e6
            if whr1 <= whr <= whr2:
                zone_area = cv2.contourArea(c)
                ct_ = CtInfo(rect=rect_, ct=c, area=rect_[2] * rect_[3], zone_area=zone_area, sides=0)
                target_cts.append(ct_)
    match sort_type:
        case "x":
            target_cts = sorted(target_cts, key=lambda ci: ci.rect[0])
        case "y":
            target_cts = sorted(target_cts, key=lambda ci: ci.rect[1])
        case "area":
            target_cts = sorted(target_cts, key=lambda ci: ci.area)
        case _:
            ...
    return target_cts


def filter_ct(
        cts: _typing.List[CtInfo],
        min_w: float,
        max_w: float,
        min_h: float,
        max_h: float,
        min_whr: float,
        max_whr: float,
        sides: int = 4,
        delta: float = 0.02,
        use_min_rect: bool = False,
        solid_area_ratio: float = 0,
        circle: bool = False
) -> _typing.List[CtInfo]:
    target_cts: _typing.List[CtInfo] = []
    for idx, cti in enumerate(cts):
        x, y, w, h = cti.rect
        min_rect_w, min_rect_h = 0, 0
        if use_min_rect:
            _, (mw, mh), angle = cv2.minAreaRect(cti.ct)
            min_rect_w, min_rect_h = mw, mh
            little, greater = min(mw, mh), max(mw, mh)
            w = little if w < h else greater
            h = little if w > h else greater

        cond1 = min_w <= w <= max_w and min_h <= h <= max_h
        ratio = w / h if h > 0 else 100000
        cond2 = min_whr <= ratio <= max_whr
        if not cond1 or not cond2:
            continue

        arc = cv2.arcLength(cti.ct, closed=True)
        epsilon = delta * arc
        points = cv2.approxPolyDP(cti.ct, epsilon=epsilon, closed=True)

        if sides == -1 or circle:
            if sides == -1:
                cond3 = True
            else:
                perimeter = cv2.arcLength(cti.ct, True)
                area = cv2.contourArea(cti.ct)
                if perimeter == 0 or area == 0:
                    cond3 = False
                else:
                    circularity = math.pi * 4 * area / (perimeter ** 2)
                    cond3 = True if 1.15 >= circularity >= 0.85 and len(points) > 4 else False
        else:
            cond3 = len(points) == sides

        if not cond3:
            continue

        cond4 = True
        if solid_area_ratio > 0:
            if min_rect_w <= 0 or min_rect_h <= 0:
                _, (min_rect_w, min_rect_h), _ = cv2.minAreaRect(cti.ct)
            min_rect_area = min_rect_w * min_rect_h
            ct_area = cv2.contourArea(cti.ct)
            cond4 = True if min_rect_area > 0 and ct_area / min_rect_area >= solid_area_ratio else False
        if not cond4:
            continue
        target_cts.append(cti)
    return target_cts


def extract_outer_frame(cts: _typing.List[CtInfo], delta: int = 20) -> _typing.List[CtInfo]:
    if len(cts) != 2:
        return cts
    r1x, r1y, r1w, r1h = cts[0].rect
    r2x, r2y, r2w, r2h = cts[-1].rect
    r1rb = r1x + r1w, r1y + r1h
    r2rb = r2x + r2w, r2y + r2h

    if abs(r1w - r2w) > abs(delta) * 2 or abs(r1h - r2h) > abs(delta) * 2:
        return cts

    if r1x >= r2x and r1y >= r2y and r1rb[0] <= r2rb[0] and r1rb[1] <= r2rb[1]:
        return cts[1:]
    if r1x <= r2x and r1y <= r2y and r1rb[0] >= r2rb[0] and r1rb[1] >= r2rb[1]:
        return cts[:1]
    return cts


def fit_line(
        p1: _typing.Sequence[float],
        p2: _typing.Sequence[float]
) -> _typing.Sequence[float]:
    x1, y1 = p1
    x2, y2 = p2
    A = y2 - y1
    B = x1 - x2
    C = x2 * y1 - x1 * y2
    return A, B, C


def intersection(
        line1: _typing.Sequence[float],
        line2: _typing.Sequence[float]
) -> _typing.Tuple[bool, _typing.Tuple[int, int]]:
    if line1 is None or line2 is None:
        return False, (0, 0)
    A1, B1, C1 = line1
    A2, B2, C2 = line2
    D = A1 * B2 - A2 * B1
    if D == 0:
        return False, (0, 0)
    x = (B1 * C2 - B2 * C1) / D
    y = (A2 * C1 - A1 * C2) / D
    return True, (int(x), int(y))


def fit_bounding_rect(pts: _typing.Sequence[_typing.Sequence[float]]) -> _MatLike:
    rect = cv2.minAreaRect(np.array(pts, dtype=np.float32))
    points = cv2.boxPoints(rect)
    bounding = np.zeros((4, 2), dtype=np.float32)
    s = points.sum(axis=1)
    bounding[0] = points[np.argmin(s)]
    bounding[2] = points[np.argmax(s)]

    diff = np.diff(points, axis=1)
    bounding[1] = points[np.argmin(diff)]
    bounding[3] = points[np.argmax(diff)]
    return bounding


def side_segment_length(bounding_rect: _MatLike) -> _typing.Sequence[float]:
    if bounding_rect is None:
        return [0, 0, 0, 0]
    min_b_int = bounding_rect.astype(dtype=np.int32)
    dis1 = distance(p1=min_b_int[0], p2=min_b_int[1])
    dis2 = distance(p1=min_b_int[1], p2=min_b_int[2])
    dis3 = distance(p1=min_b_int[2], p2=min_b_int[3])
    dis4 = distance(p1=min_b_int[3], p2=min_b_int[0])
    return dis1, dis2, dis3, dis4


def center(rect: _Rect) -> _typing.Sequence[float]:
    return (rect[0] + rect[2]) / 2, (rect[1] + rect[3]) / 2


def distance(p1: _typing.Sequence[float], p2: _typing.Sequence[float]) -> float:
    return float(np.linalg.norm(np.array(p1) - np.array(p2)))


def do_shrink(im: _MatLike, line_size: float = 1) -> _typing.Tuple[_MatLike, float]:
    h, w = im.shape[:2]
    grey_im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    bin_im = do_binary(im=grey_im, blur_size=(5, 5), auto=True)
    bin_im = do_open(im=bin_im, k=(1, max(1, int(line_size * 0.67))))
    ref_bin_im = bin_im.copy()
    bin_im = do_dilate(im=bin_im, k=(int(line_size * 1.5), 1))
    cts = do_find_cts(im=bin_im, mode=cv2.RETR_LIST, sort_type="area", min_size=(1, h / 4))

    if len(cts) == 0:
        # no number. shrink 1/5.
        gap = 10
        start = w // 2 - gap
        start = max(start, 0)
        end = w // 2 + gap
        end = min(end, bin_im.shape[1])
        ret_im = im[:, start:end]
        return ret_im, 255

    if len(cts) >= 2:
        rx, ry, rw, rh = cts[0].rect
        dl, dt, dr, db = rx, ry, rx + rw, ry + rh
        for ct in cts:
            tx, ty, tw, th = ct.rect
            if tx < dl:
                dl = tx
            if ty < dt:
                dt = ty
            if tx + tw > dr:
                dr = tx + tw
            if ty + th > db:
                db = ty + th
        x, y, dw, dh = dl, dt, dr - dl, db - dt
    else:
        x, y, dw, dh = cts[-1].rect
    whr = dw / dh
    p_wwr = dw / im.shape[1]
    p_hhr = dh / im.shape[0]
    if 0.5 <= whr <= 1.3 and p_wwr >= 0.5 and p_hhr >= 0.55:
        max_area = dw * dh
        ks = min(ref_bin_im.shape[:2]) // 8
        ks = int(max(line_size * 2, ks))

        roi_zone = ref_bin_im[y:y + dh, x:x + dw]
        roi_zone = do_erode(im=roi_zone, k=(ks, ks))
        non_count = cv2.countNonZero(roi_zone)
        ratio1 = non_count / max_area
        if 0.87 <= p_wwr and 0.87 <= p_hhr and 0.24 <= ratio1:
            gap = min(im.shape[1] // 10, 10)
            return np.ones((im.shape[0], gap, im.shape[2]), dtype=np.uint8) * 255, 255
        if 0.028 < ratio1 <= 1:
            return im, 255

    min_w_threshold = int(im.shape[1] / 3)
    if dw < min_w_threshold:
        dx = (min_w_threshold - dw) // 2
        left = max(0, x - dx)
        right = left + min_w_threshold
    else:
        left = x  # x if x <= 1 else x - 1
        right = x + dw  # if x + dw < im.shape[1] - 1 else x + dw + 1
    tmp_im = bin_im[:, left:right]
    step = 2
    left_offset, right_offset = 0, tmp_im.shape[1]
    tc = int(tmp_im.shape[1] // 2)
    for side in range(tc):
        strip = tmp_im[:, side:side + step]
        cnt = cv2.countNonZero(strip)
        if cnt / tmp_im.shape[0] / 2 < 0.5:
            left_offset = side
            break

    for side in range(tmp_im.shape[1], tc, -1):
        strip = tmp_im[:, side - step: side]
        cnt = cv2.countNonZero(strip)
        if cnt / tmp_im.shape[0] / 2 < 0.5:
            right_offset = side
            break

    ret_im = im[:, left:right][:, left_offset:right_offset]
    bar1 = im[:, :left]
    bar2 = im[:, right:]
    remain = np.ones((bar1.shape[0], bar1.shape[1] + bar2.shape[1], bar1.shape[2]))
    remain[:, :bar1.shape[1]] = bar1
    remain[:, bar1.shape[1]:] = bar2
    B, G, R = cv2.mean(remain)[:3]
    grey_val = 0.114 * B + 0.587 * G + 0.299 * R

    return ret_im, grey_val


def mat_to_md5(im: _MatLike) -> str:
    if im is None:
        return "shit"
    im_bytes = im.tobytes()
    md5_hash = hashlib.md5()
    md5_hash.update(im_bytes)
    return md5_hash.hexdigest()


def b64_to_mat(im_str: str) -> _MatLike | None:
    if im_str is None:
        return None
    if ';base64,' in im_str:
        im_str = im_str.split(';base64,')[1]
    try:
        im_bytes = base64.b64decode(im_str)
        im_array = np.frombuffer(im_bytes, np.uint8)
        mat = cv2.imdecode(im_array, cv2.IMREAD_COLOR)
        return mat
    except Exception as e:
        _logger.debug(f"decode exception: {str(e)}")
        return None


def mat_to_b64(im: _MatLike, quality: int = 100, with_header: bool = True) -> str:
    if im is None or im.size == 0:
        return ""

    ret, data = cv2.imencode(".jpg", im, params=[cv2.IMWRITE_JPEG_QUALITY, quality])
    if not ret:
        return ""
    im_bytes = data.tobytes()
    _logger.debug(f"im base64 size: {len(im_bytes)}, {len(im_bytes) / 1024 / 1024}")
    return data_to_b64(im_bytes, with_header=with_header)


def data_to_b64(data: bytes, with_header: bool = True) -> str:
    b64_bytes = base64.b64encode(data)
    base64_string = b64_bytes.decode('utf-8')
    prefix = "data:image/jpeg;base64," if with_header else ""
    return f"{prefix}{base64_string}"


##############################
#       ocr functions
##############################

@functools.lru_cache
def get_qr_detector():
    return cv2.QRCodeDetector()


def read_qr(im: _MatLike) -> _typing.Tuple[str, _typing.Any, int]:
    if im is None:
        return "", [], 1
    im_h, im_w = im.shape[:2]
    try:
        qr, box, _ = get_qr_detector().detectAndDecode(img=im)
        qr_box = box.squeeze().tolist() if box is not None else []
        for ptx, pty in qr_box:
            if ptx <= 0 or ptx >= im_w or pty <= 0 or pty >= im_h:
                qr_box = []
                break
        return qr, qr_box, 1
    except Exception as e:
        _logger.debug(f"read qr exception: {str(e)}")
        return "", [], 1


def read_codes(im: _MatLike) -> _typing.List[_typing.Tuple[str, _typing.Any, int]]:
    im_h, im_w = im.shape[:2]
    ret = []
    try:
        codes = zxingcpp.read_barcodes(image=im, text_mode=TextMode.Plain)
        codes = codes if codes is not None else []
        for code in codes:
            code_type = -1
            if code.format == zxingcpp.BarcodeFormat.QRCode:
                code_type = 1
            elif (code.format == zxingcpp.BarcodeFormat.Code128
                  or code.format == zxingcpp.BarcodeFormat.Code39
                  or code.format == zxingcpp.BarcodeFormat.Code93):
                code_type = 2

            points = []
            p: zxingcpp.Position = code.position
            if p is not None:
                points.append([p.top_left.x, p.top_left.y])
                points.append([p.top_right.x, p.top_right.y])
                points.append([p.bottom_right.x, p.bottom_right.y])
                points.append([p.bottom_left.x, p.bottom_left.y])
            for p in points:
                if p[0] is None or p[1] is None or p[0] < 0 or p[0] > im_w or p[1] < 0 or p[1] > im_h:
                    points = []
                    break
            ret.append(
                (code.text, points, code_type)
            )
    except Exception as e:
        _logger.debug(f"zxing read qr exception: {str(e)}")
        ret = [read_qr(im)]

    return ret


def read_code(im: _MatLike, code_type: int = 1) -> _typing.Tuple[str, _typing.Any, int]:
    ret = read_codes(im=im)
    ret = list(filter(lambda item: item.get('type', -1) == code_type, ret))
    return ret[0] if len(ret) > 0 else ('', [], code_type)


def get_text_boxes(
        info: _typing.Dict[str, _typing.Any]
) -> _typing.Tuple[_typing.List[_OCRRunUnit], _typing.List[_OCRRunUnit]]:
    if info is None:
        return [], []
    ec = info.get("errorCode", "-1")
    if ec != "0":
        return [], []
    rst: _typing.Dict[str, _typing.Any] = info.get("Result")
    if rst is None:
        return [], []
    regions: _typing.List[_typing.Any] = rst.get("regions", [])
    if regions is None:
        return [], []
    all_words: _typing.List[_OCRRunUnit] = []
    all_lines: _typing.List[_OCRRunUnit] = []
    for region in regions:
        if not isinstance(region, dict):
            continue

        lines = region.get("lines")
        if not isinstance(lines, list):
            continue
        for line in lines:
            if not isinstance(line, dict):
                continue
            bounding = line.get("boundingBox")
            if isinstance(bounding, str):
                comps = bounding.split(",")
                points = [list(map(lambda i: int(i), comps[c:c + 2])) for c in range(0, len(comps), 2)]
                txt = line.get("text", "")
                all_lines.append((points, txt, 0))
            words = line.get("words")
            if not isinstance(words, list):
                continue
            for word in words:
                if not isinstance(word, dict):
                    continue
                bounding = word.get("boundingBox")
                if isinstance(bounding, str):
                    comps = bounding.split(",")
                    p = [list(map(lambda i: int(i), comps[c:c + 2])) for c in range(0, len(comps), 2)]
                    o_txt = word.get("word", "")
                    txt = o_txt.strip(" _.。“”'‘’*-——|")
                    if len(txt) == 0:
                        word_type = 0
                    elif txt.isdigit():
                        word_type = 1
                    elif txt[0].isdecimal() or txt[-1].isdecimal():
                        word_type = 2
                    else:
                        word_type = 3
                    all_words.append((p, o_txt, word_type))

    all_words.sort(key=lambda k: k[0][0][1], reverse=False)
    return all_words, all_lines


def read_runs(runs: _typing.List[_OCRRunUnit]) -> str:
    def _x(run: _OCRRunUnit) -> float:
        x = np.array(run[0])[:, :1].reshape((-1, 1)).squeeze().mean()
        return float(x)

    elements = sorted(runs, key=lambda run: _x(run))
    id_unit = [
        ''.join(re.findall(r"\d+", str(e[1])))
        for e in elements
    ]
    # _logger.debug(f"id unit: {id_unit}")
    return ''.join(id_unit)


def find_run(runs: _typing.List[_OCRRunUnit], label: str) -> _typing.List[_OCRRunUnit]:
    target_run = []
    for run in runs:
        tags = label
        if run[1] in tags or tags in run[1]:
            target_run.append(run)
    return target_run


def drop_overlapping_runs(
    runs: _typing.List[_OCRRunUnit]
) -> _typing.List[_OCRRunUnit]:
    if not runs:
        return runs

    def geometry(run: _OCRRunUnit) -> _typing.Tuple[float, float, float, float, float, float, float]:
        x1 = min(run[0][0][0], run[0][3][0])
        x2 = max(run[0][1][0], run[0][2][0])
        y1 = min(run[0][0][1], run[0][1][1])
        y2 = min(run[0][2][1], run[0][3][1])
        return (x2 - x1) * (y2 - y1), (x2 - x1) / 2, (y2 - y1) / 2, x1, y1, x2, y2

    max_run = sorted(runs, key=lambda r: geometry(r)[0], reverse=True)[0]
    _, cx, cy, cx1, cy1, cx2, cy2 = geometry(max_run)
    ret = []
    for element in runs:
        _, pcx, pcy, px1, py1, px2, py2 = geometry(element)
        if px1 == cx1 and px2 == cx2 and py1 == cy1 and py2 == cy2 and element[1] == max_run[1]:
            ret.append(element)
        if px1 >= cx1 and px2 <= cx2 and py1 >= cy1 and py2 <= cy2:
            continue
        ret.append(element)
    return ret


def split_to_room(
        runs: _typing.List[_OCRRunUnit],
        rows: int,
        cols: int,
        src_w: int,
        src_h: int,
        r_gap: int,
        c_gap: int
) -> _typing.List[_typing.List[_OCRRunUnit]]:
    ret_dict = {}
    for element in runs:
        points = element[0]
        cx, cy = np.array(points).mean(axis=0)
        target_row, target_col = 0, 0
        for r in range(rows):
            top, bottom = r * (src_h + r_gap) + r_gap, (r + 1) * (src_h + r_gap)
            for c in range(cols):
                left, right = c * (src_w + c_gap) + c_gap, (c + 1) * (src_w + c_gap)
                if top <= cy <= bottom and left <= cx <= right:
                    target_row, target_col = r, c
                    break

        offset_x, offset_y = target_col * (src_w + c_gap) + c_gap, target_row * (src_h + r_gap) + r_gap
        key = f"{target_row}_{target_col}"
        comps = ret_dict.get(key, [])
        comps.append(
            ([[max(0, pt[0] - offset_x), max(0, pt[1] - offset_y)] for pt in element[0]], element[1], element[2])
        )
        ret_dict[key] = comps
    all_rst = list(ret_dict.values())

    # deal overlapping\inset
    all_rst = list(map(lambda g: drop_overlapping_runs(g), all_rst))
    return all_rst


def do_ocr(
        im: _MatLike,
        key: str,
        secret: str
) -> _typing.Tuple[bool, int, _typing.Dict[str, _typing.Any], _typing.Any]:
    if im is None:
        return False, 0, {}, None
    bk = im

    b64_str = mat_to_b64(bk, quality=95, with_header=False)
    result = _ocr_slave(b64_str, key=key, secret=secret)
    if result[-1] in ["13003", "12001", "10004", "5004", "1004"]:
        _logger.debug(f"ocr fail: {result[-1]}. retry ...")
        b64_str = mat_to_b64(bk, quality=80, with_header=False)
        result = _ocr_slave(b64_str, key=key, secret=secret)
    return result[:-1]  # type: ignore


def _ocr_slave(
        b64_str: str,
        key: str, secret: str
) -> _typing.Tuple[bool, int, _typing.Dict[str, _typing.Any], _typing.Any, str]:
    data = build_param(
        im_str=b64_str,
        key=key,
        secret=secret
    )
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    try:
        resp = requests.post(
            url="https://openapi.youdao.com/ocr_hand_writing",
            headers=header,
            data=data
        )
        json_str = str(object=resp.content, encoding="utf-8")
        json_dict = json.loads(s=json_str)
        ecode = json_dict.get("errorCode", "0")
        status = resp.status_code if ecode == "0" else int(ecode)
        return ecode == "0", status, json_dict, resp, ecode
    except Exception as e:
        _logger.debug(f"ocr exception: {str(e)}")
        return False, -1, {}, None, ""


def build_param(im_str: str, lang: str = "zh-CHS",
                angle: int = 0, concat_lines: int = 0,
                key: str = "", secret: str = "",
                ) -> _typing.Dict[str, _typing.Any]:
    q = "".join(im_str)
    salt = str(uuid.uuid1())
    cur_time = str(int(time.time()))
    sign = calculate_sign(app_key=key, app_secret=secret, q=q, salt=salt, cur_time=cur_time)
    return {
        "img": im_str,
        "langType": lang,
        "docType": "json",
        "imageType": "1",
        "concatLines": concat_lines,
        "angle": angle,
        "appKey": key,
        "salt": salt,
        "curtime": cur_time,
        "signType": "v3",
        "sign": sign
    }


def calculate_sign(app_key: str, app_secret: str, q: str, salt: str, cur_time: str):
    strSrc = app_key + get_input(q) + salt + cur_time + app_secret
    return encrypt(strSrc)


def get_input(p: str):
    if p is None:
        return p
    input_len = len(p)
    return p if input_len <= 20 else p[0:10] + str(input_len) + p[input_len - 10:input_len]


def encrypt(src: str):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(src.encode('utf-8'))
    return hash_algorithm.hexdigest()


class CompositionIdRecognizer(object):
    _rows = 3
    _col = 2
    _debug: bool = False
    _id_key: str = "studentId"
    _enable_ocr: bool = True
    _enable_code: bool = False
    _quality: int = 100
    _with_header: bool = True

    _input_im: _MatLike = None
    _base_im: _MatLike = None
    _canvas: _MatLike = None
    _id_boxes_info: _QueryInfo = False, []
    _id_container_info: _QueryInfo = False, []
    _dot_boxes_info: _QueryInfo = False, []
    _side_boxes_info: _QueryInfo = False, []
    orientation: _Orientation = 'unknown'

    sid: str = ''
    _id_source: IdSource = IdSource.UNKNOWN
    _qr_code: str = ''
    _bar_code: str = ''
    _id_box_roi: _MatLike = None
    _id_container_roi: _MatLike = None

    def __init__(self, key: str = None, secret: str = None):
        """
        Initialize the recognizer. If the parameter is None or '',
        the values will be read from the environment variables:
        YD_OCR_KEY and YD_OCR_SECRET respectively.
        :param key: yd ocr key
        :param secret: yd ocr secret
        """
        key = os.getenv('YD_OCR_KEY') if not key else key
        secret = os.getenv('YD_OCR_SECRET') if not secret else secret
        self._ocr_key = key
        self._ocr_secret = secret

    @property
    def _reference_size(self) -> _typing.Tuple[float, float]:
        w = min(self._base_im.shape[:2])
        unit = w * 0.0184873949
        return unit * 0.5, unit * 1.1

    @property
    def _radius(self) -> float:
        if len(self._dot_boxes_info[1]) >= 1:
            sizes = [cti.rect[2:] for cti in self._dot_boxes_info[1]]
            return float(np.array(sizes).mean())
        return sum(self._reference_size) / 2

    @property
    def _id_container_width(self) -> float:
        return self._radius * 47.27272727

    @property
    def _id_container_height(self) -> float:
        return self._id_container_width * 0.21923076

    @property
    def _id_box_width(self) -> float:
        return self._radius * 21.181819

    @property
    def _id_box_height(self) -> float:
        return self._id_box_width * 0.137339

    @property
    def _side_anchor_height(self) -> float:
        return self._radius * 2.45454545

    @property
    def _sharpen_parameter(self) -> _typing.List[_typing.Tuple[float, float]]:
        return [(0, 0), (6, 1)]

    @property
    def _clahe_parameters(self) -> _typing.List[_typing.Tuple[float, int, int]]:
        return [(0, 8, 8)]

    @property
    def _im_parameters(self) -> _typing.List[ImParam]:
        return [
            ImParam(blur_size=5, dilate_size=3, auto_binary=False, thresh=90,
                    zone_auto_bin=True, zone_max=255, zone_block_size=-1, zone_c=2),
            ImParam(blur_size=5, dilate_size=3, auto_binary=False, thresh=90,
                    zone_auto_bin=True, zone_max=255, zone_block_size=-1, zone_c=8),
            ImParam(blur_size=5, dilate_size=3, auto_binary=False, thresh=90,
                    zone_auto_bin=True, zone_max=255, zone_block_size=-1, zone_c=14),
            ImParam(blur_size=5, dilate_size=3, auto_binary=False, thresh=90,
                    zone_auto_bin=True, zone_max=200, zone_block_size=-1, zone_c=14),
            ImParam(blur_size=3, dilate_size=3, auto_binary=True, thresh=90),
            ImParam(blur_size=3, dilate_size=3, auto_binary=False, thresh=90),
            ImParam(blur_size=3, dilate_size=3, auto_binary=False, thresh=70),
            ImParam(blur_size=3, dilate_size=3, auto_binary=False, thresh=80),
        ]

    def recognize(
            self,
            input_im: RecInputType,
            id_key: str = "studentId",
            enable_ocr: bool = True,
            enable_code: bool = True,
            quality: int = 100,
            append_im_header: bool = True
    ) -> RecognitionResult:
        """
        提取学号
        :param input_im: 输入图像, 接收base64 string | MatLike | bytes 类型的输出
        :param id_key: 二维码信息中, 学号对应的key值
        :param enable_ocr: 是否允许进行OCR识别, 若开启, 则会在二维码或条形码识别失败后尝试OCR识别. 默认开启.
        :param enable_code: 是否允许二维码或条形码识别, 若开启, 则优先使用读取条形码或二维码. 读取失败的情况下, 会尝试进行OCR
        :param quality: 生成base64时的压缩系数(0-100), 默认为100, 表示不压缩
        :param append_im_header: 生成base64时, 是否携带data type信息, 默认携带
        :return:
        """
        self._debug = False
        self._id_key = id_key
        self._enable_ocr = enable_ocr
        self._enable_code = enable_code
        self._with_header = append_im_header
        self._quality = quality
        try:
            return self._do_recognize(input_im=input_im)
        except Exception as e:
            _logger.debug(f"recognize exception: {str(e)}")
            return RecognitionResult(status=StatusCode.ERR_UNKNOWN)

    def _clean_context(self, *category: _ContextCategory):
        for c in category:
            match c:
                case 'id':
                    self._id_boxes_info = False, []
                case 'side':
                    self._side_boxes_info = False, []
                case 'container':
                    self._id_container_info = False, []
                case 'dot':
                    self._dot_boxes_info = False, []

    def _from_scanner(self) -> bool:
        im_w = min(self._base_im.shape[:2])
        if self._dot_boxes_info[0]:
            pts = [center(ct.rect) for ct in self._dot_boxes_info[1][:2]]
            side = distance(pts[0], pts[1])
            return side / im_w >= 0.68
        if self._side_boxes_info[0]:
            pts = [center(ci.rect) for ci in self._side_boxes_info[1]]
            bounding = fit_bounding_rect(pts)
            sides_length = side_segment_length(bounding)
            l1 = sum(sides_length[::2]) / 2
            l2 = sum(sides_length[1::2]) / 2
            side = min(l1, l2)
            return side >= 0.85

        if self._id_container_info[0]:
            x, y, w, h = self._id_container_info[1][-1].rect
            return w / im_w >= 0.8

        if self._id_boxes_info[0]:
            x, y, w, h = self._id_boxes_info[1][-1].rect
            return w / im_w >= 0.3

        return False

    def _extract_code(self, im: _MatLike) -> _typing.Tuple[str, _typing.Any, _typing.Any]:
        if im is None:
            return '', None, None
        raw_bar_info, raw_qr_info = None, None
        qr_code, text = "", ""
        codes = read_codes(im=im)
        if codes:
            bar_codes = list(filter(lambda item: item[2] == 2, codes))
            if bar_codes:
                text = bar_codes[0][0]
                raw_bar_info = bar_codes[0]
            qr_codes = list(filter(lambda item: item[2] == 1, codes))
            if qr_codes:
                qr_code = qr_codes[0][0]
                raw_qr_info = qr_codes[0]
        else:
            qr_code, qr_points, _ = read_qr(im=im)
            raw_qr_info = qr_code, qr_points, 1

        if text:
            return text, raw_qr_info, raw_bar_info
        if not qr_code:
            return '', raw_qr_info, raw_bar_info
        try:
            _logger.debug(f"json: {qr_code}")
            qr_info: _typing.Dict = json.loads(qr_code)
            sid = qr_info.get(self._id_key, '')
            return sid, raw_qr_info, raw_bar_info
        except Exception as e:
            _logger.debug(f"parse json err: {str(e)}")

        return "", raw_qr_info, raw_bar_info

    def _do_recognize(self, input_im: RecInputType) -> RecognitionResult:
        if isinstance(input_im, _MatLike):
            mat = input_im.copy()
        elif isinstance(input_im, str):
            mat = b64_to_mat(input_im)
        elif isinstance(input_im, bytes):
            data = np.frombuffer(input_im, dtype=np.uint8)
            mat = cv2.imdecode(data, flags=cv2.IMREAD_COLOR)
        else:
            return RecognitionResult(status=StatusCode.ERR_IM_NOT_EXIST)

        if mat is None:
            return RecognitionResult(status=StatusCode.ERR_DECODE_FAIL)
        self._input_im = mat
        if self._enable_code:
            try:
                self.sid, self._qr_code, self._bar_code = self._extract_code(im=self._input_im)
            except Exception as e:
                _logger.debug(f"read code error: {str(e)}")
        if self.sid:
            self._id_source = IdSource.QR_CODE if self._bar_code is None else IdSource.BAR_CODE
            self.orientation = self._query_orientation_by_code()
            rotated_im = self._try_rotate(im=self._input_im, orientation=self.orientation)
            return self._build_result(
                status=StatusCode.OK,
                im=rotated_im
            )

        # complex calculate.
        self._base_im = self._input_im.copy()
        self._canvas = self._base_im.copy()
        try:
            self._do_layout_analysis()
        except Exception as e:
            _logger.debug(f"layout analysis error: {str(e)}")
        if self._enable_ocr:
            status = self._do_ocr()
        else:
            status = StatusCode.OK if self._id_box_roi is not None else StatusCode.ERR_LAYOUT_ANALYSIS_FAIL

        return self._build_result(status=status, im=self._input_im)

    def _extract_info(
            self,
            condition: _Callable,
            pre_action: _typing.Callable[[_typing.Any], None] = None
    ) -> _typing.Tuple[bool, _typing.List[CtInfo], _MatLike, _typing.List[CtInfo]]:
        min_size = self._reference_size[0]
        if pre_action is None:
            self._id_boxes_info = False, []
            self._id_container_info = False, []
            self._side_boxes_info = False, []
            self._dot_boxes_info = False, []
        cts, target_cts, bin_im = [], [], None
        for s_idx, sp in enumerate(self._sharpen_parameter):
            for c_idx, cp in enumerate(self._clahe_parameters):
                s_im = do_sharpen(im=self._base_im, sigma=sp[0], strength=sp[1])
                c_im = do_clahe(im=s_im, limit=cp[0], size=(cp[1], cp[2]))
                g_im = cv2.cvtColor(src=c_im, code=cv2.COLOR_BGR2GRAY)
                for p_idx, p in enumerate(self._im_parameters):
                    bin_im = do_binary(
                        im=g_im,
                        blur_size=(p.blur_size, p.blur_size),
                        auto=p.auto_binary,
                        zone_auto=p.zone_auto_bin,
                        zone_auto_max=p.zone_max,
                        zone_auto_c=p.zone_c,
                        zone_auto_block_size=p.zone_block_size,
                        bin_thresh=p.thresh
                    )
                    cts = do_find_cts(
                        im=bin_im,
                        mode=cv2.RETR_LIST,
                        min_size=(min_size, min_size),
                        min_whr=0.407 * 0.8,
                        max_whr=7.28125 * 1.2,
                    )
                    if not self._dot_boxes_info[0]:
                        self._dot_boxes_info = self._find_circles(cts)
                    if not self._id_boxes_info[0]:
                        self._id_boxes_info = self._find_id_boxes(cts)
                    if not self._id_container_info[0]:
                        self._id_container_info = self._find_id_container(cts)
                    if not self._side_boxes_info[0]:
                        self._side_boxes_info = self._find_side_anchor_boxes(cts)
                    if condition is None:
                        if self._dot_boxes_info[0]:
                            return True, self._dot_boxes_info[1], bin_im, cts

                    ret, target_cts = condition(cts)
                    if ret:
                        return True, target_cts, bin_im, cts

        return False, target_cts, bin_im, cts

    def _search_id_box_in_container(self):
        if self._id_boxes_info[0] or not self._id_container_info[0]:
            return
        _, dst = do_warp(full_im=self._base_im, ct=self._id_container_info[1][-1], whr=4.5614)
        self._id_container_roi = dst
        if dst is None:
            return
        ls = max(dst.shape[0] * 0.026315789, 3)
        roi = dst[ls:-ls, ls:-ls]
        for p in self._im_parameters:
            bin_im = do_binary(
                im=roi,
                blur_size=(p.blur_size, p.blur_size),
                auto=p.auto_binary,
                zone_auto=p.zone_auto_bin,
                zone_auto_max=p.zone_max,
                zone_auto_c=p.zone_c,
                zone_auto_block_size=p.zone_block_size,
                bin_thresh=p.thresh
            )
            roi_h, roi_w = bin_im.shape[:2]
            refer_w = roi_w * 0.44807692
            refer_h = refer_w * 0.137339
            cts = do_find_cts(
                im=roi,
                mode=cv2.RETR_EXTERNAL,
                min_size=(refer_w * 0.8, refer_h * 0.8),
                max_size=(refer_w * 1.2, refer_h * 1.2),
                min_whr=7.28125 * 0.8,
                max_whr=7.28125 * 1.2,
            )
            ret, boxes = self._find_box(
                cts=cts,
                refer_w=refer_w,
                refer_h=refer_h,
                whr=7.28125,
                refer_im=roi,
                condition=lambda ct: len(ct) >= 1
            )
            if ret:
                self._id_boxes_info = ret, boxes
                self._id_box_roi = do_warp(full_im=roi, ct=boxes[-1], whr=7.28125)[1]
                return

    def _make_contour_mask(self, cts: _typing.List[CtInfo], refer_im: _MatLike) -> _MatLike:
        cv_cts = [ci.ct for ci in cts]
        mask = np.zeros(refer_im.shape[:2], dtype=np.uint8)
        cv2.drawContours(image=mask, contourIdx=-1, contours=cv_cts, thickness=-1, color=(255, 255, 255))
        ks = int(max(self._query_line_size() * 1, 1))
        mask = do_open(im=mask, k=(ks, ks))
        return mask

    def _find_box(
            self,
            cts: _typing.List[CtInfo],
            refer_w: float,
            refer_h: float,
            whr: float,
            refer_im: _MatLike = None,
            condition: _typing.Callable[[_typing.List[CtInfo]], bool] = None
    ) -> _QueryInfo:
        min_w = refer_w * 0.7
        max_w = refer_w * 1.3
        min_h = refer_h * 0.7
        max_h = refer_h * 1.3
        refer_im = refer_im if refer_im is not None else self._base_im
        boxes = filter_ct(
            cts=cts,
            min_w=min_w,
            max_w=max_w,
            min_h=min_h,
            max_h=max_h,
            min_whr=whr * 0.85,
            max_whr=whr * 1.15,
            use_min_rect=True,
            solid_area_ratio=0.85
        )
        if len(boxes) == 0:
            mask = self._make_contour_mask(cts, refer_im=refer_im)
            candidate_cts = do_find_cts(
                im=mask,
                mode=cv2.RETR_LIST,
                min_size=(min_w, min_h),
                max_size=(max_w, max_h),
                min_whr=whr * 0.7,
                max_whr=whr * 1.4
            )
            boxes = filter_ct(
                cts=candidate_cts,
                min_w=min_w,
                max_w=max_w,
                min_h=min_h,
                max_h=max_h,
                min_whr=whr * 0.8,
                max_whr=whr * 1.2,
                use_min_rect=True
            )
        ret = len(boxes) >= 1
        if condition is not None:
            ret = condition(boxes)
        return ret, sorted(boxes, key=lambda ct: ct.area)

    def _find_id_container(self, cts: _typing.List[CtInfo]) -> _QueryInfo:
        ret = self._find_box(
            cts=cts,
            refer_w=self._id_container_width,
            refer_h=self._id_container_height,
            whr=4.5614,
            condition=lambda boxes: len(boxes) >= 1
        )
        if not ret[0]:
            return ret
        bounding_info = self._qr_bounding()
        if bounding_info[0]:
            qrx, qry, qrw, qrh = bounding_info[1]
            candidates = []
            for ct in ret[1]:
                if (ct.rect[0] < qrx
                        and ct.rect[1] < qry
                        and ct.rect[0] + ct.rect[2] > qrx + qrw
                        and ct.rect[1] + ct.rect[3] > qry + qrh):
                    candidates.append(ct)
        else:
            candidates = ret[1]

        candidates = extract_outer_frame(candidates)
        return len(candidates) == 1, candidates

    def _find_id_boxes(self, cts: _typing.List[CtInfo]) -> _QueryInfo:
        ret = self._find_box(
            cts=cts,
            refer_w=self._id_box_width,
            refer_h=self._id_box_height,
            whr=7.28125,
            condition=lambda boxes: len(boxes) >= 1
        )
        if not ret[0]:
            return ret

        bounding_info = self._qr_bounding()
        if bounding_info[0]:
            qrx, qry, qrw, qrh = bounding_info[1]
            limit_top, limit_bottom = qry - qrh / 2, qry + qrh / 2
            candidates = []
            for ct in ret[1]:
                ctx, cty = center(ct.rect)
                if qrx <= ctx <= qrx + qrw and qry <= cty <= qry + qrh:
                    continue
                if limit_top <= cty <= limit_bottom:
                    candidates.append(ct)
        else:
            candidates = ret[1]

        candidates = extract_outer_frame(candidates)

        return len(candidates) == 1, candidates

    def _find_side_anchor_boxes(self, cts: _typing.List[CtInfo]) -> _QueryInfo:
        side1 = self._radius
        side2 = self._side_anchor_height

        params = [
            [side1, side2, 0.407],
            [side2, side1, 2.4545]
        ]
        boxes = [
            filter_ct(
                cts=cts,
                min_w=p[0] * 0.8, max_w=p[0] * 1.2,
                min_h=p[1] * 0.8, max_h=p[1] * 1.2,
                min_whr=p[2] * 0.8, max_whr=p[2] * 1.2,
                use_min_rect=True, solid_area_ratio=0.8,
            )
            for p in params
        ]

        return len(boxes[0]) >= 7 and len(boxes[1]) >= 4, [b for c in boxes for b in c]

    def _find_circles(self, cts: _typing.List[CtInfo]) -> _QueryInfo:
        boxes = filter_ct(
            cts=cts,
            min_w=self._radius * 0.8,
            max_w=self._radius * 1.2,
            min_h=self._radius * 0.8,
            max_h=self._radius * 1.2,
            min_whr=0.85,
            max_whr=1.15,
            use_min_rect=True,
            solid_area_ratio=np.pi / 4 * 0.95,
            circle=True
        )
        bounding_info = self._qr_bounding()
        if bounding_info[0]:
            qrx, qry, qrw, qrh = bounding_info[1]
            limit_top, limit_bottom = qry - qrh / 2, qry + qrh / 2
            candidates = []
            for ct in boxes:
                ctx, cty = center(ct.rect)
                if qrx <= ctx <= qrx + qrw or qry <= cty <= qry + qrh:
                    continue
                if limit_top <= cty <= limit_bottom:
                    candidates.append(ct)
        else:
            candidates = boxes
        return len(candidates) >= 2, candidates

    def _qr_bounding(self) -> _typing.Tuple[bool, _typing.Sequence[int]]:
        if not self._qr_code or not self._qr_code[0]:
            return False, [0, 0, 0, 0]
        box = self._qr_code[1]
        tl, rb = np.min(box, axis=0), np.max(box, axis=0)
        qr_size = rb - tl
        return True, [*tl.tolist(), *qr_size.tolist()]

    def _query_line_size(self) -> int:
        if len(self._dot_boxes_info[1]) >= 1:
            return max(2, int(self._radius * 0.16363636 + 0.5))
        if self._id_box_roi is not None:
            return max(int(self._id_box_roi.shape[0] * 2 / 32 + 0.5), 2)
        refer = int(self._base_im.shape[1] * 0.003361345 + 0.5)
        return max(refer, 2)

    def _try_rotate(self, im: _MatLike, orientation: _Orientation) -> _MatLike:
        if orientation == 'ttl' or orientation == 'ttr' or orientation == 'ttb':
            code = {
                'ttl': cv2.ROTATE_90_CLOCKWISE,
                'ttr': cv2.ROTATE_90_COUNTERCLOCKWISE,
                'ttb': cv2.ROTATE_180
            }[orientation]
            return do_rotate(im=im, code=code)
        return im

    def _query_orientation_by_code(self) -> _Orientation:
        refer_box = None
        if self._qr_code:
            refer_box = self._qr_code[1]
        elif self._bar_code:
            refer_box = self._bar_code[1]
        if not refer_box:
            return 'unknown'

        imh = self._input_im.shape[0]
        _, cy = np.array(refer_box).mean(axis=0)
        return 'ttt' if cy < imh * 0.5 else 'ttb'

    def _query_orientation(self) -> _Orientation:
        ori: _Orientation = self._query_orientation_by_code()
        if ori != "unknown":
            return ori
        if self._dot_boxes_info[0] and (self._id_boxes_info[0] or self._id_container_info[0]):
            dot1_x, dot1_y = center(self._dot_boxes_info[1][0].rect)
            dot2_x, dot2_y = center(self._dot_boxes_info[1][1].rect)
            if self._id_boxes_info[0]:
                cx, cy = center(self._id_boxes_info[1][-1].rect)
            else:
                cx, cy = center(self._id_container_info[1][-1].rect)

            if dot1_y < cy and dot2_y < cy:
                ori = 'ttt'
            elif dot1_y > cy and dot2_y > cy:
                ori = 'ttb'
            elif dot1_x < cx and dot2_x < cx:
                ori = 'ttl'
            elif dot1_x > cx and dot2_x > cx:
                ori = 'ttr'

        if self._dot_boxes_info[0] or self._id_boxes_info[0] or self._id_container_info[0]:
            if self._side_boxes_info[0]:
                pts = [center(ci.rect) for ci in self._side_boxes_info[1]]
                bounding = fit_bounding_rect(pts)
                cx, cy = np.mean(bounding, axis=0)
                sides_length = side_segment_length(bounding)
                landscape = sum(sides_length[::2]) > sum(sides_length[1::2])
            else:
                h, w = self._base_im.shape[:2]
                cx, cy = w / 2, h / 2
                landscape = w > h

            if self._dot_boxes_info[0]:
                dot1_x, dot1_y = center(self._dot_boxes_info[1][0].rect)
                dot2_x, dot2_y = center(self._dot_boxes_info[1][1].rect)
                dot_x, dot_y = (dot1_x + dot1_y) / 2, (dot1_y + dot2_y) / 2
            elif self._id_boxes_info[0]:
                dot_x, dot_y = center(self._id_boxes_info[1][-1].rect)
            else:
                dot_x, dot_y = center(self._id_container_info[1][-1].rect)

            if landscape:
                ori = 'ttl' if dot_x < cx else 'ttr'
            else:
                ori = 'ttt' if dot_y < cy else 'ttb'
            ...

        return ori

    def _do_layout_analysis(self):
        _, _, bin_im, cts = self._extract_info(condition=self._find_circles)
        self.orientation = self._query_orientation()
        if self.orientation == 'ttl' or self.orientation == 'ttr' or self.orientation == 'ttb':
            code = {
                'ttl': cv2.ROTATE_90_CLOCKWISE,
                'ttr': cv2.ROTATE_90_COUNTERCLOCKWISE,
                'ttb': cv2.ROTATE_180
            }[self.orientation]
            self._base_im = do_rotate(im=self._base_im, code=code)
            self._canvas = self._base_im.copy()
            _, _, bin_im, cts = self._extract_info(condition=self._find_circles)

        if not self._id_boxes_info[0]:
            _, _, bin_im, cts = self._extract_info(
                condition=self._find_id_boxes,
                pre_action=self._clean_context('id')  # type: ignore
            )
        if not self._id_container_info[0]:
            _, _, bin_im, cts = self._extract_info(
                condition=self._find_id_container,
                pre_action=self._clean_context('container')  # type: ignore
            )
        if not self._id_boxes_info[0] and self._id_container_info[0]:
            self._search_id_box_in_container()

        self.orientation = self._query_orientation()
        if self._id_boxes_info[0] and self._id_box_roi is None:
            self._id_box_roi = do_warp(full_im=self._base_im, ct=self._id_boxes_info[1][-1], whr=7.28125)[1]
        if self._id_container_info[0] and self._id_container_roi is None:
            self._id_container_roi = do_warp(full_im=self._base_im, ct=self._id_container_info[1][-1], whr=4.5614)[1]

        if self.orientation == 'ttb':
            self._id_box_roi = do_rotate(im=self._id_box_roi, code=cv2.ROTATE_180)
            self._id_container_roi = do_rotate(im=self._id_container_roi, code=cv2.ROTATE_180)

    def _rebuild_id_im(self) -> _typing.Tuple[_MatLike | None, _MatLike | None]:

        if self._id_box_roi is None:
            return None, None

        ls = int(self._query_line_size() * 1.3)
        roi = self._id_box_roi[ls:-ls, ls:-ls]
        h, w = roi.shape[:2]
        step = w // 2
        left = roi[:, :step]
        lh, lw = left.shape[:2]
        right = roi[:, step:]
        rh, rw = right.shape[:2]
        pad = 0
        left_subs = [left[:, int(i * lw / 5) + pad: int((i + 1) * lw / 5) - pad] for i in range(5)]
        right_subs = [right[:, int(i * rw / 5) + pad: int((i + 1) * rw / 5) - pad] for i in range(5)]
        subs = [*left_subs, *right_subs]
        sls = self._query_line_size()
        subs_shrinks = [do_shrink(s, line_size=sls / 2) for s in subs]
        subs = [s[0] for s in subs_shrinks]
        gray_val = np.mean(np.array([s[1] for s in subs_shrinks]))
        gray_val = 255 if self._from_scanner() or gray_val > 200 else gray_val
        gray_val = min(255, int(gray_val * 1.2))
        eh, ew, channel = subs[0].shape
        pw = max(ew // 10, 4)
        placeholder = np.ones((eh, pw, channel), dtype=np.uint8) * int(gray_val)

        empties = [placeholder for _ in range(len(subs))]
        elements = [item for sub in zip(subs, empties) for item in sub]
        id_im = cv2.hconcat(elements)

        if id_im is None:
            return None, None

        id_im_sharpened = do_sharpen(id_im, sigma=3, strength=1)
        id_im_clahe = do_clahe(id_im, limit=3, size=(8, 8))
        src_ims = [id_im, id_im_sharpened, id_im_clahe]
        h, w = id_im.shape[:2]
        col_gap = w // 2
        row_gap = h
        row, col = self._rows, self._col
        box_w = (w + col_gap) * col + col_gap
        box_h = (h + row_gap) * row + row_gap
        box = np.ones((box_h, box_w, id_im.shape[2]), dtype=np.uint8) * 255
        for r in range(row):
            for c in range(col):
                index = r * col + c
                dy = r * (h + row_gap) + row_gap
                dx = c * (w + col_gap) + col_gap
                box[dy:dy + h, dx:dx + w] = src_ims[index % len(src_ims)]

        return box, id_im

    def _do_ocr(self) -> StatusCode:
        if self._enable_code and self._id_container_roi is not None:
            self.sid, self._qr_code, self._bar_code = self._extract_code(im=self._id_container_roi)
        if self.sid:
            self._id_source = IdSource.QR_CODE if self._bar_code is None else IdSource.BAR_CODE
            return StatusCode.OK

        if self._enable_ocr and (not self._ocr_key or not self._ocr_secret):
            return StatusCode.ERR_OCR_AUTH_FAIL

        id_box, id_unit = self._rebuild_id_im()
        if id_box is None:
            paper_analysis = True
            id_box = self._input_im
        else:
            paper_analysis = False
        # do_show(f"id box: {time.time()}", id_box)
        ocr_sentry = time.time()
        ocr_ret, code, ocr_info, resp = do_ocr(im=id_box, key=self._ocr_key, secret=self._ocr_secret)
        _logger.debug(f"ocr time cost: {time.time() - ocr_sentry}")
        if not ocr_ret:
            _logger.debug(f"OCR ERR: {code}")
            return StatusCode.ERR_OCR_FAIL

        self._id_source = IdSource.OCR
        words_run, lines_run = get_text_boxes(ocr_info)
        if not words_run:
            # 测试时发现, 某些图片识别时接口响应正常, 但ocr返回的regions为空list, 调整尺寸后可恢复正常
            h_, w_ = id_box.shape[:2]
            dst_size = w_ - 1, int((w_ - 1) * h_ / w_)
            id_box = cv2.resize(src=id_box, dsize=dst_size)
            ocr_ret, code, ocr_info, resp = do_ocr(im=id_box, key=self._ocr_key, secret=self._ocr_secret)
            if not ocr_ret:
                return StatusCode.ERR_OCR_FAIL
            words_run, lines_run = get_text_boxes(ocr_info)

        if not paper_analysis:
            id_ocr_units = split_to_room(
                runs=words_run,
                rows=self._rows,
                cols=self._col,
                src_w=id_unit.shape[1],
                src_h=id_unit.shape[0],
                r_gap=id_unit.shape[0],
                c_gap=id_unit.shape[1] // 2
            )
            ids = [read_runs(r) for r in id_ocr_units]
            ids_max10 = [e for e in ids if len(e) <= 10]
            candidates = ids_max10 if ids_max10 else ids
            if not candidates:
                return StatusCode.ERR_OCR_FAIL
            group = collections.Counter(candidates)
            self.sid = group.most_common()[0][0]
        else:
            tag = "学号"
            target_run_list = find_run(runs=lines_run, label=tag)
            if target_run_list:
                target_run = target_run_list[-1]
                candidates = []
                rp1, rp2, rp3, rp4 = target_run[0]
                r_top = min(rp1[1], rp2[1], rp3[1], rp4[1])
                r_bottom = max(rp1[1], rp2[1], rp3[1], rp4[1])
                r_height = r_bottom - r_top
                bound_top, bound_bottom = max(0, r_top - r_height / 2), r_bottom + r_height
                for run in words_run:
                    p1, p2, p3, p4 = run[0]
                    p_left = min(p1[0], p4[0])
                    p_top = min(p1[1], p2[1], p3[1], p4[1])
                    p_bottom = max(p1[1], p2[1], p3[1], p4[1])
                    p_cy = p_top / 2 + p_bottom / 2
                    if bound_top <= p_cy <= bound_bottom:
                        candidates.append(run)
                sorted_runs = sorted(candidates, key=lambda p: min(p[0][0][0], p[0][3][0]))
                text_parts = ''.join([s[1] for s in sorted_runs])
                _logger.debug(f"text part: {text_parts}")
                comps = text_parts.split(tag)
                if comps:
                    tail = comps[-1]
                    sid_parts = [t for t in tail if t.isascii() and t.isdecimal()]
                    self.sid = ''.join(sid_parts)

        return StatusCode.OK

    def _build_result(self, status: StatusCode, im: _MatLike) -> RecognitionResult:
        b64_resp = mat_to_b64(im=im, quality=self._quality, with_header=self._with_header)
        return RecognitionResult(
            status=status,
            sid=self.sid,
            raw_qr_code='' if not self._qr_code else self._qr_code[0],
            raw_bar_code='' if not self._bar_code else self._bar_code[0],
            b64_response=b64_resp,
            original_direction=CardDirection.NORMAL if self.orientation == 'ttt' else CardDirection.INVERTED,
            id_source=self._id_source
        )


if __name__ == '__main__':
    APP_KEY = ''
    APP_SECRET = ''
    t_debug = True
    t_start = time.time()

    # im_path = "/Users/asan/Documents/python/ecard/resource/composition/c03.jpg"
    im_path = "/Users/asan/Downloads/作文批改2/1班读后续写答题卡/20251204_091229_0308.JPG"
    t_im = cv2.imread(im_path, flags=cv2.IMREAD_COLOR)

    # [1]. 初始化识别器
    t_recognizer = CompositionIdRecognizer(key=APP_KEY, secret=APP_SECRET)

    # # [2.1]. 方式一: 接收MatLike形式的输入
    # t_ret = t_recognizer.recognize(input_im=t_im, enable_ocr=True, enable_code=True)
    # _logger.debug(f"ret: {time.time() - t_start}, {t_ret}")

    _logger.debug("--*--" * 20)

    # [2.2]. 方式二: 接收base64 string形式的输入
    t_64 = mat_to_b64(im=t_im, quality=100, with_header=True)  # 模拟base64 string
    t_64_ret = t_recognizer.recognize(input_im=t_64, enable_ocr=True, enable_code=True)
    _logger.debug(f"ret: {time.time() - t_start}, {t_64_ret}")

    # # [2.3]. 方式三: 接收bytes类型的输入, 适用于接收文件流的形式
    # some_bytes: bytes | None = None  # 模拟bytes
    # t_bytes_ret = t_recognizer.recognize(input_im=some_bytes, enable_ocr=True, enable_code=True)
    #
    # _logger.debug(f"ret: {time.time() - t_start}, {t_bytes_ret}")

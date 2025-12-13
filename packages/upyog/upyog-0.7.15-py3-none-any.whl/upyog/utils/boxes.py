def xyxy_to_xywh(xyxy):
    assert len(xyxy) == 4
    x1, y1, x2, y2 = xyxy
    w = x2 - x1
    h = y2 - y1
    return (x1, y1, w, h)


def xyxys_to_xywh(xyxys):
    return [xyxy_to_xywh(xyxy) for xyxy in xyxys]


def xywh_to_xyxy(xywh):
    assert len(xywh) == 4
    x1, y1, w, h = xywh
    x2 = x1 + w
    y2 = y1 + h
    return (x1, y1, x2, y2)


def xywhs_to_xyxy(xywhs):
    return [xywh_to_xyxy(xywh) for xywh in xywhs]

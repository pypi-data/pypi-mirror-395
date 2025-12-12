# import math
# from typing import Tuple


# def conv2d_output_shape(
#     input_shape: Tuple[int, int],
#     kernel_shape: Tuple[int, int],
#     stride: int = 1,
#     padding: int = 0,
#     dilation: int = 1,
# ) -> Tuple[int, int]:
#     # input_shape = (H, W), kernel_shape=(kH, kW)
#     H, W = input_shape
#     kH, kW = kernel_shape
#     out_h = ((H + 2 * padding - dilation * (kH - 1) - 1) // stride) + 1
#     out_w = ((W + 2 * padding - dilation * (kW - 1) - 1) // stride) + 1
#     return (out_h, out_w)


# def maxpool_output_shape(
#     input_shape: Tuple[int, int], pool_size: int = 2, stride: int = 2, padding: int = 0
# ) -> Tuple[int, int]:
#     H, W = input_shape
#     out_h = ((H + 2 * padding - pool_size) // stride) + 1
#     out_w = ((W + 2 * padding - pool_size) // stride) + 1
#     return (out_h, out_w)


# def iou(
#     boxA: Tuple[float, float, float, float], boxB: Tuple[float, float, float, float]
# ) -> float:
#     # boxes as (x1,y1,x2,y2)
#     xA = max(boxA[0], boxB[0])
#     yA = max(boxA[1], boxB[1])
#     xB = min(boxA[2], boxB[2])
#     yB = min(boxA[3], boxB[3])
#     interW = max(0.0, xB - xA)
#     interH = max(0.0, yB - yA)
#     interArea = interW * interH
#     areaA = max(0.0, boxA[2] - boxA[0]) * max(0.0, boxA[3] - boxA[1])
#     areaB = max(0.0, boxB[2] - boxB[0]) * max(0.0, boxB[3] - boxB[1])
#     union = areaA + areaB - interArea
#     if union == 0:
#         return 0.0
#     return interArea / union


# # def nms(boxes, scores, iou_threshold=0.5):
# #     # simple NMS returning indices (keeps code minimal)
# #     idxs = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
# #     keep = []
# #     while idxs:
# #         i = idxs.pop(0)
# #         keep.append(i)
# #         idxs = [j for j in idxs if iou(boxes[i], boxes[j]) < iou_threshold]
# #     return keep


# def nms(boxes, scores=None, iou_threshold=0.5):
#     """
#     Performs Non-Maximum Suppression.

#     Accepts either:
#     1) boxes = [(x1,y1,x2,y2)], scores=[...]
#     2) boxes = [(x1,y1,x2,y2,score)]  ← auto-detected

#     Returns list of kept indices.
#     """

#     # Auto-extract scores if they are inside the boxes list
#     if scores is None:
#         if len(boxes) > 0 and len(boxes[0]) == 5:
#             scores = [b[4] for b in boxes]
#             boxes = [b[:4] for b in boxes]
#         else:
#             raise ValueError("Scores missing. Provide scores or 5-tuple boxes.")

#     # Convert to list
#     boxes = list(boxes)
#     scores = list(scores)

#     # Sort indices by descending score
#     idxs = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
#     keep = []

#     def iou(a, b):
#         x1 = max(a[0], b[0])
#         y1 = max(a[1], b[1])
#         x2 = min(a[2], b[2])
#         y2 = min(a[3], b[3])

#         inter = max(0, x2 - x1) * max(0, y2 - y1)
#         area_a = (a[2] - a[0]) * (a[3] - a[1])
#         area_b = (b[2] - b[0]) * (b[3] - b[1])

#         return inter / (area_a + area_b - inter + 1e-9)

#     while idxs:
#         best = idxs.pop(0)
#         keep.append(best)

#         idxs = [i for i in idxs if iou(boxes[best], boxes[i]) < iou_threshold]

#     return keep




from typing import Tuple

def conv2d_output_shape(
    input_shape: Tuple[int, int],
    kernel_shape: Tuple[int, int],
    stride: int = 1,
    padding: int = 0,
    dilation: int = 1,
) -> Tuple[int, int]:
    # input_shape = (H, W), kernel_shape=(kH, kW)
    H, W = input_shape
    kH, kW = kernel_shape
    out_h = ((H + 2 * padding - dilation * (kH - 1) - 1) // stride) + 1
    out_w = ((W + 2 * padding - dilation * (kW - 1) - 1) // stride) + 1
    return (out_h, out_w)

def maxpool_output_shape(
    input_shape: Tuple[int, int], pool_size: int = 2, stride: int = 2, padding: int = 0
) -> Tuple[int, int]:
    H, W = input_shape
    out_h = ((H + 2 * padding - pool_size) // stride) + 1
    out_w = ((W + 2 * padding - pool_size) // stride) + 1
    return (out_h, out_w)

def iou(
    boxA: Tuple[float, float, float, float], boxB: Tuple[float, float, float, float]
) -> float:
    # boxes as (x1,y1,x2,y2)
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    interW = max(0.0, xB - xA)
    interH = max(0.0, yB - yA)
    interArea = interW * interH
    areaA = max(0.0, boxA[2] - boxA[0]) * max(0.0, boxA[3] - boxA[1])
    areaB = max(0.0, boxB[2] - boxB[0]) * max(0.0, boxB[3] - boxB[1])
    union = areaA + areaB - interArea
    if union == 0:
        return 0.0
    return interArea / union

def nms(boxes, scores=None, iou_threshold=0.5):
    """
    Performs Non-Maximum Suppression.

    Accepts either:
    1) boxes = [(x1,y1,x2,y2)], scores=[...]
    2) boxes = [(x1,y1,x2,y2,score)]  ← auto-detected

    Returns list of kept indices.
    """

    # Auto-extract scores if they are inside the boxes list
    if scores is None:
        if len(boxes) > 0 and len(boxes[0]) == 5:
            scores = [b[4] for b in boxes]
            boxes = [b[:4] for b in boxes]
        else:
            raise ValueError("Scores missing. Provide scores or 5-tuple boxes.")

    boxes = list(boxes)
    scores = list(scores)

    # Sort indices by descending score
    idxs = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    keep = []

    def _iou(a, b):
        x1 = max(a[0], b[0])
        y1 = max(a[1], b[1])
        x2 = min(a[2], b[2])
        y2 = min(a[3], b[3])

        inter = max(0, x2 - x1) * max(0, y2 - y1)
        area_a = (a[2] - a[0]) * (a[3] - a[1])
        area_b = (b[2] - b[0]) * (b[3] - b[1])

        return inter / (area_a + area_b - inter + 1e-9)

    while idxs:
        best = idxs.pop(0)
        keep.append(best)
        idxs = [i for i in idxs if _iou(boxes[best], boxes[i]) < iou_threshold]

    return keep

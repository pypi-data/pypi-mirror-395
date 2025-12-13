from os.path import isfile

import numpy as np
from morphodeep.tools.image import imread

try :
    import tensorflow as tf
except :
    a=1#print(" Tensorflow is not installed ...")


#####IOU
@tf.function
def iou_cell(masks_gt, masks_pred, c):
    # print(f" --> CELL {c}")
    empty = tf.cast([c[0], -1, 0, 0, 0, 0], tf.float32)
    gt_mask = tf.where(masks_gt == c)
    vals = tf.gather_nd(masks_pred, gt_mask)
    next_cells, idx, count = tf.unique_with_counts(vals)  # get all pred cells with a overap with the given cell
    best_match_idx = tf.math.argmax(count)
    best_match = next_cells[best_match_idx]
    if best_match == tf.cast(0, best_match.dtype): return empty  # No Match at all
    # print(f"Best match -> {best_match}")
    # Get The Overlap Bounding Box
    pd_mask = tf.where(masks_pred == best_match)
    box_max = tf.maximum(tf.reduce_max(pd_mask, axis=0), tf.reduce_max(gt_mask, axis=0)) + 1
    box_min = tf.minimum(tf.reduce_min(pd_mask, axis=0), tf.reduce_min(gt_mask, axis=0))
    box_shape = box_max - box_min

    if not tf.math.count_nonzero(box_shape) == len(box_shape):   return empty  # Empty Boxes

    gt_binary = tf.tensor_scatter_nd_update(tf.zeros(box_shape), gt_mask - box_min, tf.ones([tf.shape(gt_mask)[0], ]))
    pd_binary = tf.tensor_scatter_nd_update(tf.zeros(box_shape), pd_mask - box_min,
                                            2 * tf.ones([tf.shape(pd_mask)[0], ]))

    values, indices, count = tf.unique_with_counts(tf.reshape(tf.math.add(gt_binary, pd_binary), [-1]))
    # print(" --> "+str(values)+ " idx="+str(indices)+ " count="+str(count))
    good = tf.cast(tf.gather_nd(count, tf.where(values == tf.cast(3.0, tf.float32))), tf.float32)
    if tf.shape(good)[0] == 0: good = tf.cast([0], tf.float32)
    over = tf.cast(tf.gather_nd(count, tf.where(values == tf.cast(1.0, tf.float32))),  tf.float32)  # GT only -> OVER SEGMENTATION
    if tf.shape(over)[0] == 0: over = tf.cast([0], tf.float32)
    under = tf.cast(tf.gather_nd(count, tf.where(values == tf.cast(2.0, tf.float32))),  tf.float32)  # PRED only -> UNDER SEGMETATION
    if tf.shape(under)[0] == 0: under = tf.cast([0], tf.float32)
    total = good + under + over
    iou_v = tf.cast(0, tf.float32) if total == 0 else good / total

    #print(f"cell {c} -> match {[tf.cast(best_match, tf.float32)]} -> iou_v={iou_v} Best good: {good}, under={under}, over={over}")
    return tf.concat([c, [tf.cast(best_match, tf.float32)], iou_v, good, under, over], 0)


@tf.function
def iou_tf(masks_gt, masks_pred):
    masks_gt = tf.cast(masks_gt, tf.float32)
    masks_pred = tf.cast(masks_pred, tf.float32)
    cells, _ = tf.unique(tf.reshape(masks_gt, [-1]))
    cells = tf.cast(tf.gather(cells, tf.where(cells > 0)), tf.float32)  # REMOVE BACKGROUND
    if len(cells) <= 1:   return tf.cast(0, tf.float32)  # No Cells
    all_ious = tf.map_fn(fn=lambda c: iou_cell(masks_gt, masks_pred, c), elems=cells)
    return all_ious


def iou_loop(masks_gt, masks_pred):
    cells, _ = tf.unique(tf.reshape(masks_gt, [-1]))
    if len(cells) <= 1:   return tf.cast(0, tf.float32)  # No Cells
    cells = tf.cast(tf.gather(cells, tf.where(cells > 0)), tf.float32)  # REMOVE BACKGROUND
    if len(cells) <= 1:   return tf.cast(0, tf.float32)  # No Cells
    eval = []
    for c in cells:
        eval.append(iou_cell(masks_gt, masks_pred, c))
    return eval


def eval_metrics(masks_gt, masks_pred, threshold=0.5):
    if masks_gt is None or masks_pred is None or (masks_gt.shape != masks_pred.shape):
        return 0,0,0,0,0,[]
    iou_gt_pred = np.array(iou_tf(masks_gt, masks_pred))
    if len(iou_gt_pred.shape) == 0 : return 0,0,0,0,0,[]  # NO CELLS
    FN = list(iou_gt_pred[iou_gt_pred[:, 1] <= 0, 0])  # Missing Cells -> FALSE NEGATIVE
    #print(f"FN: {len(FN)}")
    iou_gt_pred = iou_gt_pred[iou_gt_pred[:, 1] > 0, :]  # IOUS ONLY ON ALL TRUE POSITIVE
    iou_cells = iou_gt_pred[:, 2]  # IOU VALUES
    idx = np.where(iou_gt_pred[:, 4] > iou_gt_pred[:, 5])
    iou_over = np.copy(iou_cells)
    iou_over[idx] = 1 + (1 - iou_over[idx])  # IOU UNVER VS OVER

    # Average Precision on IOU > threshold
    keep_cells = iou_cells >= threshold
    TP = list(iou_gt_pred[keep_cells, 0])  # Good Cells -> TRUE POSITIVE
    FN = FN + list(iou_gt_pred[iou_cells < threshold, 0])

    # Missing Cells
    matched_cells = list(np.uint16(iou_gt_pred[keep_cells, 1]))
    pred_cells = np.unique(masks_pred)
    pred_cells = pred_cells[pred_cells != 0]
    FP = []
    for c in pred_cells:
        if c not in matched_cells:
            FP.append(c)

    nFN = len(FN)
    nTP = len(TP)
    nFP = len(FP)
    precision = nTP / (nTP + nFP) if (nTP + nFP) > 0 else 0.0
    recall = nTP / (nTP + nFN) if (nTP + nFN) > 0 else 0.0
    error_rate=(nFP+nFN)/(nTP+nFN)
    average_precision = (nTP) / (nTP + nFN + nFP)
    return  error_rate,average_precision,precision, recall, np.mean(iou_cells), iou_over

def ms(v,d=2):
    if type(v)==str: v=float(v.strip())
    if type(v) == list:
        if len(v) == 0:
            return "0"
        else:
            v = np.array(v)
    if type(v)==np.array or type(v)==np.ndarray: v=v.mean() #No MEAN FOR IOUS !
    v=round(v, d)
    a="%.2f" % v
    return a

def metricS(er,ap,iou,d=2): #Return Metrics in String Format
    s=", "
    s += f"ER:{ms(er,d)} ,"
    s += f"AP:{ms(ap,d)} ,"
    s += f"IOU:{ms(iou,d)} "

    return  s



def voi_metrics(masks_gt, masks_pred, ignore_label=0, log_base=2):
    '''
    Compute Variation of Information metrics between two label maps.
    Returns (vi_split, vi_merge, vi_total) with default log base 2 (bits).
    Background label defined by ignore_label is ignored in the contingency table.
    '''
    if masks_gt is None or masks_pred is None:
        return 0.0, 0.0, 0.0
    if masks_gt.shape != masks_pred.shape:
        return 0.0, 0.0, 0.0

    gt = masks_gt.ravel()
    pd = masks_pred.ravel()

    valid = (gt != ignore_label) & (pd != ignore_label)
    if not np.any(valid):
        return 0.0, 0.0, 0.0

    gt = gt[valid]
    pd = pd[valid]

    gt_vals, gt_inv = np.unique(gt, return_inverse=True)
    pd_vals, pd_inv = np.unique(pd, return_inverse=True)
    G = gt_vals.shape[0]
    S = pd_vals.shape[0]

    # contingency table via flat indexing
    combined = gt_inv.astype(np.int64) * np.int64(S) + pd_inv.astype(np.int64)
    counts = np.bincount(combined, minlength=G * S).astype(np.float64)
    contingency = counts.reshape(G, S)

    n = contingency.sum()
    if n <= 0:
        return 0.0, 0.0, 0.0

    p_ij = contingency / n
    p_g = p_ij.sum(axis=1, keepdims=True)
    p_s = p_ij.sum(axis=0, keepdims=True)

    # avoid log(0); only compute where p_ij>0
    mask = p_ij > 0
    if log_base == 2:
        log_fn = np.log2
    else:
        log_fn = np.log

    eps = np.finfo(np.float64).tiny

    # VI_split = H(S|G) = - sum p(g,s) log ( p(g,s) / p(g) )
    ratio_split = p_ij / np.maximum(p_g, eps)
    vi_split = -np.sum(p_ij[mask] * log_fn(ratio_split[mask]))

    # VI_merge = H(G|S) = - sum p(g,s) log ( p(g,s) / p(s) )
    ratio_merge = p_ij / np.maximum(p_s, eps)
    vi_merge = -np.sum(p_ij[mask] * log_fn(ratio_merge[mask]))

    return float(vi_split), float(vi_merge), float(vi_split + vi_merge)

def eval_file(gt,pred):
    if not isfile(gt):
        print(f" Miss Ground truth Images {gt}")
        return None
    if not isfile(pred):
        print(f" Miss Predicted Images {pred}")
        return None
    gti = imread(gt)
    predi = imread(pred)
    error_rate,average_precision,precision, recall, iou, iou_over = eval_metrics(gti, predi)
    return f"Error Rate:{error_rate}, Average Precision:{average_precision}, Precision:{precision}, Recall:{recall}, IoU:{iou}"


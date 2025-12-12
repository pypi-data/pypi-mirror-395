'''Intersection over Union. In the current primitive form, it is treated as a separate module.'''


__all__ = ['iou_impl']


def iou_impl(inter_volume, obj1_volume, obj2_volume, eps=1E-7):
    return inter_volume / (obj1_volume + obj2_volume - inter_volume + eps)

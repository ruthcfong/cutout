import random

import torch
import numpy as np


class Cutout(object):
    """Randomly mask out one or more patches from an image.

    Args:
        n_holes (int): Number of patches to cut out of each image.
        length (int): The length (in pixels) of each square patch.
        orig_prob (float): Probability to the original image is preserved.
            Default: 0.0.
        variant (str): Type of cutout to use; choose from 'delete' and
            'preserve'. Default: 'delete'.
    """
    def __init__(self, n_holes, length, orig_prob=0.0, variant='delete'):
        self.n_holes = n_holes
        self.length = length
        self.orig_prob = orig_prob
        self.variant = variant

    def __call__(self, img):
        """
        Args:
            img (Tensor): Tensor image of size (C, H, W).
        Returns:
            Tensor: Image with n_holes of dimension length x length cut out of it.
        """
        # Show the original image with probability p = self.orig_prob.
        if self.orig_prob >= random.random():
            return img

        h = img.size(1)
        w = img.size(2)

        # TODO(ruthfong): Convert to torch code.
        mask = np.ones((h, w), np.float32)

        for n in range(self.n_holes):
            y = np.random.randint(h)
            x = np.random.randint(w)

            y1 = np.clip(y - self.length // 2, 0, h)
            y2 = np.clip(y + self.length // 2, 0, h)
            x1 = np.clip(x - self.length // 2, 0, w)
            x2 = np.clip(x + self.length // 2, 0, w)

            mask[y1: y2, x1: x2] = 0.

        mask = torch.from_numpy(mask)

        if self.variant == 'preserve':
            mask = 1. - mask
        elif self.variant == 'delete':
            pass
        else:
            assert False

        mask = mask.expand_as(img)
        img = img * mask

        return img

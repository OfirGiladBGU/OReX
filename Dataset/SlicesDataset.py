import torch
from torch.utils.data import Dataset
import numpy as np

from Dataset.Helpers import *
from Dataset.Sampler import sample_plane, sample_hull
from Globals import OUTSIDE_LABEL, INSIDE_LABEL


class SlicesDataset(Dataset):
    def __init__(self, xyzs, labels, boundary_xyzs=None):

        if boundary_xyzs is None:
            boundary_xyzs = np.empty((0, 3))
        self.densities = torch.tensor(np.concatenate((labels, np.full(len(boundary_xyzs), OUTSIDE_LABEL)))).view((-1, 1))
        self.xyzs = torch.tensor(np.concatenate((xyzs, boundary_xyzs)))

        self.size = len(self.xyzs)

    @classmethod
    def from_csl(cls, csl, gen):
        data = [sample_plane(plane, gen) for plane in csl.planes if not plane.is_empty]

        xyzs_list = []
        labels_list = []

        for plane_data, plane in zip(data, [p for p in csl.planes if not p.is_empty]):
            # sample_plane now returns (xyzs, labels, labeler, pca, plane_normal)
            xyzs, labels, labeler, pca, plane_normal = plane_data

            # repair ambiguous labels (0.5) by small normal perturbation
            if len(xyzs) > 0:
                half_mask = (labels == (INSIDE_LABEL + OUTSIDE_LABEL) / 2)
                if np.any(half_mask):
                    eps = 1e-3 * max(1.0, np.max(np.abs(csl.all_vertices)))
                    pts = xyzs[half_mask]
                    # move a tiny amount along plane normal in both directions
                    moved_pos = pts + plane_normal * eps
                    moved_neg = pts - plane_normal * eps

                    # project moved points into plane local 2D coords for labeler
                    # pca.inverse_transform maps 2D->3D, so to get 2D we need pca.transform
                    try:
                        pts2d = pca.transform(pts)
                        pos2d = pca.transform(moved_pos)
                        neg2d = pca.transform(moved_neg)
                    except Exception:
                        # if PCA fails, skip repair
                        pts2d = pos2d = neg2d = None

                    if pts2d is not None:
                        lab_pos = labeler(pos2d)
                        lab_neg = labeler(neg2d)

                        # prefer a definite label (0.0 or 1.0) when found
                        new_labels = labels.copy()
                        for i, (lp, ln, idx) in enumerate(zip(lab_pos, lab_neg, np.where(half_mask)[0])):
                            if lp != (INSIDE_LABEL + OUTSIDE_LABEL) / 2:
                                new_labels[idx] = lp
                            elif ln != (INSIDE_LABEL + OUTSIDE_LABEL) / 2:
                                new_labels[idx] = ln
                        labels = new_labels

            xyzs_list.append(xyzs)
            labels_list.append(labels)

        boundary = sample_hull(csl)
        return cls(np.concatenate(xyzs_list), np.concatenate(labels_list), boundary)

    def __len__(self):
        return self.size

    def __getitem__(self, idx):
        return self.xyzs[idx], self.densities[idx]

    def to_ply(self, file_name):
        header = f'ply\nformat ascii 1.0\nelement vertex {self.size}\n' \
                 f'property float x\nproperty float y\nproperty float z\n' \
                 f'property float quality\n' \
                 f'property uchar red\n' \
                 f'property uchar green\n' \
                 f'property uchar blue\n' \
                 f'element face 0\nproperty list uchar int vertex_index\nend_header\n'

        with open(file_name, 'w') as f:
            f.write(header)
            for xyz, density in zip(self.xyzs, self.densities):
                color = np.zeros(3, dtype=int)
                color[int(density * 2)] = 255
                f.write('{:.10f} {:.10f} {:.10f} {:.10f} {} {} {}\n'.format(*xyz, density[0], *color))

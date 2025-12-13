"""Plot functions for 2D (geometric dim) spaces."""

import numpy as np
import torch

from scimba_torch.domain.meshless_domain.base import VolumetricDomain
from scimba_torch.geometry.regularized_sdf_projectors import RegularizedSdfProjector
from scimba_torch.plots._utils.plots_utilities import (
    get_regular_mesh_as_np_array,
    get_regular_mesh_as_np_meshgrid,
)
from scimba_torch.utils.scimba_tensors import LabelTensor


def _get_mesh_and_mask_and_labels_for_3d_plot(
    spatial_domain: VolumetricDomain,
    # parameters_values: list[float],
    n_visu: int,
) -> tuple[
    tuple[np.ndarray, np.ndarray],
    np.ndarray,
    np.ndarray,
    np.ndarray,
]:
    ebb = spatial_domain.get_extended_bounds_postmap(0.05)
    x_mesh, y_mesh, z_mesh = get_regular_mesh_as_np_meshgrid(ebb, n_visu)
    # get xy vector and mask
    xyz = get_regular_mesh_as_np_array(ebb, n_visu)

    labels = np.zeros(n_visu**3, dtype=np.int32)

    if spatial_domain.is_mapped:
        return NotImplemented

    else:
        mask = spatial_domain.is_outside_postmap_np(xyz)
        for i, subdomain in enumerate(spatial_domain.list_subdomains):
            condition = subdomain.is_inside_postmap_np(xyz)
            labels[condition] = i + 1

    return ((x_mesh, y_mesh, z_mesh), xyz, mask, labels)


def _plot_3x_regularized_sdf_projector(
    fig,
    rsdfproj: RegularizedSdfProjector,
    **kwargs,
):
    n_visu = kwargs.get("n_visu", 64)
    n_exact = kwargs.get("n_exact", 2000)
    tol = kwargs.get("tol_implicit_plot", 1e-3)
    colormap = kwargs.get("colormap", "turbo")

    nblines, nbcols = 1, 3

    bounding_box = rsdfproj.geometric_domain.bounds.cpu().detach().numpy()

    if rsdfproj.domain_sampler.from_sample:
        points_ex = rsdfproj.domain_sampler.points
        normals_ex = rsdfproj.domain_sampler.normals
    else:
        points_ex, normals_ex = rsdfproj.domain_sampler.bc_sample(n_exact)
        points_ex = points_ex.x
        normals_ex = normals_ex.x

    axe_index = 1
    axe = fig.add_subplot(nblines, nbcols, axe_index)
    rsdfproj.losses.plot(axe, **kwargs)

    # compute approximated points of the bc
    _, xyz, _, xyzl = _get_mesh_and_mask_and_labels_for_3d_plot(
        rsdfproj.geometric_domain, n_visu
    )
    xyz_tensor = LabelTensor(
        torch.tensor(xyz, dtype=torch.double), torch.tensor(xyzl, dtype=torch.int32)
    )
    mu_tensor = LabelTensor(
        torch.ones(xyz_tensor.x.shape[0], 0, dtype=torch.double)
    )  # Assuming mu is a constant tensor of ones
    phi = rsdfproj.space.evaluate(xyz_tensor, mu_tensor)
    phi = phi.get_components()[:, 0].cpu().detach().numpy()
    x_ap, y_ap, z_ap = xyz[np.abs(phi) < tol].T
    x_ex, y_ex, z_ex = points_ex.cpu().detach().numpy().T

    axe_index = 2
    axe = fig.add_subplot(nblines, nbcols, axe_index, projection="3d")

    xyz_tensor = LabelTensor(points_ex)
    xyz_tensor.x.requires_grad = True
    mu_tensor = LabelTensor(torch.ones(xyz_tensor.x.shape[0], 0, dtype=torch.double))
    phi = rsdfproj.space.evaluate(xyz_tensor, mu_tensor)
    phi_np = phi.get_components()[:, 0].cpu().detach().numpy()
    max_phi = np.max(np.abs(phi_np))
    mean_phi = np.mean(np.abs(phi_np))

    im = axe.scatter(
        x_ex,
        y_ex,
        z_ex,
        c=np.abs(phi_np),
        s=1.5,
        cmap=colormap,
        label="exact bound. pnts",
    )
    axe.scatter(
        x_ap, y_ap, z_ap, color="grey", s=1, alpha=0.5, label="approx bound. pnts"
    )
    fig.colorbar(im, ax=axe)
    axe.set_title("Max phi: %.2e, Mean phi: %.2e" % (max_phi, mean_phi))
    axe.set_xlim(bounding_box[0][0], bounding_box[0][1])
    axe.set_ylim(bounding_box[1][0], bounding_box[1][1])
    axe.set_zlim(bounding_box[2][0], bounding_box[2][1])
    axe.set_aspect("equal")
    axe.legend()

    axe_index = 3
    axe = fig.add_subplot(nblines, nbcols, axe_index, projection="3d")

    # Compute the gradient of the levelset function at the exact boundary
    phi_x, phi_y, phi_z = rsdfproj.space.grad(phi, xyz_tensor)
    phi_x_np = phi_x[:, 0].cpu().detach().numpy()
    phi_y_np = phi_y[:, 0].cpu().detach().numpy()
    phi_z_np = phi_z[:, 0].cpu().detach().numpy()

    n_x, n_y, n_z = normals_ex.cpu().detach().numpy().T

    axe.scatter(
        x_ex,
        y_ex,
        z_ex,
        s=1,
        # label="Exact boundary points"
    )
    axe.quiver(
        x_ex[::20],
        y_ex[::20],
        z_ex[::20],
        n_x[::20],
        n_y[::20],
        n_z[::20],
        color="red",
        label="exact",
        alpha=0.5,
    )
    axe.quiver(
        x_ex[::20],
        y_ex[::20],
        z_ex[::20],
        phi_x_np[::20],
        phi_y_np[::20],
        phi_z_np[::20],
        color="blue",
        label="approximated",
        alpha=0.5,
    )
    axe.set_title("normals at the exact boundary")
    axe.set_aspect("equal")
    axe.set_xlim(bounding_box[0][0], bounding_box[0][1])
    axe.set_ylim(bounding_box[1][0], bounding_box[1][1])
    axe.set_zlim(bounding_box[2][0], bounding_box[2][1])
    axe.legend()


if __name__ == "__main__":  # pragma: no cover
    pass

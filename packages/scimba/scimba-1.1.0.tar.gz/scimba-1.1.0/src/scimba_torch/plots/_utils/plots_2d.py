"""Plot functions for 2D (geometric dim) spaces."""

import warnings
from typing import Any, Sequence

import matplotlib.pyplot as plt
import numpy as np
import torch
from scipy.spatial import KDTree

from scimba_torch.approximation_space.abstract_space import AbstractApproxSpace
from scimba_torch.domain.meshless_domain.base import VolumetricDomain
from scimba_torch.geometry.regularized_sdf_projectors import RegularizedSdfProjector
from scimba_torch.integration.monte_carlo import DomainSampler
from scimba_torch.plots._utils.eval_utilities import eval_on_np_tensors
from scimba_torch.plots._utils.parameters_utilities import get_mu_mu_str
from scimba_torch.plots._utils.plots_2d_utilities import (
    _get_np_vect_from_cut_2d,
    _plot_2d_contourf,
    _plot_2d_cut_values,
)
from scimba_torch.plots._utils.plots_utilities import (
    COLORS_LIST,
    LINESTYLE_LIST,
    get_objects_nblines_nbcols,
    get_regular_mesh_as_np_array,
    get_regular_mesh_as_np_meshgrid,
)
from scimba_torch.plots._utils.time_utilities import get_t_t_str
from scimba_torch.plots._utils.velocity_utilities import get_v_v_str
from scimba_torch.utils.scimba_tensors import LabelTensor


def _get_mesh_and_mask_and_labels_for_2d_plot(
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
    x_mesh, y_mesh = get_regular_mesh_as_np_meshgrid(ebb, n_visu)
    # get xy vector and mask
    xy = get_regular_mesh_as_np_array(ebb, n_visu)

    labels = np.zeros(n_visu**2, dtype=np.int32)

    if spatial_domain.is_mapped:
        assert spatial_domain.mapping is not None  # for type checking
        if not spatial_domain.mapping.is_invertible:
            tol = 1e-2
            m_is_empty = np.vectorize(lambda lis: len(lis) == 0)
            # construct a KDTree from a point cloud sampled on the domain
            sampler = DomainSampler(spatial_domain)
            sample = sampler.sample(n_visu * n_visu)
            p_cloud = sample.x.detach().cpu().numpy()
            labels = sample.labels.detach().cpu().numpy()
            # plt.scatter(p_cloud[:, 0], p_cloud[:, 1], marker=".")
            # plt.show()
            KDT = KDTree(p_cloud)
            indexes = KDT.query_ball_point(xy, tol)
            mask = m_is_empty(indexes)
            # print("mask.shape: ", mask.shape)
        else:
            mask = spatial_domain.is_outside_postmap_np(xy)
            for i, subdomain in enumerate(spatial_domain.list_subdomains):
                condition = subdomain.is_inside_postmap_np(xy)
                labels[condition] = i + 1

    # alternative: construct a mesh of the not mapped domain, get mask,
    # then map the mesh
    # ebb = spatial_domain.get_extended_bounds(0.05)
    # xy = get_regular_mesh_as_np_array(ebb, n_visu)
    # mask = spatial_domain.is_outside_np(xy)
    # xy = (
    #    spatial_domain.mapping(torch.tensor(xy, dtype=torch.get_default_dtype()))
    #    .detach()
    #    .cpu()
    #    .numpy()
    # )
    # xyr = xy.reshape((n_visu, n_visu, 2), copy=True)
    # x_mesh = xyr[:, :, 0]
    # y_mesh = xyr[:, :, 1]

    else:
        mask = spatial_domain.is_outside_postmap_np(xy)
        for i, subdomain in enumerate(spatial_domain.list_subdomains):
            condition = subdomain.is_inside_postmap_np(xy)
            labels[condition] = i + 1

    return ((x_mesh, y_mesh), xy, mask, labels)


def _get_meshes_and_masks_for_2d_cuts(
    spatial_domain: VolumetricDomain,
    # parameters_values: list[float],
    cuts: np.ndarray,
    n_visu: int,
):
    points, normals = cuts[:, 0, :], cuts[:, 1, :]
    norms = np.linalg.norm(normals, axis=-1)
    if np.any(np.isclose(norms, 0.0)):
        raise ValueError(
            "in get_meshes_and_masks_for_2d_cuts: 2 norm of normal vector must be not "
            "close to 0"
        )
    normals /= norms[:, None]

    tol = 5e-2
    KDT_l: list[Any] = []
    m_is_empty = np.vectorize(lambda lis: len(lis) == 0)
    if spatial_domain.is_mapped:
        assert spatial_domain.mapping is not None  # for type checking
        if not spatial_domain.mapping.is_invertible:
            # construct a KDTree from a point cloud sampled on the domain
            sampler = DomainSampler(spatial_domain)
            p_cloud = (sampler.sample(n_visu * n_visu)).x.detach().cpu().numpy()
            KDT_l.append(KDTree(p_cloud))

    ebb = spatial_domain.get_extended_bounds_postmap(0.05)
    meshes_and_masks = []
    for i in range(len(cuts)):
        mesh = _get_np_vect_from_cut_2d(ebb, points[i, ...], normals[i, ...], n_visu)
        if spatial_domain.is_mapped:
            assert spatial_domain.mapping is not None  # for type checking
            if not spatial_domain.mapping.is_invertible:
                # create the mask from the KDTree
                indexes = KDT_l[0].query_ball_point(mesh, tol)
                mask = m_is_empty(indexes)
                # print("mask.shape: ", mask.shape)
            else:
                mask = spatial_domain.is_outside_postmap_np(mesh)
        else:
            mask = spatial_domain.is_outside_postmap_np(mesh)
        meshes_and_masks.append((mesh, mask))

    return meshes_and_masks


def _get_cut_object_linestyle_dict(objects: list[str]) -> dict:
    res = {"approximation": LINESTYLE_LIST[0]}
    if len(objects) > len(LINESTYLE_LIST):
        warnings.warn(
            f"in plots_2d.py: no more than {len(LINESTYLE_LIST)} objects can be plot "
            f"on cuts ({len(objects)} asked); only the first {len(LINESTYLE_LIST)} "
            f"will be plotted on cuts",
            UserWarning,
        )
    for i, object in enumerate(objects):
        if i < len(LINESTYLE_LIST):
            res[object] = LINESTYLE_LIST[i]
    return res


def __plot_2x_abstract_approx_space(
    fig,
    space: AbstractApproxSpace,
    spatial_domain: VolumetricDomain,
    parameters_values: Sequence[np.ndarray],
    time_values: Sequence[np.ndarray],
    velocity_values: Sequence[np.ndarray],
    components: Sequence[int],
    oneline: bool,
    **kwargs,
):
    objects, nblines, nbcols, loss_only_on_first_line = get_objects_nblines_nbcols(
        spatial_domain.dim,
        oneline,
        parameters_values,
        time_values,
        velocity_values,
        components,
        **kwargs,
    )

    # print("oneline: ", oneline)
    # print("parameters_values: ", parameters_values)
    # print("velocity_values: ", velocity_values)
    # print("loss_only_on_first_line: ", loss_only_on_first_line)
    # print("nblines: %d, nbcols: %d" % (nblines, nbcols))
    # print("objects: ", objects)
    # print("input kwargs: ", kwargs)

    # dictionary of symbols for eval and derivatives
    symb_dict = {
        "components": ["u"],
        "space_variables": ["x", "y"],
    }
    if len(time_values) > 0:
        symb_dict["time_variable"] = ["t"]
    if len(velocity_values) > 0:
        nbvelocity_variables = velocity_values[0].shape[-1]
        velocity_variables = ["v" + str(i) for i in range(nbvelocity_variables)]
        symb_dict["phase_variables"] = velocity_variables
    # print("symb_dict: ", symb_dict)

    if len(parameters_values) == 0:
        parameters_values = [np.array([])]
    if len(time_values) == 0:
        time_values = [np.array([])]
    if len(velocity_values) == 0:
        velocity_values = [np.array([])]

    default_velocity_strs = ["" for _ in velocity_values]
    velocity_strs = kwargs.get("velocity_strs", default_velocity_strs)

    # assert not (
    #     ((len(parameters_values) > 1) and (len(time_values) > 1))
    #     or ((len(parameters_values) > 1) and (len(velocity_values) > 1))
    #     or ((len(time_values) > 1) and (len(velocity_values) > 1))
    # )

    list_to_explore = parameters_values
    if len(time_values) > 1:
        list_to_explore = time_values
    if len(velocity_values) > 1:
        list_to_explore = velocity_values
    if len(components) > 1:
        list_to_explore = components

    n_visu = kwargs.get("n_visu", 512)
    mesh_and_mask_and_labels = _get_mesh_and_mask_and_labels_for_2d_plot(
        spatial_domain, n_visu
    )

    mus_mu_strs = [
        get_mu_mu_str(parameters_values[i], n_visu**2)
        for i in range(len(parameters_values))
    ]
    # print(mus_mu_strs)
    ts_t_strs = [
        get_t_t_str(time_values[i], n_visu**2) for i in range(len(time_values))
    ]
    vs_v_strs = [
        get_v_v_str(velocity_values[i], n_visu**2, velocity_strs[i])
        for i in range(len(velocity_values))
    ]
    # p_index = (lambda i: 0) if len(parameters_values) == 1 else (lambda i: i)
    m_index = (lambda i: 0) if len(mus_mu_strs) == 1 else (lambda i: i)
    t_index = (lambda i: 0) if len(ts_t_strs) == 1 else (lambda i: i)
    v_index = (lambda i: 0) if len(vs_v_strs) == 1 else (lambda i: i)
    c_index = (lambda i: 0) if len(components) == 1 else (lambda i: i)

    kwargs_for_eval = {}
    for key in ["solution", "error", "residual"]:
        if key in kwargs and kwargs[key] is not None:
            kwargs_for_eval[key] = kwargs[key]
    for key in ["derivatives"]:
        if key in kwargs and kwargs[key] is not None:
            kwargs_for_eval[key] = []
            for der in kwargs[key]:
                if der is not None:
                    kwargs_for_eval[key].append(der)
    if "time_discrete" in kwargs:
        kwargs_for_eval["time_discrete"] = True

    evals = [
        eval_on_np_tensors(
            space,
            ts_t_strs[t_index(i)][0],
            mesh_and_mask_and_labels[1],
            vs_v_strs[v_index(i)][0],
            mus_mu_strs[m_index(i)][0],
            symb_dict,
            components[c_index(i)],
            labelsx=mesh_and_mask_and_labels[-1],
            **kwargs_for_eval,
        )
        for i in range(len(list_to_explore))
    ]

    cuts_data_for_plots: Sequence[Any] = [[] for _ in range(len(list_to_explore))]
    cut_object_linestyle_dict = _get_cut_object_linestyle_dict(objects)
    if "cuts" in kwargs:
        cuts = np.array(kwargs["cuts"])
        if cuts.ndim == 2:
            cuts = cuts[None, :, :]
        cuts_meshes_and_masks = _get_meshes_and_masks_for_2d_cuts(
            spatial_domain, cuts, n_visu
        )
        mu_cuts = [
            get_mu_mu_str(parameters_values[i], n_visu)[0]
            for i in range(len(parameters_values))
        ]
        t_cuts = [
            get_t_t_str(time_values[i], n_visu)[0] for i in range(len(time_values))
        ]
        v_cuts = [
            get_v_v_str(velocity_values[i], n_visu)[0]
            for i in range(len(velocity_values))
        ]
        # if len(t_cuts) == 0:
        #     t_cuts.append(np.array([]))
        for i in range(len(list_to_explore)):
            for j in range(len(cuts_meshes_and_masks)):
                eval = eval_on_np_tensors(
                    space,
                    t_cuts[t_index(i)],
                    cuts_meshes_and_masks[j][0],
                    v_cuts[v_index(i)],
                    mu_cuts[m_index(i)],
                    symb_dict,
                    components[c_index(i)],
                    **kwargs_for_eval,
                )
                data = (
                    cuts_meshes_and_masks[j][0],
                    eval,
                    cuts_meshes_and_masks[j][1],
                )
                cuts_data_for_plots[i].append(data)

    axe_index = 1
    for i in range(len(list_to_explore)):
        if "loss" in kwargs:
            if (i == 0) or (not loss_only_on_first_line):
                if kwargs["loss"] is not None:
                    axe_losses = fig.add_subplot(nblines, nbcols, axe_index)
                    losses = kwargs["loss"]
                    losses.plot(axe_losses, **kwargs)
            axe_index += 1

        for key in objects:
            if key in evals[i]:
                # print("axe_index: ", axe_index)
                n_axe = fig.add_subplot(nblines, nbcols, axe_index)
                _plot_2d_contourf(
                    fig,
                    n_axe,
                    mesh_and_mask_and_labels[0],
                    evals[i][key],
                    mesh_and_mask_and_labels[2],
                    key,
                    ts_t_strs[t_index(i)][1],
                    vs_v_strs[v_index(i)][1],
                    mus_mu_strs[m_index(i)][1],
                    cuts_data=cuts_data_for_plots[i],
                    linestyle_dict=cut_object_linestyle_dict,
                    **kwargs,
                )
            axe_index += 1

        for j in range(len(cuts_data_for_plots[i])):
            axe_cut = fig.add_subplot(nblines, nbcols, axe_index)
            _plot_2d_cut_values(
                fig,
                axe_cut,
                cuts_data_for_plots[i][j],
                COLORS_LIST[j],
                j,
                cut_object_linestyle_dict,
            )
            axe_index += 1

    plt.gca().set_rasterization_zorder(-1)


def _plot_2x_regularized_sdf_projector(
    fig,
    rsdfproj: RegularizedSdfProjector,
    **kwargs,
):
    n_visu = kwargs.get("n_visu", 512)
    n_exact = kwargs.get("n_exact", 2000)
    tol = kwargs.get("tol_implicit_plot", 1e-3)
    colormap = kwargs.get("colormap", "turbo")

    bounding_box = rsdfproj.geometric_domain.bounds.cpu().detach().numpy()

    if rsdfproj.domain_sampler.from_sample:
        points_ex = rsdfproj.domain_sampler.points
        normals_ex = rsdfproj.domain_sampler.normals
    else:
        points_ex, normals_ex = rsdfproj.domain_sampler.bc_sample(n_exact)
        points_ex = points_ex.x
        normals_ex = normals_ex.x

    # compute approximated points of the bc
    _, xy, _, xyl = _get_mesh_and_mask_and_labels_for_2d_plot(
        rsdfproj.geometric_domain, n_visu
    )
    xy_tensor = LabelTensor(
        torch.tensor(xy, dtype=torch.double), torch.tensor(xyl, dtype=torch.int32)
    )
    mu_tensor = LabelTensor(
        torch.ones(xy_tensor.x.shape[0], 0, dtype=torch.double)
    )  # Assuming mu is a constant tensor of ones
    phi = rsdfproj.space.evaluate(xy_tensor, mu_tensor)
    phi = phi.get_components()[:, 0].cpu().detach().numpy()
    x_ap, y_ap = xy[np.abs(phi) < tol].T
    x_ex, y_ex = points_ex.cpu().detach().numpy().T
    nblines, nbcols = 1, 3

    # axe_index = 1
    # axe = fig.add_subplot(nblines, nbcols, axe_index)
    # # Plot exact boundary points
    # axe.scatter(x_ex, y_ex, s=1, label="Exact BC")
    # axe.scatter(x_ap, y_ap, s=1, color="orange", linewidths=1.5, label="Approx. BC")
    # axe.set_title("Exact and approached boundary points")
    # axe.set_xlim(bounding_box[0][0], bounding_box[0][1])
    # axe.set_ylim(bounding_box[1][0], bounding_box[1][1])
    # axe.legend()

    axe_index = 2
    axe = fig.add_subplot(nblines, nbcols, axe_index)

    xy_tensor = LabelTensor(points_ex)
    xy_tensor.x.requires_grad = True
    mu_tensor = LabelTensor(torch.ones(xy_tensor.x.shape[0], 0, dtype=torch.double))
    phi = rsdfproj.space.evaluate(xy_tensor, mu_tensor)
    phi_np = phi.get_components()[:, 0].cpu().detach().numpy()
    max_phi = np.max(np.abs(phi_np))
    mean_phi = np.mean(np.abs(phi_np))

    im = axe.scatter(
        x_ex, y_ex, c=np.abs(phi_np), s=1.5, cmap=colormap, label="exact bound. pnts"
    )
    axe.scatter(x_ap, y_ap, color="grey", s=1, alpha=0.5, label="approx bound. pnts")
    fig.colorbar(im, ax=axe)
    axe.set_title("Max phi: %.2e, Mean phi: %.2e" % (max_phi, mean_phi))
    axe.set_xlim(bounding_box[0][0], bounding_box[0][1])
    axe.set_ylim(bounding_box[1][0], bounding_box[1][1])
    axe.set_aspect("equal")
    axe.legend()

    axe_index = 3
    axe = fig.add_subplot(nblines, nbcols, axe_index)

    # Compute the gradient of the levelset function at the exact boundary
    phi_x, phi_y = rsdfproj.space.grad(phi, xy_tensor)
    phi_x_np = phi_x[:, 0].cpu().detach().numpy()
    phi_y_np = phi_y[:, 0].cpu().detach().numpy()

    n_x, n_y = normals_ex.cpu().detach().numpy().T

    axe.scatter(
        x_ex,
        y_ex,
        s=1,
        # label="Exact boundary points"
    )
    axe.quiver(
        x_ex[::20],
        y_ex[::20],
        n_x[::20],
        n_y[::20],
        color="red",
        label="exact",
        alpha=0.5,
    )
    axe.quiver(
        x_ex[::20],
        y_ex[::20],
        phi_x_np[::20],
        phi_y_np[::20],
        color="blue",
        label="approximated",
        alpha=0.5,
    )
    axe.set_title("normals at the exact boundary")
    axe.set_aspect("equal")
    axe.set_xlim(bounding_box[0][0], bounding_box[0][1])
    axe.set_ylim(bounding_box[1][0], bounding_box[1][1])
    axe.legend()


if __name__ == "__main__":  # pragma: no cover
    pass

"""Plotting functions for regularized sdf projectors."""

import matplotlib.pyplot as plt

from scimba_torch.geometry.regularized_sdf_projectors import RegularizedSdfProjector
from scimba_torch.plots._utils.plots_2d import _plot_2x_regularized_sdf_projector
from scimba_torch.plots._utils.plots_3d import _plot_3x_regularized_sdf_projector
from scimba_torch.plots.plots_nd import plot_abstract_approx_space


def plot_regularized_sdf_projector(
    rsdfproj: RegularizedSdfProjector,
    **kwargs,
) -> None:
    """Plot an regularized sdf projector.

    Args:
        rsdfproj: the time-discrete solver
        **kwargs: arbitrary keyword arguments

    Keyword Args:
        ...: see examples

    Implemented only for 2 and 3 dimensional spaces.
    """
    if rsdfproj.geometric_domain.dim == 2:
        sizeofobjects = [4, 3]
        nblines, nbcols = 2, 3
        fig = plt.figure(
            figsize=(sizeofobjects[0] * nbcols, sizeofobjects[1] * nblines),
            layout="constrained",
        )
        subfigs = fig.subfigures(nblines, 1, wspace=0.07)

        plot_abstract_approx_space(
            rsdfproj.space,  # the approximation space
            rsdfproj.geometric_domain,  # the spatial domain
            [],  # the parameter's domain
            loss=rsdfproj.losses,  # for plot of the loss: the losses
            residual=rsdfproj.pde,  # for plot of the residual: the pde
            fig=subfigs[0],
            **kwargs,
        )

        _plot_2x_regularized_sdf_projector(subfigs[1], rsdfproj, **kwargs)

    elif rsdfproj.geometric_domain.dim == 3:
        sizeofobjects = [4, 3]
        nblines, nbcols = 1, 3
        fig = plt.figure(
            figsize=(sizeofobjects[0] * nbcols, sizeofobjects[1] * nblines),
            layout="constrained",
        )

        _plot_3x_regularized_sdf_projector(fig, rsdfproj, **kwargs)

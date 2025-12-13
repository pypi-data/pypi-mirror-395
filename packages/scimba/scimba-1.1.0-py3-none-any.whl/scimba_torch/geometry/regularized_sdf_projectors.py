"""A module for learning regularized signed distance functions."""

from abc import ABC
from typing import cast

import torch

from scimba_torch.approximation_space.abstract_space import AbstractApproxSpace
from scimba_torch.approximation_space.nn_space import NNxSpace
from scimba_torch.domain.meshless_domain.base import VolumetricDomain
from scimba_torch.geometry.monte_carlo_hypersurface import HyperSurfaceSampler
from scimba_torch.geometry.parametric_hypersurface import ParametricHyperSurface
from scimba_torch.geometry.regularized_eikonal_pde import RegEikonalPDE
from scimba_torch.integration.monte_carlo import TensorizedSampler
from scimba_torch.integration.monte_carlo_parameters import UniformParametricSampler
from scimba_torch.neural_nets.coordinates_based_nets.mlp import GenericMLP
from scimba_torch.numerical_solvers.elliptic_pde.pinns import (
    AnagramPinnsElliptic,
    NaturalGradientPinnsElliptic,
    PinnsElliptic,
)
from scimba_torch.optimizers.losses import GenericLosses, MassLoss

# from scimba_torch.optimizers.optimizers_data import OptimizerData
from scimba_torch.physical_models.elliptic_pde.abstract_elliptic_pde import (
    StrongFormEllipticPDE,
)
from scimba_torch.physical_models.elliptic_pde.linear_order_2 import (
    LinearOrder2PDE,
)


class RegularizedSdfProjector(ABC):
    """The abstract class for Regularized SDF projectors.

    SDF = Signed Distance Function

    Args:
        points_file: A .txt file of points on the curve, default to None.
        parametric_hyper_surface: a parametric HyperSurface, default to None.
            One among points_file, parametric_hyper_surface must be provided.
        bounding_domain: a bounding domain for the surface. Mandatory if
            parametric_hyper_surface is given.
        **kwargs: arbitrary keyword arguments

    Keyword Args:
        architecture: the architecture of the NN to be used (default: GenericMLP).
        layer_sizes: the size of the hidden layers (default: [10] * 4).
        activation_type: the activation function (default: "sine").
        ...
    """

    def __init__(
        self,
        points_file: str | None = None,
        parametric_hyper_surface: ParametricHyperSurface | None = None,
        bounding_domain: VolumetricDomain
        | list[tuple[float, float]]
        | torch.Tensor
        | None = None,
        **kwargs,
    ):
        self.domain_sampler = HyperSurfaceSampler(
            points_file=points_file,
            parametric_hyper_surface=parametric_hyper_surface,
            bounding_domain=bounding_domain,
        )

        self.geometric_domain = self.domain_sampler.bounding_domain

        sampler = TensorizedSampler((self.domain_sampler, UniformParametricSampler([])))

        architecture = kwargs.get("arch", GenericMLP)
        layer_sizes = kwargs.get("layer_sizes", [10] * 4)
        activation_type = kwargs.get("activation_type", "sine")
        self.space: AbstractApproxSpace = NNxSpace(
            1,
            0,
            architecture,
            self.geometric_domain,
            sampler,
            layer_sizes=layer_sizes,
            activation_type=activation_type,
        )

        self.pde: StrongFormEllipticPDE | LinearOrder2PDE = RegEikonalPDE(self.space)

        self.losses = GenericLosses(
            [
                ("residual", torch.nn.MSELoss(), 1.0),
                ("regularization", torch.nn.MSELoss(), 0.0),
                ("dirichlet", torch.nn.MSELoss(), 10.0),
                ("neumann", MassLoss(), 2.0),
            ],
        )

        self.in_weights = [1.0, 0.0]
        self.bc_weights = [1.0, 0.2**2]  # square because of the MassLoss
        self.bc_weight = 10.0

        # super().__init__(pde, bc_type="weak", losses=losses, bc_weight=10.0, **kwargs)


class RegularizedSdfPinnsElliptic(RegularizedSdfProjector, PinnsElliptic):
    """The class for Regularized SDF projectors without preconditioning.

    SDF = Signed Distance Function

    Args:
        points_file: A .txt file of points on the curve, default to None.
        parametric_hyper_surface: a parametric HyperSurface, default to None.
            One among points_file, parametric_hyper_surface must be provided.
        bounding_domain: a bounding domain for the surface. Mandatory if
            parametric_hyper_surface is given.
        **kwargs: arbitrary keyword arguments

    Keyword Args:
        architecture: the architecture of the NN to be used (default: GenericMLP).
        layer_sizes: the size of the hidden layers (default: [10] * 4).
        activation_type: the activation function (default: "sine").
        ...
    """

    def __init__(
        self,
        points_file: str | None = None,
        parametric_hyper_surface: ParametricHyperSurface | None = None,
        bounding_domain: VolumetricDomain
        | list[tuple[float, float]]
        | torch.Tensor
        | None = None,
        **kwargs,
    ):
        super().__init__(
            points_file, parametric_hyper_surface, bounding_domain, **kwargs
        )

        if "in_weights" not in kwargs:
            kwargs["in_weights"] = self.in_weights
        if "bc_weights" not in kwargs:
            kwargs["bc_weights"] = self.bc_weights
        if "bc_weight" not in kwargs:
            kwargs["bc_weight"] = self.bc_weight

        super(RegularizedSdfProjector, self).__init__(
            self.pde, bc_type="weak", losses=self.losses, **kwargs
        )


class RegularizedSdfEnergyNaturalGradient(
    RegularizedSdfProjector, NaturalGradientPinnsElliptic
):
    """The class for Regularized SDF projectors with Energy Natural Gradient.

    SDF = Signed Distance Function

    Args:
        points_file: A .txt file of points on the curve, default to None.
        parametric_hyper_surface: a parametric HyperSurface, default to None.
            One among points_file, parametric_hyper_surface must be provided.
        bounding_domain: a bounding domain for the surface. Mandatory if
            parametric_hyper_surface is given.
        **kwargs: arbitrary keyword arguments

    Keyword Args:
        architecture: the architecture of the NN to be used (default: GenericMLP).
        layer_sizes: the size of the hidden layers (default: [10] * 4).
        activation_type: the activation function (default: "sine").
        ...
    """

    def __init__(
        self,
        points_file: str | None = None,
        parametric_hyper_surface: ParametricHyperSurface | None = None,
        bounding_domain: VolumetricDomain
        | list[tuple[float, float]]
        | torch.Tensor
        | None = None,
        **kwargs,
    ):
        super().__init__(
            points_file, parametric_hyper_surface, bounding_domain, **kwargs
        )

        if "in_weights" not in kwargs:
            kwargs["in_weights"] = self.in_weights
        if "bc_weights" not in kwargs:
            kwargs["bc_weights"] = self.bc_weights
        if "bc_weight" not in kwargs:
            kwargs["bc_weight"] = self.bc_weight

        super(RegularizedSdfProjector, self).__init__(
            self.pde, bc_type="weak", losses=self.losses, **kwargs
        )


class RegularizedSdfAnagram(RegularizedSdfProjector, AnagramPinnsElliptic):
    """The class for Regularized SDF projectors with Anagram.

    SDF = Signed Distance Function

    Args:
        points_file: A .txt file of points on the curve, default to None.
        parametric_hyper_surface: a parametric HyperSurface, default to None.
            One among points_file, parametric_hyper_surface must be provided.
        bounding_domain: a bounding domain for the surface. Mandatory if
            parametric_hyper_surface is given.
        **kwargs: arbitrary keyword arguments

    Keyword Args:
        architecture: the architecture of the NN to be used (default: GenericMLP).
        layer_sizes: the size of the hidden layers (default: [10] * 4).
        activation_type: the activation function (default: "sine").
        ...
    """

    def __init__(
        self,
        points_file: str | None = None,
        parametric_hyper_surface: ParametricHyperSurface | None = None,
        bounding_domain: VolumetricDomain
        | list[tuple[float, float]]
        | torch.Tensor
        | None = None,
        **kwargs,
    ):
        super().__init__(
            points_file, parametric_hyper_surface, bounding_domain, **kwargs
        )

        if "in_weights" not in kwargs:
            kwargs["in_weights"] = self.in_weights
        if "bc_weights" not in kwargs:
            kwargs["bc_weights"] = self.bc_weights
        if "bc_weight" not in kwargs:
            kwargs["bc_weight"] = self.bc_weight

        super(RegularizedSdfProjector, self).__init__(
            self.pde, bc_type="weak", losses=self.losses, **kwargs
        )


def learn_regularized_sdf(
    points_file: str | None = None,
    parametric_hyper_surface: ParametricHyperSurface | None = None,
    bounding_domain: VolumetricDomain
    | list[tuple[float, float]]
    | torch.Tensor
    | None = None,
    mode: str = "new",
    load_from: str | None = None,
    save_to: str | None = None,
    **kwargs,
) -> PinnsElliptic:
    """Learn a SDF from either a file of points or a parametric hypersurface.

    SDF = Signed Distance Function

    Args:
        points_file: A .txt file of points on the curve, default to None.
        parametric_hyper_surface: a parametric HyperSurface, default to None.
            One among points_file, parametric_hyper_surface must be provided.
        bounding_domain: a bounding domain for the surface. Mandatory if
            parametric_hyper_surface is given.
        mode: either "new" for new solving, "load" for loading from a file
            or "resume" for loading from a file and continue solving.
        load_from: the file from which loading the model.
        save_to: the file where saving the model.
        **kwargs: arbitrary keyword arguments

    Keyword Args:
        architecture: the architecture of the NN to be used (default: GenericMLP).
        layer_sizes: the size of the hidden layers (default: [10] * 4).
        activation_type: the activation function (default: "sine").
        epochs: the number of optimization steps
        n_collocation: the number of collocation points in the domain
        n_bc_collocation: the number of collocation points on the contour
        ...

    Returns:
        the PINN approximating the SDF

    Raises:
        NotImplementedError: the preconditioner is not known
        ValueError: when loading file is not provided
    """
    preconditioner = kwargs.get("preconditioner", "ENG")

    if preconditioner == "ENG":
        pinn: PinnsElliptic = RegularizedSdfEnergyNaturalGradient(
            points_file, parametric_hyper_surface, bounding_domain, **kwargs
        )
    elif preconditioner == "Anagram":
        pinn = RegularizedSdfAnagram(
            points_file, parametric_hyper_surface, bounding_domain, **kwargs
        )
    elif preconditioner == "None":
        pinn = RegularizedSdfPinnsElliptic(
            points_file, parametric_hyper_surface, bounding_domain, **kwargs
        )
    else:
        raise NotImplementedError(
            "not implemented for preconditioner %s" % preconditioner
        )

    if mode in ["load", "resume"] and load_from is None:
        raise ValueError("Please provide the name of a file to load the PINN from.")

    new_solving = mode == "new"
    resume_solving = mode == "resume"
    try_load = resume_solving or (not new_solving)
    load_ok = try_load and pinn.load(cast(str, load_from))
    solve = (not load_ok) or (resume_solving or new_solving)

    if solve:
        pinn.solve(**kwargs)

    if solve and save_to is not None:
        pinn.save(save_to)

    return pinn


if __name__ == "__main__":  # pragma: no cover
    import matplotlib.pyplot as plt

    from scimba_torch.geometry.utils import (
        write_points_normals_to_file,
    )
    from scimba_torch.plots.plot_regularized_sdf_projector import (
        plot_regularized_sdf_projector,
    )

    bean_2d = ParametricHyperSurface.bean_2d()
    bean_2d_bb = [(-0.4, 1.2), (-1.2, 0.4)]

    points, normals = bean_2d.sample(2000)
    write_points_normals_to_file(points, normals, "test.xy")

    torch.manual_seed(0)

    # pinn = RegularizedSdfEnergyNaturalGradient(
    #     points_file=None,
    #     parametric_hyper_surface=bean_2d,
    #     bounding_domain=bean_2d_bb
    # )
    pinn = RegularizedSdfEnergyNaturalGradient(
        points_file="test.xy", layer_sizes=[10] * 4
    )

    # pinn = RegularizedSdfEnergyNaturalGradient(
    #     points_file=None,
    #     parametric_hyper_surface=bean_2d,
    #     bounding_domain=bean_2d_bb,
    #     svd_threshold=1e-1
    # )

    new_training = True
    if new_training or not pinn.load(__file__, "pinnsbean"):
        pinn.solve(epochs=400, n_collocation=4000, n_bc_collocation=2000, verbose=True)
        pinn.save(__file__, "pinnsbean")

    plot_regularized_sdf_projector(
        pinn,
        n_visu=512,  # number of points for the visualization
        draw_contours=True,
        n_drawn_contours=20,
    )

    plt.show()

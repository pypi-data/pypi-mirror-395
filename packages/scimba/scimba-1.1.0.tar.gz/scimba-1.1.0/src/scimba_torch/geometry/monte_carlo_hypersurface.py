"""A module for sampling hypersurfaces."""

import warnings

import torch

from scimba_torch.domain.meshless_domain.base import VolumetricDomain
from scimba_torch.domain.meshless_domain.domain_nd import HypercubeND
from scimba_torch.geometry.parametric_hypersurface import ParametricHyperSurface
from scimba_torch.geometry.utils import (
    compute_bounding_box,
    read_points_normals_from_file,
)
from scimba_torch.integration.monte_carlo import DomainSampler
from scimba_torch.utils.scimba_tensors import LabelTensor


class HyperSurfaceSampler(DomainSampler):
    """Sampler for HyperSurfaces.

    It is constructed either from a .txt files containing points on the hypersurface,
    or from a ParametricHyperSurface.

    Args:
        points_file: A .txt file of points on the curve, default to None.
        parametric_hyper_surface: a parametric HyperSurface, default to None.
            One among points_file, parametric_hyper_surface must be provided.
        bounding_domain: a bounding domain for the surface. If None whereas
            parametric_hyper_surface is given, estimated by sampling.
        **kwargs: arbitrary keyword arguments

    Keyword Args:
        nb_points_for_estimation: in case where bounding box is estimated,
            number of points for estimation; default in 10 000.
        inflation_for_estimation: in case where bounding box is estimated,
            inflation factor used after estimation by sampling.


    Raises:
        ValueError: Arguments are not correct.
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
        if points_file is not None and parametric_hyper_surface is not None:
            raise ValueError(
                "first and second argument can not be simultaneously not None"
            )

        # Now a warning plus estimation with sampling
        # if parametric_hyper_surface is not None and bounding_domain is None:
        #     raise ValueError(
        #         "if constructed from parametric hypersurface, "
        #         "bounding domain must be given"
        #     )

        if bounding_domain is not None:
            if isinstance(bounding_domain, list) or isinstance(
                bounding_domain, torch.Tensor
            ):
                self.bounding_domain: VolumetricDomain = HypercubeND(
                    bounding_domain, is_main_domain=True
                )
            else:
                self.bounding_domain = bounding_domain

        self.from_sample = points_file is not None
        self.points = torch.zeros((0, 0))
        self.normals = torch.zeros((0, 0))
        if points_file is not None:
            self.points, self.normals = read_points_normals_from_file(points_file)
            if bounding_domain is None:
                inflated_bb = compute_bounding_box(self.points, 0.05)
                self.bounding_domain = HypercubeND(inflated_bb, is_main_domain=True)

        else:  # parametric_hyper_surface is not None
            assert isinstance(parametric_hyper_surface, ParametricHyperSurface)
            self.parametric_hyper_surface = parametric_hyper_surface
            if bounding_domain is None:
                nb_points = kwargs.get("nb_points_for_estimation", 10_000)
                inflation_factor = kwargs.get("inflation_for_estimation", 0.1)
                msg = (
                    "if constructed from parametric hypersurface,"
                    " a bounding domain should be given; it will be estimated with"
                    f" {nb_points} points and inflation {inflation_factor}"
                )
                warnings.warn(msg, UserWarning, stacklevel=2)
                inflated_bb = parametric_hyper_surface.estimate_bounding_box(
                    nb_samples=nb_points, inflation=inflation_factor
                )
                self.bounding_domain = HypercubeND(inflated_bb, is_main_domain=True)

        if not self.bounding_domain.is_main_domain:
            # self.bounding_domain.list_subdomains: list[VolumetricDomain] = []
            # self.bounding_domain.list_holes: list[VolumetricDomain] = []
            raise ValueError("bounding_domain must be a main domain")

        with warnings.catch_warnings(category=UserWarning):
            warnings.simplefilter("ignore")
            super().__init__(self.bounding_domain)

    def bc_sample(self, n: int | list[int]) -> tuple[LabelTensor, LabelTensor]:
        """Samples `n` points on the hypersurface.

        Args:
            n: Number of points to sample.

        Returns:
            A tuple of tensors of sampled points and normals.

        Raises:
            NotImplementedError: when the first argument is a list
        """
        if isinstance(n, list):
            raise NotImplementedError("first argument must not be a list")

        if self.from_sample:
            indices = torch.randint(low=0, high=self.points.shape[0], size=(n,))
            points = self.points[indices]
            normals = self.normals[indices]
        else:
            points, normals = self.parametric_hyper_surface.sample(n)

        points.requires_grad = True
        return LabelTensor(points), LabelTensor(normals)


if __name__ == "__main__":  # pragma: no cover
    import matplotlib.pyplot as plt

    from scimba_torch.geometry.utils import (
        write_points_normals_to_file,
    )

    bean_2d = ParametricHyperSurface.bean_2d()
    bean_2d_bb = [(-0.4, 1.2), (-1.2, 0.4)]

    sampler_from_surf = HyperSurfaceSampler(
        points_file=None, parametric_hyper_surface=bean_2d, bounding_domain=bean_2d_bb
    )

    points_in = sampler_from_surf.sample(1000)

    points, normals = sampler_from_surf.bc_sample(1000)

    points_in_np = points_in.x.cpu().detach().numpy()
    points_np = points.x.cpu().detach().numpy()
    normals_np = normals.x.cpu().detach().numpy()

    plt.figure(figsize=(7, 7))
    plt.scatter(points_in_np[:, 0], points_in_np[:, 1], s=1, label="inside")
    plt.scatter(points_np[:, 0], points_np[:, 1], s=1, color="red", label="bc")
    plt.quiver(
        points_np[::20, 0],
        points_np[::20, 1],
        normals_np[::20, 0],
        normals_np[::20, 1],
        color="red",
        label="normals",
        alpha=0.5,
    )
    plt.legend()

    plt.show()

    points_, normals_ = bean_2d.sample(1000)
    write_points_normals_to_file(points_, normals_, "test.xy")
    sampler_from_file = HyperSurfaceSampler(
        points_file="test.xy", parametric_hyper_surface=None, bounding_domain=None
    )

    points_in = sampler_from_file.sample(1000)

    points, normals = sampler_from_file.bc_sample(1000)

    points_in_np = points_in.x.cpu().detach().numpy()
    points_np = points.x.cpu().detach().numpy()
    normals_np = normals.x.cpu().detach().numpy()

    plt.figure(figsize=(7, 7))
    plt.scatter(points_in_np[:, 0], points_in_np[:, 1], s=1, label="inside")
    plt.scatter(points_np[:, 0], points_np[:, 1], s=1, color="red", label="bc")
    plt.quiver(
        points_np[::20, 0],
        points_np[::20, 1],
        normals_np[::20, 0],
        normals_np[::20, 1],
        color="red",
        label="normals",
        alpha=0.5,
    )
    plt.legend()

    plt.show()

    sampler_from_file = HyperSurfaceSampler(
        points_file="test.xy",
        parametric_hyper_surface=None,
        bounding_domain=[(-1.0, 2.0), (-2.0, 1.0)],
    )

    points_in = sampler_from_file.sample(1000)

    points, normals = sampler_from_file.bc_sample(1000)

    points_in_np = points_in.x.cpu().detach().numpy()
    points_np = points.x.cpu().detach().numpy()
    normals_np = normals.x.cpu().detach().numpy()

    plt.figure(figsize=(7, 7))
    plt.scatter(points_in_np[:, 0], points_in_np[:, 1], s=1, label="inside")
    plt.scatter(points_np[:, 0], points_np[:, 1], s=1, color="red", label="bc")
    plt.quiver(
        points_np[::20, 0],
        points_np[::20, 1],
        normals_np[::20, 0],
        normals_np[::20, 1],
        color="red",
        label="normals",
        alpha=0.5,
    )
    plt.legend()

    plt.show()

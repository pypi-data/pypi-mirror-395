"""A module for parametric hypersurfaces."""

from __future__ import annotations

from typing import cast

import torch

from scimba_torch.domain.meshless_domain.base import SurfacicDomain, VolumetricDomain
from scimba_torch.domain.meshless_domain.domain_nd import HypercubeND
from scimba_torch.geometry.utils import compute_bounding_box
from scimba_torch.integration.monte_carlo import SurfacicSampler
from scimba_torch.utils.mapping import Mapping
from scimba_torch.utils.typing_protocols import FuncTypeCallable


class ParametricHyperSurface(SurfacicDomain):
    r"""Base class for representing a parametric hypersurface.

    .. math::
        \{ y = \text{surface}(t) | t \in D \}
        where D is the parametric domain.

    Args:
        parametric_domain: The parametric domain.
        surface: Mapping from the parametric domain to the domain.
    """

    def __init__(
        self,
        parametric_domain: VolumetricDomain | list[tuple[float, float]] | torch.Tensor,
        surface: Mapping,
    ):
        if isinstance(parametric_domain, list) or isinstance(
            parametric_domain, torch.Tensor
        ):
            nparametric_domain = HypercubeND(parametric_domain)
            super().__init__("hypersurface", nparametric_domain, surface)
        else:
            super().__init__("hypersurface", parametric_domain, surface)
        self.sampler = SurfacicSampler(self)

    def sample(self, n: int) -> tuple[torch.Tensor, torch.Tensor]:
        """Sample points on the hypersurface.

        Args:
            n: the number of points to sample.

        Returns:
            A tuple of tensors, the points and the normals.
        """
        res = self.sampler.sample(n, compute_normals=True)
        return cast(tuple[torch.Tensor, torch.Tensor], res)

    def estimate_bounding_box(
        self, nb_samples: int = 2000, inflation: float = 0.1
    ) -> torch.Tensor:
        """Estimate a bounding box for the parametric curve by sampling points on it.

        Args:
            nb_samples: the number of points to sample.
            inflation: the inflation factor for over-estimation.

        Returns:
            A bounding box of shape (d,2) containing all the points.
        """
        points, _ = self.sample(nb_samples)
        bounding_box = compute_bounding_box(points, inflation)
        return bounding_box

    @staticmethod
    def bean_2d(
        a: int = 3, b: int = 5, theta: float = -torch.pi / 2
    ) -> ParametricHyperSurface:
        """Bean 2D curve.

        Args:
            a: a.
            b: b.
            theta: the rotation angle.

        Returns:
            The Bean 2D as a parametric hypersurface.
        """

        def bean_2d_function(t: torch.Tensor) -> torch.Tensor:
            """The bean 2d function.

            Args:
                t: The argument.

            Returns:
                c(t).
            """
            sin = torch.sin(t)
            cos = torch.cos(t)

            x = (sin**a + cos**b) * cos
            y = (sin**a + cos**b) * sin

            return torch.cat((x, y), dim=-1)

        bean_2d_mapping = Mapping(1, 2, cast(FuncTypeCallable, bean_2d_function))
        bean_2d_mapping = Mapping.compose(bean_2d_mapping, Mapping.rot_2d(theta))
        return ParametricHyperSurface([(0.0, 2 * torch.pi)], bean_2d_mapping)


if __name__ == "__main__":  # pragma: no cover
    from pathlib import Path

    import matplotlib.pyplot as plt

    from scimba_torch.geometry.utils import (
        read_points_normals_from_file,
        write_points_normals_to_file,
    )

    bean_2d = ParametricHyperSurface.bean_2d()

    points, normals = bean_2d.sample(1000)

    # print("points: ", points)
    # print("normals: ", normals)

    points_np = points.cpu().detach().numpy()
    normals_np = normals.cpu().detach().numpy()

    plt.figure(figsize=(7, 7))
    plt.scatter(points_np[:, 0], points_np[:, 1], s=1, label="BC")
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

    filename = "test.xy"
    write_points_normals_to_file(points, normals, filename)

    points2, normals2 = read_points_normals_from_file(filename)

    assert points2.shape == points.shape
    assert normals2.shape == normals.shape
    assert torch.all(points == points2)
    assert torch.all(normals == normals2)

    filepath = Path(filename)
    if filepath.is_file():
        filepath.unlink()

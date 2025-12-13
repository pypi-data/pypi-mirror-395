"""Some utility functions."""

import numpy as np
import torch


def compute_bounding_box(points: torch.Tensor, inflation: float = 0.05) -> torch.Tensor:
    """Compute a bounding box for a vector of points.

    Args:
        points: the vector of points, shape (batch, d).
        inflation: the factor for inflation.

    Returns:
        A bounding box of shape (d,2) containing all the points.

    Raises:
        ValueError: points is not a vector of n points of dim d
    """
    if not (points.ndim == 2):
        raise ValueError(f"first argument must be a tensor (n, d), got {points.shape}")

    if points.shape[1] == 0:
        return torch.tensor([])

    bounding_box = torch.stack(
        (
            torch.min(points, dim=0, keepdim=False)[0],
            torch.max(points, dim=0, keepdim=False)[0],
        ),
        dim=-1,
    )
    # print("bounding_box: ", bounding_box)
    # inflate the bounding box
    maxwidth = torch.max(bounding_box[:, 1] - bounding_box[:, 0])
    inflated_bb = (
        torch.ones_like(
            bounding_box,
            dtype=torch.get_default_dtype(),
            device=torch.get_default_device(),
        )
        * (inflation / 2.0)
        * maxwidth
    )
    inflated_bb[:, 0] = bounding_box[:, 0] - inflated_bb[:, 0]
    inflated_bb[:, 1] = bounding_box[:, 1] + inflated_bb[:, 1]

    return inflated_bb


def write_points_normals_to_file(
    points: np.ndarray | torch.Tensor,
    normals: np.ndarray | torch.Tensor,
    filename: str,
    delimiter: str = " ",
) -> None:
    """Writes the couple of points, normals to a text file.

    Args:
        points: the tensor of points; shape must be [n,d].
        normals: the tensor of normals; shape must be [n,d].
        filename: the file to write to.
        delimiter: the delimiter, default is whitespace.

    Raises:
        ValueError: input tensors does not have appropriated shape.
    """
    if not (
        (points.ndim == 2)
        and (normals.ndim == 2)
        and (points.shape[0] == normals.shape[0])
        and (points.shape[1] == normals.shape[1])
    ):
        raise ValueError(
            "first and second arguments mustbe tensors of the same shape (n,d)"
        )
    with open(filename, "w") as f:
        for i in range(points.shape[0]):
            # Convertir chaque élément en chaîne avec une précision maximale
            linep = delimiter.join(f"{x:.18e}" for x in points[i].tolist())
            linen = delimiter.join(f"{x:.18e}" for x in normals[i].tolist())
            f.write(linep + delimiter + linen + "\n")


def read_points_normals_from_file(
    filename: str,
    delimiter: str = " ",
) -> tuple[torch.Tensor, torch.Tensor]:
    """Reads points and normals from file.

    Args:
        filename: file to read from.
        delimiter: the delimiter, default is whitespace.

    Returns:
        a tuple of points, normals

    Raises:
        ValueError: input file does not have an even number of columns.
    """
    points_normals = np.loadtxt(
        filename, dtype=np.float64, ndmin=2, delimiter=delimiter
    )
    dim = points_normals.shape[1]
    if dim % 2:
        raise ValueError("there must be an even number of columns in input file")
    dim = dim // 2
    points, normals = points_normals[:, :dim], points_normals[:, dim:]
    return (
        torch.tensor(
            points, dtype=torch.get_default_dtype(), device=torch.get_default_device()
        ),
        torch.tensor(
            normals, dtype=torch.get_default_dtype(), device=torch.get_default_device()
        ),
    )

"""The PDE for learning a Regularized Signed Distance Function."""

import torch

from scimba_torch.approximation_space.abstract_space import AbstractApproxSpace
from scimba_torch.physical_models.elliptic_pde.abstract_elliptic_pde import (
    StrongFormEllipticPDE,
)
from scimba_torch.utils.scimba_tensors import LabelTensor, MultiLabelTensor
from scimba_torch.utils.typing_protocols import VarArgCallable


class RegEikonalPDE(StrongFormEllipticPDE):
    """Base class for representing a regularized Eikonal PDE.

    Args:
        space: The approximation space for the problem.
        **kwargs: Additional keyword arguments.
    """

    def __init__(self, space: AbstractApproxSpace, **kwargs):
        super().__init__(space, residual_size=2, bc_residual_size=2, **kwargs)

        def f_rhs(x: LabelTensor, mu: LabelTensor) -> tuple[torch.Tensor, torch.Tensor]:
            x1 = x.get_components()[0]
            return torch.ones_like(x1), torch.zeros_like(x1)

        def f_bc(x: LabelTensor, mu: LabelTensor) -> tuple[torch.Tensor, torch.Tensor]:
            x1 = x.get_components()[0]
            return torch.zeros_like(x1), torch.zeros_like(x1)

        self.f = f_rhs
        self.g = f_bc

    def rhs(
        self, w: MultiLabelTensor, x: LabelTensor, mu: LabelTensor
    ) -> tuple[torch.Tensor, torch.Tensor]:
        r"""Compute the right-hand side (RHS) of the PDE.

        Args:
            w: State tensor.
            x: Spatial coordinates tensor.
            mu: Parameter tensor.

        Returns:
             The source term \( f(x, \mu) \).
        """
        return self.f(x, mu)

    def operator(
        self, w: MultiLabelTensor, x: LabelTensor, mu: LabelTensor
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """Compute the operator of the PDE.

        Args:
            w: State tensor.
            x: Spatial coordinates tensor.
            mu: Parameter tensor.

        Returns:
            The result of applying the operator to the state.
        """
        # # Eikonal equation
        # u = w.get_components()
        # u_x, u_y = self.grad(u, x)
        # old_norm_gradu = u_x**2 + u_y**2  # torch.norm(gradu, dim=0)
        #
        # # Regularization term (penalization of the laplacian)
        # u_xx, _ = self.grad(u_x, x)
        # _, u_yy = self.grad(u_y, x)
        #
        # # return a tuple
        # return old_norm_gradu, u_xx + u_yy

        if x.dim == 1:
            grad_u = self.grad(w, x)
            assert isinstance(grad_u, torch.Tensor)
            # a bit of help for the type-checker
            norm_gradu = grad_u**2
            regularization = self.grad(grad_u[:, 0], x)
            assert isinstance(regularization, torch.Tensor)
            # a bit of help for the type-checker
            return norm_gradu, regularization

        grad_u = torch.concatenate(tuple(self.grad(w, x)), dim=-1)
        norm_gradu = torch.sum(grad_u**2, keepdim=True, dim=-1)

        regularization = tuple(self.grad(grad_u[:, 0], x))[0]
        for i in range(1, grad_u.shape[-1]):
            regularization += tuple(self.grad(grad_u[:, i], x))[i]

        return norm_gradu, regularization

    def functional_operator(
        self,
        func: VarArgCallable,
        x: torch.Tensor,
        mu: torch.Tensor,
        theta: torch.Tensor,
    ) -> torch.Tensor:
        """Apply the functional operator for the differential equation.

        Args:
            func: The callable function to apply.
            x: Spatial coordinates tensor.
            mu: Parameter tensor.
            theta: Theta parameter tensor.

        Returns:
            The result of applying the functional operator.
        """
        # Eikonal equation
        grad_u = torch.func.jacrev(func, 0)
        grad_u_val = grad_u(x, mu, theta)
        # norm_gradu = grad_u_val[..., 0] ** 2 + grad_u_val[..., 1] ** 2
        norm_gradu = torch.sum(grad_u_val**2, dim=-1)
        hessian_u = torch.func.jacrev(grad_u, 0)(x, mu, theta)
        # laplacian = hessian_u[..., 0, 0] + hessian_u[..., 1, 1]
        laplacian = torch.einsum("...ii->...i", hessian_u).sum(dim=-1)

        return torch.concatenate((norm_gradu, laplacian), dim=0)

    def bc_rhs(
        self, w: MultiLabelTensor, x: LabelTensor, n: LabelTensor, mu: LabelTensor
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """Compute the RHS for the boundary conditions.

        Args:
            w: State tensor.
            x: Boundary coordinates tensor.
            n: Normal vector tensor.
            mu: Parameter tensor.

        Returns:
            The boundary condition g(x, μ).
        """
        return self.g(x, mu)

    def bc_operator(
        self, w: MultiLabelTensor, x: LabelTensor, n: LabelTensor, mu: LabelTensor
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """Compute the operator for the boundary conditions.

        Args:
            w: State tensor.
            x: Boundary coordinates tensor.
            n: Normal vector tensor.
            mu: Parameter tensor.

        Returns:
            The boundary operator applied to the state.
        """
        # Dirichlet Condition
        u = w.get_components()
        assert isinstance(u, torch.Tensor)
        # a bit of help for the type-checker

        # Neumann Condition
        if x.dim == 1:
            grad_u = self.grad(w, x)
        else:
            grad_u = torch.concatenate(tuple(self.grad(w, x)), dim=-1)
        n_ = n.x

        dot = torch.einsum("bd,bd->b", grad_u, n_).unsqueeze(-1)

        den = (
            torch.linalg.norm(n_, dim=-1) * torch.linalg.norm(grad_u, dim=-1)
        ).unsqueeze(-1)

        neumann = 1.0 - dot / den  # [:, None]

        # return a tuple
        return u, neumann

    def functional_operator_bc(
        self,
        func: VarArgCallable,
        x: torch.Tensor,
        n: torch.Tensor,
        mu: torch.Tensor,
        theta: torch.Tensor,
    ) -> torch.Tensor:
        """Apply the functional operator for boundary conditions.

        Args:
            func: The callable function to apply.
            x: Spatial coordinates tensor.
            n: Normal vector tensor.
            mu: Parameter tensor.
            theta: Theta parameter tensor.

        Returns:
            The result of applying the functional operator.
        """
        u = func(x, mu, theta)
        grad_u = torch.func.jacrev(func, 0)(x, mu, theta)
        dot = grad_u @ n
        den = torch.linalg.norm(n) * torch.linalg.norm(grad_u)
        neumann = 1.0 - dot / den
        return torch.concatenate((u, neumann), dim=0)

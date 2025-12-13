"""Implement the Neural Semi-Lagrangian scheme."""

import copy
from typing import Callable

import torch

from scimba_torch.numerical_solvers.abstract_projector import AbstractNonlinearProjector
from scimba_torch.numerical_solvers.temporal_pde.time_discrete import (
    ExplicitTimeDiscreteScheme,
)
from scimba_torch.physical_models.temporal_pde.advection_diffusion_equation import (
    AdvectionReactionDiffusion,
)
from scimba_torch.utils.scimba_tensors import LabelTensor


class Characteristic:
    """Class to handle the characteristics of a PDE.

    Args:
        pde: The PDE for which to compute characteristics.
        **kwargs: Additional keyword arguments.
    """

    def __init__(
        self,
        pde: AdvectionReactionDiffusion,
        **kwargs,
    ):
        # set pde
        self.pde = pde

        # set function to determine the exact foot

        self.exact_foot = kwargs.get("exact_foot", None)

        if self.pde.constant_advection:
            self.exact_foot = self.exact_foot_constant_advection

        self.has_exact_foot = self.exact_foot is not None

        # set dimension and boundary condition properties

        domain = pde.space.spatial_domain
        self.dim = domain.dim

        self.periodic = kwargs.get("periodic", False)
        self.flipped_periodic = kwargs.get("flipped_periodic", False)
        self.dirichlet = kwargs.get("dirichlet", None)

        message = (
            "Choose only one type of boundary condition among periodic, "
            "flipped periodic, and dirichlet, or none of them."
        )
        assert (
            self.periodic + self.flipped_periodic + (self.dirichlet is not None) <= 1
        ), message

        if self.periodic or self.flipped_periodic or self.dirichlet:
            if pde.space.type_space == "space":
                lo, up = domain.bounds.T
                if domain.domain_type == "Cylinder3D":
                    self.periodic = "cylinder"
            else:
                domain_x = pde.space.spatial_domain
                lo_x, up_x = domain_x.bounds.T
                domain_v = pde.space.velocity_domain
                lo_v, up_v = domain_v.bounds.T
                lo = torch.cat((lo_x, lo_v))
                up = torch.cat((up_x, up_v))

            self.lower_bound = lo[None, ...]
            self.upper_bound = up[None, ...]
            self.lower_upper = self.lower_bound + self.upper_bound
            self.domain_size = self.upper_bound - self.lower_bound

        if self.dirichlet:
            instance_1 = isinstance(self.dirichlet, Callable)
            instance_2 = isinstance(self.dirichlet, (list, tuple))
            assert instance_1 or instance_2, (
                "Dirichlet boundary condition must be a callable or a list of callables"
            )
            if instance_2:
                assert len(self.dirichlet) == self.dim, (
                    "Dirichlet boundary condition must be a list with one entry "
                    "per dimension (e.g., [[bc_left, bc_right]] for 1D)."
                )
                for d in self.dirichlet:
                    assert isinstance(d, (list, tuple)), (
                        "Each entry of the dirichlet list must be a list or tuple"
                    )
                    assert len(d) == 2, (
                        "Each entry of the dirichlet list must have two elements: "
                        'the "left" and "right" boundary conditions '
                        "(e.g., [[bc_left, bc_right], [bc_bottom, bc_top]] for 2D)."
                    )
                    for d_i in d:
                        assert isinstance(d_i, Callable) or d_i is None, (
                            "Each boundary condition must be a callable or None"
                        )

        # set diffusion information

        kind_diffusion = kwargs.get("kind_diffusion", "directionwise")

        self.diffusion_coefficient = kwargs.get("diffusion_coefficient", 0)

        if self.diffusion_coefficient > 0:
            self.diffusion_directions = self.make_diffusion_directions(kind_diffusion)
            self.diffusion_increment = 2 * self.dim * self.diffusion_coefficient

    def make_diffusion_directions(self, kind: str = "directionwise") -> torch.Tensor:
        """Creates the diffusion directions based on the chosen kind.

        Args:
            kind: The kind of diffusion directions to create (Default: "directionwise").

        Returns:
            The created diffusion directions.
        """
        assert kind in [
            "simplex",
            "directionwise",
            "hypercube",
        ], "Unknown diffusion directions"

        d = self.dim
        e = torch.eye(d, d)
        o = torch.ones(d)

        if kind == "simplex":
            v = torch.zeros((d + 1, d))
            v[:d] = e * (1 + 1 / d) ** 0.5 - o[:, None] * (1 + (d + 1) ** 0.5) / d**1.5
            v[d] = o / d**0.5

        elif kind == "directionwise":
            v = torch.zeros((2 * d, d))
            v[:d] = e
            v[d:] = -e

        elif kind == "hypercube":
            i = torch.arange(2**d)
            bits = (i[:, None] >> torch.arange(d - 1, -1, -1)) & 1
            v = 1 - 2 * bits
            v = v / d**0.5

        return v[:, None, :]

    def ensure_periodicity(self, y: torch.Tensor):
        """Ensures that the points x are within the domain bounds.

        If the points are outside the bounds, they are wrapped around the domain.

        Args:
            y: The points.

        Returns:
            The points within the domain bounds.
        """
        if not self.periodic and not self.flipped_periodic:
            return y

        lb = self.lower_bound
        ub = self.upper_bound
        ds = self.domain_size
        lu = self.lower_upper

        if self.periodic:
            if self.periodic == "cylinder":
                new_y3 = lb[..., 2] + torch.remainder(
                    y[..., 2] - lb[..., 2], ds[..., 2]
                )
                y1, y2 = y[..., 0], y[..., 1]
                return torch.stack((y1, y2, new_y3), dim=-1)
            else:
                return lb + torch.remainder(y - lb, ds)

        elif self.flipped_periodic:
            assert y.shape[-1] == 2, "Flipped periodicity only supported in 2D"
            assert self.diffusion_coefficient == 0, (
                "Flipped periodicity not supported with diffusion"
            )

            y1, y2 = y[0, ...].T
            y1_ = y1.clone()
            y2_ = y2.clone()

            mask = y1_ > ub[0, 0]
            y1_[mask] = y1_[mask] - ds[0, 0]
            y2_[mask] = lu[0, 1] - y2_[mask]

            mask = y1_ < lb[0, 0]
            y1_[mask] = y1_[mask] + ds[0, 0]
            y2_[mask] = lu[0, 1] - y2_[mask]

            mask = y2_ > ub[0, 1]
            y2_[mask] = y2_[mask] - ds[0, 1]
            y1_[mask] = lu[0, 0] - y1_[mask]

            mask = y2_ < lb[0, 1]
            y2_[mask] = y2_[mask] + ds[0, 1]
            y1_[mask] = lu[0, 0] - y1_[mask]

            y = torch.stack([y1_[None, :], y2_[None, :]], dim=-1)

        return y

    def handle_dirichlet(
        self, w: torch.Tensor, x: LabelTensor, mu: LabelTensor, t: float, dt: float
    ) -> torch.Tensor:
        """Handles Dirichlet boundary conditions.

        If the foot of the characteristic curve is outside the domain,
        the Dirichlet boundary condition is applied.

        Args:
            w: The input values at the foot of the characteristic curve.
            x: The points at the foot of the characteristic curve.
            mu: The physical parameters.
            t: The current time.
            dt: The time step.

        Returns:
            The values after applying Dirichlet boundary conditions.
        """
        if not self.dirichlet:
            return w

        if isinstance(self.dirichlet, Callable):
            return self.dirichlet(w, x, mu, t, dt)

        for i_d, d in enumerate(self.dirichlet):
            # left boundary
            if d[0] is not None:
                mask = x.x[:, i_d] < self.lower_bound[0, i_d]
                if torch.any(mask):
                    res = d[0](x[mask], mu[mask], t + dt / 2)
                    w[mask] = res.x if isinstance(res, LabelTensor) else res
            # right boundary
            if d[1] is not None:
                mask = x.x[:, i_d] > self.upper_bound[0, i_d]
                if torch.any(mask):
                    res = d[1](x[mask], mu[mask], t + dt / 2)
                    w[mask] = res.x if isinstance(res, LabelTensor) else res
        return w

    def exact_foot_constant_advection(
        self, t: torch.Tensor, x: torch.Tensor, mu: torch.Tensor, dt: float
    ) -> torch.Tensor:
        """Computes the foot of the (backwards) characteristic curve.

        The curve is originating from point x at time t + dt, towards point y at time t.

        In the case of constant advection, the foot is given by
        y = x - a * dt.

        Args:
            t: The current time.
            x: The current points.
            mu: The physical parameters.
            dt: The time step.

        Returns:
            The foot of the characteristic curve.
        """
        a_ = self.pde.a(t, x, mu)
        return x - a_ * dt

    @staticmethod
    def backwards_ode_integrator(
        f: Callable,
        t: torch.Tensor,
        x: torch.Tensor,
        mu: torch.Tensor,
        dt: float,
        scheme: str = "rk4",
    ) -> torch.Tensor:
        """Computes the solution of the ODE dx/dt = f(t, x, mu) at time t - dt.

        Use a numerical scheme.

        Args:
            f: The function defining the ODE.
            t: The current time.
            x: The current points.
            mu: The physical parameters.
            dt: The time step.
            scheme: The numerical scheme used for integrating the ODE. Default is "rk4".

        Returns:
            The numberical solution at time t - dt.
        """
        assert scheme in ["euler_exp", "rk4"], "Unknown scheme in ODE integrator"

        if scheme == "euler_exp":
            return x - dt * f(t, x, mu)

        elif scheme == "rk4":
            k1 = f(t, x, mu)
            k2 = f(t - dt / 2, x - k1 * dt / 2, mu)
            k3 = f(t - dt / 2, x - k2 * dt / 2, mu)
            k4 = f(t - dt, x - k3 * dt, mu)
            return x - dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

    def numerical_foot(
        self, t: torch.Tensor, x: torch.Tensor, mu: torch.Tensor, dt: float, **kwargs
    ) -> torch.Tensor:
        """Computes the foot of the (backwards) characteristic curve.

        The curve is originating from point x at time t + dt, towards point y at time t.

        In the case of non-constant advection, the foot is computed
        using a numerical scheme, with n_sub_steps sub-steps.

        Args:
            t: The current time.
            x: The current points.
            mu: The physical parameters.
            dt: The time step.
            **kwargs: Additional keyword arguments including:

                - scheme (str): The numerical scheme used for integrating the ODE.
                  Default is "rk4".
                - n_sub_steps (int): The number of sub-steps used for integrating the
                  ODE. Default is 5.

        Returns:
            torch.Tensor: The foot of the characteristic curve.
        """
        scheme = kwargs.get("scheme", "rk4")
        n_sub_steps = kwargs.get("n_sub_steps", 5)

        local_dt = dt / n_sub_steps

        for nt in range(n_sub_steps):
            local_t = t + dt - nt * local_dt
            x = self.backwards_ode_integrator(
                self.pde.a, local_t, x, mu, local_dt, scheme
            )
        return x

    def get_foot(
        self, t: LabelTensor, x: LabelTensor, mu: LabelTensor, dt: float, **kwargs
    ) -> LabelTensor:
        """Computes the foot of the (backwards) characteristic curve.

        The curve is originating from point x at time t + dt, towards point y at time t.

        If an exact foot is provided, it is used.
        Otherwise, a numerical foot is computed.

        Periodic and flipped periodic boundary conditions are supported.

        Args:
            t: The current time.
            x: The current points.
            mu: The physical parameters.
            dt: The time step.
            **kwargs: Additional keyword arguments including:

                - scheme (str): The numerical scheme used for integrating the ODE,
                  in case no exact foot is provided. Default is "rk4".
                - n_sub_steps (int): The number of sub-steps used for integrating the
                  ODE, in case no exact foot is provided. Default is 5.

        Returns:
            The foot of the characteristic curve.
        """
        if self.has_exact_foot:
            y = self.exact_foot(t, x, mu, dt)
        else:
            y = self.numerical_foot(t, x, mu, dt, **kwargs)

        if isinstance(y, LabelTensor):
            y = y.x

        y = y[None, ...]

        if self.diffusion_coefficient > 0:
            # TODO: try to use the Euler-Maruyama method for the advection-diffusion,
            # with sub-time-steps
            coeff = self.diffusion_increment * dt
            v = coeff**0.5 * self.diffusion_directions
            # y has shape (n_points, dim)
            # v has shape (dim + 1, 1, dim)
            y = y + v

        y = self.ensure_periodicity(y)

        # TODO: the labels of y should be x.labels, but shifted in space
        # TODO: handle the labels for the diffusion case (at the moment, x.labels
        # doesn't even have the right shape)
        return y

    def get_foot_kinetic_pde(
        self,
        t: LabelTensor,
        x: LabelTensor,
        v: LabelTensor,
        mu: LabelTensor,
        dt: float,
        **kwargs,
    ) -> LabelTensor:
        """Computes the foot of the (backwards) characteristic curve for a kinetic PDE.

        Use get_foot.

        Args:
            t: The current time.
            x: The current points.
            v: The velocity points.
            mu: The physical parameters.
            dt: The time step.
            **kwargs: Additional keyword arguments including:

                - scheme (str): The numerical scheme used for integrating the ODE,
                  in case no exact foot is provided. Default is "rk4".
                - n_sub_steps (int): The number of sub-steps used for integrating the
                  ODE, in case no exact foot is provided. Default is 5.

        Returns:
            The foot of the characteristic curve.
        """
        dim_x = x.shape[1]
        xv = x.concatenate(v, dim=1)

        foot = self.get_foot(t, xv, mu, dt, **kwargs)

        return foot[..., :dim_x], foot[..., dim_x:]


class NeuralSemiLagrangian(ExplicitTimeDiscreteScheme):
    """Implement the Neural Semi-Lagrangian scheme.

    Args:
        characteristic: The characteristics model.
        projector: The projector for training the model.
        **kwargs: Additional hyperparameters for the scheme.
    """

    def __init__(
        self,
        characteristic: Characteristic,
        projector: AbstractNonlinearProjector,
        **kwargs,
    ):
        super().__init__(characteristic.pde, projector, **kwargs)
        self.characteristic = characteristic
        self.dim = characteristic.dim

    def construct_rhs(
        self, pde_n: AdvectionReactionDiffusion, t: float, dt: float, **kwargs
    ) -> Callable:
        """Constructs the RHS of the Neural Semi-Lagrangian scheme.

        Computes the foot of the characteristic curve originating from point x at time
        t + dt, towards point y at time t.

        Args:
            pde_n: The PDE to solve at the current time step.
            t: The current time.
            dt: The time step.
            **kwargs: Additional keyword arguments including:

                - scheme (str): The numerical scheme used for integrating the ODE,
                  in case no exact foot is provided. Default is "rk4".
                - n_sub_steps (int): The number of sub-steps used for integrating the
                  ODE, in case no exact foot is provided. Default is 5.

        Returns:
            The RHS function for the Neural Semi-Lagrangian scheme.
        """
        assert pde_n.space.type_space in ["space", "phase_space"]

        if pde_n.space.type_space == "space":

            def res(x: LabelTensor, mu: LabelTensor) -> torch.Tensor:
                t_ = torch.ones((x.shape[0], 1)) * t
                y = self.characteristic.get_foot(t_, x, mu, dt, **kwargs)

                u = []
                for yi in y:
                    y_ = LabelTensor(yi)
                    ev = pde_n.space.evaluate(y_, mu).w
                    u.append(self.characteristic.handle_dirichlet(ev, y_, mu, t, dt))
                u_n = torch.stack(u, dim=2).mean(dim=-1)

                return u_n.detach()

        else:

            def res(x: LabelTensor, v: LabelTensor, mu: LabelTensor) -> torch.Tensor:
                t_ = torch.ones((x.shape[0], 1)) * t
                x_foot, v_foot = self.characteristic.get_foot_kinetic_pde(
                    t_, x, v, mu, dt, **kwargs
                )

                u_ = []
                for x_foot_i, v_foot_i in zip(x_foot, v_foot):
                    x_foot_i = LabelTensor(x_foot_i)
                    v_foot_i = LabelTensor(v_foot_i)
                    u_.append(pde_n.space.evaluate(x_foot_i, v_foot_i, mu).w)
                u_n = torch.stack(u_, dim=2).mean(dim=-1)

                return u_n.detach()

        return res

    def update(self, t: float, dt: float, **kwargs):
        """Computes the next time step of the Neural Semi-Lagrangian method.

        Args:
            t: Current time.
            dt: Time step.
            **kwargs: Additional keyword arguments.
        """
        self.projector.best_loss = 1e10
        pde_n = copy.deepcopy(self.pde)

        self.projector.rhs = self.construct_rhs(pde_n, t, dt, **kwargs)
        self.projector.solve(**kwargs)

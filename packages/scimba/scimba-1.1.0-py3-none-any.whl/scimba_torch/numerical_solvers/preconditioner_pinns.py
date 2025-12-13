"""Preconditioners for pinns."""

import warnings
from collections import OrderedDict
from typing import Any, cast

import torch

from scimba_torch.approximation_space.abstract_space import AbstractApproxSpace
from scimba_torch.numerical_solvers.functional_operator import (
    # _is_type_keys,
    TYPE_DICT_OF_VMAPS,
    TYPE_FUNC_ARGS,
    # TYPE_ARGS,
    # TYPE_DICT_OF_FUNC_ARGS,
    FunctionalOperator,
    # vectorize_dict_of_func,
)
from scimba_torch.numerical_solvers.preconditioner_solvers import (
    MatrixPreconditionerSolver,
    _mjactheta,
    # functional_operator_id
    _transpose_i_j,
)
from scimba_torch.physical_models.elliptic_pde.abstract_elliptic_pde import (
    EllipticPDE,
    # StrongForm_EllipticPDE,
)
from scimba_torch.physical_models.elliptic_pde.linear_order_2 import (
    LinearOrder2PDE,
)
from scimba_torch.physical_models.kinetic_pde.abstract_kinetic_pde import KineticPDE
from scimba_torch.physical_models.temporal_pde.abstract_temporal_pde import TemporalPDE

ACCEPTED_PDE_TYPES = EllipticPDE | TemporalPDE | KineticPDE | LinearOrder2PDE


def _element(i: int, func: TYPE_FUNC_ARGS) -> TYPE_FUNC_ARGS:
    """Extract a specific element from the output of a function.

    Args:
        i: Index of the element to extract.
        func: The function whose output element is to be extracted.

    Returns:
        A function that extracts the i-th element from the output of func.
    """
    return lambda *args: func(*args)[i, ...]


class MatrixPreconditionerPinn(MatrixPreconditionerSolver):
    """Matrix-based preconditioner for pinns.

    Args:
        space: The approximation space.
        pde: The PDE to be solved.
        **kwargs: Additional keyword arguments:

            - in_lhs_name: Name of the operator to be used in the left-hand side
              assembly. (default: "functional_operator")
    """

    def __init__(
        self,
        space: AbstractApproxSpace,
        pde: ACCEPTED_PDE_TYPES,
        **kwargs,
    ):
        super().__init__(space, pde, **kwargs)

        in_lhs_name = kwargs.get("in_lhs_name", "functional_operator")

        self.operator = FunctionalOperator(self.pde, in_lhs_name)

        self.Phi = self.operator.apply_func_to_dict_of_func(
            _transpose_i_j(-1, -2, _mjactheta),
            self.operator.apply_to_func(self.eval_func),
        )
        self.vectorized_Phi = self.vectorize_along_physical_variables(self.Phi)

        self.operator_bc: None | FunctionalOperator = None
        self.vectorized_Phi_bc: None | TYPE_DICT_OF_VMAPS = None
        if self.has_bc:
            self.operator_bc = FunctionalOperator(self.pde, "functional_operator_bc")
            self.Phi_bc = self.operator_bc.apply_func_to_dict_of_func(
                _transpose_i_j(-1, -2, _mjactheta),
                self.operator_bc.apply_to_func(self.eval_func),
            )
            self.vectorized_Phi_bc = self.vectorize_along_physical_variables_bc(
                self.Phi_bc
            )

        self.operator_ic: None | FunctionalOperator = None
        self.vectorized_Phi_ic: None | TYPE_DICT_OF_VMAPS = None
        if self.has_ic:
            self.operator_ic = FunctionalOperator(self.pde, "functional_operator_ic")
            self.Phi_ic = self.operator_ic.apply_func_to_dict_of_func(
                _transpose_i_j(-1, -2, _mjactheta),
                self.operator_ic.apply_to_func(self.eval_func),
            )
            self.vectorized_Phi_ic = self.vectorize_along_physical_variables_ic(
                self.Phi_ic
            )


TYPE_LIST_FLOAT_OR_INT = list[float | int]
TYPE_VALUES = float | int | TYPE_LIST_FLOAT_OR_INT
TYPE_DICT_OF_WEIGHTS = OrderedDict[int, TYPE_VALUES]


def _is_type_list_float_or_int(arg: Any):
    """Check if argument has type TYPE_LIST_FLOAT_OR_INT.

    Args:
        arg: argument to be type checked.

    Returns:
        True iff key has type TYPE_LIST_FLOAT_OR_INT
    """
    return isinstance(arg, list) and all(isinstance(el, float | int) for el in arg)


def _is_type_value(arg: Any):
    """Check if argument has type TYPE_VALUES.

    Args:
        arg: argument to be type checked.

    Returns:
        True iff key has type TYPE_VALUES
    """
    return (
        isinstance(arg, int)
        or isinstance(arg, float)
        or _is_type_list_float_or_int(arg)
    )


def _is_type_dict_of_weight(weight: Any):
    """Check if argument has type TYPE_DICT_OF_WEIGHTS.

    Args:
        weight: argument to be type checked.

    Returns:
        True iff key has type TYPE_DICT_OF_WEIGHTS
    """
    return (
        isinstance(weight, OrderedDict)
        and all(isinstance(key, int) for key in weight)
        and all(_is_type_value(weight[key]) for key in weight)
    )


def _check_and_format_weight_argument(
    weight: Any, keys: list[int]
) -> OrderedDict[int, torch.Tensor]:
    """Format weight argument.

    Args:
        weight: the weight argument.
        keys: the keys (flatten) of coresponding functional operator.

    Returns:
        the formatted weight argument.

    Raises:
        KeyError: the weight argument has incorrect keys
        TypeError: the weight argument has incorrect type
    """
    if isinstance(weight, float | int):
        res = OrderedDict(
            [
                (
                    key,
                    torch.sqrt(torch.tensor([weight], dtype=torch.get_default_dtype())),
                )
                for key in keys
            ]
        )
    elif isinstance(weight, list) and all(
        isinstance(wk, float) or isinstance(wk, int) for wk in weight
    ):
        res = OrderedDict(
            [
                (key, torch.sqrt(torch.tensor(weight, dtype=torch.get_default_dtype())))
                for key in keys
            ]
        )
    elif _is_type_dict_of_weight(weight):
        keys_w = [key for key in weight]
        keys_equal = all(k in keys for k in keys_w) and all(k in keys_w for k in keys)
        if not keys_equal:
            raise KeyError("weight dict must have keys {keys}")
        res = OrderedDict()
        for key in weight:
            if isinstance(weight[key], float):
                res[key] = torch.sqrt(
                    torch.tensor([weight[key]], dtype=torch.get_default_dtype())
                )
            elif isinstance(weight[key], list):
                res[key] = torch.sqrt(
                    torch.tensor(weight[key], dtype=torch.get_default_dtype())
                )
    else:
        raise TypeError(
            "weight argument must be of type float,"
            "list[float], or OrderedDict[int, float | list[float]]"
        )

    return res


class EnergyNaturalGradientPreconditioner(MatrixPreconditionerPinn):
    """Energy-based natural gradient preconditioner.

    Args:
        space: The approximation space.
        pde: The PDE to be solved, which can be an instance of EllipticPDE,
            TemporalPDE, KineticPDE, or LinearOrder2PDE.
        **kwargs: Additional keyword arguments:

            - matrix_regularization: Regularization parameter for the preconditioning
              matrix (default: 1e-6).
    """

    def __init__(
        self,
        space: AbstractApproxSpace,
        pde: ACCEPTED_PDE_TYPES,
        **kwargs,
    ):
        super().__init__(space, pde, **kwargs)
        self.matrix_regularization = kwargs.get("matrix_regularization", 1e-6)

        self.in_weights = _check_and_format_weight_argument(
            self.in_weights, self.operator.flatten_keys
        )
        if self.has_bc:
            assert isinstance(self.operator_bc, FunctionalOperator)  # for type checking
            self.bc_weights = _check_and_format_weight_argument(
                self.bc_weights, self.operator_bc.flatten_keys
            )
            # print(self.bc_weights)
        if self.has_ic:
            assert isinstance(self.operator_ic, FunctionalOperator)  # for type checking
            self.ic_weights = _check_and_format_weight_argument(
                self.ic_weights, self.operator_ic.flatten_keys
            )

    def compute_preconditioning_matrix(
        self, labels: torch.Tensor, *args: torch.Tensor, **kwargs
    ) -> torch.Tensor:
        """Compute the preconditioning matrix using the main operator.

        Args:
            labels: The labels tensor.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            The preconditioning matrix.
        """
        N = args[0].shape[0]
        theta = self.get_formatted_current_theta()

        Phi = self.operator.apply_dict_of_vmap_to_label_tensors(
            self.vectorized_Phi, theta, labels, *args
        )

        if len(self.in_weights) == 1:  # apply the same weights to all labels
            for key in self.in_weights:  # dummy loop
                Phi[:, :, :] *= self.in_weights[key]
        else:  # apply weights for each labels
            for key in self.in_weights:
                Phi[labels == key, :, :] *= self.in_weights[key]

        M = torch.einsum("ijk,ilk->jl", Phi, Phi) / N
        M += self.matrix_regularization * torch.eye(self.ndof)

        return self.in_weight * M

    def compute_preconditioning_matrix_bc(
        self, labels: torch.Tensor, *args: torch.Tensor, **kwargs
    ) -> torch.Tensor:
        """Compute the boundary condition preconditioning matrix.

        Args:
            labels: The labels tensor.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            The boundary condition preconditioning matrix.
        """
        N = args[0].shape[0]
        theta = self.get_formatted_current_theta()

        self.operator_bc = cast(FunctionalOperator, self.operator_bc)
        self.vectorized_Phi_bc = cast(TYPE_DICT_OF_VMAPS, self.vectorized_Phi_bc)

        Phi = self.operator_bc.apply_dict_of_vmap_to_label_tensors(
            self.vectorized_Phi_bc, theta, labels, *args
        )

        if len(self.bc_weights) == 1:  # apply the same weights to all labels
            for key in self.bc_weights:  # dummy loop
                Phi[:, :, :] *= self.bc_weights[key]
        else:  # apply weights for each labels
            for key in self.bc_weights:
                Phi[labels == key, :, :] *= self.bc_weights[key]

        M = torch.einsum("ijk,ilk->jl", Phi, Phi) / N
        M += self.matrix_regularization * torch.eye(self.ndof)

        return self.bc_weight * M

    def compute_preconditioning_matrix_ic(
        self, labels: torch.Tensor, *args: torch.Tensor, **kwargs
    ) -> torch.Tensor:
        """Compute the initial condition preconditioning matrix.

        Args:
            labels: The labels tensor.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            The initial condition preconditioning matrix.
        """
        N = args[0].shape[0]
        theta = self.get_formatted_current_theta()

        self.operator_ic = cast(FunctionalOperator, self.operator_ic)
        self.vectorized_Phi_ic = cast(TYPE_DICT_OF_VMAPS, self.vectorized_Phi_ic)

        Phi = self.operator_ic.apply_dict_of_vmap_to_label_tensors(
            self.vectorized_Phi_ic, theta, labels, *args
        )

        if len(self.ic_weights) == 1:  # apply the same weights to all labels
            for key in self.ic_weights:  # dummy loop
                Phi[:, :, :] *= self.ic_weights[key]
        else:  # apply weights for each labels
            for key in self.ic_weights:
                Phi[labels == key, :, :] *= self.ic_weights[key]

        M = torch.einsum("ijk,ilk->jl", Phi, Phi) / N
        M += self.matrix_regularization * torch.eye(self.ndof)

        return self.ic_weight * M

    def compute_full_preconditioning_matrix(
        self, data: tuple | dict, **kwargs
    ) -> torch.Tensor:
        """Compute the full preconditioning matrix.

        Include contributions from the main operator, boundary conditions, and initial
        conditions.

        Args:
            data: Input data, either as a tuple or a dictionary.
            **kwargs: Additional keyword arguments.

        Returns:
            The full preconditioning matrix.
        """
        M = self.get_preconditioning_matrix(data, **kwargs)

        if self.has_bc:
            M += self.get_preconditioning_matrix_bc(data, **kwargs)

        if self.has_ic:
            M += self.get_preconditioning_matrix_ic(data, **kwargs)

        return M

    def __call__(
        self,
        epoch: int,
        data: tuple | dict,
        grads: torch.Tensor,
        res_l: tuple,
        res_r: tuple,
        **kwargs,
    ) -> torch.Tensor:
        """Apply the preconditioner to the input gradients.

        Args:
            epoch: Current training epoch.
            data: Input data, either as a tuple or a dictionary.
            grads: Gradient tensor to be preconditioned.
            res_l: Left residuals.
            res_r: Right residuals.
            **kwargs: Additional keyword arguments.

        Returns:
            The preconditioned gradient tensor.
        """
        M = self.compute_full_preconditioning_matrix(data, **kwargs)
        preconditioned_grads = torch.linalg.lstsq(M, grads).solution
        return preconditioned_grads


def _get_residual_size(pde: Any, bc: bool = False) -> int:
    """Utility function to get residual size.

    Args:
        pde: the pde.
        bc: get bc_residual_size instead of residual_size.

    Returns:
        bc_residual_size instead or residual_size.

    Raises:
        AttributeError: If the `residual_size`, `bc_residual_size`, or
            `ic_residual_size` attributes are not integers.
    """
    name = "bc_residual_size" if bc else "residual_size"

    warning_message = (
        "input pde or pde.space_component does not have a %s attribute; 1 used instead"
    ) % name
    error_message = (
        "attribute %s of input pde or pde.space_component must be an integer"
    ) % name

    res = 1

    if hasattr(pde, name):
        assert hasattr(pde, name)
        if not isinstance(getattr(pde, name), int):
            raise AttributeError(error_message)
        else:
            res = getattr(pde, name)
    elif hasattr(pde, "space_component"):
        assert hasattr(pde, "space_component")
        if hasattr(pde.space_component, name):
            assert hasattr(pde.space_component, name)
            if not isinstance(getattr(pde.space_component, name), int):
                raise AttributeError(error_message)
            else:
                res = getattr(pde.space_component, name)
        else:
            warnings.warn(warning_message, UserWarning)
    else:
        warnings.warn(warning_message, UserWarning)

    return res


def _get_ic_residual_size(pde: Any) -> int:
    """Utility function to get ic residual size.

    Args:
        pde: the pde.

    Returns:
        ic_residual_size

    Raises:
        AttributeError: If the `residual_size`, `bc_residual_size`, or
            `ic_residual_size` attributes are not integers.
    """
    name = "ic_residual_size"

    warning_message = ("input pde does not have a %s attribute; 1 used instead") % name
    error_message = ("attribute %s of input pde must be an integer") % name

    res = 1

    if hasattr(pde, name):
        assert hasattr(pde, name)
        if not isinstance(getattr(pde, name), int):
            raise AttributeError(error_message)
        else:
            res = getattr(pde, name)
    else:
        warnings.warn(warning_message, UserWarning)

    return res


class AnagramPreconditioner(MatrixPreconditionerPinn):
    """Anagram preconditioner.

    This preconditioner is based on the anagram method, which aims to improve
    convergence by transforming the problem into a more favorable form.

    Args:
        space: The approximation space.
        pde: The PDE to be solved, which can be an instance of EllipticPDE,
            TemporalPDE, KineticPDE, or LinearOrder2PDE.
        **kwargs: Additional keyword arguments:

            - `svd_threshold` (:code:`float`): Threshold for singular value
              decomposition (default: 1e-6).
            - `bc_weight` (:code:`float`): Weight for boundary condition contributions
              (default: 1.0).
            - `ic_weight` (:code:`float`): Weight for initial condition contributions
              (default: 1.0).
    """

    def __init__(
        self,
        space: AbstractApproxSpace,
        pde: ACCEPTED_PDE_TYPES,
        **kwargs,
    ):
        super().__init__(space, pde, **kwargs)
        self.svd_threshold = kwargs.get("svd_threshold", 1e-6)

        # if self.space.nb_unknowns > 1:
        #     raise ValueError(
        #         "Anagram preconditioner is only implemented for scalar problems."
        #     )

        self.residual_size: int = _get_residual_size(pde)
        self.bc_residual_size: int = 1
        self.ic_residual_size: int = 1

        if self.has_bc:
            self.bc_residual_size = _get_residual_size(pde, bc=True)

        if self.has_ic:
            self.ic_residual_size = _get_ic_residual_size(pde)

    def compute_preconditioning_matrix(
        self, labels: torch.Tensor, *args: torch.Tensor, **kwargs
    ) -> torch.Tensor:
        """Compute the preconditioning matrix using the main operator.

        Args:
            labels: The labels tensor.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            The preconditioning matrix.
        """
        theta = self.get_formatted_current_theta()
        return self.operator.apply_dict_of_vmap_to_label_tensors(
            self.vectorized_Phi, theta, labels, *args
        ).squeeze()

    def compute_preconditioning_matrix_bc(
        self, labels: torch.Tensor, *args: torch.Tensor, **kwargs
    ) -> torch.Tensor:
        """Compute the boundary condition preconditioning matrix.

        Args:
            labels: The labels tensor.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            The boundary condition preconditioning matrix.
        """
        theta = self.get_formatted_current_theta()

        self.operator_bc = cast(FunctionalOperator, self.operator_bc)
        self.vectorized_Phi_bc = cast(TYPE_DICT_OF_VMAPS, self.vectorized_Phi_bc)

        return self.operator_bc.apply_dict_of_vmap_to_label_tensors(
            self.vectorized_Phi_bc, theta, labels, *args
        ).squeeze()

    def compute_preconditioning_matrix_ic(
        self, labels: torch.Tensor, *args: torch.Tensor, **kwargs
    ) -> torch.Tensor:
        """Compute the initial condition preconditioning matrix.

        Args:
            labels: The labels tensor.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            The initial condition preconditioning matrix.
        """
        theta = self.get_formatted_current_theta()

        self.operator_ic = cast(FunctionalOperator, self.operator_ic)
        self.vectorized_Phi_ic = cast(TYPE_DICT_OF_VMAPS, self.vectorized_Phi_ic)

        return self.operator_ic.apply_dict_of_vmap_to_label_tensors(
            self.vectorized_Phi_ic, theta, labels, *args
        ).squeeze()

    def assemble_right_member(
        self, data: tuple | dict, res_l: tuple, res_r: tuple
    ) -> torch.Tensor:
        """Assemble the right-hand side of the equation.

        Args:
            data: Input data, either as a tuple or a dictionary.
            res_l: Left residuals.
            res_r: Right residuals.

        Returns:
            The assembled right-hand side tensor.
        """
        in_tup = tuple(left - right for left, right in zip(res_l, res_r))

        if len(self.operator.dict_of_operators) == 1:
            return torch.cat(in_tup, dim=0)

        # concatenate components:
        nb_comp_per_label = self.residual_size // len(self.operator.flatten_keys)
        # print("nb_comp_per_label: ", nb_comp_per_label)
        in_tup = tuple(
            tuple((in_tup[i + j]) for i in range(0, len(in_tup), nb_comp_per_label))
            for j in range(nb_comp_per_label)
        )

        args = self.get_args_for_operator(data)

        out_tup = tuple(
            # self.operator.cat_tuple_of_tensors(res, args[0], args[1])
            self.operator.cat_tuple_of_tensors_along_flatten_keys(res, args[0], args[1])
            for res in in_tup
        )

        return torch.cat(out_tup, dim=0)

    def assemble_right_member_bc(
        self, data: tuple | dict, res_l: tuple, res_r: tuple
    ) -> torch.Tensor:
        """Assemble the right-hand side for boundary conditions.

        Args:
            data: Input data, either as a tuple or a dictionary.
            res_l: Left residuals.
            res_r: Right residuals.

        Returns:
            The assembled right-hand side tensor for boundary conditions.
        """
        self.operator_bc = cast(FunctionalOperator, self.operator_bc)

        in_tup = tuple(left - right for left, right in zip(res_l, res_r))

        if len(self.operator_bc.dict_of_operators) == 1:
            return torch.cat(in_tup, dim=0)

        # concatenate components:
        nb_comp_per_label = self.bc_residual_size // len(self.operator_bc.flatten_keys)
        # print("nb_comp_per_label: ", nb_comp_per_label)
        in_tup = tuple(
            tuple((in_tup[i + j]) for i in range(0, len(in_tup), nb_comp_per_label))
            for j in range(nb_comp_per_label)
        )
        # print("len(in_tup): ", len(in_tup))
        # print("len(in_tup[0]): ", len(in_tup[0]))

        args = self.get_args_for_operator_bc(data)

        out_tup = tuple(
            # self.operator_bc.cat_tuple_of_tensors(res, args[0], args[1])
            self.operator_bc.cat_tuple_of_tensors_along_flatten_keys(
                res, args[0], args[1]
            )
            for res in in_tup
        )

        return torch.cat(out_tup, dim=0)

    def assemble_right_member_ic(
        self, data: tuple | dict, res_l: tuple, res_r: tuple
    ) -> torch.Tensor:
        """Assemble the right-hand side for initial conditions.

        Args:
            data: Input data, either as a tuple or a dictionary.
            res_l: Left residuals.
            res_r: Right residuals.

        Returns:
            The assembled right-hand side tensor for initial conditions.
        """
        self.operator_ic = cast(FunctionalOperator, self.operator_ic)

        in_tup = tuple(left - right for left, right in zip(res_l, res_r))

        if len(self.operator_ic.dict_of_operators) == 1:
            return torch.cat(in_tup, dim=0)

        # concatenate components:
        nb_comp_per_label = self.ic_residual_size // len(self.operator_ic.flatten_keys)
        # print("nb_comp_per_label: ", nb_comp_per_label)
        in_tup = tuple(
            tuple((in_tup[i + j]) for i in range(0, len(in_tup), nb_comp_per_label))
            for j in range(nb_comp_per_label)
        )

        args = self.get_args_for_operator_ic(data)

        out_tup = tuple(
            # self.operator_ic.cat_tuple_of_tensors(res, args[0], args[1])
            self.operator_ic.cat_tuple_of_tensors_along_flatten_keys(
                res, args[0], args[1]
            )
            for res in in_tup
        )

        return torch.cat(out_tup, dim=0)

    def __call__(
        self,
        epoch: int,
        data: tuple | dict,
        grads: torch.Tensor,
        res_l: tuple,
        res_r: tuple,
        **kwargs,
    ) -> torch.Tensor:
        """Apply the Anagram preconditioner to the input gradients.

        Args:
            epoch: Current training epoch.
            data: Input data, either as a tuple or a dictionary.
            grads: Gradient tensor to be preconditioned.
            res_l: Left residuals.
            res_r: Right residuals.
            **kwargs: Additional keyword arguments.

        Returns:
            The preconditioned gradient tensor.
        """
        phi = self.get_preconditioning_matrix(data, **kwargs)
        # print("phi.shape: ", phi.shape)
        if phi.ndim > 2:
            phi = torch.cat(
                tuple(phi[:, :, i, ...] for i in range(phi.shape[2])), dim=0
            )
        # print("phi.shape: ", phi.shape)
        if self.has_bc:
            phib = self.get_preconditioning_matrix_bc(data, **kwargs)
            # print("phib.shape: ", phib.shape)
            if phib.ndim > 2:
                phib = torch.cat(
                    tuple(phib[:, :, i, ...] for i in range(phib.shape[2])), dim=0
                )
            # print("phib.shape: ", phib.shape)
            phi = torch.cat((phi, phib), dim=0)
            # print("phi.shape: ", phi.shape)
        if self.has_ic:
            phii = self.get_preconditioning_matrix_ic(data, **kwargs)
            # print("phii.shape: ", phii.shape)
            if phii.ndim > 2:
                phii = torch.cat(
                    tuple(phii[:, :, i, ...] for i in range(phii.shape[2])), dim=0
                )
            # print("phii.shape: ", phi.shape)
            phi = torch.cat((phi, phii), dim=0)

        # ### compute pseudo inverse via svd
        U, Delta, Vt = torch.linalg.svd(
            phi,
            full_matrices=False,
        )
        mask = Delta > self.svd_threshold  # Keep only values greater than...
        # print(
        #     "nb sv : %d, kept: %d, max: %.2e, threshold: %.2e, relative: %.2e"
        #     % (
        #         Delta.shape[0],
        #         torch.sum(mask),
        #         torch.max(Delta).item(),
        #         self.svd_threshold,
        #         torch.max(Delta).item() * self.svd_threshold,
        #     )
        # )
        Delta_inv = torch.zeros_like(Delta)
        Delta_inv[mask] = 1.0 / Delta[mask]
        phi_plus = Vt.T @ torch.diag(Delta_inv) @ U.T  # correct
        #
        nextindex = 0
        begin = nextindex
        # length = len(self.operator.dict_of_operators)
        length = self.residual_size
        end = nextindex + length
        res = self.assemble_right_member(data, res_l[begin:end], res_r[begin:end])
        nextindex += length

        # print("res.shape: ", res.shape)

        if self.has_bc:
            self.operator_bc = cast(FunctionalOperator, self.operator_bc)
            begin = nextindex
            # length = len(self.operator_bc.dict_of_operators)
            length = self.bc_residual_size
            end = nextindex + length
            resb = self.assemble_right_member_bc(
                data, res_l[begin:end], res_r[begin:end]
            )
            # print("resb.shape: ", resb.shape)
            res = torch.cat((res, resb), dim=0)
            # print("res.shape: ", res.shape)
            nextindex += length
        if self.has_ic:
            self.operator_ic = cast(FunctionalOperator, self.operator_ic)
            begin = nextindex
            # length = len(self.operator_ic.dict_of_operators)
            length = self.ic_residual_size
            end = nextindex + length
            resi = self.assemble_right_member_ic(
                data, res_l[begin:end], res_r[begin:end]
            )
            res = torch.cat((res, resi), dim=0)
            nextindex += length

        preconditioned_grads = phi_plus @ res
        #
        return preconditioned_grads

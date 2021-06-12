
from e2cnn.diffops.steerable_basis import SteerableDiffopBasis
from e2cnn.diffops.irreps_basis import *
from e2cnn.diffops.basis import DiffopBasis, LaplaceProfile, TensorBasis

from e2cnn.group import *

from typing import List, Union

__all__ = [
    "kernels_SO2_act_R2",
    # "kernels_O2_act_R2",
    "kernels_CN_act_R2",
    "kernels_DN_act_R2",
    "kernels_Flip_act_R2",
    # "kernels_Trivial_act_R2",
]


def kernels_Flip_act_R2(in_repr: Representation, out_repr: Representation,
                        max_power: int,
                        axis: float = np.pi / 2,
                        max_frequency: int = None,
                        max_offset: int = None) -> DiffopBasis:
    r"""

    Builds a basis for convolutional kernels equivariant to reflections.
    ``in_repr`` and ``out_repr`` need to be :class:`~e2cnn.group.Representation` s of :class:`~e2cnn.group.CyclicGroup`
    with ``N=2``.

    Because the equivariance constraints allow any choice of radial profile, we use a
    :class:`~e2cnn.kernels.GaussianRadialProfile`.
    ``radii`` specifies the radial distances at which the rings are centered while ``sigma`` contains the width of each
    of these rings (see :class:`~e2cnn.kernels.GaussianRadialProfile`).

    The parameter ``axis`` is the angle in radians (with respect to the horizontal axis, rotating counter-clockwise)
    which defines the reflection axis.

    The analytical angular solutions of kernel constraints belong to an infinite dimensional space and so can be
    expressed in terms of infinitely many basis elements. Only a finite subset can however be implemented.
    ``max_frequency`` and ``max_offset`` defines two ways to do so and therefore it is necessary to specify one of them.
    See :func:`~e2cnn.kernels.kernels_CN_act_R2` for more details.
    
    .. todo ::
        remove ``max_offset`` as it is equivalent to ``max_frequency`` here


    Args:
        in_repr (Representation): the representation specifying the transformation of the input feature field
        out_repr (Representation): the representation specifying the transformation of the output feature field
        radii (list): radii of the rings defining the basis for the radial profile
        sigma (list or float): widths of the rings defining the basis for the radial profile
        axis (float): angle defining the reflection axis
        max_frequency (int): maximum frequency of the basis
        max_offset (int): maximum offset in the frequencies of the basis

    """
    assert in_repr.group == out_repr.group
    group = in_repr.group
    assert isinstance(group, CyclicGroup) and group.order() == 2

    angular_basis = SteerableDiffopBasis(R2FlipsSolution, in_repr, out_repr,
                                         axis=axis,
                                         max_frequency=max_frequency,
                                         max_offset=max_offset)

    radial_profile = LaplaceProfile(max_power)
    
    return TensorBasis(radial_profile, angular_basis)


def kernels_SO2_act_R2(in_repr: Representation, out_repr: Representation,
                       max_power: int
                       ) -> DiffopBasis:
    r"""

    Builds a basis for differential operators equivariant to continuous rotations, modeled by the
    group :math:`SO(2)`.
    ``in_repr`` and ``out_repr`` need to be :class:`~e2cnn.group.Representation` s of :class:`~e2cnn.group.SO2`.
    
    Because the equivariance constraints allow any choice of radial profile, we use a
    :class:`~e2cnn.diffops.LaplaceProfile`, which is the most general choice.
    ``max_power`` specifies the maximum power of the Laplacian. The maximum order of differential
    operators in the basis will be two times ``max_power`` plus the maximum order of the angular basis.

    Args:
        in_repr (Representation): the representation specifying the transformation of the input feature field
        out_repr (Representation): the representation specifying the transformation of the output feature field
        max_power (int): maximum power of the Laplacian for the radial profile

    """
    assert in_repr.group == out_repr.group

    group = in_repr.group

    assert isinstance(group, SO2)
    
    angular_basis = SteerableDiffopBasis(R2ContinuousRotationsSolution, in_repr, out_repr)

    radial_profile = LaplaceProfile(max_power)
    
    return TensorBasis(radial_profile, angular_basis)


def kernels_CN_act_R2(in_repr: Representation, out_repr: Representation,
                    max_power: int,
                    max_frequency: int = None,
                    max_offset: int = None,
                    ) -> DiffopBasis:
    r"""

    Builds a basis for convolutional kernels equivariant to :math:`N` discrete rotations, modeled by
    the group :math:`C_N`.
    ``in_repr`` and ``out_repr`` need to be :class:`~e2cnn.group.Representation` s of :class:`~e2cnn.group.CyclicGroup`.

    Because the equivariance constraints allow any choice of radial profile, we use a
    :class:`~e2cnn.diffops.LaplaceProfile`, which is the most general choice.
    ``max_power`` specifies the maximum power of the Laplacian. The maximum order of differential
    operators in the basis will be two times ``max_power`` plus the maximum order of the angular basis.

    The analytical angular solutions of kernel constraints belong to an infinite dimensional space and so can be
    expressed in terms of infinitely many basis elements, each associated with one unique frequency. Because the kernels
    are then sampled on a finite number of points (e.g. the cells of a grid), only low-frequency solutions needs to be
    considered. This enables us to build a finite dimensional basis containing only a finite subset of all analytical
    solutions. ``max_frequency`` is an integer controlling the highest frequency sampled in the basis.

    Frequencies also appear in a basis with a period of :math:`N`, i.e. if the basis contains an element with frequency
    :math:`k`, then it also contains an element with frequency :math:`k + N`.
    In the analytical solutions shown in Table 11 `here <https://arxiv.org/abs/1911.08251>`_, each solution has a
    parameter :math:`t` or :math:`\hat{t}`.
    ``max_offset`` defines the maximum absolute value of these two numbers.

    Either ``max_frequency`` or ``max_offset`` must be specified.


    Args:
        in_repr (Representation): the representation specifying the transformation of the input feature field
        out_repr (Representation): the representation specifying the transformation of the output feature field
        max_power (int): maximum power of the Laplacian for the radial profile
        max_frequency (int): maximum frequency of the basis
        max_offset (int): maximum offset in the frequencies of the basis

    """

    assert in_repr.group == out_repr.group

    group = in_repr.group

    assert isinstance(group, CyclicGroup)

    angular_basis = SteerableDiffopBasis(R2DiscreteRotationsSolution, in_repr, out_repr,
                                         max_frequency=max_frequency,
                                         max_offset=max_offset)

    radial_profile = LaplaceProfile(max_power)

    return TensorBasis(radial_profile, angular_basis)


def kernels_DN_act_R2(in_repr: Representation, out_repr: Representation,
                      max_power: int,
                      axis: float = np.pi/2,
                      max_frequency: int = None, max_offset: int = None) -> DiffopBasis:
    r"""

    Builds a basis for convolutional kernels equivariant to reflections and :math:`N` discrete rotations,
    modeled by the group :math:`D_N`.
    ``in_repr`` and ``out_repr`` need to be :class:`~e2cnn.group.Representation` s
    of :class:`~e2cnn.group.DihedralGroup`.

    Because the equivariance constraints allow any choice of radial profile, we use a
    :class:`~e2cnn.diffops.LaplaceProfile`, which is the most general choice.
    ``max_power`` specifies the maximum power of the Laplacian. The maximum order of differential
    operators in the basis will be two times ``max_power`` plus the maximum order of the angular basis.
    
    The parameter ``axis`` is the angle in radians (with respect to the horizontal axis, rotating counter-clockwise)
    which defines the reflection axis for the reflection element of the group.

    Frequencies also appear in a basis with a period of :math:`N`, i.e. if the basis contains an element with frequency
    :math:`k`, then it also contains an element with frequency :math:`k + N`.
    In the analytical solutions shown in Table 12 `here <https://arxiv.org/abs/1911.08251>`_, each solution has a
    parameter :math:`t` or :math:`\hat{t}`.
    ``max_offset`` defines the maximum absolute value of these two numbers.
    
    Either ``max_frequency`` or ``max_offset`` must be specified.
    

    Args:
        in_repr (Representation): the representation specifying the transformation of the input feature field
        out_repr (Representation): the representation specifying the transformation of the output feature field
        max_power (int): maximum power of the Laplacian for the radial profile
        max_frequency (int): maximum frequency of the basis
        max_offset (int): maximum offset in the frequencies of the basis
        axis (float): angle defining the reflection axis


    """
    assert in_repr.group == out_repr.group
    
    group = in_repr.group

    assert isinstance(group, DihedralGroup)
    
    angular_basis = SteerableDiffopBasis(R2FlipsDiscreteRotationsSolution, in_repr, out_repr,
                                         axis=axis,
                                         max_frequency=max_frequency,
                                         max_offset=max_offset)

    radial_profile = LaplaceProfile(max_power)

    return TensorBasis(radial_profile, angular_basis)

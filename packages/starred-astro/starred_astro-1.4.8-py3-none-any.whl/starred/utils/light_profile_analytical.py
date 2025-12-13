# Utility methods for Sersic profiles
#
# Adapted from Herculens

import jax.numpy as jnp
from jax import lax

smoothing = 0.00001


def sersic_ellipse(x, y, R_sersic, n_sersic, e1, e2, center_x, center_y, amp, max_R_frac=100.0):
    """

    :param x:
    :param y:
    :param amp: surface brightness/amplitude value at the half light radius
    :param R_sersic: semi-major axis half light radius, in pixel
    :param n_sersic: Sersic index
    :param e1: eccentricity parameter
    :param e2: eccentricity parameter
    :param center_x: center in x-coordinate
    :param center_y: center in y-coordinate
    :param max_R_frac: truncation radius, in units of R_sersic (float)
    :return: Sersic profile value at (x, y)
    """

    R_sersic = jnp.maximum(0, R_sersic)
    phi_G, q = ellipticity2phi_q(e1, e2)
    center_x = lax.cond(center_x % 1. == 0.5, lambda x: x + 1e-4, lambda x: x, operand=center_x)
    center_y = lax.cond(center_y % 1. == 0.5, lambda x: x + 1e-4, lambda x: x,
                        operand=center_y)  # this is to avoid cancelling gradient if the sersic is exactly placed on the center of a pixel
    R = get_distance_from_center(x, y, phi_G, q, center_x, center_y)
    result = r_sersic(R, R_sersic, n_sersic, max_R_frac)
    return amp * result


def get_distance_from_center(x, y, phi_G, q, center_x, center_y):
    """
    Get the distance from the center of Sersic, accounting for orientation and axis ratio
    :param x:
    :param y:
    :param phi_G: orientation angle in rad
    :param q: axis ratio
    :param center_x: center x of sersic
    :param center_y: center y of sersic
    """
    x_shift = x - center_x
    y_shift = y - center_y
    cos_phi = jnp.cos(phi_G)
    sin_phi = jnp.sin(phi_G)
    xt1 = cos_phi * x_shift + sin_phi * y_shift
    xt2 = -sin_phi * x_shift + cos_phi * y_shift
    xt2difq2 = xt2 / (q * q)
    R = jnp.sqrt(xt1 * xt1 + xt2 * xt2difq2)
    return R


def R_stable(R):
    """
    Floor R_ at self._smoothing for numerical stability
    :param R: radius
    :return: smoothed and stabilized radius
    """
    return jnp.maximum(smoothing, R)


def r_sersic(R, R_sersic, n_sersic, max_R_frac=100.0):
    """

    :param R: radius (array or float)
    :param R_sersic: Sersic radius (half-light radius)
    :param n_sersic: Sersic index (float)
    :param max_R_frac: maximum window outside of which the mass is zeroed, in units of R_sersic (float)
    :return: kernel of the Sersic surface brightness at R
    """
    # Must avoid item assignment on JAX arrays
    R_ = R_stable(R)
    R_sersic_ = R_stable(R_sersic)
    bn = b_n(n_sersic)
    R_frac = R_ / R_sersic_
    good_inds = (jnp.asarray(R_frac) <= max_R_frac).astype(int)
    result = good_inds * jnp.exp(-bn * (R_frac ** (1. / n_sersic) - 1.))
    return jnp.nan_to_num(result)


def b_n(n):
    """
    b(n) computation. This is the approximation of the exact solution to the relation, 2*incomplete_gamma_function(2n; b_n) = Gamma_function(2*n).
    :param n: the sersic index
    :return:
    """
    bn = 1.9992 * n - 0.3271
    return bn


def phi_q2_ellipticity(phi, q):
    """
    transforms orientation angle and axis ratio into complex ellipticity moduli e1, e2

    :param phi: angle of orientation (in radian)
    :param q: axis ratio minor axis / major axis
    :return: eccentricities e1 and e2 in complex ellipticity moduli
    """
    e1 = (1. - q) / (1. + q) * jnp.cos(2 * phi)
    e2 = (1. - q) / (1. + q) * jnp.sin(2 * phi)
    return e1, e2


def ellipticity2phi_q(e1, e2):
    """Transform complex ellipticity components to position angle and axis ratio.

    Parameters
    ----------
    e1, e2 : float or array_like
        Ellipticity components.

    Returns
    -------
    phi, q : same type as e1, e2
        Position angle (rad) and axis ratio (semi-minor / semi-major axis)

    """
    # replace value by low float instead to avoid NaNs
    # e1 = lax.cond(e1 == 0.0, lambda _: 1e-4, lambda _: e1, operand=None)  # does not work with TFP!
    # e2 = lax.cond(e2 == 0.0, lambda _: 1e-4, lambda _: e2, operand=None)  # does not work with TFP!
    e1 = jnp.where(e1 == 0., 1e-4, e1)
    e2 = jnp.where(e2 == 0., 1e-4, e2)
    phi = jnp.arctan2(e2, e1) / 2.
    c = jnp.sqrt(e1 ** 2 + e2 ** 2)
    c = jnp.minimum(c, 0.9999)
    q = (1. - c) / (1. + c)
    return phi, q

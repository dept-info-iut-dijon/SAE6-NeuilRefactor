from typing import List, Tuple

from PySide6.QtGui import QVector2D
from numpy import ndarray, dot, zeros, array
from numpy.linalg import norm


class Subspace:
    """
    Class to represent a subspace of a linear space
    """

    def __init__(self, basis: List[ndarray], orthonormal: bool = False) -> None:
        """
        Constructor.
        The subspace is characterized by a basis
        The basis doest not have to be orthonormal
        :param basis: the basis
        :param orthonormal: if the flag is true, the basis is assumed to be orthonormal
        """
        if orthonormal:
            self.basis = basis
        else:
            # Gramm-Schmidt orthonormalization.
            self.basis = []
            for v in basis:
                w = v.copy()
                for e in self.basis:
                    w = w - dot(w, e) * e
                self.basis.append(w / norm(w))

    def projection(self, v: ndarray) -> ndarray:
        res = zeros(self.basis[0].shape)
        for e in self.basis:
            res = res + dot(v, e) * e
        return res


def parallelogram(v1: QVector2D, v2: QVector2D, v3: QVector2D) -> Tuple[QVector2D, QVector2D, QVector2D]:
    """
    Take three vectors v1, v2, and v3 in R^2 and return the closest triple (u1, u2, u3) such that u3 = u1 + u2
    :param v1: the first vector
    :param v2: the second vector
    :param v3: the third vector, assumed to be close to v1 + v2
    """
    basis = [
        array([1, 0, 0, 0, 1, 0]),
        array([0, 1, 0, 0, 0, 1]),
        array([0, 0, 1, 0, 1, 0]),
        array([0, 0, 0, 1, 0, 1])
    ]
    w = array(v1.toTuple() + v2.toTuple() + v3.toTuple())
    subspace = Subspace(basis)
    p = subspace.projection(w)
    return QVector2D(*p[0:2]), QVector2D(*p[2:4]), QVector2D(*p[4:6])


def rectangle(v1: QVector2D, v2: QVector2D, v3: QVector2D) -> Tuple[QVector2D, QVector2D, QVector2D]:
    """
    Take three vectors v1, v2, and v3 in R^2 and return a "close" triple (u1, u2, u3) such that
    - u3 = u1 + u2
    - u1 · u2 = 0
    For the moment the orthogonal condition is handle is a rather dirty way...
    :param v1: the first vector
    :param v2: the second vector, supposed to be close to the orthogonal of v1
    :param v3: the third vector, assumed to be close to v1 + v2
    """
    w1, w2, _ = parallelogram(v1, v2, v3)
    u1 = w1
    aux = u1 / u1.length()
    u2 = w2 - QVector2D.dotProduct(w2, aux) * aux
    return u1, u2, u1 + u2


def square(v1: QVector2D, v2: QVector2D, v3: QVector2D) -> Tuple[QVector2D, QVector2D, QVector2D]:
    """
    Take three vectors v1, v2, and v3 in R^2 and return a "close" triple (u1, u2, u3) such that
    - u3 = u1 + u2
    - u1 · u2 = 0
    - u1 and u2 have the same norm
    For the moment the orthonormal condition is handle is a rather dirty way...
    :param v1: the first vector
    :param v2: the second vector, supposed to be close to the orthogonal of v1
    :param v3: the third vector, assumed to be close to v1 + v2
    """
    w1, w2, _ = parallelogram(v1, v2, v3)
    u1 = w1
    aux = u1 / u1.length()
    u2 = w2 - QVector2D.dotProduct(w2, aux) * aux
    u2 = (u1.length() / u2.length()) * u2
    return u1, u2, u1 + u2


def reflect(u: QVector2D) -> QVector2D:
    """
    Reflect the vector across the x-axis
    PySide and OpenGL use a different orientation of the y-axis
    - pointed downward for PySide
    - pointed upward for OpenGL
    This function is meant to fix this difference
    """
    return QVector2D(u.x(), -u.y())

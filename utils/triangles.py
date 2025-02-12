from typing import Tuple

from PySide6.QtCore import QPointF
from PySide6.QtGui import QVector2D


def apex_permutation_angle(vertices: Tuple[QPointF, QPointF, QPointF]) -> Tuple[int, int, int]:
    """
    Given a triple of points representing the vertices of a triangle,
    Return a 3-cycle (represented by a triple of integers) though as a permutation of the vertices,
    so that the angle at the first apex is the largest
    """
    dot_products = []
    for i in range(3):
        u = QVector2D(vertices[(i + 1) % 3] - vertices[i % 3])
        v = QVector2D(vertices[(i + 2) % 3] - vertices[i % 3])
        dot_products.append(QVector2D.dotProduct(u, v))

    p0, p1, p2 = dot_products
    if p0 <= p1 and p0 <= p2:
        return 0, 1, 2

    if p1 <= p2 and p1 <= p0:
        return 1, 2, 0

    if p2 <= p0 and p2 <= p1:
        return 2, 0, 1

    raise Exception("apex permutation failed")


def apex_permutation_length(vertices: Tuple[QPointF, QPointF, QPointF]) -> Tuple[int, int, int]:
    """
    Given a triple of points representing the vertices of a triangle, assumed to be almost isosceles
    Return a 3-cycle (represented by a triple of integers) though as a permutation of the vertices,
    so that the angle at the first apex is the one where the two side with same length meet.
    """
    u01 = QVector2D(vertices[1] - vertices[0])
    u12 = QVector2D(vertices[2] - vertices[1])
    u20 = QVector2D(vertices[0] - vertices[2])

    defect0 = abs(u01.length() - u20.length())
    defect1 = abs(u12.length() - u01.length())
    defect2 = abs(u20.length() - u12.length())

    if defect0 <= defect1 and defect0 <= defect2:
        return 0, 1, 2

    if defect1 <= defect2 and defect1 <= defect0:
        return 1, 2, 0

    if defect2 <= defect0 and defect2 <= defect1:
        return 2, 0, 1

    raise Exception("apex permutation failed")

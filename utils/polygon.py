from numpy import array, pi, cos, sin, sqrt


class Polygon:
    """
    Regular polygon in the hyperbolic plane
    """

    def __init__(self, n, theta):
        """
        Constructor
        :param n: number of sides of the polygon
        :param theta: angle at the apex
        """
        self.n = n
        self.theta = theta
        self.alpha = pi / self.n

        self._lengths = None

    @property
    def lengths(self):
        """
        Hyperbolic sine and cosine of the lengths of the appropriate triangle:
        The polygon is the union of n isosceles triangles meeting at the center.
        The triangle considered here is 'half' of one above triangle
        i.e. a right-angled triangle OAB, where
        - O is the center of the polygon and AOB = alpha
        - B is a vertex of the polygone and OBA = theta / 2
        - OAB is a right angle.
        In the code the convention is the following
        - OB = rho
        - OA = h
        - AB = ell
        :return:
        """
        if self._lengths is None:
            ca = cos(self.alpha)
            sa = sin(self.alpha)
            cb = cos(0.5 * self.theta)
            sb = sin(0.5 * self.theta)
            ca_sq = ca * ca
            sb_sq = sb * sb

            ch_rho = (ca * cb) / (sa * sb)
            sh_rho = sqrt(ca_sq - sb_sq) / (sa * sb)
            ch_h = cb / sa
            sh_h = sqrt(ca_sq - sb_sq) / sa
            ch_ell = ca / sb
            sh_ell = sqrt(ca_sq - sb_sq) / sb

            self._lengths = [ch_rho, sh_rho, ch_h, sh_h, ch_ell, sh_ell]

        return self._lengths

    @property
    def translation(self):
        _, _, ch, sh, _, _ = self.lengths
        ch2 = ch * ch + sh * sh
        sh2 = 2 * sh * ch
        return array([
            ch2, 0, sh2,
            0, 1, 0,
            sh2, 0, ch2
        ])

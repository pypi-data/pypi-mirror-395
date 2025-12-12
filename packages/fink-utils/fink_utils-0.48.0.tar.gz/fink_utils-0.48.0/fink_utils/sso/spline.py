import numpy as np
from numpy.linalg import solve
from numpy.polynomial.polynomial import Polynomial


from line_profiler import profile


class _spline(object):
    """Cubic spline class

    Spline function is defined by function values at nodes and the first
    derivatives at both ends.  Outside the range of nodes, the extrapolations
    are linear based on the first derivatives at the corresponding ends.
    """

    @profile
    def __init__(self, x, y, dy):
        """
        Spline initialization

        Parameters
        ----------
        x, y : array_like float
            The (x, y) values at nodes that defines the spline
        dy : array_like float with two elements
            The first derivatives of the left and right ends of the nodes
        """
        self.x = np.asarray(x)
        self.y = np.asarray(y)
        self.dy = np.asarray(dy)
        n = len(self.y)
        h = self.x[1:] - self.x[:-1]
        r = (self.y[1:] - self.y[:-1]) / (self.x[1:] - self.x[:-1])
        B = np.zeros((n - 2, n))
        for i in range(n - 2):
            k = i + 1
            B[i, i : i + 3] = [h[k], 2 * (h[k - 1] + h[k]), h[k - 1]]
        C = np.empty((n - 2, 1))
        for i in range(n - 2):
            k = i + 1
            C[i] = 3 * (r[k - 1] * h[k] + r[k] * h[k - 1])
        C[0] = C[0] - self.dy[0] * B[0, 0]
        C[-1] = C[-1] - self.dy[1] * B[-1, -1]
        B = B[:, 1 : n - 1]
        dys = solve(B, C)
        dys = np.array([self.dy[0]] + [tmp for tmp in dys.flatten()] + [self.dy[1]])
        A0 = self.y[:-1]
        A1 = dys[:-1]
        A2 = (3 * r - 2 * dys[:-1] - dys[1:]) / h
        A3 = (-2 * r + dys[:-1] + dys[1:]) / h**2
        self.coef = np.array([A0, A1, A2, A3]).T
        self.polys = [Polynomial(c) for c in self.coef]
        self.polys.insert(
            0, Polynomial([self.y[0] - self.x[0] * self.dy[0], self.dy[0]])
        )
        self.polys.append(
            Polynomial([self.y[-1] - self.x[-1] * self.dy[-1], self.dy[-1]])
        )

    @profile
    def __call__(self, x):
        x = np.asarray(x)
        out = np.zeros_like(x)
        idx = x < self.x[0]
        if idx.any():
            out[idx] = self.polys[0](x[idx])
        for i in range(len(self.x) - 1):
            idx = (self.x[i] <= x) & (x < self.x[i + 1])
            if idx.any():
                out[idx] = self.polys[i + 1](x[idx] - self.x[i])
        idx = x >= self.x[-1]
        if idx.any():
            out[idx] = self.polys[-1](x[idx])
        return out


class _spline_positive(_spline):
    """
    Define a spline class that clips negative function values
    """

    def __call__(self, x):
        y = super().__call__(x)
        if hasattr(y, "__iter__"):
            y[y < 0] = 0
        else:
            if y < 0:
                y = 0
        return y


_phi1v = (
    np.deg2rad([7.5, 30.0, 60, 90, 120, 150]),
    [7.5e-1, 3.3486016e-1, 1.3410560e-1, 5.1104756e-2, 2.1465687e-2, 3.6396989e-3],
    [-1.9098593, -9.1328612e-2],
)
_phi1 = _spline_positive(*_phi1v)
_phi2v = (
    np.deg2rad([7.5, 30.0, 60, 90, 120, 150]),
    [9.25e-1, 6.2884169e-1, 3.1755495e-1, 1.2716367e-1, 2.2373903e-2, 1.6505689e-4],
    [-5.7295780e-1, -8.6573138e-8],
)
_phi2 = _spline_positive(*_phi2v)
_phi3v = (
    np.deg2rad([0.0, 0.3, 1.0, 2.0, 4.0, 8.0, 12.0, 20.0, 30.0]),
    [
        1.0,
        8.3381185e-1,
        5.7735424e-1,
        4.2144772e-1,
        2.3174230e-1,
        1.0348178e-1,
        6.1733473e-2,
        1.6107006e-2,
        0.0,
    ],
    [-1.0630097, 0],
)
_phi3 = _spline_positive(*_phi3v)

from __future__ import annotations

import math
from array import array
from .h2_vector import H2Vector


class Matrix3D:
    PI = math.pi
    TAU = math.tau
    HALF_PI = math.pi * 0.5
    THIRD_PI = math.pi / 3
    QUARTER_PI = math.pi * 0.25

    def __init__(self, i: H2Vector, j: H2Vector, k: H2Vector):
        self.i: H2Vector = i
        self.j: H2Vector = j
        self.k: H2Vector = k

    @property
    def as_json(self) -> dict:
        return {
            "class_name": self.__class__.__name__,
            "i": [*self.i],
            "j": [*self.j],
            "k": [*self.k]
        }

    @classmethod
    def from_json(cls, json_data: dict) -> 'Matrix3D':
        return Matrix3D(H2Vector(*json_data["i"]), H2Vector(*json_data["j"]), H2Vector(*json_data["k"]))

    @property
    def determinant(self) -> float:
        d, e, f = self.i.y, self.j.y, self.k.y
        g, h, i = self.i.z, self.j.z, self.k.z

        return (
            self.i.x * (e*i - f*h)
            - self.j.x * (d*i - f*g)
            + self.k.x * (d*h - e*g))

    @property
    def inverse(self) -> 'Matrix3D':
        # WORKING MAGIC BELOW

        determinant = self.determinant
        if abs(determinant) < 1e-9:
            raise ValueError("Matrix3D is singular and cannot be inverted.")
        inverse_determinant = 1.0 / determinant

        a, b, c = self.i.x, self.j.x, self.k.x
        d, e, f = self.i.y, self.j.y, self.k.y
        g, h, i = self.i.z, self.j.z, self.k.z

        # cofactors Cij (cofactor of element at row i, col j)
        C00 = (e * i - f * h)
        C01 = -(d * i - f * g)
        C02 = (d * h - e * g)

        C10 = -(b * i - c * h)
        C11 = (a * i - c * g)
        C12 = -(a * h - b * g)

        C20 = (b * f - c * e)
        C21 = -(a * f - c * d)
        C22 = (a * e - b * d)

        # adjugate = transpose of cofactor matrix, so columns of inverse are:
        # first column  = (C00, C01, C02)
        # second column = (C10, C11, C12)
        # third column  = (C20, C21, C22)
        return Matrix3D(
            H2Vector(C00, C01, C02) * inverse_determinant,
            H2Vector(C10, C11, C12) * inverse_determinant,
            H2Vector(C20, C21, C22) * inverse_determinant
        )

    @property
    def transpose(self) -> 'Matrix3D':
        return Matrix3D(
            H2Vector(self.i.x, self.j.x, self.k.x),
            H2Vector(self.i.y, self.j.y, self.k.y),
            H2Vector(self.i.z, self.j.z, self.k.z)
        )

    def set_value(self, row: int, column: int, value: float):
        if column == 0:
            self.i[row] = value
        elif column == 1:
            self.j[row] = value
        elif column == 2:
            self.k[row] = value

    def apply_on_vector(self, vector: H2Vector) -> H2Vector:
        return self.i * vector.x + self.j * vector.y + self.k * vector.z

    def apply_on_vectors(self, vectors: list[H2Vector]) -> list[H2Vector]:
        return list(map(self.apply_on_vector, vectors))

    def before(self, matrix: 'Matrix3D') -> 'Matrix3D':
        new_i: H2Vector = matrix.apply_on_vector(self.i)
        new_j: H2Vector = matrix.apply_on_vector(self.j)
        new_k: H2Vector = matrix.apply_on_vector(self.k)

        return Matrix3D(new_i, new_j, new_k)

    def after(self, matrix: 'Matrix3D') -> 'Matrix3D':
        new_i: H2Vector = self.apply_on_vector(matrix.i)
        new_j: H2Vector = self.apply_on_vector(matrix.j)
        new_k: H2Vector = self.apply_on_vector(matrix.k)

        return Matrix3D(new_i, new_j, new_k)

    def lerp(self, matrix: 'Matrix3D', t: float) -> 'Matrix3D':
        new_i: H2Vector = self.i.lerp_euclidean(matrix.i, t)
        new_j: H2Vector = self.j.lerp_euclidean(matrix.j, t)
        new_k: H2Vector = self.k.lerp_euclidean(matrix.k, t)

        return Matrix3D(new_i, new_j, new_k)

    def copy(self) -> 'Matrix3D':
        return Matrix3D(
            H2Vector(*self.i),
            H2Vector(*self.j),
            H2Vector(*self.k)
        )

    def __matmul__(self, other: H2Vector | Matrix3D) -> H2Vector | Matrix3D:
        if type(other) == H2Vector:
            return self.apply_on_vector(other)

        elif type(other) == Matrix3D:
            return self.after(other)

        raise ValueError(f"Type {type(other)} isnt supported for matmul.")

    @classmethod
    def get_identity(cls) -> 'Matrix3D':
        return Matrix3D(
            H2Vector(1, 0, 0),
            H2Vector(0, 1, 0),
            H2Vector(0, 0, 1)
        )

    @classmethod
    def get_scale(cls, x_scale: float, y_scale: float, z_scale: float) -> 'Matrix3D':
        return Matrix3D(
            H2Vector(x_scale, 0, 0),
            H2Vector(0, y_scale, 0),
            H2Vector(0, 0, z_scale)
        )

    @classmethod
    def get_shear(cls, x_shear: float, y_shear: float, z_shear: float,
                  order: tuple[int, int, int] = (0, 1, 2)) -> 'Matrix3D':
        x_shear_matrix: Matrix3D = Matrix3D(
            H2Vector(1, 0, 0),
            H2Vector(x_shear, 1, 0),
            H2Vector(x_shear, 0, 1)
        )

        y_shear_matrix: Matrix3D = Matrix3D(
            H2Vector(1, y_shear, 0),
            H2Vector(0, 1, 0),
            H2Vector(0, y_shear, 1)
        )

        z_shear_matrix: Matrix3D = Matrix3D(
            H2Vector(1, 0, z_shear),
            H2Vector(0, 1, z_shear),
            H2Vector(0, 0, 1)
        )

        matrices: list[Matrix3D] = [None, None, None]
        matrices[order[0]] = x_shear_matrix
        matrices[order[1]] = y_shear_matrix
        matrices[order[2]] = z_shear_matrix

        assert (None not in matrices)

        matrices[1] = matrices[1].after(matrices[0])
        matrices[2] = matrices[2].after(matrices[1])

        return matrices[2]

    @property
    def as_string(self) -> str:
        return (f"|{self.i.x}, {self.j.x}, {self.k.x}|\n"
                f"|{self.i.y}, {self.j.y}, {self.k.y}|\n"
                f"|{self.i.z}, {self.j.z}, {self.k.z}|\n")

    def __str__(self):
        return self.as_string

    def __repr__(self):
        return self.as_string

    @property
    def as_array(self) -> array:
        return array('f', [
            self.i.x, self.j.x, self.k.x,
            self.i.y, self.j.y, self.k.y,
            self.i.z, self.j.z, self.k.z
        ])

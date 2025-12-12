import math

class Vec2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def rotate(self, angle_rad: float) -> "Vec2":
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        return Vec2(
            self.x * cos_a - self.y * sin_a,
            self.x * sin_a + self.y * cos_a
        )

    def __repr__(self):
        return f"Vec2({self.x:.3f}, {self.y:.3f})"

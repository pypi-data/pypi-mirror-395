import math
from shapely import LineString, Point
from typing import Tuple, List, Union
class RectangleGenerator:
    """
    用于生成绕指定中心点旋转后的矩形坐标的工具类。
    """

    def __init__(self):
        # 类的初始化，目前不需要特殊设置
        pass

    @staticmethod
    def _rotate_point(cx: float, cy: float, x: float, y: float, angle_radians: float) -> dict:
        """
        内部静态方法：将一个点 (x, y) 绕中心点 (cx, cy) 逆时针旋转 angle_radians。

        参数:
            cx (float): 旋转中心点 X 坐标
            cy (float): 旋转中心点 Y 坐标
            x (float): 要旋转的点 X 坐标
            y (float): 要旋转的点 Y 坐标
            angle_radians (float): 旋转角度（弧度）

        返回:
            dict: 包含 'x' 和 'y' 键的新坐标。
        """
        """Rotate a point counterclockwise around (cx, cy) by angle_radians."""
        x_rotated = cx + (x - cx) * math.cos(angle_radians) - (y - cy) * math.sin(angle_radians)
        y_rotated = cy + (x - cx) * math.sin(angle_radians) + (y - cy) * math.cos(angle_radians)

        return {"x": x_rotated, "y": y_rotated}

    def generate_rotated_rectangle(self, center_x: float, center_y: float, width: float, height: float,
                                   angle_degrees: float) -> list[dict]:
        """
        生成旋转后的矩形的四个角点坐标。

        参数:
            center_x (float): 矩形中心点 X 坐标
            center_y (float): 矩形中心点 Y 坐标
            width (float): 矩形宽度
            height (float): 矩形高度
            angle_degrees (float): 逆时针旋转角度（度）

        返回:
            list[dict]: 包含四个角点坐标字典的列表，顺序为左下、右下、右上、左上（相对未旋转时）。
        """
        # 1. 角度转换
        angle_radians = math.radians(angle_degrees)

        # Define the corners of the unrotated rectangle
        x0, y0 = center_x - width / 2, center_y - height / 2
        x1, y1 = center_x + width / 2, center_y - height / 2
        x2, y2 = center_x + width / 2, center_y + height / 2
        x3, y3 = center_x - width / 2, center_y + height / 2

        # 3. 旋转角点
        points = [
            self._rotate_point(center_x, center_y, x0, y0, angle_radians),
            self._rotate_point(center_x, center_y, x1, y1, angle_radians),
            self._rotate_point(center_x, center_y, x2, y2, angle_radians),
            self._rotate_point(center_x, center_y, x3, y3, angle_radians)
        ]
        return points

    def generate_projected_point(self, lane_points: List[Tuple[float, float]], x: float, y: float) -> Tuple[
        float, float]:
        """
        同步方法：将点 (x, y) 投影到由 lane_points 定义的 LineString 上。

        参数:
            lane_points (List[Tuple[float, float]]): 定义车道的坐标点列表。
            x (float): 要投影的点的 X 坐标。
            y (float): 要投影的点的 Y 坐标。

        返回:
            Tuple[float, float]: 投影点 (newP) 的 (x, y) 坐标。
        """
        # 1. 创建几何对象
        line = LineString(lane_points)
        p = Point(x, y)

        # 2. 核心投影计算
        # line.project(p) 计算点 p 沿线 line 的投影距离（fractional distance）
        # line.interpolate(...) 使用该距离在 line 上找到精确的点
        # .coords[0] 提取该点的 (x, y) 坐标
        newP: Tuple[float, float] = line.interpolate(line.project(p)).coords[0]

        return newP


# 示例用法
if __name__ == '__main__':
    generator = RectangleGenerator()

    # 绕 (10, 10) 中心点，宽 40，高 20，逆时针旋转 30 度
    coords = generator.generate_rotated_rectangle(
        center_x=10,
        center_y=10,
        width=40,
        height=20,
        angle_degrees=30
    )
    print("旋转后的矩形坐标 (30度):")
    for p in coords:
        print(f"  x: {p['x']:.2f}, y: {p['y']:.2f}")
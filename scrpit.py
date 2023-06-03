import math

class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __str__(self) -> str:
        return f"{{x: {self.x}; y: {self.y}}}"
        
    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other) -> bool:
        return self.x != other.x or self.y != other.y
        
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
        
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
        
    def mulOnConst(self, k: int):
        return Vector(self.x * k, self.y * k)
    
    def calcScalarProduct(self, other) -> float:
        return self.x * other.x + self.y * other.y
        
    def calcDistance(self, target) -> float:
        return (target - self).getLength()
    
    def getLength(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)
    
    def normalize(self):
        length = self.getLength()
        return Vector(self.x / length, self.y / length)

class Line:
    def __init__(self, start: Vector, end: Vector):
        self.start = start
        self.end = end
        
    def __str__(self):
        return f'Line: from({self.start}); to({self.end})'
        
    
    def pointOnLine(self, point):
        '''Проверить, что точка лежит на прямой'''
        if self.end.y == self.start.y:
            return point.y - self.start.y < 1e-6
        
        if self.end.x == self.start.x:
            return point.x - self.start.x < 1e-6

        leftPart = (point.x - self.start.x) / (self.end.x - self.start.x)
        rightPart = (point.y - self.start.y) / (self.end.y - self.start.y)
        return abs(leftPart - rightPart) < 1e-6
        
    def pointOnSegment(self, point):
        '''Проверить, что точка лежит на отрезке'''
        x_min, x_max = min(self.start.x, self.end.x), max(self.start.x, self.end.x)
        y_min, y_max = min(self.start.y, self.end.y), max(self.start.y, self.end.y)
        return self.pointOnLine(point) and x_min <= point.x <= x_max and y_min <= point.y <= y_max
    
    def getNormal(self) -> Vector:
        '''Получить единичный вектор нормали к прямой'''
        B = -1
        A = (self.end.y - self.start.y) / (self.end.x - self.start.x)
        
        dx = self.end.x - self.start.x
        normal = Vector(-A, -B) if dx >= 0 else Vector(A, B)
        return normal.normalize()
    
    def getProjectionFrom(self, targetPoint: Vector) -> Vector:
        '''Проекция точки на прямую'''
        if self.end.y == self.start.y:
            return Vector(targetPoint.x, self.end.y)
        
        if self.end.x == self.start.x:
            return Vector(self.end.x, targetPoint.y)

        B = -1
        A = (self.end.y - self.start.y) / (self.end.x - self.start.x)
        C = self.start.y - A * self.start.x
        distance = abs(A * targetPoint.x + B * targetPoint.y + C) / math.sqrt(A**2 + B**2)

        normal = self.getNormal()
        return targetPoint + normal.mulOnConst(distance)
        

def pointInsideShape(points: list[Vector], targetPoint: Vector):
    '''Проверить, что точка лежит внутри фигуры, образуемой списком точек'''
    lines = [Line(points[i % len(points)], points[(i + 1) % len(points)]) for i in range(len(points))]

    minDistance = float("inf")
    targetLine = None # type: Line
    projectPoint = None # type: Vector
    for line in lines:
        h = line.getProjectionFrom(targetPoint)
        distance = targetPoint.calcDistance(h)
        if distance < minDistance:
            minDistance = distance
            targetLine = line
            projectPoint = h

    print(f'тестируемая точка: {targetPoint}')
    print(f'минимальное расстояние: {minDistance}')
    print(f'ближайшая линия: {targetLine}')
    print(f'проекция на ближайшую линию: {projectPoint}')

    normal = targetLine.getNormal()
    directLine = projectPoint - targetPoint
    scalarRes = normal.calcScalarProduct(directLine)
    
    print(f'scalarRes: {scalarRes}')
    return scalarRes > 0 and targetLine.pointOnSegment(projectPoint)


if __name__ == '__main__':
    targetPoints = [
        Vector(9, 4),       # F
        Vector(7, 2),       # G
        Vector(12, 1),      # H
        Vector(11, 1.5)     # I
    ]

    points = [
        Vector(7, 1),
        Vector(5, 5),
        Vector(9, 5),
        Vector(11, 3),
        Vector(10, 1)
    ]

    for targetPoint in targetPoints:
        inside = pointInsideShape(points, targetPoint)
        if inside:
            print(f'Точка {targetPoint} внутри')
        else:
            print(f'Точка {targetPoint} снаружи')

        print("====================================")
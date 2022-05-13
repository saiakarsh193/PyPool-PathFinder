class TP:
    def __init__(self, point, name, parent, level, history):
        self.point = point
        self.name = name
        self.parent = parent
        self.level = level
        self.history = history
        self.children = []

    def __str__(self):
        return 'TP<{point}, ={name}, ^{parent}, l{level}, {history}, ({noc})>'.format(
                point = self.point,
                name = self.name,
                parent = self.parent.name if self.parent != None else None,
                level = self.level,
                history = self.history,
                noc = len(self.children),
                )

    def addChild(self, point, name):
        child = TP(point, name, self, self.level + 1, self.history + [name])
        self.children.append(child)


class TP:
    def __init__(self, point, name, cpoint, parent, level, history):
        self.point = point # attack point
        self.name = name # ball/pocket name
        self.cpoint = cpoint # centre of the ball/pocket
        self.parent = parent # parent TP
        self.level = level # level of TP
        self.history = history # history of the node (all its ancestors)
        self.children = [] # pointers to its children

    def __str__(self):
        return 'TP<{point}, ={name}, ^{parent}, l{level}, {history}, ({noc})>'.format(
                point = self.point,
                name = self.name,
                parent = self.parent.name if self.parent != None else None,
                level = self.level,
                history = self.history,
                noc = len(self.children),
                )

    def addChild(self, point, name, cpoint):
        child = TP(point, name, cpoint, self, self.level + 1, self.history + [name])
        self.children.append(child)


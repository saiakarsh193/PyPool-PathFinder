class TP:
    def __init__(self, point, name, cpoint, parent, level, history, extend_point=None):
        self.point = point # attack point
        self.name = name # ball/pocket name
        self.cpoint = cpoint # centre of the ball/pocket
        self.parent = parent # parent TP
        self.level = level # level of TP
        self.history = history # history of the node (all its ancestors)
        self.children = [] # pointers to its children
        self.extend_point = extend_point # this point is used for bounce involved TP

    def __str__(self):
        return 'TP<{point}, ={name}, ^{parent}, l{level}, {history}, ({noc})>'.format(
                point = self.point,
                name = self.name,
                parent = self.parent.name if self.parent != None else None,
                level = self.level,
                history = self.history,
                noc = len(self.children),
                )

    def addChild(self, point, name, cpoint, extend_point=None):
        child = TP(point, name, cpoint, self, self.level + 1, self.history + [name], extend_point)
        # if there is an extend point, meaning if there is a bounce, then we add a level to it
        # this is because the bounce is considered as a level
        # to reduce complex shots from being considered
        if(extend_point != None):
            child.level += 1
        self.children.append(child)


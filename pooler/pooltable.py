from pooler.vector import Vector
from pooler.line import Line 
from pooler.targetpoint import TP
import math

class PoolTable:
    def __init__(self, data):
        # importing the metadata
        self.ball_radius = data['metadata']['ball_radius']
        self.pocket_radius = data['metadata']['pocket_radius']
        self.table_width = data['metadata']['table_width']
        self.table_height = data['metadata']['table_height']

        # converting ball points to vectors
        self.balls = data['balls']
        for ball, value in self.balls.items():
            self.balls[ball] = Vector(value)

        # conveting pockets to vectors with ids/names
        # pocket names
        # a  b  c
        #
        # d     e
        #
        # f  g  h
        self.pocket_names = ['a', 'c', 'h', 'f', 'b', 'g', 'e', 'd']
        self.pockets = {}
        for pocket, value in zip(self.pocket_names, data['pockets']):
            self.pockets[pocket] = Vector(value)
        
        # assigning the cue ball
        self.cue = '0'

        # max recursion depth for path finding
        self.max_depth = 3

        # threshold for closest point and target point angle (for possibility of steep shot)
        self.fp_tp_threshold = 5 # degrees

        # counters for logging
        self.total_addchild = 1
        self.total_endps = 0
        self.total_childrecur = 0

    def printTP(self, rootp):
        # for printing the TP tree wrt as cur and child pairs
        print('cur:', rootp)
        print('chilren:')
        for child in rootp.children:
            print(child)
        print()
        for child in rootp.children:
            self.printTP(child)

    def calculatePaths(self):
        # calculate the root target point for each pocket
        # the root is a DAG that has all the shots for that pocket
        # for choosing the valid shots, we only choose those ending with the cue ball
        self.proots = []
        for pocket in self.pockets.keys():
            # get the root TP of pocket
            self.proots.append(self.calculateRootForPocket(pocket))
        print('Total children recursion checks done:', self.total_childrecur)
        print('Total children calculated:', self.total_addchild)

    def calculateRootForPocket(self, pocket):
        # the TP for pocket is not centre but with offset such that the it coincides with the table edge
        # attack point, name, centre point, parent, level, history
        rootpoint = TP(self.getPocketOffsetPoint(pocket), pocket, self.pockets[pocket], None, 0, [])
        # nocue is set to true because we dont want the cue ball to be a direct child of pocket (we dont want to scratch)
        self.calculateTPChildren(rootpoint, nocue=True)
        return rootpoint

    def getPocketOffsetPoint(self, pocket):
        # calculating the offset for each pocket root point and returning the new point
        rad_vec = self.pocket_radius * (1 / 1.414);
        if(pocket == 'a'):
            diff_vec = Vector(rad_vec, -rad_vec)
        elif(pocket == 'b'):
            diff_vec = Vector(0, -self.pocket_radius)
        elif(pocket == 'c'):
            diff_vec = Vector(-rad_vec, -rad_vec)
        elif(pocket == 'd'):
            diff_vec = Vector(self.pocket_radius, 0)
        elif(pocket == 'e'):
            diff_vec = Vector(-self.pocket_radius, 0)
        elif(pocket == 'f'):
            diff_vec = Vector(rad_vec, rad_vec)
        elif(pocket == 'g'):
            diff_vec = Vector(0, self.pocket_radius)
        else:
            diff_vec = Vector(-rad_vec, rad_vec)
        return self.pockets[pocket] + diff_vec

    def calculateTPChildren(self, tp, nocue=False):
        # calculating the child nodes for a given TP node
        # if the node is cue or has reached max level, we do not need to calculate the children
        if(tp.name == self.cue or tp.level >= self.max_depth):
            return

        # iterating through all the balls
        for ball in self.balls.keys():
            # assumption that the ball shouldn't have been considered already (not present in history)
            # if nocue is True, we dont consider the cue ball as a child
            if(ball not in tp.history and not(nocue == True and ball == self.cue)):

                # calculating the point for direct shot from ball to target
                # we use cpoint (the centre for the ball/pocket to estimate the possibility of the shot)
                # print('Doing:', ball, tp.name, (None if tp.parent == None else tp.parent.name))
                cap = self.calculateAPDirect(self.balls[ball], tp.point, tp.cpoint)
                # if there is a valid point, then it adds it as a child
                if(cap != None):
                    tp.addChild(cap, ball, self.balls[ball])
                    self.total_addchild += 1

                self.total_childrecur += 1

        # recursively calculate the children for each child node of the current TP node
        for child in tp.children:
            self.calculateTPChildren(child)

    def calculateAPDirect(self, source, target, cpoint):
        # calculate the attack point before hand
        atp = self.calculateAttackPoint(source, target)
        # find angle of attack for source and target
        # find angle of attack for source and closest point on the line (target-source) to cpoint
        # this is done because if angfp is less than angtp, it means the shortest point (fp) comes first in the line of attack of target
        # this implies it is impossible to hit the target as the ball will strike the fp first before it ever reaches target (dis from target to cpoint is ball_radius)
        # we use a threshold to ignore very steep shots too
        angtp = Vector.AngleBetween(target - cpoint, source - cpoint)
        fp = self.getFootOfPerpendicular(cpoint, source, target)
        # if the cpoint, target and source are on the same line (straight shot), then fp will be cpoint
        if(fp.equals(cpoint)):
            # we then only check if the target is in the LOS (line of sight) of the source wrt to the cpoint ball
            # required condition: angtp <= 90
            # general condition: angfp - angtp >= self.fp_tp_threshold
            # angtp <= angfp - self.fp_tp_threshold
            # angfp - self.fp_tp_threshold = 90
            angfp = self.fp_tp_threshold + 90
        else:
            angfp = Vector.AngleBetween(fp - cpoint, source - cpoint)
        # if shot is physically possible and there are no balls in its way
        if(angfp - angtp >= self.fp_tp_threshold and not self.checkPathBallCollision(atp, target, source, cpoint)):
            return atp
        else:
            return None

    def checkPathBallCollision(self, a, b, source, target):
        # finds if there is any ball in the path a->b
        # exceptions are source and target ball/pocket
        for cball in self.balls.values():
            if(not (source.equals(cball) or target.equals(cball))):
                # get foot of perpendicular of the ball wrt the path, and also the fac
                fp, fac = self.getFootOfPerpendicular(cball, a, b, getfac=True)
                # closest distance between path and ball
                fpdist = (cball - fp).mag
                # if the ball lies in the path (0 < fac < 1) and the distance is less than the radius (for collision to occur)
                if(fac > 0 and fac < 1 and fpdist < self.ball_radius):
                    return True
        return False

    def getFootOfPerpendicular(self, a, b, c, getfac=False):
        # finds the foot of perpendicular from the line (b->c) to point (a)
        fac = Vector.Dot(a - b, c - b) / (c - b).mag**2
        if(getfac):
            return b + (c - b) * fac, fac
        else:
            return b + (c - b) * fac

    def calculateAPBounce(self, source, target):
        return

    def calculateAttackPoint(self, source, target):
        # calculates the attack point on ball (source) towards the target
        d = target - source
        d = d / d.mag
        atp = source + d * (-2 * self.ball_radius)
        return atp

    def getPaths(self):
        # to calculate the total paths possible from the pocket roots
        paths = []
        for rootp in self.proots:
            # we do a DFS from each pocket root TP
            # we dont need a visit list as the graph is a DAG
            ends = []
            stack = [rootp]
            while(len(stack) > 0):
                cur = stack.pop(-1)
                # whenever we encounter a cue node, we know that it is a valid path
                # so we add that node to the ends list
                if(cur.name == self.cue):
                    ends.append(cur)
                # adding the children to the stack
                for child in cur.children:
                    stack.append(child)

            # now we convert each endpoint TP to a path
            for endpoint in ends:
                # first we expand the end TP to a list of points leading all the way to the pocket
                epoints = self.expandToPoints(endpoint)
                # we convert the list of points to a list of lines and get the path
                epath = self.makePathFromPoints(epoints)
                # add the path to the total paths
                paths.append(epath)
                self.total_endps += 1
        print('Total endpoints found:', self.total_endps)
        return paths

    def expandToPoints(self, tp):
        # we expand the end TP to list of points by recursively traversing to the parent till we reach the pocket (whose parent is None)
        cur = tp
        epath = [cur.point]
        while(cur.parent != None):
            cur = cur.parent
            epath.append(cur.point)
        return epath

    def makePathFromPoints(self, points):
        # we convert points to lines by taking two points and making a Line object from them
        path = []
        for i in range(len(points) - 1):
            path.append(Line(points[i], points[i + 1]))

        # we then convert the Line object into a list
        for ind, line in enumerate(path):
            path[ind] = line.toList()
        return path

    def getLines(self):
        # to get a list of lines directly
        tpaths = self.getPaths()
        tlines = []
        for path in tpaths:
            tlines += path
        return tlines


from collections import namedtuple, deque, defaultdict, Counter


class Go(object):

    colors = {"black": 'b', "white": 'w', "none": '-'}

    PointT = namedtuple('Point', ['x', 'y', 'c'])

    def Point(self, x, y, c=None):
        if c is None:
            c = self.colors["none"]
        return self.PointT(x, y, c)

    def __init__(self, size):
        self.size = size
        self.board = [[self.colors["none"] for x in range(
            size)] for y in range(size)]

    def __str__(self):
        return "\n".join(["".join(row) for row in self.board])

    def on_board(self, p):
        return p.y in range(self.size) and p.x in range(self.size)

    def neighbors(self, p):
        ''' Return set of Points adjacent to p on the board'''
        nbs = [(p.x, p.y + 1), (p.x, p.y - 1),
               (p.x + 1, p.y), (p.x - 1, p.y)]
        points = filter(self.on_board, [self.Point(*n) for n in nbs])
        return [self.Point(a.x, a.y, self.board[a.y][a.x]) for a in points]

    def friends(self, p):
        ''' Return set of p and stones connected to p that are the same color'''

        def _close_friends(p2):
            return filter(lambda f: f.c == p2.c, self.neighbors(p2) + [p2])

        friends = deque()
        friends.append(p)
        seen = set()
        while friends:
            friend = friends.pop()
            for f in _close_friends(friend):
                if not f in seen:
                    friends.append(f)
            seen.add(friend)
        return seen

    def adjacent_color_map(self, group):
        ''' Return a dict with number of intersections
            adjacent to this group for each color
        '''
        bycolor = defaultdict(set)
        for p in group:
            for nbr in self.neighbors(p):
                bycolor[p.c].add(nbr)
        return {k: len(v) for (k, v) in bycolor.items()}

    def score(self):
        to_visit = set(self.Point(x, y, c) for y, l in enumerate(self.board) for x, c in enumerate(l))
        scores = Counter()
        while to_visit:
            p = to_visit.pop()
            if p.c == self.colors["none"]:
                also_empty = self.friends(p)
                to_visit -= also_empty
                scores.update(self.adjacent_color_map(also_empty))
            else:
                scores.update([p.c])
        return dict(scores)

    def liberties(self, p):
        ''' Return number of liberties for the group attached with p'''
        def _lib(p2):
            return filter(lambda n: n.c == self.colors["none"], self.neighbors(p2))
        return len(reduce(lambda S, p: S.union(_lib(p)), self.friends(p), set()))

    def _play(self, p):
        if p.c not in self.colors:
            return "invalid color"
        if not self.on_board(p):
            return "proposed play not on board"
        if self.board[p.y][p.x] != self.colors["none"]:
            return "occupied territory"
        if self.liberties(p) == 0:
            return "You have too much to live for"
        self.board[p.y][p.x] = self.colors[p.c]
        return "ok"

    def play(self, color, col, row):
        return self._play(self.Point(col, row, color))

if __name__ == '__main__':
    a = Go(19)
    print(a.play("black", 4, 4))
    print(a.play("white", 4, 4))
    print(a.play("white", 4, 5))
    print(a.play("white", 4, 6))
    print(a.play("white", 4, 7))
    print(a.play("white", 5, 7))
    print(a.play("white", 6, 7))
    print(a.play("white", 6, 6))
    print(a.play("white", 6, 5))
    print(a.play("white", 5, 5))
    print(a.liberties(a.Point(4, 4, "b")))
    print(a.liberties(a.Point(4, 5, "w")))
    print(a.liberties(a.Point(4, 6, "w")))
    print(a.liberties(a.Point(5, 6, "w")))
    print a
    print(a.adjacent_color_map([a.Point(4, 5, "w")]))
    print(a.score())

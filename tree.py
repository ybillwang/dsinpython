from linked_queue import LinkedQueue


class Tree:
    class Position:
        def element(self):
            raise NotImplementedError('Must implemented by subclass')

        def __eq__(self, other):
            raise NotImplementedError('Must implemented by subclass')

        def __ne__(self, other):
            return not (self == other)

    def __iter__(self):
        for p in self.positions():
            yield p.element()

    def root(self):
        raise NotImplementedError('Must implemented by subclass')

    def parent(self, p):
        raise NotImplementedError('Must implemented by subclass')

    def num_children(self, p):
        raise NotImplementedError('Must implemented by subclass')

    def children(self, p):
        raise NotImplementedError('Must implemented by subclass')

    def __len__(self):
        raise NotImplementedError('Must implemented by subclass')

    def is_root(self, p):
        return self.root() == p

    def is_leaf(self, p):
        return self.num_children(p) == 0

    def is_empty(self):
        return len(self) == 0

    def depth(self, p):
        if self.is_root(p):
            return 0
        else:
            return 1 + self.depth(self.parent(p))

    def _height1(self):
        return max(self.depth(p) for p in self.positions() if self.is_leaf(p))

    def _height2(self, p):
        if self.is_leaf(p):
            return 0
        else:
            return 1+max(self._height2(c) for c in self.children(p))

    def height(self, p=None):
        if p is None:
            p = self.root()
        return self._height2(p)

    def preorder(self):
        if not self.is_empty():
            for p in self._subtree_preorder(self.root()):
                yield p

    def preorder_indent(T, p, d):
        print(2*d*' '+str(p.element()))
        for c in T.children(p):
            preorder_indent(T, c, d+1)

    def preorder_label(T, p, d, path):
        label = '.'.join(str(j+1) for j in path)
        print(2*d*' '+label, p.element())
        path.append(0)
        for c in T.children(p):
            preorder_label(T, c, d+1, path)
            path[-1] += 1
        path.pop()

    def _subtree_preorder(self, p):
        yield p
        for c in self.children(p):
            for other in self._subtree_preorder(c):
                yield other

    def positions(self):
        return self.preorder()

    def postorder(self):
        if not self.is_empty():
            for p in self._subtree_postorder(self.root()):
                yield p

    def _subtree_postorder(self, p):
        for c in self.children(p):
            for other in self._subtree_postorder(c):
                yield other
            yield p

    def breadthfirst(self):
        if not self.is_empty():
            fringe = LinkedQueue()
            fringe.enqueue(self.root())
            while not fringe.is_empty():
                p = fringe.dequeue()
                yield p
                for c in self.children(p):
                    fringe.enqueue(c)

    def parenthesize(T, p):
        print(p.element(), end='')
        if not T.is_leaf(p):
            first_time = True
            for c in T.children(p):
                sep = ' (' if first_time else ', '
                print(sep, end='')
                first_time = False
                parenthesize(T, c)
            print(')', end='')

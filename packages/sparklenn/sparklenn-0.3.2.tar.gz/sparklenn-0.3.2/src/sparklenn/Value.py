class Value:
    def __init__(self, data, _children=(), _op=''):
        self.data = data
        self._children = set(_children)
        self._op = _op
        self.grad = 0.0
        self._backward = lambda: None
    
    def __repr__(self):
        return f"Value(data={self.data}), children={len(self._children)}, op={self._op})"
    
    def __add__(self, other):
        if isinstance(other, (int, float)):
            other = Value(other)
        out = Value(self.data + other.data, (self, other), '+')

        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward
        return out
    
    def __sub__(self, other):
        if isinstance(other, (int, float)):
            other = Value(other)
        out = Value(self.data - other.data, (self, other), '-')

        def _backward():
            self.grad += out.grad
            other.grad += -1 * out.grad
        out._backward = _backward
        return out
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            other = Value(other)
        out = Value(self.data * other.data, (self, other), '*')

        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward
        return out
    
    def __radd__(self, other):
        return Value(other + self.data)

    def __rsub__(self, other):
        return Value(other - self.data)

    def __rsum__(self, other):
        return Value(other + self.data)
    
    def __pow__(self, other):
        assert isinstance(other, (int, float)), "only supporting int/float powers for now"
        out = Value(self.data ** other, (self,), f'**{other}')

        def _backward():
            self.grad += (other * self.data ** (other - 1)) * out.grad
        out._backward = _backward
        return out
    
    def tanh(self):
        x = self.data 
        t = (2 / (1 + pow(2.718281828459045, -2 * x))) - 1
        out = Value(t, (self,), 'tanh')

        def _backward():
            self.grad += (1 - t ** 2) * out.grad
        out._backward = _backward
        return out
    
    def backward(self):
        topo = []
        visited = set()

        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._children:
                    build_topo(child)
                topo.append(v)
        build_topo(self)

        self.grad = 1.0
        for node in reversed(topo):
            node._backward()
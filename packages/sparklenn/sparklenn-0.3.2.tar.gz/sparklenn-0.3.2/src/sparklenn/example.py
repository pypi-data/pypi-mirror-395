from .MLP import MLP

mlp = MLP(3, [4, 4, 1])
xs = [[2.0, -3.0, 10.0],
      [3.0, -1.0, -5.0],
      [4.0, 2.0, -2.0],
      [0.5, 0.5, 1.0]]
ys = [1.0, -1.0, 1.0, 1.0]
ypred = [mlp(x) for x in xs]


for epoch in range(10):
    for p in mlp.parameters():
        p.data += -0.01 * p.grad
    y_pred = [mlp(x) for x in xs] # forward pass
    loss = sum((yout - ytgt) ** 2 for yout, ytgt in zip(y_pred, ys)) 
    loss.backward()  # backward pass
    print({'epoch': epoch, 'loss': loss})


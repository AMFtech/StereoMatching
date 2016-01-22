def frange(x, y, jump):
  while x < y:
    yield x
    x += jump

lst = frange(0.1, 0.5, 0.1)    
print lst
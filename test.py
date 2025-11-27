def foo(id, **kwargs):
    print(id)
    for p,v in kwargs.items():
        print(p,v)

foo(3, b=7, c=5, d = 7)
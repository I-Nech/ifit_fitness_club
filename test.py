def foo(a, *args, b=5, **kwargs):
    print(a,b)
    print(args)
    print(kwargs)

foo(3, 6, 4, b=7, c=5, d = 7)
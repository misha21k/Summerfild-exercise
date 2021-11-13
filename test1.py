def fun():
    f = fun.cache.get(5, None)
    return 4
fun.cache = {}

print(fun())
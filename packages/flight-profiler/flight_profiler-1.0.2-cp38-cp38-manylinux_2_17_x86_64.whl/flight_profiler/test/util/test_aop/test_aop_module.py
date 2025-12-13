def func_to_wrap(v):
    return v

def nested_func_to_wrap():
    def nested_func():
        return 5
    return nested_func()

def nested_func_to_wrap_deref(v):
    def nested_func(y=5):
        return v
    return nested_func()

async def async_func_to_wrap(v):
    return v

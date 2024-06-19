from functools import wraps

# sample "bare" decorator
# this is a decorator that does not take any arguments
# it is applied to a function by writing @wrapper
# a simple decorator takes a single argument, the function to decorate
# it returns a new function (which usually uses the original function
# somehow) which python will use to replace the original function
def wrapper(fn):
    # wraps is a decorator that copies the metadata (such as the name)
    # of the original function
    @wraps(fn)
    def inner(*args, **kwargs):
        # in a def, *args and **kwargs are variadic parameters
        # they are used to capture all positional and keyword arguments
        print("before")

        # this is the actual call to the original function
        # *args and **kwargs are used to pass the arguments to the function
        result = fn(*args, **kwargs)
        print("after")

        # return the result of the original function
        return result

    return inner

# a more complex decorator that takes arguments
# it would be applied to a function by writing
# @custom_wrapper(prologue_str, epilogue_str)
# custom_wrapper *returns a decorator* that takes a single argument,
# the function!
# the decorator it returns is the one that actually wraps the function
# this is a common pattern for decorators that take arguments, which
# we see in Flask's route decorators.
# The approach for the inner function is the same as the simple decorator
def custom_wrapper(prologue, epilogue):
    def decorator(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            print(prologue)
            result = fn(*args, **kwargs)
            print(epilogue)
            return result

        return inner
    
    return decorator


@custom_wrapper("prologue", "epilogue")
def hello():
    print('Hello, world!')

@wrapper
def bye():
    print('Bye, world!')

@wrapper
def greet(name):
    print(f'Hello, {name}!')

# Print the functions (not their result) to see what they are
# Because of the @wraps decorator, the original name of the function
# is preserved (this is important for debugging, introspection,
# and for registering routes in Flask!)
print(hello)
print(bye)
print(greet)

# call the wrapped functions
# notice that even though bye and greet take a different number of
# arguments, the wrapper can handle both due to the use of *args and **kwargs
hello()
bye()
greet("everyone")


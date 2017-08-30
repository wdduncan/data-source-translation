import os


def print_function_output(print_flag=True):
    """
    This function is used as a decorator to control whether the funciton's output is printed to screen.
    Because the print_function_output takes and argument to decorator syntax includes parens "()".
    If print_flag is True, to show output, the syntax is:
        @print_function_output()
        def foo(): ...
    This is equivalent to:
        foo = print_function_output()(foo)
    If print_flag is True, to suppress output, the syntax
        @print_function_output(False)
        def foo(): ...
    This is equivalent to:
        foo = print_function_output(False)(foo)
    For examples of decorators see:
        http://blog.endpoint.com/2013/12/python-decorator-basics.html
        https://www.thecodeship.com/patterns/guide-to-python-function-decorators/
    :param print_flag: if true, turles prints to screen
    :return: decorator function
    """
    def decorator(function):
        def wrapper(*args, **kwargs):
            output = function(*args, **kwargs) # call function and strore output

            # check to print and return output
            if print_flag: print output
            return output
        return wrapper # decorator will return wrapper(), and wrapper will return the output

    return decorator


def get_tablename_from_file(filepath, remove_ext=True):
    if remove_ext:
        return os.path.splitext(os.path.basename(filepath))[0]
    else:
        return os.path.basename(filepath)


def print_axioms(axioms):
    # for axiom in axioms: print axiom
    print "\n".join(axioms)

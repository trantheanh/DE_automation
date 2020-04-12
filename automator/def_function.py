import inspect


def test_function(func):
    def get_func(**kwargs):
        desc = inspect.getfullargspec(func)
        try:
            inputs = {}
            for arg in desc.args:
                inputs[arg] = kwargs[arg]
            return func(**inputs)
        except:
            return None
        finally:
            pass

    get_func.__name__ = func.__name__

    return get_func


def value_function(func):
    def get_func(**kwargs):
        desc = inspect.getfullargspec(func)
        try:
            inputs = {}
            for arg in desc.args:
                inputs[arg] = kwargs[arg]
            return func(**inputs)
        except:
            return ""
        finally:
            pass

    get_func.__name__ = func.__name__

    return get_func

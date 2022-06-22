# ======================================================================================================================

# Author: BERKYT

# ======================================================================================================================


class ExceptionStaticType(Exception):
    pass


def decorate_static_type(func):
    dict_args = func.__annotations__

    def wrap(*args, **kwargs):
        for tuple_args in zip(args, dict_args.values(), dict_args):
            if not isinstance(tuple_args[0], tuple_args[1]):
                raise ExceptionStaticType('Функция {}: '
                                          'Аргумент "{}" '
                                          'имеет тип "{}", а ожидался "{}".'.format(func.__name__,
                                                                                    tuple_args[2],
                                                                                    type(tuple_args[0]).__name__,
                                                                                    tuple_args[1].__name__))

        for tuple_args in zip(kwargs, dict_args):
            if not isinstance(kwargs[tuple_args[0]], dict_args[tuple_args[0]]):
                raise ExceptionStaticType('Функция {}: '
                                          'Аргумент "{}" '
                                          'имеет тип "{}", а ожидался "{}".'.
                                          format(func.__name__,
                                                 tuple_args[0],
                                                 type(kwargs[tuple_args[0]]).__name__,
                                                 type(tuple_args[0]).__name__))

        func_result = func(*args, **kwargs)

        if ((lambda key: key in dict_args.keys())('return') and
                isinstance(func_result, dict_args['return'])):
            pass
        elif not (lambda key: key in dict_args.keys())('return'):
            pass
        else:
            raise ExceptionStaticType('Функция {}: Возвращает "{}", а ожидалось "{}". '.
                                      format(func.__name__,
                                             type(func_result).__name__,
                                             dict_args['return'].__name__))

        return func_result

    return wrap

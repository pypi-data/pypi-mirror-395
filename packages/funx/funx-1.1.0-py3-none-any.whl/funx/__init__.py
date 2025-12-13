# Copyright (c) 2025 Khiat Mohammed Abderrezzak
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Author: Khiat Mohammed Abderrezzak <khiat.dev@gmail.com>


"""Python utility functions for cleaner, more readable code"""


from __future__ import annotations
from collections.abc import Iterator, Sized
from types import FunctionType, NoneType, UnionType
from typing import (
    Any,
    Dict,
    get_args,
    get_origin,
    List,
    Literal,
    Set,
    Tuple,
    Type,
    Union,
)


__all__: List = [
    "false",
    "fn",
    "func",
    "function",
    "none",
    "true",
    "array",
    "callables",
    "delattrs",
    "hasattrs",
    "isinstances",
    "issubsclass",
    "lens",
    "types",
]


false: bool = False


fn = FunctionType


func = FunctionType


function = FunctionType


none: NoneType = None


true: bool = True


def array(*args: Any) -> List[Any]:
    return list(args)


def callables(
    *objs: object, logic: str = "and"
) -> Union[bool, Tuple[bool, List[object]]]:

    # or "if not objs:" to enable all cases including 1 obj only at least
    if len(objs) < 2:

        raise TypeError(f"callables() takes at least two arguments ({len(objs)} given)")

    if logic != "and" and logic != "or":

        raise TypeError("logic type undefined !")

    missing: List[object] = []

    for obj in objs:

        if not callable(obj):

            missing.append(obj)

    if not missing:

        return True

    if len(missing) < len(objs):

        if logic == "and":

            return False, missing

        if logic == "or":

            return True, missing

    return False


def delattrs(
    *objs: object,
    attrname: Union[str, Tuple[str, ...]],
    logic: str = "mixed",
    match: bool = True,
    strict: bool = True,
) -> Union[bool, Tuple[bool, Union[Dict[object, Set[str]], List[object], List[str]]]]:

    if not objs:

        raise TypeError("delattrs expected at least 1 argument, got 0")

    # many to one
    if isinstance(attrname, str):

        # 1/2 or half of (one to one relationship) (enabling it)
        # if you just want to take the test, follow these steps :
        # write a new condition "if True:" on top of the current cond
        # comment the old and original condition "if len(objs) > 1:"
        # comment the last TypeError in this section
        # save and test :)

        # 1/2 or half of (one to one relationship) (disabling it again)
        # uncomment the old and original condition
        # remove 1 tab before it using (shift + tab)
        # remove the new condition on top of it
        # uncomment the last TypeError in this section
        # save and run :)

        # warning : if you want to remove this condition directly
        # to enable 1/2 or half of (one to one relationship) definitively
        # must first change the logic and handle it to work good
        # without this condition and with no errors

        if len(objs) > 1:

            missing: List[object] = []

            for obj in objs:

                try:

                    delattr(obj, attrname)

                except AttributeError as e0:

                    missing.append(obj)

            if logic == "mixed" or logic == "and":

                if not missing:

                    return True

                return False, missing

            if logic == "or":

                if not missing:

                    return True

                if len(missing) < len(objs):

                    return True, missing

                return False

            raise TypeError("logic type undefined !")

        raise TypeError(
            "length of objs must be greater than 1 in many to one relationship"
        )

    # one to many & many to one & many to many (with matching and without)
    if isinstance(attrname, tuple):

        if len(objs) > 1:

            missing: Dict[object, Set[str]] = {}

            if not match:

                if len(attrname) > 1:

                    for obj in objs:

                        for attr in attrname:

                            try:

                                delattr(obj, attr)

                            except AttributeError as e1:

                                if obj not in missing:

                                    missing[obj] = {attr}

                                if attr not in missing[obj]:

                                    missing[obj].add(attr)

                    if logic == "mixed" or logic == "and-or":

                        for value in missing.values():

                            if len(value) == len(attrname):

                                return False, missing

                        return True

                    if logic == "or-or":

                        if not missing:

                            return True

                        if len(missing) != len(objs):

                            return True, missing

                        for value in missing.values():

                            if len(value) != len(attrname):

                                return True, missing

                        return False

                    if logic == "or-and":

                        if not missing:

                            return True

                        if len(missing) < len(objs):

                            return True, missing

                        return False

                    if logic == "and-and":

                        if not missing:

                            return True

                        return False, missing

                    raise TypeError("logic type undefined !")

                return delattrs(*objs, attrname=attrname[0], logic=logic)

            if len(objs) != len(attrname):

                if strict:

                    raise TypeError(
                        "length of tuple of attrs names must match number of objects"
                    )

            for obj, attr in zip(objs, attrname):

                try:

                    delattr(obj, attr)

                except AttributeError as e2:

                    if obj not in missing:

                        missing[obj] = {attr}

                    if attr not in missing[obj]:

                        missing[obj].add(attr)

            if logic == "mixed" or logic == "and":

                if not missing:

                    return True

                return False, missing

            if logic == "or":

                if not missing:

                    return True

                if len(missing) < len(objs):

                    return True, missing

                return False

            raise TypeError("logic type undefined !")

        # 1/2 or half of (one to one relationship) (enabling it)
        # if you just want to take the test, follow these steps :
        # write a new condition "if True:" on top of the current cond
        # comment the old and original condition "if len(attrname) > 1:"
        # comment # 3 & # 4 and uncomment # 1 & # 2
        # comment the last TypeError in this section
        # save and test :)

        # 1/2 or half of (one to one relationship) (disabling it again)
        # uncomment the old and original condition
        # remove 1 tab before it using (shift + tab)
        # remove the new condition on top of it
        # comment # 1 & # 2 and uncomment # 3 & # 4
        # uncomment the last TypeError in this section
        # save and run :)

        # warning : if you want to remove this condition directly
        # to enable 1/2 or half of (one to one relationship) definitively
        # must first change the logic and handle it to work good
        # without this condition and with no errors

        if len(attrname) > 1:

            if not match:

                missing: List[str] = []

                for attr in attrname:

                    try:

                        delattr(objs[0], attr)

                    except AttributeError as e3:

                        missing.append(attr)

                if logic == "mixed" or logic == "or":

                    if not missing:

                        return True

                    if len(missing) < len(attrname):

                        return True, missing

                    return False

                if logic == "and":

                    if not missing:

                        return True

                    return False, missing

                raise TypeError("logic type undefined !")

            # if len(attrname) == 1 or not strict:  # 1

            #     return hasattr(objs[0], attrname[0])  # 2

            if not strict:  # 3

                raise TypeError("number of objects must be at least 2")  # 4

            raise TypeError(
                "length of objects must match number of tuple of attrs names"
            )

        raise TypeError(
            "length of tuple of attrs names must be greater than 1 in one to many relationship"
        )

    # one to many & many to one & many to many (without matching)
    if get_origin(attrname) is Literal:

        # Literal["x", "x"] is Literal["x"] duplicate values not accepted
        # Union["x", "x"] or ("x" | "x") is the same "x"
        args: Tuple[str] = get_args(attrname)

        if len(args) == 1:

            return delattrs(*objs, attrname=args[0], logic=logic)

        if len(objs) == 1:

            return delattrs(objs[0], attrname=args, match=False)

        if logic == "mixed" or logic == "and":

            return delattrs(*objs, attrname=args, match=False)

        if logic == "or":

            return delattrs(*objs, attrname=args, match=False, logic="or-or")

        raise TypeError("logic type undefined !")

    raise TypeError(
        "delattrs() kw arg 'attrname' must be a string, a tuple or a literal of strings"
    )


def hasattrs(
    *objs: object,
    attrname: Union[str, Tuple[str, ...]],
    logic: str = "mixed",
    match: bool = True,
    strict: bool = True,
) -> bool:

    if not objs:

        raise TypeError("hasattrs expected at least 1 argument, got 0")

    # many to one
    if isinstance(attrname, str):

        # 1/2 or half of (one to one relationship) (enabling it)
        # if you just want to take the test, follow these steps :
        # write a new condition "if True:" on top of the current cond
        # comment the old and original condition "if len(objs) > 1:"
        # comment the last TypeError in this section
        # save and test :)

        # 1/2 or half of (one to one relationship) (disabling it again)
        # uncomment the old and original condition
        # remove 1 tab before it using (shift + tab)
        # remove the new condition on top of it
        # uncomment the last TypeError in this section
        # save and run :)

        # warning : if you want to remove this condition directly
        # to enable 1/2 or half of (one to one relationship) definitively
        # must first change the logic and handle it to work good
        # without this condition and with no errors

        if len(objs) > 1:

            if logic == "mixed" or logic == "and":

                return all(hasattr(obj, attrname) for obj in objs)

            if logic == "or":

                return any(hasattr(obj, attrname) for obj in objs)

            raise TypeError("logic type undefined !")

        raise TypeError(
            "length of objects must be greater than 1 in many to one relationship"
        )

    # one to many & many to one & many to many (with matching and without)
    if isinstance(attrname, tuple):

        if len(objs) > 1:

            if not match:

                if len(attrname) > 1:

                    if logic == "mixed" or logic == "and-or":

                        return all(
                            any(hasattr(obj, attr) for attr in attrname) for obj in objs
                        )

                        # # or like this using recursion (one to many)
                        # return all(
                        #     hasattrs(obj, attrname=attrname, match=False)
                        #     for obj in objs
                        # )

                    if logic == "or-or":

                        return any(
                            any(hasattr(obj, attr) for attr in attrname) for obj in objs
                        )

                        # # or like this using recursion (one to many)
                        # return any(
                        #     hasattrs(obj, attrname=attrname, match=False)
                        #     for obj in objs
                        # )

                        # # or like this using recursion (many to one) (special case)
                        # return any(
                        #     hasattrs(*objs, attrname=attr, logic="or")
                        #     for attr in attrname
                        # )

                    if logic == "or-and":

                        return any(
                            all(hasattr(obj, attr) for attr in attrname) for obj in objs
                        )

                        # # or like this using recursion (one to many)
                        # return any(
                        #     hasattrs(obj, attrname=attrname, logic="and", match=False)
                        #     for obj in objs
                        # )

                    if logic == "and-and":

                        return all(
                            all(hasattr(obj, attr) for attr in attrname) for obj in objs
                        )

                        # # or like this using recursion (one to many)
                        # return all(
                        #     hasattrs(obj, attrname=attrname, logic="and", match=False)
                        #     for obj in objs
                        # )

                        # # or like this using recursion (many to one) (special case)
                        # return all(hasattrs(*objs, attrname=attr) for attr in attrname)

                    raise TypeError("logic type undefined !")

                return hasattrs(*objs, attrname=attrname[0], logic=logic)

            if len(objs) != len(attrname):

                if strict:

                    raise TypeError(
                        "length of tuple of attrs names must match number of objects"
                    )

            if logic == "mixed" or logic == "and":

                return all(hasattr(obj, attr) for obj, attr in zip(objs, attrname))

            if logic == "or":

                return any(hasattr(obj, attr) for obj, attr in zip(objs, attrname))

            raise TypeError("logic type undefined !")

        # 1/2 or half of (one to one relationship) (enabling it)
        # if you just want to take the test, follow these steps :
        # write a new condition "if True:" on top of the current cond
        # comment the old and original condition "if len(attrname) > 1:"
        # comment # 3 & # 4 and uncomment # 1 & # 2
        # comment the last TypeError in this section
        # save and test :)

        # 1/2 or half of (one to one relationship) (disabling it again)
        # uncomment the old and original condition
        # remove 1 tab before it using (shift + tab)
        # remove the new condition on top of it
        # comment # 1 & # 2 and uncomment # 3 & # 4
        # uncomment the last TypeError in this section
        # save and run :)

        # warning : if you want to remove this condition directly
        # to enable 1/2 or half of (one to one relationship) definitively
        # must first change the logic and handle it to work good
        # without this condition and with no errors

        if len(attrname) > 1:

            if not match:

                if logic == "mixed" or logic == "or":

                    return any(hasattr(objs[0], attr) for attr in attrname)

                if logic == "and":

                    return all(hasattr(objs[0], attr) for attr in attrname)

                raise TypeError("logic type undefined !")

            # if len(attrname) == 1 or not strict:  # 1

            #     return hasattr(objs[0], attrname[0])  # 2

            if not strict:  # 3

                raise TypeError("number of objects must be at least 2")  # 4

            raise TypeError(
                "length of objects must match number of tuple of attrs names"
            )

        raise TypeError(
            "length of tuple of attrs names must be greater than 1 in one to many relationship"
        )

    # one to many & many to one & many to many (without matching)
    if get_origin(attrname) is Literal:

        # Literal["x", "x"] is Literal["x"] duplicate values not accepted
        # Union["x", "x"] or ("x" | "x") is the same "x"
        args: Tuple[str] = get_args(attrname)

        if len(args) == 1:

            return hasattrs(*objs, attrname=args[0], logic=logic)

        if len(objs) == 1:

            return hasattrs(objs[0], attrname=args, match=False)

        if logic == "mixed" or logic == "and":

            return hasattrs(*objs, attrname=args, match=False)

        if logic == "or":

            return hasattrs(*objs, attrname=args, match=False, logic="or-or")

        raise TypeError("logic type undefined !")

    raise TypeError(
        "hasattrs() kw arg 'attrname' must be a string, a tuple or a literal of strings"
    )


def isinstances(
    *objs: object,
    datatype: Union[Type, Tuple[Type, ...], UnionType],
    logic: str = "and",
    match: bool = True,
    strict: bool = True,
) -> bool:

    # or "if not objs:" to enable all cases including 1 obj only at least
    if len(objs) < 2:

        raise TypeError(f"isinstances expected at least 2 arguments, got {len(objs)}")

    # (one to one , one to many) (disabled) & many to one , (many to many (without matching))
    if isinstance(datatype, type) or get_origin(datatype) is Union:

        try:

            if logic == "and":

                return all(map(datatype.__instancecheck__, objs))

            if logic == "or":

                return any(map(datatype.__instancecheck__, objs))

        except TypeError as e0:

            raise TypeError(
                "isinstances() kw arg 'datatype' must be a type, a tuple of types, or a union"
            ) from None

        raise TypeError("logic type undefined !")

    # (one to many) (disabled) & many to many (without matching)
    if isinstance(datatype, UnionType):

        if logic == "and":

            return all(map(Union[*get_args(datatype)].__instancecheck__, objs))

        if logic == "or":

            return any(map(Union[*get_args(datatype)].__instancecheck__, objs))

        raise TypeError("logic type undefined !")

        # # or like this using recursion
        # return isinstances(*objs, datatype=get_args(datatype), logic=logic, match=False)

    # (one to one , one to many) (disabled) & many to one , (many to many (with matching and without))
    if isinstance(datatype, tuple):

        if not match:

            try:

                if logic == "and":

                    return all(map(Union[*datatype].__instancecheck__, objs))

                if logic == "or":

                    return any(map(Union[*datatype].__instancecheck__, objs))

            except AttributeError as e1:

                raise TypeError(
                    "isinstances() kw arg 'datatype' must be a type, a tuple of types, or a union"
                ) from None

            raise TypeError("logic type undefined !")

        if len(objs) != len(datatype):

            if strict:

                raise TypeError("length of tuple of types must match number of objects")

        try:

            if logic == "and":

                return all(map(isinstance, objs, datatype))

            if logic == "or":

                return any(map(isinstance, objs, datatype))

        except TypeError as e2:

            raise TypeError(
                "isinstances() kw arg 'datatype' must be a type, a tuple of types, or a union"
            ) from None

        raise TypeError("logic type undefined !")

    # one to one (disabled) , many to one
    if get_origin(datatype) is not None:

        if logic == "and":

            return all(map(datatype.__instancecheck__, objs))

        if logic == "or":

            return any(map(datatype.__instancecheck__, objs))

        raise TypeError("logic type undefined !")

    raise TypeError(
        "isinstances() kw arg 'datatype' must be a type, a tuple of types, or a union"
    )


def issubsclass(
    *clss: Type,
    classname: Union[Type, Tuple[Type, ...], UnionType],
    logic: str = "mixed",
    match: bool = True,
    strict: bool = True,
) -> bool:

    # comment this lines :
    # 1, # 2, # 3, # 4, # 5, # 6, # 7, # 8, # 9
    # to enable full (one to one) relationship

    if not clss:

        raise TypeError(f"issubsclass expected at least 1 arguments, got {len(clss)}")

    # one to one (disabled) one to many & many to one , (many to many (without matching))
    if isinstance(classname, type) or get_origin(classname) is Union:

        if len(clss) == 1:  # 1

            if isinstance(classname, type) or len(get_args(classname)) == 1:  # 2

                raise TypeError("one to one relationship not allowed")  # 3

        try:

            if logic == "mixed" or logic == "and":

                return all(map(classname.__subclasscheck__, clss))

            if logic == "or":

                return any(map(classname.__subclasscheck__, clss))

        except TypeError as e0:

            raise TypeError("issubsclass() args must be classes") from None

        raise TypeError("logic type undefined !")

    # one to many & many to many (without matching)
    if isinstance(classname, UnionType):

        try:

            if logic == "mixed" or logic == "and":

                return all(map(Union[*get_args(classname)].__subclasscheck__, clss))

            if logic == "or":

                return any(map(Union[*get_args(classname)].__subclasscheck__, clss))

        except TypeError as e1:

            raise TypeError("issubsclass() args must be classes") from None

        raise TypeError("logic type undefined !")

        # # or like this using recursion
        # return issubsclass(
        #     *clss, classname=get_args(classname), logic=logic, match=False
        # )

    # one to one (disabled) one to many & many to one , (many to many (with matching and without))
    if isinstance(classname, tuple):

        if len(clss) == 1 and len(classname) == 1:  # 4

            raise TypeError("one to one relationship not allowed")  # 5

        if not match:

            if len(clss) == 1 and len(classname) > 1:

                try:

                    if logic == "mixed" or logic == "or":

                        for name in classname:

                            if issubclass(clss[0], name):

                                return True

                        return False

                    if logic == "and":

                        for name in classname:

                            if not issubclass(clss[0], name):

                                return False

                        return True

                except TypeError as e2:

                    raise TypeError("issubsclass() args must be classes") from None

                raise TypeError("logic type undefined !")

            if len(clss) > 1 and len(classname) == 1:

                try:

                    if logic == "mixed" or logic == "and":

                        return all(map(Union[classname[0]].__subclasscheck__, clss))

                    if logic == "or":

                        return any(map(Union[classname[0]].__subclasscheck__, clss))

                except TypeError as e3:

                    raise TypeError("issubsclass() args must be classes") from None

                raise TypeError("logic type undefined !")

            try:

                if logic == "mixed" or logic == "and-or":

                    return all(map(Union[*classname].__subclasscheck__, clss))

                    # # or like this using recursion (one to many)
                    # return all(
                    #     issubsclass(cl, classname=classname, match=False) for cl in clss
                    # )

                if logic == "or-or":

                    return any(map(Union[*classname].__subclasscheck__, clss))

                    # # or like this using recursion (one to many)
                    # return any(
                    #     issubsclass(cl, classname=classname, match=False) for cl in clss
                    # )

                    # # or like this using recursion (many to one) (special case)
                    # return any(
                    #     issubsclass(*clss, classname=clname, logic="or", match=False)
                    #     for clname in classname
                    # )

                if logic == "or-and":

                    for cl in clss:

                        for clname in classname:

                            if not issubclass(cl, clname):

                                break
                        else:

                            return True

                    return False

                    # # or like this using recursion (one to many)
                    # return any(
                    #     issubsclass(cl, classname=classname, logic="and", match=False)
                    #     for cl in clss
                    # )

                if logic == "and-and":

                    for cl in clss:

                        for clname in classname:

                            if not issubclass(cl, clname):

                                return False

                    return True

                    # # or like this using recursion (one to many)
                    # return all(
                    #     issubsclass(cl, classname=classname, logic="and", match=False)
                    #     for cl in clss
                    # )

                    # # or like this using recursion (many to one) (special case)
                    # return all(
                    #     issubsclass(*clss, classname=clname, match=False)
                    #     for clname in classname
                    # )

            except TypeError as e4:

                raise TypeError("issubsclass() args must be classes") from None

            raise TypeError("logic type undefined !")

        if len(clss) != len(classname):

            if strict:

                raise TypeError("length of tuple of types must match number of classes")

            if len(clss) == 1:  # 6

                raise TypeError("number of classes must be at least 2")  # 7

        try:

            if logic == "mixed" or logic == "and":

                return all(map(issubclass, clss, classname))

            if logic == "or":

                return any(map(issubclass, clss, classname))

        except TypeError as e5:

            raise TypeError("issubsclass() args must be classes") from None

        raise TypeError("logic type undefined !")

    # one to one (disabled) , many to one
    if get_origin(classname) is not None:

        if len(clss) == 1:  # 8

            raise TypeError("one to one relationship not allowed")  # 9

        try:

            if logic == "mixed" or logic == "and":

                return all(map(classname.__subclasscheck__, clss))

            if logic == "or":

                return any(map(classname.__subclasscheck__, clss))

        except TypeError as e6:

            raise TypeError("issubsclass() args must be classes") from None

        raise TypeError("logic type undefined !")

    raise TypeError(
        "issubsclass() kw arg 'classname' must be a class, a tuple of classes, or a union"
    )


def lens(*objs: Sized) -> Tuple[Union[int, Iterator[int]], bool]:
    """Return the lengths of one or more containers as a tuple contain a int or map object, and a bool of ints.

    Examples:
    >>> lens([1, 2, 3], "hello", {1, 2})
    (<map object at @ddress>, False)
    >>> lens([1, 2, 3], [4, 5, 6])
    (3, True)
    """

    # or "if not objs:" to enable all cases including 1 obj only at least
    if len(objs) < 2:

        raise TypeError(f"lens() takes at least two arguments ({len(objs)} given)")

    equal: bool = all(len(obj) == len(objs[0]) for obj in objs)

    if not equal:

        return map(len, objs), equal

    return len(objs[0]), equal


def types(*objs: object) -> Tuple[Union[Type, Iterator[Type]], bool]:
    """Return the types of one or more objects as a tuple contain a type or map object, and a bool of types.

    Examples:
    >>> types(1, "hi", [1, 2])
    (<map object at @ddress>, False)
    >>> types(1, 2)
    (<class 'int'>, True)
    """

    # or "if not objs:" to enable all cases including 1 obj only at least
    if len(objs) < 2:

        raise TypeError(f"types() takes at least two arguments ({len(objs)} given)")

    equal: bool = all(type(obj) == type(objs[0]) for obj in objs)

    if not equal:

        return map(type, objs), equal

    return type(objs[0]), equal


def _main() -> None:

    print("-----------callables-----------")

    # # one arg (disabled)
    # # use callable directly in this case is the best practice

    # print(callables(int))  # True
    # print(callables(1))  # False

    # two args +

    # AND

    print(callables(float, int, str))  # True

    print(callables(1.1, int, "one"))  # (False, [1.1, 'one'])

    print(callables(1.1, 1, "one"))  # False

    # OR

    print(callables(float, int, str, logic="or"))  # True

    print(callables(1.1, int, "one", logic="or"))  # (True, [1.1, 'one'])

    print(callables(1.1, 1, "one", logic="or"))  # False

    # ------------------------------

    # Class 1

    class C1:

        cattr: int = 1  # class attribute

        ca1: int = 2  # class attribute 1

        ca2: int = 3  # class attribute 2

        ca3: int = 5  # class attribute 3

        def __init__(self: C1) -> None:

            self.iattr: int = 7  # instance attribute

            self.ia1: int = 11  # instance attribute 1

            self.ia2: int = 13  # instance attribute 2

            self.ia3: int = 17  # instance attribute 3

    # Class 2

    class C2:

        cattr: int = 1  # class attribute

        ca1: int = 2  # class attribute 1

        ca2: int = 3  # class attribute 2

        ca3: int = 5  # class attribute 3

        def __init__(self: C2) -> None:

            self.iattr: int = 7  # instance attribute

            self.ia1: int = 11  # instance attribute 1

            self.ia2: int = 13  # instance attribute 2

            self.ia3: int = 17  # instance attribute 3

            self.siattr: int = 19  # special instance attribute

        scattr: int = 23  # special class attribute

    # Class 3

    class C3:

        cattr: int = 1  # class attribute

        ca1: int = 2  # class attribute 1

        ca2: int = 3  # class attribute 2

        ca3: int = 5  # class attribute 3

        def __init__(self: C3) -> None:

            self.iattr: int = 7  # instance attribute

            self.ia1: int = 11  # instance attribute 1

            self.ia2: int = 13  # instance attribute 2

            self.ia3: int = 17  # instance attribute 3

    i1: C1 = C1()  # C1 instance

    i2: C2 = C2()  # C2 instance

    i3: C3 = C3()  # C3 instance

    # print("-----------delattrs-----------")

    # # one to one (disabled)
    # # use delattr directly in this case is the best practice

    # print(delattrs(i1, attrname="iattr"))  # True
    # print(delattrs(C1, attrname="cattr"))  # True

    # print(delattrs(i1, attrname=("iattr",)))  # True
    # print(delattrs(C1, attrname=("cattr",)))  # True

    # print(delattrs(i1, attrname=Literal["iattr"]))  # True
    # print(delattrs(C1, attrname=Literal["cattr"]))  # True

    # print(delattrs(i1, attrname=("iattr",), match=False))  # True
    # print(delattrs(C1, attrname=("cattr",), match=False))  # True

    # print(delattrs(i1, attrname=("iattr",), strict=False))  # True
    # print(delattrs(C1, attrname=("cattr",), strict=False))  # True

    # Deceptive method (but also handeled when one to one disabled)

    # print(delattrs(i1, attrname=("iattr", "iatr"), strict=False))  # True
    # print(delattrs(C1, attrname=("cattr", "iatr"), strict=False))  # True

    # one to many

    # OR

    # print(delattrs(i1, attrname=Literal["ia1", "ia2", "ia3"]))  # True
    # print(delattrs(C1, attrname=Literal["ca1", "ca2", "ca3"]))  # True

    # print(
    #     delattrs(i1, attrname=Literal["iatt", "iatr", "iattr"])
    # )  # (True, ['iatt', 'iatr'])
    # print(
    #     delattrs(C1, attrname=Literal["catt", "catr", "cattr"])
    # )  # (True, ['catt', 'catr'])

    # print(delattrs(i1, attrname=Literal["iatt", "iatr", "iattrx"]))  # False
    # print(delattrs(C1, attrname=Literal["catt", "catr", "cattrx"]))  # False

    # print(delattrs(i1, attrname=("ia1", "ia2", "ia3"), match=False))  # True
    # print(delattrs(C1, attrname=("ca1", "ca2", "ca3"), match=False))  # True

    # print(
    #     delattrs(i1, attrname=("iatt", "iatr", "iattr"), match=False)
    # )  # (True, ['iatt', 'iatr'])
    # print(
    #     delattrs(C1, attrname=("catt", "catr", "cattr"), match=False)
    # )  # (True, ['catt', 'catr'])

    # print(delattrs(i1, attrname=("iatt", "iatr", "iattrx"), match=False))  # False
    # print(delattrs(C1, attrname=("catt", "catr", "cattrx"), match=False))  # False

    # AND

    # print(
    #     delattrs(i1, attrname=("ia1", "ia2", "ia3"), logic="and", match=False)
    # )  # True
    # print(
    #     delattrs(C1, attrname=("ca1", "ca2", "ca3"), logic="and", match=False)
    # )  # True

    # print(
    #     delattrs(i1, attrname=("iatt", "iatr", "iattr"), logic="and", match=False)
    # )  # (False, ['iatt', 'iatr'])
    # print(
    #     delattrs(C1, attrname=("catt", "catr", "cattr"), logic="and", match=False)
    # )  # (False, ['catt', 'catr'])

    # many to one

    # AND

    # print(delattrs(i1, i2, i3, attrname="iattr"))  # True
    # print(delattrs(C1, C2, C3, attrname="cattr"))  # True

    # # (False, [<__main__._main.<locals>.C1 object at @ddress>, <__main__._main.<locals>.C3 object at @ddress>])
    # print(delattrs(i1, i2, i3, attrname="siattr"))
    # # (False, [<class '__main__._main.<locals>.C1'>, <class '__main__._main.<locals>.C3'>])
    # print(delattrs(C1, C2, C3, attrname="scattr"))

    # print(delattrs(i1, i2, i3, attrname=Literal["iattr"]))  # True
    # print(delattrs(C1, C2, C3, attrname=Literal["cattr"]))  # True

    # # (False, [<__main__._main.<locals>.C1 object at @ddress>, <__main__._main.<locals>.C3 object at @ddress>])
    # print(delattrs(i1, i2, i3, attrname=Literal["siattr"]))
    # # (False, [<class '__main__._main.<locals>.C1'>, <class '__main__._main.<locals>.C3'>])
    # print(delattrs(C1, C2, C3, attrname=Literal["scattr"]))

    # print(delattrs(i1, i2, i3, attrname=("iattr",), match=False))  # True
    # print(delattrs(C1, C2, C3, attrname=("cattr",), match=False))  # True

    # # (False, [<__main__._main.<locals>.C1 object at @ddress>, <__main__._main.<locals>.C3 object at @ddress>])
    # print(delattrs(i1, i2, i3, attrname=("siattr",), match=False))
    # # (False, [<class '__main__._main.<locals>.C1'>, <class '__main__._main.<locals>.C3'>])
    # print(delattrs(C1, C2, C3, attrname=("scattr",), match=False))

    # OR

    # print(delattrs(i1, i2, i3, attrname="iattr", logic="or"))  # True
    # print(delattrs(C1, C2, C3, attrname="cattr", logic="or"))  # True

    # # (True, [<__main__._main.<locals>.C1 object at @ddress>, <__main__._main.<locals>.C3 object at @ddress>])
    # print(delattrs(i1, i2, i3, attrname="siattr", logic="or"))
    # # (True, [<class '__main__._main.<locals>.C1'>, <class '__main__._main.<locals>.C3'>])
    # print(delattrs(C1, C2, C3, attrname="scattr", logic="or"))

    # print(delattrs(i1, i2, i3, attrname="iatr", logic="or"))  # False
    # print(delattrs(C1, C2, C3, attrname="catr", logic="or"))  # False

    # print(delattrs(i1, i2, i3, attrname=Literal["iattr"], logic="or"))  # True
    # print(delattrs(C1, C2, C3, attrname=Literal["cattr"], logic="or"))  # True

    # # (True, [<__main__._main.<locals>.C1 object at @ddress>, <__main__._main.<locals>.C3 object at @ddress>])
    # print(delattrs(i1, i2, i3, attrname=Literal["siattr"], logic="or"))
    # # (True, [<class '__main__._main.<locals>.C1'>, <class '__main__._main.<locals>.C3'>])
    # print(delattrs(C1, C2, C3, attrname=Literal["scattr"], logic="or"))

    # print(delattrs(i1, i2, i3, attrname=Literal["iattrx"], logic="or"))  # False
    # print(delattrs(C1, C2, C3, attrname=Literal["cattrx"], logic="or"))  # False

    # print(delattrs(i1, i2, i3, attrname=("iattr",), logic="or", match=False))  # True
    # print(delattrs(C1, C2, C3, attrname=("cattr",), logic="or", match=False))  # True

    # # (True, [<__main__._main.<locals>.C1 object at @ddress>, <__main__._main.<locals>.C3 object at @ddress>])
    # print(delattrs(i1, i2, i3, attrname=("siattr",), logic="or", match=False))
    # # (True, [<class '__main__._main.<locals>.C1'>, <class '__main__._main.<locals>.C3'>])
    # print(delattrs(C1, C2, C3, attrname=("scattr",), logic="or", match=False))

    # print(delattrs(i1, i2, i3, attrname=("iattrx",), logic="or", match=False))  # False
    # print(delattrs(C1, C2, C3, attrname=("cattrx",), logic="or", match=False))  # False

    # many to many (pattern matching)

    # AND

    # print(delattrs(i1, i2, i3, attrname=("iattr", "iattr", "iattr")))  # True
    # print(delattrs(C1, C2, C3, attrname=("cattr", "cattr", "cattr")))  # True

    # # (False, {<__main__._main.<locals>.C3 object at @ddress>: {'iattrx'}})
    # print(delattrs(i1, i2, i3, attrname=("iattr", "iattr", "iattrx")))
    # # (False, {<class '__main__._main.<locals>.C3'>: {'cattrx'}})
    # print(delattrs(C1, C2, C3, attrname=("cattr", "cattr", "cattrx")))

    # OR

    # print(
    #     delattrs(i1, i2, i3, attrname=("iattr", "iattr", "iattr"), logic="or")
    # )  # True
    # print(
    #     delattrs(C1, C2, C3, attrname=("cattr", "cattr", "cattr"), logic="or")
    # )  # True

    # # (True, {<__main__._main.<locals>.C3 object at @ddress>: {'iattrx'}})
    # print(delattrs(i1, i2, i3, attrname=("iattr", "iattr", "iattrx"), logic="or"))
    # # (True, {<class '__main__._main.<locals>.C3'>: {'cattrx'}})
    # print(delattrs(C1, C2, C3, attrname=("cattr", "cattr", "cattrx"), logic="or"))

    # print(
    #     delattrs(i1, i2, i3, attrname=("iattrx", "iattrx", "iattrx"), logic="or")
    # )  # False
    # print(
    #     delattrs(C1, C2, C3, attrname=("cattrx", "cattrx", "cattrx"), logic="or")
    # )  # False

    # many to many (without matching)

    # AND

    # print(delattrs(i1, i2, i3, attrname=Literal["iatt", "iatr", "iattr"]))  # True
    # print(delattrs(C1, C2, C3, attrname=Literal["catt", "catr", "cattr"]))  # True

    # # (False, {<__main__._main.<locals>.C1 object at @ddress>: {'iatt', 'iattrx', 'siattr'}, <__main__._main.<locals>.C2 object at @ddress>: {'iatt', 'iattrx'}, <__main__._main.<locals>.C3 object at @ddress>: {'iatt', 'iattrx', 'siattr'}})
    # print(delattrs(i1, i2, i3, attrname=Literal["iatt", "siattr", "iattrx"]))
    # # (False, {<class '__main__._main.<locals>.C1'>: {'cattrx', 'scattr', 'catt'}, <class '__main__._main.<locals>.C2'>: {'cattrx', 'catt'}, <class '__main__._main.<locals>.C3'>: {'cattrx', 'scattr', 'catt'}})
    # print(delattrs(C1, C2, C3, attrname=Literal["catt", "scattr", "cattrx"]))

    # AND-OR

    # print(delattrs(i1, i2, i3, attrname=("iatt", "iatr", "iattr"), match=False))  # True
    # print(delattrs(C1, C2, C3, attrname=("catt", "catr", "cattr"), match=False))  # True

    # # (False, {<__main__._main.<locals>.C1 object at @ddress>: {'iattrx', 'siattr', 'iatt'}, <__main__._main.<locals>.C2 object at @ddress>: {'iattrx', 'iatt'}, <__main__._main.<locals>.C3 object at @ddress>: {'iattrx', 'siattr', 'iatt'}})
    # print(delattrs(i1, i2, i3, attrname=("iatt", "siattr", "iattrx"), match=False))
    # # (False, {<class '__main__._main.<locals>.C1'>: {'scattr', 'cattrx', 'catt'}, <class '__main__._main.<locals>.C2'>: {'cattrx', 'catt'}, <class '__main__._main.<locals>.C3'>: {'scattr', 'cattrx', 'catt'}})
    # print(delattrs(C1, C2, C3, attrname=("catt", "scattr", "cattrx"), match=False))

    # OR

    # print(
    #     delattrs(i1, i2, i3, attrname=Literal["ia1", "iattr", "ia2"], logic="or")
    # )  # True
    # print(
    #     delattrs(C1, C2, C3, attrname=Literal["ca1", "cattr", "ca2"], logic="or")
    # )  # True

    # print(
    #     delattrs(i1, i2, i3, attrname=Literal["iatt", "iatr", "siattr"], logic="or")
    # )  # (True, {<__main__._main.<locals>.C1 object at @ddress>: {'iatt', 'siattr', 'iatr'}, <__main__._main.<locals>.C2 object at @ddress>: {'iatt', 'iatr'}, <__main__._main.<locals>.C3 object at @ddress>: {'iatt', 'siattr', 'iatr'}})
    # print(
    #     delattrs(C1, C2, C3, attrname=Literal["catt", "catr", "scattr"], logic="or")
    # )  # (True, {<class '__main__._main.<locals>.C1'>: {'catr', 'catt', 'scattr'}, <class '__main__._main.<locals>.C2'>: {'catr', 'catt'}, <class '__main__._main.<locals>.C3'>: {'catr', 'catt', 'scattr'}})

    # print(
    #     delattrs(i1, i2, i3, attrname=Literal["iatt", "iatr", "iattrx"], logic="or")
    # )  # False
    # print(
    #     delattrs(C1, C2, C3, attrname=Literal["catt", "catr", "cattrx"], logic="or")
    # )  # False

    # OR-OR

    # print(
    #     delattrs(
    #         i1, i2, i3, attrname=("ia1", "iattr", "ia2"), logic="or-or", match=False
    #     )
    # )  # True
    # print(
    #     delattrs(
    #         C1, C2, C3, attrname=("ca1", "cattr", "ca2"), logic="or-or", match=False
    #     )
    # )  # True

    # print(
    #     delattrs(
    #         i1, i2, i3, attrname=("iatt", "iatr", "siattr"), logic="or-or", match=False
    #     )
    # )  # (True, {<__main__._main.<locals>.C1 object at @ddress>: {'iatt', 'siattr', 'iatr'}, <__main__._main.<locals>.C2 object at @ddress>: {'iatt', 'iatr'}, <__main__._main.<locals>.C3 object at @ddress>: {'iatt', 'siattr', 'iatr'}})
    # print(
    #     delattrs(
    #         C1, C2, C3, attrname=("catt", "catr", "scattr"), logic="or-or", match=False
    #     )
    # )  # (True, {<class '__main__._main.<locals>.C1'>: {'catr', 'scattr', 'catt'}, <class '__main__._main.<locals>.C2'>: {'catr', 'catt'}, <class '__main__._main.<locals>.C3'>: {'catr', 'scattr', 'catt'}})

    # print(
    #     delattrs(
    #         i1, i2, i3, attrname=("iatt", "iatr", "iattrx"), logic="or-or", match=False
    #     )
    # )  # False
    # print(
    #     delattrs(
    #         C1, C2, C3, attrname=("catt", "catr", "cattrx"), logic="or-or", match=False
    #     )
    # )  # False

    # OR-AND

    # print(
    #     delattrs(
    #         i1, i2, i3, attrname=("ia1", "ia2", "ia3"), logic="or-and", match=False
    #     )
    # )  # True
    # print(
    #     delattrs(
    #         C1, C2, C3, attrname=("ca1", "ca2", "ca3"), logic="or-and", match=False
    #     )
    # )  # True

    # print(
    #     delattrs(
    #         i1, i2, i3, attrname=("ia1", "siattr", "ia2"), logic="or-and", match=False
    #     )
    # )  # (True, {<__main__._main.<locals>.C1 object at @ddress>: {'siattr'}, <__main__._main.<locals>.C3 object at @ddress>: {'siattr'}})
    # print(
    #     delattrs(
    #         C1, C2, C3, attrname=("ca1", "scattr", "ca2"), logic="or-and", match=False
    #     )
    # )  # (True, {<class '__main__._main.<locals>.C1'>: {'scattr'}, <class '__main__._main.<locals>.C3'>: {'scattr'}})

    # print(
    #     delattrs(
    #         i1, i2, i3, attrname=("iatt", "iatr", "iattrx"), logic="or-and", match=False
    #     )
    # )  # False
    # print(
    #     delattrs(
    #         C1, C2, C3, attrname=("catt", "catr", "cattrx"), logic="or-and", match=False
    #     )
    # )  # False

    # AND-AND

    # print(delattrs(i1, i2, i3, attrname=("ia1", "ia2", "ia3"), logic="and-and", match=False))  # True
    # print(delattrs(C1, C2, C3, attrname=("ca1", "ca2", "ca3"), logic="and-and", match=False))  # True

    # print(
    #     delattrs(
    #         i1, i2, i3, attrname=("ia1", "siattr", "ia2"), logic="and-and", match=False
    #     )
    # )  # (False, {<__main__._main.<locals>.C1 object at @ddress>: {'siattr'}, <__main__._main.<locals>.C3 object at @ddress>: {'siattr'}})
    # print(
    #     delattrs(
    #         C1, C2, C3, attrname=("ca1", "scattr", "ca2"), logic="and-and", match=False
    #     )
    # )  # (False, {<class '__main__._main.<locals>.C1'>: {'scattr'}, <class '__main__._main.<locals>.C3'>: {'scattr'}})

    # many to many (pattern matching without strict mode)

    # AND

    # print(
    #     delattrs(
    #         i1,
    #         i2,
    #         i3,
    #         attrname=("iattr", "iattr", "iattr", "iatt", "iatr"),
    #         strict=False,
    #     )
    # )  # True
    # print(
    #     delattrs(
    #         C1,
    #         C2,
    #         C3,
    #         attrname=("cattr", "cattr", "cattr", "catt", "catr"),
    #         strict=False,
    #     )
    # )  # True

    # print(
    #     delattrs(
    #         i1,
    #         i2,
    #         i3,
    #         attrname=("iattr", "iattr", "iattrx", "iatt", "iatr"),
    #         strict=False,
    #     )
    # )  # (False, {<__main__._main.<locals>.C3 object at @ddress>: {'iattrx'}})
    # print(
    #     delattrs(
    #         C1,
    #         C2,
    #         C3,
    #         attrname=("cattr", "cattr", "cattrx", "catt", "catr"),
    #         strict=False,
    #     )
    # )  # (False, {<class '__main__._main.<locals>.C3'>: {'cattrx'}})

    # OR

    # print(
    #     delattrs(
    #         i1,
    #         i2,
    #         i3,
    #         attrname=("iattr", "iattr", "iattr", "iatt", "iatr"),
    #         logic="or",
    #         strict=False,
    #     )
    # )  # True
    # print(
    #     delattrs(
    #         C1,
    #         C2,
    #         C3,
    #         attrname=("cattr", "cattr", "cattr", "catt", "catr"),
    #         logic="or",
    #         strict=False,
    #     )
    # )  # True

    # print(
    #     delattrs(
    #         i1,
    #         i2,
    #         i3,
    #         attrname=("iattr", "iattr", "iattrx", "iatt", "iatr"),
    #         logic="or",
    #         strict=False,
    #     )
    # )  # (True, {<__main__._main.<locals>.C3 object at @ddress>: {'iattrx'}})
    # print(
    #     delattrs(
    #         C1,
    #         C2,
    #         C3,
    #         attrname=("cattr", "cattr", "cattrx", "catt", "catr"),
    #         logic="or",
    #         strict=False,
    #     )
    # )  # (True, {<class '__main__._main.<locals>.C3'>: {'cattrx'}})

    # print(
    #     delattrs(
    #         i1,
    #         i2,
    #         i3,
    #         attrname=("iattrx", "iattrx", "iattrx", "iatt", "iatr"),
    #         logic="or",
    #         strict=False,
    #     )
    # )  # False
    # print(
    #     delattrs(
    #         C1,
    #         C2,
    #         C3,
    #         attrname=("cattrx", "cattrx", "cattrx", "catt", "catr"),
    #         logic="or",
    #         strict=False,
    #     )
    # )  # False

    print("-----------hasattrs-----------")

    # # one to one (disabled)
    # # use hasattr directly in this case is the best practice

    # print(hasattrs(i1, attrname="iattr"))  # True
    # print(hasattrs(i1, attrname="cattr"))  # True
    # print(hasattrs(C1, attrname="cattr"))  # True

    # print(hasattrs(i1, attrname=("iattr",)))  # True
    # print(hasattrs(i1, attrname=("cattr",)))  # True
    # print(hasattrs(C1, attrname=("cattr",)))  # True

    # print(hasattrs(i1, attrname=Literal["iattr"]))  # True
    # print(hasattrs(i1, attrname=Literal["cattr"]))  # True
    # print(hasattrs(C1, attrname=Literal["cattr"]))  # True

    # print(hasattrs(i1, attrname=("iattr",), match=False))  # True
    # print(hasattrs(i1, attrname=("cattr",), match=False))  # True
    # print(hasattrs(C1, attrname=("cattr",), match=False))  # True

    # print(hasattrs(i1, attrname=("iattr",), strict=False))  # True
    # print(hasattrs(i1, attrname=("cattr",), strict=False))  # True
    # print(hasattrs(C1, attrname=("cattr",), strict=False))  # True

    # Deceptive method (but also handeled when one to one disabled)

    # print(hasattrs(i1, attrname=("iattr", "iatr"), strict=False))  # True
    # print(hasattrs(i1, attrname=("cattr", "iatr"), strict=False))  # True
    # print(hasattrs(C1, attrname=("cattr", "iatr"), strict=False))  # True

    # one to many

    print(hasattrs(i1, attrname=Literal["iatt", "iatr", "iattr"]))  # True
    print(hasattrs(i1, attrname=Literal["catt", "catr", "cattr"]))  # True
    print(hasattrs(C1, attrname=Literal["catt", "catr", "cattr"]))  # True

    print(hasattrs(i1, attrname=("iatt", "iatr", "iattr"), match=False))  # True
    print(hasattrs(i1, attrname=("catt", "catr", "cattr"), match=False))  # True
    print(hasattrs(C1, attrname=("catt", "catr", "cattr"), match=False))  # True

    print(
        hasattrs(i1, attrname=("ia1", "ia2", "ia3"), logic="and", match=False)
    )  # True
    print(
        hasattrs(i1, attrname=("ca1", "ca2", "ca3"), logic="and", match=False)
    )  # True
    print(
        hasattrs(C1, attrname=("ca1", "ca2", "ca3"), logic="and", match=False)
    )  # True

    # many to one

    # AND

    print(hasattrs(i1, i2, i3, attrname="iattr"))  # True
    print(hasattrs(i1, i2, i3, attrname="cattr"))  # True
    print(hasattrs(C1, C2, C3, attrname="cattr"))  # True

    print(hasattrs(i1, i2, i3, attrname=Literal["iattr"]))  # True
    print(hasattrs(i1, i2, i3, attrname=Literal["cattr"]))  # True
    print(hasattrs(C1, C2, C3, attrname=Literal["cattr"]))  # True

    print(hasattrs(i1, i2, i3, attrname=("iattr",), match=False))  # True
    print(hasattrs(i1, i2, i3, attrname=("cattr",), match=False))  # True
    print(hasattrs(C1, C2, C3, attrname=("cattr",), match=False))  # True

    # OR

    print(hasattrs(i1, i2, i3, attrname="siattr", logic="or"))  # True
    print(hasattrs(i1, i2, i3, attrname="scattr", logic="or"))  # True
    print(hasattrs(C1, C2, C3, attrname="scattr", logic="or"))  # True

    print(hasattrs(i1, i2, i3, attrname=Literal["siattr"], logic="or"))  # True
    print(hasattrs(i1, i2, i3, attrname=Literal["scattr"], logic="or"))  # True
    print(hasattrs(C1, C2, C3, attrname=Literal["scattr"], logic="or"))  # True

    print(hasattrs(i1, i2, i3, attrname=("siattr",), logic="or", match=False))  # True
    print(hasattrs(i1, i2, i3, attrname=("scattr",), logic="or", match=False))  # True
    print(hasattrs(C1, C2, C3, attrname=("scattr",), logic="or", match=False))  # True

    # many to many (pattern matching)

    # AND

    print(hasattrs(i1, i2, i3, attrname=("iattr", "iattr", "iattr")))  # True
    print(hasattrs(i1, i2, i3, attrname=("cattr", "cattr", "cattr")))  # True
    print(hasattrs(C1, C2, C3, attrname=("cattr", "cattr", "cattr")))  # True

    # OR

    print(hasattrs(i1, i2, i3, attrname=("iatt", "siattr", "iatr"), logic="or"))  # True
    print(hasattrs(i1, i2, i3, attrname=("catt", "scattr", "catr"), logic="or"))  # True
    print(hasattrs(C1, C2, C3, attrname=("catt", "scattr", "catr"), logic="or"))  # True

    # many to many (without matching)

    # AND

    print(hasattrs(i1, i2, i3, attrname=Literal["iatt", "iatr", "iattr"]))  # True
    print(hasattrs(i1, i2, i3, attrname=Literal["catt", "catr", "cattr"]))  # True
    print(hasattrs(C1, C2, C3, attrname=Literal["catt", "catr", "cattr"]))  # True

    # AND-OR

    print(hasattrs(i1, i2, i3, attrname=("iatt", "iatr", "iattr"), match=False))  # True
    print(hasattrs(i1, i2, i3, attrname=("catt", "catr", "cattr"), match=False))  # True
    print(hasattrs(C1, C2, C3, attrname=("catt", "catr", "cattr"), match=False))  # True

    # OR

    print(
        hasattrs(
            i1,
            i2,
            i3,
            attrname=Literal["iatt", "iatr", "siattr"],
            logic="or",
            match=False,
        )
    )  # True
    print(
        hasattrs(
            i1,
            i2,
            i3,
            attrname=Literal["catt", "catr", "scattr"],
            logic="or",
            match=False,
        )
    )  # True
    print(
        hasattrs(
            C1,
            C2,
            C3,
            attrname=Literal["catt", "catr", "scattr"],
            logic="or",
            match=False,
        )
    )  # True

    # OR-OR

    print(
        hasattrs(
            i1,
            i2,
            i3,
            attrname=("iatt", "iatr", "siattr"),
            logic="or-or",
            match=False,
        )
    )  # True
    print(
        hasattrs(
            i1,
            i2,
            i3,
            attrname=("catt", "catr", "scattr"),
            logic="or-or",
            match=False,
        )
    )  # True
    print(
        hasattrs(
            C1,
            C2,
            C3,
            attrname=("catt", "catr", "scattr"),
            logic="or-or",
            match=False,
        )
    )  # True

    # OR-AND

    print(
        hasattrs(
            i1,
            i2,
            i3,
            attrname=("ia1", "iattr", "siattr"),
            logic="or-and",
            match=False,
        )
    )  # True
    print(
        hasattrs(
            i1,
            i2,
            i3,
            attrname=("ca1", "cattr", "scattr"),
            logic="or-and",
            match=False,
        )
    )  # True
    print(
        hasattrs(
            C1,
            C2,
            C3,
            attrname=("ca1", "cattr", "scattr"),
            logic="or-and",
            match=False,
        )
    )  # True

    # AND-AND

    print(
        hasattrs(
            i1,
            i2,
            i3,
            attrname=("ia1", "ia2", "ia3"),
            logic="and-and",
            match=False,
        )
    )  # True
    print(
        hasattrs(
            i1,
            i2,
            i3,
            attrname=("ca1", "ca2", "ca3"),
            logic="and-and",
            match=False,
        )
    )  # True
    print(
        hasattrs(
            C1,
            C2,
            C3,
            attrname=("ca1", "ca2", "ca3"),
            logic="and-and",
            match=False,
        )
    )  # True

    # many to many (pattern matching without strict mode)

    # AND

    print(
        hasattrs(
            i1,
            i2,
            i3,
            attrname=("iattr", "iattr", "iattr", "iatt", "iatr"),
            strict=False,
        )
    )  # True
    print(
        hasattrs(
            i1,
            i2,
            i3,
            attrname=("cattr", "cattr", "cattr", "catt", "catr"),
            strict=False,
        )
    )  # True
    print(
        hasattrs(
            C1,
            C2,
            C3,
            attrname=("cattr", "cattr", "cattr", "catt", "catr"),
            strict=False,
        )
    )  # True

    # OR

    print(
        hasattrs(
            i1,
            i2,
            i3,
            attrname=("iatt", "siattr", "iatr", "iatt", "iatr"),
            logic="or",
            strict=False,
        )
    )  # True
    print(
        hasattrs(
            i1,
            i2,
            i3,
            attrname=("catt", "scattr", "catr", "catt", "catr"),
            logic="or",
            strict=False,
        )
    )  # True
    print(
        hasattrs(
            C1,
            C2,
            C3,
            attrname=("catt", "scattr", "catr", "catt", "catr"),
            logic="or",
            strict=False,
        )
    )  # True

    print("----------isinstances----------")

    # # one to one (disabled)
    # # use isinstance directly in this case is the best practice

    # print(isinstances(3, datatype=int))  # True

    # print(isinstances(int, datatype=Type))  # True

    # print(isinstances(3, datatype=Union[int]))  # True

    # # match=True and strict=True (default)
    # print(isinstances(3, datatype=(int,)))  # True

    # # match=False and strict=True
    # # but when match=False, strict don't matter True or False
    # print(isinstances(3, datatype=(int,), match=False))  # True

    # # match=True and strict=False
    # # in this case take just int with 3 the second type ignored
    # print(isinstances(3, datatype=(int, str), strict=False))  # True

    # print(isinstances(3, datatype=(int | float,)))  # True

    # print(isinstances(3, datatype=(Union[int, float],)))  # True

    # print(isinstances(3, datatype=(int | float, int | float), strict=False))  # True

    # print(
    #     isinstances(3, datatype=(Union[int, float], Union[int, float]), strict=False)
    # )  # True

    # # one to many (disabled)
    # # use isinstance directly in this case is the best practice

    # print(isinstances(3, datatype=int | float))  # True

    # print(isinstances(3, datatype=Union[int, float]))  # True

    # print(isinstances(3, datatype=(int, float), match=False))  # True

    # many to one

    # AND

    print(isinstances(int, str, datatype=Type))  # True

    print(isinstances(3, 7, datatype=int))  # True

    print(isinstances(3, 7, datatype=Union[int]))  # True

    print(isinstances(3, 7, datatype=(int,), match=False))  # True

    # OR

    print(isinstances(int, "1", datatype=Type, logic="or"))  # True

    print(isinstances(3, 7.0, datatype=int, logic="or"))  # True

    print(isinstances(3, 7.0, datatype=Union[int], logic="or"))  # True

    print(isinstances(3, 7.0, datatype=(int,), logic="or", match=False))  # True

    # many to many

    # AND

    print(isinstances(3, 7, datatype=int | float))  # True

    print(isinstances(3, 7, datatype=Union[int, float]))  # True

    print(isinstances(3, 7, datatype=(int, float), match=False))  # True

    # OR

    print(isinstances(3, "7", datatype=int | float, logic="or"))  # True

    print(isinstances(3, "7", datatype=Union[int, float], logic="or"))  # True

    print(isinstances(3, "7", datatype=(int, float), logic="or", match=False))  # True

    # pattern matching |
    #                  v

    # AND (with strict mode)

    print(isinstances(3, 7, datatype=(int, int)))  # True

    print(isinstances(3, 7, datatype=(int | float, int | float)))  # True

    print(isinstances(3, 7, datatype=(Union[int, float], Union[int, float])))  # True

    # AND (without strict mode)

    print(isinstances(3, 7, datatype=(int, int, float), strict=False))  # True

    print(
        isinstances(3, 7, datatype=(int | float, int | float, str | bool), strict=False)
    )  # True

    print(
        isinstances(
            3,
            7,
            datatype=(Union[int, float], Union[int, float], Union[str, bool]),
            strict=False,
        )
    )  # True

    # OR (with strict mode)

    print(isinstances(3, 7, datatype=(int, float), logic="or"))  # True

    print(isinstances(3, 7, datatype=(int | float, str | float), logic="or"))  # True

    print(
        isinstances(3, 7, datatype=(Union[int, float], Union[str, float]), logic="or")
    )  # True

    # OR (without strict mode)

    print(
        isinstances(3, 7, datatype=(int, str, float), logic="or", strict=False)
    )  # True

    print(
        isinstances(
            3,
            7,
            datatype=(int | NoneType, str | float, bool | complex),
            logic="or",
            strict=False,
        )
    )  # True

    print(
        isinstances(
            3,
            7,
            datatype=(Union[int, type], Union[str, float], Union[bool, complex]),
            logic="or",
            strict=False,
        )
    )  # True

    print("----------issubsclass----------")

    # # one to one (disabled)
    # # use issubclass directly in this case is the best practice

    # print(issubsclass(bool, classname=int))  # True

    # print(issubsclass(type, classname=Type))  # True

    # print(issubsclass(bool, classname=Union[int]))  # True

    # # match=True and strict=True (default)
    # print(issubsclass(bool, classname=(int,)))  # True

    # # match=False and strict=True
    # # but when match=False, strict don't matter True or False
    # print(issubsclass(bool, classname=(int,), match=False))  # True

    # # match=True and strict=False
    # # in this case take just int with bool the second class ignored
    # print(issubsclass(bool, classname=(int, str), strict=False))  # True

    # print(issubsclass(bool, classname=(int | float,)))  # True

    # print(issubsclass(bool, classname=(int | float, int | float), strict=False))  # True

    # print(issubsclass(bool, classname=(Union[int, float],)))  # True

    # print(
    #     issubsclass(
    #         bool, classname=(Union[int, float], Union[int, float]), strict=False
    #     )
    # )  # True

    # one to many

    print(issubsclass(bool, classname=int | float))  # True

    print(issubsclass(bool, classname=Union[int, float]))  # True

    # OR

    print(issubsclass(bool, classname=(int, float), match=False))  # True

    # AND

    print(issubsclass(bool, classname=(int, object), logic="and", match=False))  # True

    # many to one

    # AND

    print(issubsclass(Type, type, classname=Type))  # True

    print(issubsclass(int, bool, classname=object))  # True

    print(issubsclass(int, bool, classname=Union[object]))  # True

    print(issubsclass(int, bool, classname=(object,), match=False))  # True

    # OR

    print(issubsclass(int, type, classname=Type, logic="or"))  # True

    print(issubsclass(bool, str, classname=int, logic="or"))  # True

    print(issubsclass(bool, str, classname=Union[int], logic="or"))  # True

    print(issubsclass(bool, str, classname=(int,), logic="or", match=False))  # True

    # many to many

    # AND

    print(issubsclass(int, bool, classname=object | float))  # True

    print(issubsclass(int, bool, classname=Union[object, float]))  # True

    # OR

    print(issubsclass(str, bool, classname=int | float, logic="or"))  # True

    print(issubsclass(str, bool, classname=Union[int, float], logic="or"))  # True

    # AND-OR

    print(issubsclass(int, bool, classname=(object, float), match=False))  # True

    # OR-OR

    print(
        issubsclass(str, bool, classname=(int, float), logic="or-or", match=False)
    )  # True

    # OR-AND

    print(
        issubsclass(str, bool, classname=(int, object), logic="or-and", match=False)
    )  # True

    # AND-AND

    print(
        issubsclass(int, bool, classname=(int, object), logic="and-and", match=False)
    )  # True

    # pattern matching |
    #                  v

    # AND (with strict mode)

    print(issubsclass(int, bool, classname=(object, int)))  # True

    print(issubsclass(int, bool, classname=(object | float, int | str)))  # True

    print(
        issubsclass(int, bool, classname=(Union[object, float], Union[int, str]))
    )  # True

    # AND (without strict mode)

    print(issubsclass(int, bool, classname=(object, int, float), strict=False))  # True

    print(
        issubsclass(
            int,
            bool,
            classname=(object | float, int | str, bool | complex),
            strict=False,
        )
    )  # True

    print(
        issubsclass(
            int,
            bool,
            classname=(Union[object, float], Union[int, str], Union[bool, complex]),
            strict=False,
        )
    )  # True

    # OR (with strict mode)

    print(issubsclass(int, bool, classname=(str, int), logic="or"))  # True

    print(
        issubsclass(str, bool, classname=(complex | float, int | str), logic="or")
    )  # True

    print(
        issubsclass(
            int, bool, classname=(Union[complex, float], Union[int, str]), logic="or"
        )
    )  # True

    # OR (without strict mode)

    print(
        issubsclass(int, bool, classname=(str, int, float), logic="or", strict=False)
    )  # True

    print(
        issubsclass(
            int,
            bool,
            classname=(type(None) | float, int | str, bool | complex),
            logic="or",
            strict=False,
        )
    )  # True

    print(
        issubsclass(
            int,
            bool,
            classname=(Union[type, float], Union[int, str], Union[bool, complex]),
            logic="or",
            strict=False,
        )
    )  # True

    print("-------------lens-------------")

    # # one arg (disabled)
    # # use len directly in this case is the best practice

    # print(lens([1, 3, 5]))  # (3, True)

    # two args +

    # (<map object at @ddress>, False)
    print(lens([1, 3, 5], "hello", {1, 3}))

    print(lens([1, 3, 5], [7, 9, 11]))  # (3, True)

    print("-------------types-------------")

    # # one arg (disabled)
    # # use type directly in this case is the best practice

    # print(types(1))  # (<class 'int'>, True)

    # two args +

    print(types(1, "hi", [1, 3]))  # (<map object at @ddress>, False)

    print(types(1, 3))  # (<class 'int'>, True)

    print("------------------------------")

    print("125 tests passed")

    print("153 tests are commented")

    print("total tests : 278")

    print("============ funx ============")


if __name__ == "__main__":
    _main()  # testing

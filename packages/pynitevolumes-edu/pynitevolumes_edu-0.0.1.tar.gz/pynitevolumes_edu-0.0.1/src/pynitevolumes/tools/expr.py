#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module for symbolic computations.

A module to provide basic tools to manipulate analytical functions
in a Numpy friendly way. It provides a micro formal language to
manipulate formal expressions and a conversion tool for fast evaluation
by Numpy.

Expressions are instances of the `Expr` class but it is most of the time
not needed to use the constructor. To create expressions, the best way
is to use `parse` on a string using letter names as variables. Some
functions are constructed with the idea that 'X' and 'Y' are the
variable names for the coordinates of a generic point in a 2d space so
it may be best to stick to this convention (even though it is not
mandatory).

Once the expression is created it can be manipulated using other
functions of this module. Note that arithmetic operations are defined on
`Expr` object which has the effect that one can easily put `Expr`
instance in arrays and use linear algebra to manipulate these arrays of
`Expr`.

Finally the purpose should be to evaluate an expression on a given
context. This must somehow be done through Python eval() function. Since
this is always a liability, the module does not make use of eval() but
provides `ev` and `ev_array` to produce strings to be passed to eval().
Note that in the context where eval() is used, `numpy` must have been
imported as `np`.

Warning
-------
Do not pass to `eval()` any string that you don't trust.

Notes
-----
This module has been created to automatize some classical symbolic
manipulations in the context of testing numerical schemes for PDE and
make this work with Numpy vectorization for efficiency. Do not
expect much more of this module than that.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
from copy import deepcopy
if TYPE_CHECKING:
    from typing import Literal, Self
    from collections.abc import Collection, Sequence

_sep = {'[', '(', ','}
_ops = {'+', '-', '*', '/', 'neg', '**'}
_ws = {' ', '\t', '\n'}


class ParseError(ValueError):
    """Error occuring during parsing of strings into Expr."""

    def __init__(self, expr: str, position: int, details: str | None = None):
        self.pos = position
        msg = f'Function parse encountered a probleme while parsing "{expr}". '
        msg += f'The problem occured at position {position}'
        super().__init__(msg)
        if details:
            self.add_note(details)


class Expr:
    """Mathematical expressions.

    Instances of the Expr class can be manipulated as formal
    mathematical expressions can, using the usual arithmetic operations
    notations of Python.

    `Expr` is not meant to be directly instantiated.


    Notes
    -----
    An `Expr` object is a tree-like object. The class implements
    arithmetic operations on `Expr` objects to construct the resulting
    `Expr`. Implicit conversion of int and float to Expr object is
    implemented during arithmetic operations. Printing an `Expr` object
    produces a string resembling the underlying mathematical expression.
    """

    def __repr__(self) -> str:
        """Represent the instance."""
        return (self.__class__.__name__ + '('
                + ', '.join([f"{k}={v}" for k, v in vars(self).items()
                            if k != 'children']) + ')')

    def tree(self, start: int = 0) -> str:
        """Return a tree-like representation of instance as a string."""
        s = repr(self)
        if not hasattr(self, 'children') or not self.children:
            return s
        else:
            for ch in reversed(self.children):
                sc = ch.tree(start+1)
                s += '\n'+(start+1)*'\t'+sc
            return s

    def __add__(self, other: object) -> Expr:
        """Return new 'op' instance with name '+'."""
        o: Expr
        if isinstance(self, Empty):
            if isinstance(other, Expr):
                return other
            else:
                return NotImplemented
        if isinstance(other, (int, float)):
            o = Numeric(other)
        elif isinstance(other, Empty):
            return self
        elif isinstance(other, Expr):
            o = other
        else:
            return NotImplemented
        return Operation('+', o, self)

    def __radd__(self, other: object) -> Expr:
        """Return new 'op' instance with name '+'."""
        o: Expr
        if isinstance(self, Empty):
            if isinstance(other, Expr):
                return other
            else:
                return NotImplemented
        if isinstance(other, (int, float)):
            o = Numeric(other)
        elif isinstance(other, Empty):
            return self
        elif isinstance(other, Expr):
            o = other
        else:
            return NotImplemented
        return Operation('+', self, o)

    def __mul__(self, other: object) -> Expr:
        """Return new 'op' instance with name '*'."""
        o: Expr
        if isinstance(self, Empty):
            if isinstance(other, Expr):
                return other
            else:
                return NotImplemented
        if isinstance(other, (int, float)):
            o = Numeric(other)
        elif isinstance(other, Empty):
            return self
        elif isinstance(other, Expr):
            o = other
        else:
            return NotImplemented
        return Operation('*', o, self)

    def __rmul__(self, other: object) -> Expr:
        """Return new 'op' instance with name '*'."""
        o: Expr
        if isinstance(self, Empty):
            if isinstance(other, Expr):
                return other
            else:
                return NotImplemented
        if isinstance(other, (int, float)):
            o = Numeric(other)
        elif isinstance(other, Empty):
            return self
        elif isinstance(other, Expr):
            o = other
        else:
            return NotImplemented
        return Operation('*', self, o)

    def __neg__(self) -> Expr:
        """Return new 'op' instance with name 'neg'."""
        if isinstance(self, Empty):
            return self
        return Operation('neg', self)

    def __sub__(self, other: object) -> Expr:
        """Return new 'op' instance with name '-'."""
        o: Expr
        if isinstance(self, Empty):
            if isinstance(other, Expr):
                return Operation('neg', other)
            else:
                return NotImplemented
        if isinstance(other, (int, float)):
            o = Numeric(other)
        elif isinstance(other, Empty):
            return self
        elif isinstance(other, Expr):
            o = other
        else:
            return NotImplemented
        return Operation('-', o, self)

    def __rsub__(self, other: object) -> Expr:
        """Return new 'op' instance with name '-'."""
        o: Expr
        if isinstance(self, Empty):
            if isinstance(other, Expr):
                return other
            else:
                return NotImplemented
        if isinstance(other, (int, float)):
            o = Numeric(other)
        elif isinstance(other, Empty):
            return self
        elif isinstance(other, Expr):
            o = other
        else:
            return NotImplemented
        return Operation('-', self, o)

    def __truediv__(self, other: object) -> Expr:
        """Return new 'op' instance with name '/'."""
        o: Expr
        if isinstance(self, Empty):
            if isinstance(other, Expr):
                return other
            else:
                return NotImplemented
        if isinstance(other, (int, float)):
            o = Numeric(other)
        elif isinstance(other, Empty):
            return self
        elif isinstance(other, Expr):
            o = other
        else:
            return NotImplemented
        return Operation('/', o, self)

    def __rtruediv__(self, other: object) -> Expr:
        """Return new 'op' instance with name '/'."""
        o: Expr
        if isinstance(self, Empty):
            if isinstance(other, Expr):
                return other
            else:
                return NotImplemented
        if isinstance(other, (int, float)):
            o = Numeric(other)
        elif isinstance(other, Empty):
            return self
        elif isinstance(other, Expr):
            o = other
        else:
            return NotImplemented
        return Operation('/', self, o)

    def __pow__(self, other: object) -> Expr:
        """Return new 'op' instance with name '**'."""
        o: Expr
        if isinstance(self, Empty):
            if isinstance(other, Expr):
                return other
            else:
                return NotImplemented
        if isinstance(other, (int, float)):
            o = Numeric(other)
        elif isinstance(other, Empty):
            return self
        elif isinstance(other, Expr):
            o = other
        else:
            return NotImplemented
        return Operation('**', o, self)

    def __rpow__(self, other: object) -> Expr:
        """Return new 'op' instance with name '**'."""
        o: Expr
        if isinstance(self, Empty):
            if isinstance(other, Expr):
                return other
            else:
                return NotImplemented
        if isinstance(other, (int, float)):
            o = Numeric(other)
        elif isinstance(other, Empty):
            return self
        elif isinstance(other, Expr):
            o = other
        else:
            return NotImplemented
        return Operation('**', self, o)

    def __eq__(self, other: object) -> bool:
        """Compare expressions through their strings."""
        return str(self) == str(other)

    def __ne__(self, other: object) -> bool:
        """Compare expressions through their strings."""
        return str(self) != str(other)

    def _simplify(self) -> Expr:
        return self

    def simplify(self) -> Expr:
        """Simplify an expression.

        Returns
        -------
        Expr
            A simplified version of the expression.

        Notes
        -----
        The simplification process is very coarse and one should not
        expect too much of it. The process is applied iteratively so
        that the result of the function is not modified by another
        application of the simplify method yields no further change.
        Simplifications taken into account are essentially adding or
        substracting 0 and multiplying or dividing by 1.
        """
        snp1 = self._simplify()
        sn = self
        while snp1 != sn:
            sn = snp1
            snp1 = sn._simplify()
        return sn

    def __bool__(self) -> bool:
        """Return False if self is Empty, True otherwise."""
        return True


class Empty(Expr):
    """Empty mathematical expression."""

    def __str__(self) -> str:
        """Return the empty string."""
        return ''

    def __bool__(self) -> bool:
        """Return False."""
        return False


class Atom(Expr):
    """Atomic expressions."""

    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        """Return the name of the atom."""
        return self.name


class Numeric(Expr):
    """Numbers."""

    def __init__(self, value: int | float):
        self.value = value

    def __str__(self) -> str:
        """Return the value as a string."""
        return str(self.value)


class Operation(Expr):
    """Arithmetic operations."""

    def __init__(self, name: Literal['+', '-', '*', '/', 'neg', '**'],
                 *children: Expr):
        if name not in _ops:
            raise ValueError('Unknown operator.')
        self.name = name
        self.children = list(children)

    def __str__(self) -> str:
        """Return the name of the operation inbetween its children."""
        if self.name in {'+', '-', '*', '/', '**'}:
            v, u = self.children
            if isinstance(u, (Empty, Numeric, Atom)):
                part_u = str(u)
            else:
                part_u = '(' + str(u) + ')'
            if isinstance(v, (Empty, Numeric, Atom)):
                part_v = str(v)
            else:
                part_v = '(' + str(v) + ')'
            return f"{part_u}{self.name}{part_v}"
        else:
            return (f'-({self.children[0]})')

    def _simplify(self) -> Expr:
        if self.name == '+':
            v, u = self.children
            if isinstance(u, Numeric) and u.value == 0:
                return v._simplify()
            if isinstance(v, Numeric) and v.value == 0:
                return u._simplify()
            if isinstance(u, Numeric) and isinstance(v, Numeric):
                return Numeric(u.value+v.value)
        if self.name == '-':
            v, u = self.children
            if isinstance(u, Numeric) and u.value == 0:
                return (-v)._simplify()
            if isinstance(v, Numeric) and v.value == 0:
                return u._simplify()
        if self.name == 'neg':
            u = self.children[0]
            if isinstance(u, Numeric):
                return Numeric(-u.value)
            if isinstance(u, Operation) and u.name == 'neg':
                return u.children[0]._simplify()
        if self.name == '*':
            v, u = self.children
            if (isinstance(u, Numeric) and u.value == 0
               or isinstance(v, Numeric) and v.value == 0):
                return Numeric(0)
            if isinstance(u, Numeric) and u.value == 1:
                return v._simplify()
            if isinstance(v, Numeric) and v.value == 1:
                return u._simplify()
            if isinstance(u, Numeric) and isinstance(v, Numeric):
                return Numeric(u.value*v.value)
        if self.name == '/':
            v, u = self.children
            if isinstance(v, Numeric) and v.value == 1:
                return u._simplify()
            if isinstance(u, Numeric) and isinstance(v, Numeric):
                return Numeric(u.value/v.value)
        if self.name == '**':
            n, u = self.children
            if isinstance(u, Numeric) and isinstance(n, Numeric):
                return Numeric(u.value**n.value)
            if isinstance(n, Numeric) and n.value == 1:
                return u._simplify()
        return Operation(self.name, *[c._simplify() for c in self.children])


class Function(Expr):
    """Functions.

    For functions, the `call` mechanism is akin to composition.

    """

    def __init__(self, name: str, arity: int = 1, *children: Expr):
        self.name = name
        self.arity = arity
        if not children:
            self.children = []
        else:
            if len(children) != arity:
                raise ValueError("Attempting to pass more children than "
                                 + " arity of function.")
            else:
                self.children = list(children)

    def __str__(self) -> str:
        """Return the name of the function followed by its children."""
        arg_list = ''
        for c in reversed(self.children):
            arg_list += f'{c.__str__()}, '
        return f'{self.name}({arg_list[:-2]})'

    def __call__(self, e: object) -> Self | Function:
        """Compose of function with an expression."""
        if self.children:
            raise ValueError("Expression is not a pure function, it "
                             + "has already been composed.")
        if self.arity == 0:
            if isinstance(e, Empty):
                return self
            else:
                raise ValueError("Wrong number of arguments in call.")
        else:
            if isinstance(e, (List, Tuple)):
                if self.arity == len(e):
                    return Function(self.name, self.arity, *e.children)
                elif self.arity == 1:
                    return Function(self.name, self.arity, e)
                else:
                    raise ValueError("Wrong number of arguments in call.")
            elif isinstance(e, Expr):
                if self.arity != 1:
                    raise ValueError("Wrong number of arguments in call.")
                else:
                    return Function(self.name, self.arity, e)
        raise TypeError("Function can only be composed with expressions.")

    def _simplify(self) -> Expr:
        return Function(self.name, self.arity,
                        *[c._simplify() for c in self.children])


class List(Expr):
    """Lists."""

    def __init__(self, *children: Expr):
        self.children = list(children)

    def __len__(self) -> int:
        """Return number of elements."""
        return len(self.children)

    def __str__(self) -> str:
        """Return children separated by commas inbetween parens."""
        arg_list = ''
        for c in reversed(self.children):
            arg_list += f'{c.__str__()}, '
        return f'[{arg_list[:-2]}]'

    def _simplify(self) -> Expr:
        return List(*[c._simplify() for c in self.children])


class Tuple(Expr):
    """Tuples."""

    def __init__(self, *children: Expr):
        self.children = list(children)

    def __len__(self) -> int:
        """Return number of elements."""
        return len(self.children)

    def __str(self) -> str:
        """Return children separated by commas inbetween brackets."""
        arg_list = ''
        for c in reversed(self.children):
            arg_list += f'{c.__str__()}, '
        return f'({arg_list[:-2]})'

    def _simplify(self) -> Expr:
        return Tuple(*[c._simplify() for c in self.children])


def _var_string(x: str | Atom) -> str:
    """Return a string containing a variable name."""
    if isinstance(x, str):
        return x
    elif isinstance(x, Atom):
        return x.name


#: Numeric : constant 0 as an expression.
ZERO = Numeric(0)

#: Numeric : constant 1 as an expression.
ONE = Numeric(1)

#: Function : natural exponential function.
exp = Function('exp')

#: Function : natural logarithm function.
log = Function('log')

#: Function : cosine function.
cos = Function('cos')

#: Function : sine function.
sin = Function('sin')

#: Function : tangent function.
tan = Function('tan')

#: Function : cotangent function.
cotan = Function('cotan')

#: Function : hyperbolic cosine function.
cosh = Function('cosh')

#: Function : hyperbolic sine function.
sinh = Function('sinh')

#: Function : hyperbolic tangent function.
tanh = Function('tanh')

#: Function : hyperbolic cotangent function.
cotanh = Function('cotanh')

#: Function : square root function.
sqrt = Function('sqrt')

#: Function : absolute value function.
abs = Function('abs')
"""Expr : absolute value function."""

#: Function : array function.
array = Function('array')

_np_fun = {'exp', 'log', 'cos', 'sin', 'tan', 'cotan', 'cosh',
           'sinh', 'tanh', 'cotanh', 'sqrt', 'abs', 'array'}


def _list_expr(le: Expr | tuple[Expr] | list[Expr]) -> Expr:
    """Create an Expr of type 'list'/'tuple' from a sequence of Expr."""
    if isinstance(le, Expr):
        return le
    elif isinstance(le, tuple):
        return Tuple(*[_list_expr(e) for e in reversed(le)])
    else:
        return List(*[_list_expr(e) for e in reversed(le)])


def array_expr(A: Expr | tuple[Expr] | list[Expr]) -> Expr:
    """Create an Expr representing an array of Expr.

    Parameters
    ----------
    A : array_like of Expr

    Returns
    -------
    Expr
        Expression abstracting the construction of an array from `A`.

    Notes
    -----
    One would typically manipulate real arrays of `Expr` to benefit from
    the arithmetic of `Expr` before using `array_expr` on the resulting
    array and passing the result to `ev_array` for vectorized
    evaluation.
    """
    return array(_list_expr(A))


def _diff(expr: Expr, var: str | Atom) -> Expr:
    """Differentiate known expressions with respect to var.

    Parameters
    ----------
    expr : Expr
        Expression to be derived.
    var : str or Atom
        Name of the variable with respect to which we derive.

    Returns
    -------
    Expr
        Derivative of `expr`.

    Notes
    -----
    These are preconstructed rules of derivation when they are known.
    Applies linearity of derivation, leibniz rule, quotient rule, chain
    rule and differentiation of known elementary functions. For other
    abstract functions inserts a D_i symbol to express derivation with
    respect to variable i of the function. Beware that no Schwarz rule
    is enforced and this feature should only be used with caution.
    """
    var_s = _var_string(var)
    if isinstance(expr, Empty):
        return expr
    if isinstance(expr, Numeric):
        return ZERO
    if isinstance(expr, Atom):
        if expr.name == var_s:
            return ONE
        else:
            return ZERO
    if isinstance(expr, Operation):
        if expr.name in {'+', '-', 'neg'}:
            return Operation(expr.name,
                             *[_diff(c, var_s) for c in expr.children]
                             ).simplify()
        if expr.name == '*':
            v, u = expr.children
            return (_diff(u, var_s)*v+u*_diff(v, var_s)
                    ).simplify()
        if expr.name == '/':
            v, u = expr.children
            return (_diff(u, var_s)/v-u*_diff(v, var_s)/v**2
                    ).simplify()
        if expr.name == '**':
            n, u = expr.children
            if isinstance(n, Numeric):
                return ((n.value)*_diff(u, var_s)*u**(n.value-1)
                        ).simplify()
            else:
                return ((_diff(n, var_s)*Function('log', 1, u)
                         + n*_diff(u, var_s)/u)*(u**n)).simplify()
    if isinstance(expr, (Tuple, List)):
        u = expr.children
        return type(expr)(*[_diff(component, var_s) for component in u])
    if isinstance(expr, Function):
        if expr.name == 'exp':
            u = expr.children[0]
            return (_diff(u, var_s)*expr).simplify()
        if expr.name == 'log':
            u = expr.children[0]
            return (_diff(u, var_s)/u).simplify()
        if expr.name == 'cos':
            u = expr.children[0]
            return (_diff(u, var_s)*(-sin(u))).simplify()
        if expr.name == 'sin':
            u = expr.children[0]
            return (_diff(u, var_s)*cos(u)).simplify()
        if expr.name == 'tan':
            u = expr.children[0]
            return (_diff(u, var_s)/cos(u)**2).simplify()
        if expr.name == 'cotan':
            u = expr.children[0]
            return (-_diff(u, var_s)/sin(u)**2).simplify()
        if expr.name == 'cosh':
            u = expr.children[0]
            return (_diff(u, var_s)*sinh(u)).simplify()
        if expr.name == 'sinh':
            u = expr.children[0]
            return (_diff(u, var_s)*cosh(u)).simplify()
        if expr.name == 'tanh':
            u = expr.children[0]
            return (_diff(u, var_s)/cosh(u)**2).simplify()
        if expr.name == 'cotanh':
            u = expr.children[0]
            return (-_diff(u, var_s)/sinh(u)**2).simplify()
        if expr.name == 'sqrt':
            u = expr.children[0]
            return (_diff(u, var_s)/(2*sqrt(u))).simplify()
        if expr.name not in _np_fun:
            n = len(expr.children)
            r = Empty()
            for i in range(n):
                r += (_diff(expr.children[n-i-1], var_s)
                      * Function(f'D_{i}{expr.name}', expr.arity,
                                 *expr.children)
                      ).simplify()
                return r.simplify()
    raise TypeError("Unkown method for differentiating expression.")


def diff(expr: Expr,
         var: str | Atom | tuple[str | Atom, int],
         *args: str | Atom | tuple[str | Atom, int]) -> Expr:
    """Apply mathematical differentiation to an expression.

    Parameters
    ----------
    expr : Expr
        The expression to be differentiated.
    var : str or Atom or tuple of (str or Atom, int)
        Variable with respect to which differentiation is taken or a
        sequence of a variable and an `int` containing the order of the
        differentiation.
    *args : str or Atom or tuple (str or Atom, int)
        Subsequent variables for higher order differentiation.

    Returns
    -------
    Expr
        If var is (x, n) computes the n-th derivative of expr with
        respect to x. If var is x, effectively treats it as (x, 1). If
        several sequences (x_i, n_i) are given computes the derivative
        of order sum(n_i) with respect to all the variables.
    """

    def unpack(v: str | Atom | tuple[str | Atom, int]
               ) -> tuple[str | Atom, int]:
        if isinstance(v, tuple):
            return v
        else:
            return v, 1
    if args:
        q = (var,) + args
    else:
        q = (var,)
    r = expr
    for v in q:
        x, n = unpack(v)
        for _ in range(n):
            r = _diff(r, x)
    return r


def laplacian(expr: Expr, *var_list: str | Atom) -> Expr:
    """Compute the laplacian of an expression.

    Parameters
    ----------
    expr : Expr
        The expression to be differentiated.
    *var_list : sequence of str or Atom
        The variable names with respect to which the differentiation
        must occur.

    Returns
    -------
    Expr
        Sum of all the second order derivatives of `expr` with respect
        to the variables appearing in `*var_list`.
    """
    r = sum((diff(expr, (xi, 2)) for xi in var_list), Empty())
    return r.simplify()


def gradient(expr: Expr, *var_list: str | Atom) -> list[Expr]:
    """Compute the gradient of an expression.

    Parameters
    ----------
    expr : Expr
        The expression to be differentiated.
    *var_list : sequence of str or Atom
        The variables names with respect to which the differentiation
        must occur.

    Returns
    -------
    list[Expr]
        List of partial derivatives with respect to each var.

    """
    return [diff(expr, xi) for xi in var_list]


def divergence(expr_iter: Collection[Expr], var_iter: Sequence[str | Atom]
               ) -> Expr:
    """Compute the divergence of a vector field.

    Parameters
    ----------
    expr_iter : sequence of Expr
        The components of the vector field.
    var_iter : sequence of str or Atom
        The sequence of variables with respect to which the
        differentiation must occur.

    Raises
    ------
    ValueError
       The two sequences must have the same length.

    Returns
    -------
    Expr
        Divergence of the vector field.

    """
    if len(expr_iter) != len(var_iter):
        raise ValueError('Dimension mismatch for the divergence:'
                         + f' {len(expr_iter)} components and {len(var_iter)}'
                         + ' variables.')
    else:
        r = sum((diff(ui, xi) for (ui, xi) in zip(expr_iter, var_iter)),
                Empty())
        return r.simplify()


def ev(expr: Expr, **where: int | float | Expr) -> str:
    """Prepare the evaluation of an Expr object.

    Parameters
    ----------
    expr : Expr
        The expression to be evaluated.
    **where: int or float or expr
        Arguments should be set in the form `name=value` where
        `value` can be any `Expr` or numeric value.

    Returns
    -------
    str
        String literal to be passed to eval().

    Notes
    -----
    The intent for the string is to be such that it could have been
    hand-written as a command that, using the package NumPy would
    produce the desired result. Note that ev() basically only replaces
    function names known to NumPy by the 'np.' + name and variables by
    other expressions known in the context of the eval() computation.

    Examples
    --------
        >>> e = parse('tan(a*b)')
        >>> ev(e, a='np.pi')
        'np.tan((np.pi*b))'
        >>> ev(e, a='np.pi', b=0.25)
        'np.tan((np.pi*0.25))'
        >>> eval(ev(e, a='np.pi', b=0.25))
        0.9999999999999999
        >>> def f(x):
            return x**2
        >>> e = parse('f(a+b)')
        >>> ev(e, a=0.1, b=0.2)
        'f((0.1+0.2))'
        >>> eval(ev(e, a=0.1, b=0.2), globals())
        0.09000000000000002
        >>>(0.1+0.2)**2
        0.09000000000000002
    """
    if isinstance(expr, Atom):
        if expr.name in where:
            return str(toExpr(where[expr.name]))
        elif expr.name == 'pi':
            return 'np.pi'
        else:
            return expr.name
    if isinstance(expr, Empty):
        return 'None'
    if isinstance(expr, Numeric):
        return str(expr.value)
    if isinstance(expr, Operation):
        if expr.name in {'+', '-', '*', '/', '**'}:
            return (f'({ev(expr.children[-1], **where)}{expr.name}'
                    + f'{ev(expr.children[0], **where)})')
        else:
            return f'(-{ev(expr.children[0], **where)})'
    if isinstance(expr, Function):
        if expr.name in _np_fun:
            return f'np.{expr.name}({ev(expr.children[0], **where)})'
        else:
            arg_eval = ''
            for c in reversed(expr.children):
                arg_eval += f'{ev(c, **where)}, '
            return f'{expr.name}({arg_eval[:-2]})'
    if isinstance(expr, Tuple):
        arg_eval = ''
        for c in reversed(expr.children):
            arg_eval += f'{ev(c, **where)}, '
        return f'({arg_eval[:-2]})'
    if isinstance(expr, List):
        arg_eval = ''
        for c in reversed(expr.children):
            arg_eval += f'{ev(c, **where)}, '
        return f'[{arg_eval[:-2]}]'
    raise TypeError("Unkown method for evaluating expression.")


def ev_array(expr: Expr, var_list: Sequence[str] = 'XY',
             array_name: str = 'x'
             ) -> str:
    """Prepare the evaluation of expression on an array.

    Return a string where variables have been replaced by the entries
    of the last dimension of an array with given name.

    Parameters
    ----------
    expr : Expr
        Expression to be evaluated.
    var_list : sequence of string, optional
        Sequence of variable names in order. The default is 'XY'.
    array_name : str, optional
        Name of the array on which evaluation occurs. The default is
        'x'.

    Returns
    -------
    str
        String literal to be passed to eval().

    Notes
    -----
    The purpose of this function is to evaluate an expression with d
    variables on the last axis of `array_name` which should then have
    dimension (at least) 2 for its last axis. The function creates a
    string that can then be passed to eval() and would be the statement
    you would have to write and execute to obtain this result.
    By default there are only two variables named `'X'` and `'Y'`,
    meaning that the default is to use two-variables expression to be
    applied to arrays with last axis 2.

    A common pattern to use this function is to create vectorized
    functions from expressions:

    .. code-block:: python

        def f(x):
            x = np.array(x)
            return eval(ev_array(expr_f))

    where `expr_f` is an expression involving only the variables `X` and
    `Y`. The function `f` can then be applied to any array with last
    axis of dimension (at least) 2.
    """
    expr = expr.simplify()
    n = len(var_list)
    for i in range(n):
        if isinstance(expr, Atom):
            if expr.name == var_list[i]:
                return f'{array_name}[..., {i}]'
            elif expr.name == 'pi':
                return 'np.pi'
        if isinstance(expr, Empty):
            return f'np.empty({array_name}[..., 0].shape)'
        if isinstance(expr, Numeric):
            return f'{expr.value}*np.ones({array_name}[..., 0].shape)'
        if isinstance(expr, Operation):
            if expr.name in {'+', '-', '*', '/', '**'}:
                v, u = expr.children
                if isinstance(u, Numeric):
                    rev0 = str(u.value)
                else:
                    rev0 = ev_array(u, var_list, array_name)
                if isinstance(v, Numeric):
                    rev1 = str(v.value)
                else:
                    rev1 = ev_array(v, var_list, array_name)
                return f'({rev0}{expr.name}{rev1})'
            if expr.name == 'neg':
                rev = ev_array(expr.children[0], var_list, array_name)
                return f'(-{rev})'
        if isinstance(expr, Function):
            if expr.name in _np_fun:
                rev = ev_array(expr.children[0], var_list, array_name)
                return f'np.{expr.name}({rev})'
            else:
                arg_eval = ''
                for c in reversed(expr.children):
                    arg_eval += f'{ev_array(c, var_list, array_name)}, '
                return f'{expr.name}({arg_eval[:-2]})'
        if isinstance(expr, Tuple):
            arg_eval = ''
            for c in reversed(expr.children):
                arg_eval += f'{ev_array(c, var_list, array_name)}, '
            return f'({arg_eval[:-2]})'
        if isinstance(expr, List):
            arg_eval = ''
            for c in reversed(expr.children):
                arg_eval += f'{ev_array(c, var_list, array_name)}, '
            return f'[{arg_eval[:-2]}]'
    raise TypeError('Ukown method for evaluating expression')


def subs(expr: Expr, **where: int | float | Expr) -> Expr:
    """Substitute an atom with another expression.

    Parameters
    ----------
    expr : Expr
        Expression in which the substitution is made.
    **where : int or float or Expr
        List of replacements to make given as arguments of the form
        `name=replacement`.

    Returns
    -------
    Expr
        Expression obtained after recursively replaced each `Expr` of
        `type`, `atom` with `replacement`.

    See Also
    --------
    ev, ev_array

    Notes
    -----
    Contrary to `ev` and `ev_array`, subs returns another `Expr` and
    thus should always be applied before the aforementioned functions
    when needed.
    """
    if isinstance(expr, Atom) and expr.name in where:
        return toExpr(where[expr.name])
    elif hasattr(expr, 'children'):
        new_children = []
        for c in expr.children:
            new_children.append(subs(c, **where))
        res = deepcopy(expr)
        res.children = new_children
        return res
    else:
        return expr


def toExpr(other: int | float | Expr) -> Expr:
    """Transform int, float or Expr to an Expr."""
    if isinstance(other, (int, float)):
        o = Numeric(other)
    elif isinstance(other, Expr):
        o = other
    else:
        raise TypeError("toExpr operates on int, float or Expr only")
    return o


def _trimpar(expr_str: str) -> str:
    """Remove superfluous outer parentheses. It keeps at least one."""
    L = len(expr_str)
    if L == 0:
        return expr_str

    def hasextrapar(e: str) -> bool:
        s = len(e)
        if e[0] != '(':
            return False
        lvl = 1
        for j in range(1, s):
            if e[j] == '(':
                lvl += 1
            if e[j] == ')':
                lvl -= 1
            if lvl == 0:
                break
        return j == s-1
    m = 0
    while hasextrapar(expr_str[m:L-m]):
        m += 1
    if m >= 2:
        return expr_str[m-1:L-m+1]
    else:
        return expr_str


def _get_priority(op: str) -> int:
    """Obtain priority of arithmetic op operation."""
    if op in {'+', '-'}:
        return 1
    if op in {'*', '/'}:
        return 2
    return 3


def _prioritize(expr: str) -> str:
    """Put parentheses in string expression to explicit op priority."""
    n = len(expr)

    def update(im: int, ip: int) -> None:
        # Add a pair of parentheses to protect an operation at indexes im
        # and ip
        nonlocal n
        n += 2
        nonlocal expr
        expr = expr[:im+1] + '(' + expr[im+1:ip] + ')' + expr[ip:]

    def findblockbound(i0: int, n: int, p: int, left: bool) -> int:
        # Start at index i0 and move left or right to find the beginning
        # or the end of a block containing  only op of similar priority.
        if left:
            mov = -1
            uplvl = ')'
            downlvl = '('

            def test(i: int) -> bool:
                return (i >= 0 and expr[i] != '[')
        else:
            mov = 1
            uplvl = '('
            downlvl = ')'

            def test(i: int) -> bool:
                return (i < n and expr[i] != ']')
        j = i0
        lvl = 0
        while test(j) and (expr[j] not in _ops
                           or _get_priority(expr[j]) >= p
                           or lvl > 0):
            if expr[j] in {downlvl, ','} and lvl == 0:
                break
            elif expr[j] == downlvl:
                lvl -= 1
            elif expr[j] == uplvl:
                lvl += 1
            j = j + mov
            # Keep moving until you encounter an operation with less priority
            # or if you encounter a parenthesis that protects your priority.
        return j

    i = 0
    while i < n:
        if expr[i] not in _ops or expr[i] == '+':
            i += 1
            continue
        if expr[i] == '-':
            # Minus get special treatment as it can mean two things provided
            # something is before or not
            if i == 0 or expr[i-1] == '(':  # neg case
                ip = findblockbound(i+1, n, 2, False)
                update(i-1, ip)
                i += 2
                continue
            else:
                i += 1
                continue
        try:
            if expr[i] == '*' and expr[i+1] == '*':
                # * Must be separated because it could be the start of **
                im = findblockbound(i-1, n, 3, True)
                ip = findblockbound(i+2, n, 3, False)
                update(im, ip)
                i += 3
                continue
        except IndexError:
            raise ParseError(expr, i, 'Ending with a single *')
        p = _get_priority(expr[i])
        im = findblockbound(i-1, n, p, True)
        ip = findblockbound(i+1, n, p, False)
        update(im, ip)
        i += 2
    return _trimpar(expr)


def _parse(expr: str) -> Expr:
    """Parse a well-formed string to construct its Expr representation.

    Parameters
    ----------
    expr : str
        Mathematical expression written in a string.

    Raises
    ------
    ValueError
        Tuples must be enclosed between parentheses.

    Returns
    -------
    Expr
        An Expr object representing expr.
    """
    def base_type(e: str) -> Expr:
        try:
            value = int(e)
        except ValueError:
            try:
                value = float(e)
            except ValueError:
                return Atom(e)
        return Numeric(value)

    n = len(expr)
    beg = ''
    i = 0
    blank = True
    while i < n:
        if expr[i] not in _ws:
            blank = False  # We have read at least one non ws character
        if expr[i] not in _sep | _ops | _ws:
            beg += expr[i]  # We are in the process of reading a name
        if expr[i] == ',':
            # Commas should not be encountered before we have
            # parsed an open parenthesis
            raise ParseError(expr, i,
                             'Hanging comma. Commas must be enclosed in '
                             + 'parentheses  () or brackets []')
        if expr[i] in {'(', '['}:
            # We start by reading until we have read the closing parenthesis
            # to this one. lvl is the number of nested parenthesis we have
            # encountered and it becomes -1 when we have met the matching
            # closed parenthesis
            open_s = expr[i]
            j = i+1
            lvl = 0
            beg_index_arg = i+1  # First character after opening parenthesis
            tuple_arg = []
            while lvl >= 0:
                if expr[j] in {'(', '['}:
                    lvl += 1
                if expr[j] in {')', ']'}:
                    lvl -= 1
                if expr[j] == ',' and lvl == 0:
                    # When we are at the main level we record if we encounter
                    # commas. Each part between two commas, or beginning and
                    # first comma is an element of the tuple/list we are
                    # constructing or an argument of the multivariate function
                    # we are constructing
                    try:
                        arg = _parse(expr[beg_index_arg:j])
                    except ParseError as e:
                        raise ParseError(expr,
                                         i+e.pos).with_traceback(e.__traceback__)
                    tuple_arg.append(arg)
                    beg_index_arg = j+1
                j += 1
            # If we have encountered commas we have already a list of arguments
            # for the tuple of function except for the one in between the last
            # encountered comma and the closing parenthesis. If we have not
            # encountered any comma, beg_index has never been updated and j
            # is the index of the first character after the closing parenthesis
            # In this case we are parsing the whole block in between brackets.
            try:
                last_arg = _parse(expr[beg_index_arg:j-1])
            except ParseError as e:
                raise ParseError(expr, i+e.pos).with_traceback(e.__traceback__)
            tuple_arg.append(last_arg)
            try:
                end = _parse(expr[j:])  # Parse what comes after the block
            except ParseError as e:
                raise ParseError(expr, i+e.pos).with_traceback(e.__traceback__)
            if beg != '':  # We are parsing a function named beg
                if open_s == '[':
                    raise ParseError(expr, i,
                                     f'Function {beg} followed by opening '
                                     + 'bracket')
                else:
                    mid = Function(beg, len(tuple_arg),
                                   *[arg for arg in reversed(tuple_arg)])
            else:  # We are parsing a tuple, a block or a list
                if len(tuple_arg) == 0:  # Nothing in between the parentheses
                    mid = Empty()
                elif len(tuple_arg) == 1:
                    # Parsing a block or a list with one element
                    if open_s == '(':
                        mid = tuple_arg[0]
                    else:
                        mid = List(mid)
                else:  # Parsing a tuple or a list
                    if open_s == '(':
                        mid = Tuple(*[arg for arg in reversed(tuple_arg)])
                    else:
                        mid = List(*[arg for arg in reversed(tuple_arg)])
            if isinstance(end, Empty):  # Nothing left to be done
                return mid
            elif isinstance(end, Operation):
                #  We are only the first operand of a larger expression so
                #  we add the resulting block to the children of the upcoming
                # operation.
                if end.name == 'neg':
                    end.name = '-'
                end.children.append(mid)
                return end

        # For operations: if beginning is not empty the first operand of
        # the operation is an atom. We recursively parse the other operand
        # and create the relevant object. If beginning is empty it means we are
        # actually reading the second operand of the operation when the first
        # operand was already a constituted block. The block will know to
        # append itself to the operation so we only need to construct the
        # Op object with only one child.

        if expr[i] == '+':
            try:
                end = _parse(expr[i+1:])
            except ParseError as e:
                raise ParseError(expr, i+e.pos).with_traceback(e.__traceback__)
            if beg != '':
                return Operation('+', end, base_type(beg))
            else:
                return Operation('+', end)
        if expr[i] == '-':
            try:
                end = _parse(expr[i+1:])
            except ParseError as e:
                raise ParseError(expr, i+e.pos).with_traceback(e.__traceback__)
            if beg != '':
                return Operation('-', end, base_type(beg))
            else:
                return Operation('neg', end)
        if expr[i] == '*':
            if expr[i+1] != '*':
                try:
                    end = _parse(expr[i+1:])
                except ParseError as e:
                    raise ParseError(expr,
                                     i+e.pos).with_traceback(e.__traceback__)
                if beg != '':
                    return Operation('*', end, base_type(beg))
                else:
                    return Operation('*', end)
            else:
                try:
                    end = _parse(expr[i+2:])
                except ParseError as e:
                    raise ParseError(expr,
                                     i+e.pos).with_traceback(e.__traceback__)
                if beg != '':
                    return Operation('**', end, base_type(beg))
                else:
                    return Operation('**', end)
        if expr[i] == '/':
            try:
                end = _parse(expr[i+1:])
            except ParseError as e:
                raise ParseError(expr, i+e.pos).with_traceback(e.__traceback__)
            if beg != '':
                return Operation('/', end, base_type(beg))
            else:
                return Operation('/', end)
        i += 1
    if blank:  # We have never encountered a non whitespace
        return Empty()
    return base_type(beg)  # Since no operations, we are an atom or a constant


def parse(expr: str) -> Expr:
    """Parse a mathematical expression in a string.

    Parameters
    ----------
    expr : str
        The mathematical expression to be parsed. The expression can be
        written using the standard convention of implicit order of
        arithmetic operations.

    Returns
    -------
    Expr
        The object representation of the mathematical expression.

    """
    return _parse(_prioritize(expr)).simplify()

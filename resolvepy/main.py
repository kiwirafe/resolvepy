from sympy import *

class RecurrenceResolutionError(Exception):
    pass

class Recurrence(IndexedBase):
    """
    Create a new instance of Recursive sequence.
    Note that it's essential to set the index manually
    after creating the object.
    """
    def __init__(self, *args, **kwargs):
        self.index = None
        self.starting = []
        self.nth = None

    def __getitem__(self, index):
        if index == self.index:
            # return the general n-th term formula for self[n]
            return self.nth
        else:
            if isinstance(index, int):
                # return the starting value for a[0..k]
                return self.starting[index]
            else:
                # return self[index] in symbol
                return super(Recurrence, self).__getitem__(index)


    def __setitem__(self, index, value):
        if isinstance(index, int):
            # for an int value, set a starting value
            if index == len(self.starting):
                # set exisiting value
                self.starting.append(value)
            else:
                # set new value
                self.starting[index] = value
        elif index is self.index:
            # set self[index]
            self.nth = value


    """
    Determine an explicit formula for the nth term.
    """
    def resolve(self):
        n = self.index
        k = len(self.starting)

        # create a characteristic equation
        # c0*a[n] + c1*a[n-1] + ... + ck*a[n-k] = 0
        a_n = self.nth.as_coefficients_dict()

        dependency = {n: -1}
        # dependency will be a dict in form {n - k: ck}
        # -1 is here because we move a[n] to the other side of the equation
        for i in a_n:
            if type(i) is Indexed and i.base is self and len(i.indices) == 1:
                index, = i.indices
                coeff = a_n[i]
                dependency[index] = coeff
            else:
                raise RecurrenceResolutionError("The recurrence relationship is not homogeneous.")

        r = Symbol('r')
        equation = sum(coeff*r**(k+i-n) for i, coeff in dependency.items())
        # the equation looks like:
        # c0 + c1*r + c2*r^2 + ... + ck*r^k = 0
        rs = roots(equation, r)

        # for every root, whose multiplicity is j, we add the following to the solution:
        # (x0 + x1*n + x2*n^2 + ... + xj*n^j) * root^n
        # in particular, when the root is single, it boils down to:
        # x0 * root^n
        # x0..xk are some constants coefficients that will be solved later
        solution = 0
        x = IndexedBase('x')
        x_index = 0
        for root, j in rs.items():
            solution += sum(x[x_index+i]*n**i for i in range(j))*root**n
            x_index += j


        # to calculate the coefficients, we build a system of equations and
        # use the starting items to solve it
        system = [solution.subs(n, i) - start for i, start in enumerate(self.starting)]
        xs = solve(system, *(x[i] for i in range(k)))
        #  = solve(system, x[0], x[1], ... , x[k])

        solution = solution.subs(xs)
        return solution

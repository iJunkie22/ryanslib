from collections import namedtuple
import operator


DiscreteVariable = namedtuple('DiscreteVariable', ['start', 'limit', 'step'])


class AlgebraEquation(object):
    variables_vals = {}
    variables_specs = {}

    def __init__(self):
        for k, v in self.variables_specs.items():
            assert isinstance(v, DiscreteVariable)
            self.variables_vals[k] = v.start

    def run_formula(self, **kwargs):
        raise NotImplementedError

    @staticmethod
    def show_variables_vals(**kwargs):
        output = str('+' * 30)
        output += "\nCurrent Variable Values\n"
        for k, v in kwargs.items():
            output += "{:<10}{:<40}\n".format(k, v)
        return output

    def iter_variable(self, var_name):
        my_disc_var = self.variables_specs[var_name]
        assert isinstance(my_disc_var, DiscreteVariable)
        var_val = my_disc_var.start
        lim_op = operator.le if (var_val < my_disc_var.limit) else operator.ge
        saved_step = my_disc_var.step

        while lim_op(var_val, my_disc_var.limit):
            yield var_val
            var_val += saved_step

    def iter_all_vars(self):
        raise NotImplementedError




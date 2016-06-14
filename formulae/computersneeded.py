from formulae import AlgebraEquation, DiscreteVariable

#  DiscreteVariable = namedtuple('DiscreteVariable', ['start', 'limit', 'step'])


class ComputersNeeded(AlgebraEquation):
    variables_specs = {'O': DiscreteVariable(0.70, 1.00, 0.10),
                       'a': DiscreteVariable(56000, 2490000, 100000), # kB/frame
                       'b': DiscreteVariable(24, 30, 6), # frames/sec
                       'P': DiscreteVariable(163, 2400, 500)} # processing power MB/s

    def run_formula(self, **kwargs):
        return 8.192 * kwargs['a'] * kwargs['b'] / (kwargs['P'] * kwargs['O'] * pow(10, 3))

    def iter_all_vars(self):
        for v1 in self.iter_variable('O'):
            for v2 in self.iter_variable('a'):
                for v3 in self.iter_variable('b'):
                    for v4 in self.iter_variable('P'):
                        rd = {'O': v1, 'a': v2, 'b': v3, 'P': v4}
                        yield self.show_variables_vals(**rd), self.run_formula(**rd)


for r1, r2 in sorted(ComputersNeeded().iter_all_vars(), key=lambda x: x[1]):
    print(r1)
    print(r2)



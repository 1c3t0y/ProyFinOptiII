from typing import List, Dict
import numpy as np
from scipy.optimize import minimize


class PPL:
    def __init__(self, costos: List, tipo_ppl: str, coeficientes: List[List], lado_derecho: List[Dict], binario: bool = False):
        self.costos = costos
        self.tipo_ppl = tipo_ppl
        self.coeficientes = coeficientes
        self.lado_derecho = lado_derecho
        self.n = len(costos)
        self.constraints = []
        if binario:
            self.bounds = [(0, 1) for x in range(0, self.n)]
        else:
            self.bounds = [(0, np.inf) for x in range(0, self.n)]
        self.x0 = np.zeros(self.n)

    @classmethod
    def objective(cls, x, costos):
        obj = 0
        for i, x in enumerate(x):
            obj += x * costos[i]
        return obj

    @classmethod
    def constraint_maker(cls, coeficientes: List, lado_derecho: Dict) -> callable:
        def constraint(x):
            signo = -1 if lado_derecho['operador'] == '<' else 1
            const = np.dot(x, coeficientes) - lado_derecho['valor']
            return signo * const

        return constraint

    def generate_constraints(self):
        for i, row in enumerate(self.coeficientes):
            fun = self.constraint_maker(row, self.lado_derecho[i])
            tipo = 'eq' if self.lado_derecho[i]['operador'] == '=' else 'ineq'
            constraint = {'type': tipo, 'fun': fun}
            self.constraints.append(constraint)

    def solve(self):
        self.generate_constraints()
        sol = minimize(self.objective, self.x0, args=self.costos,
                       method='SLSQP', bounds=self.bounds, constraints=self.constraints)
        sol.fun = sol.fun if not self.tipo_ppl == 'max' else -1 * sol.fun
        return sol

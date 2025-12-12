"""A class to manage optimization models."""

import pyomo.environ as pyo
from pyomo.opt.base import OptSolver


class OptimizationModelManager:
    def __init__(self, solver: str | OptSolver, model: pyo.AbstractModel | None = None):
        """Class to manage Pyomo optimization models.

        Args:
            solver: Pyomo OptSolver, or a string that instantiates a Pyomo OptSolver
                with this argument.
            model: Pyomo abstract model, optional.
        """
        if isinstance(solver, str):
            solver = pyo.SolverFactory(solver)
        self.solver = solver
        self.model = model
        self.model_instance: pyo.ConcreteModel | None = None
        self.is_solved: bool = False

    def set_model(self, model: pyo.AbstractModel) -> None:
        """Set a new model.

        Args:
            model: Pyomo abstract model to set.
        """
        self.model = model
        self.model_instance = None
        self.is_solved = False

    def instantiate(self, data: dict) -> None:
        """Create concrete model with instantiation data.

        Args:
            data: Dictionary with keys of model attributes and values
                of data to be set. The data needs to correspond to the abstract
                model in terms of attributes needed and their lengths, otherwise
                instantiation will fail.
        """
        data = {None: data}
        self.model_instance = self.model.create_instance(data=data)
        self.is_solved = False

    def solve(self) -> None:
        """Solve the model."""
        if not self.model_instance:
            raise RuntimeError("No concrete model to solve.")
        if self.is_solved:
            raise RuntimeError("Model is already solved.")

        self.solver.solve(self.model_instance)
        self.is_solved = True

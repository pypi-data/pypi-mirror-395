import pyomo.environ as pyo
import pytest

from annular.optimization_model_manager import OptimizationModelManager


@pytest.fixture
def dummy_model():
    """Create a model with time index."""
    model = pyo.AbstractModel()
    model.time = pyo.Set()
    model.x = pyo.Var(model.time)
    model.obj_params = pyo.Param(model.time, domain=pyo.Any, mutable=False)

    def c_rule(model):
        """Constraint. Assumes time has 2 values, 1 and 2."""
        return model.x[2] >= -2 * model.x[1] + 5

    model.c = pyo.Constraint(rule=c_rule)

    def obj_rule(model):
        """Set model objective function."""
        return sum(model.obj_params[t] * model.x[t] ** 2 for t in model.time)

    model.obj = pyo.Objective(rule=obj_rule)

    yield model


@pytest.fixture
def manager(solver):
    """Fixture for optimization model manager."""
    yield OptimizationModelManager(solver=solver)


@pytest.fixture
def instance_data():
    """Provides data for creating instance of dummy_model."""
    instance_data = {"time": [1, 2], "obj_params": {1: 0.5, 2: 3.4}}
    yield instance_data


def test_init(dummy_model, solver):
    """Test that initialization works."""
    manager = OptimizationModelManager(solver=solver)
    assert manager.model is None, "Model is not None."
    assert not manager.is_solved, "is_solved attribute is wrong."
    manager = OptimizationModelManager(solver=solver, model=dummy_model)
    assert manager.model == dummy_model, "Model is not set correctly."


def test_set_model(dummy_model, manager):
    """Test set_model method."""
    manager.set_model(dummy_model)
    assert manager.model == dummy_model, "Model is not set correctly."


def test_instantiate(dummy_model, manager, instance_data):
    """Test that instantiation works."""
    manager.set_model(dummy_model)
    manager.instantiate(data=instance_data)
    assert isinstance(manager.model_instance, pyo.ConcreteModel)
    for idx, value in instance_data["obj_params"].items():
        assert manager.model_instance.obj_params[idx] == value, "Obj fct params not set correctly."


@pytest.mark.integration
def test_solve(dummy_model, manager, instance_data):
    """Test that model solving works."""
    manager.set_model(dummy_model)
    manager.instantiate(data=instance_data)
    manager.solve()
    assert all(manager.model_instance.x[t].value is not None for t in manager.model_instance.time)
    assert manager.is_solved, "is_solved attribute is not correct."

import jax.numpy as jnp
from dynamaxsys.integrators import (
    IntegratorND,
    DoubleIntegrator2D,
    DoubleIntegrator1D,
    SingleIntegrator2D,
    SingleIntegrator1D,
    TwoPlayerRelativeIntegratorND,
)

def test_single_integrator_1d():
    sys = SingleIntegrator1D()
    x = jnp.array([0.0])
    u = jnp.array([1.0])
    x_next = sys.step(x, u)
    assert jnp.allclose(x_next, jnp.array([1.0])), f"Expected [1.0], got {x_next}"

def test_double_integrator_1d():
    sys = DoubleIntegrator1D()
    x = jnp.array([0.0, 0.0])
    u = jnp.array([2.0])
    x_next = sys.step(x, u)
    assert jnp.allclose(x_next, jnp.array([0.0, 2.0])), f"Expected [0.0, 2.0], got {x_next}"

def test_single_integrator_2d():
    sys = SingleIntegrator2D()
    x = jnp.array([0.0, 0.0])
    u = jnp.array([1.0, -1.0])
    x_next = sys.step(x, u)
    assert jnp.allclose(x_next, jnp.array([1.0, -1.0])), f"Expected [1.0, -1.0], got {x_next}"

def test_double_integrator_2d():
    sys = DoubleIntegrator2D()
    x = jnp.array([0.0, 0.0, 0.0, 0.0])
    u = jnp.array([1.0, 2.0])
    x_next = sys.step(x, u)
    assert jnp.allclose(x_next, jnp.array([0.0, 0.0, 1.0, 2.0])), f"Expected [0.0, 0.0, 1.0, 2.0], got {x_next}"

def test_two_player_relative_integrator_nd():
    sys = TwoPlayerRelativeIntegratorND(1, 2)
    x = jnp.array([0.0, 0.0])
    u = jnp.array([1.0, 2.0])
    d = jnp.array([-1.0, -2.0])
    x_next = sys.step(x, u, d)
    # Should be x + (-u + d) = [0,0] + ([-1, -2] + [-1, -2]) = [-2, -4]
    assert jnp.allclose(x_next, jnp.array([-2.0, -4.0])), f"Expected [-2.0, -4.0], got {x_next}"

if __name__ == "__main__":
    test_single_integrator_1d()
    test_double_integrator_1d()
    test_single_integrator_2d()
    test_double_integrator_2d()
    test_two_player_relative_integrator_nd()
    print("All tests passed.")

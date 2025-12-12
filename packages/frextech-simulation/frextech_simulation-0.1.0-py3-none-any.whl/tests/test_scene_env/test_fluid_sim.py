from scene_env import FluidSim

def test_fluid_sim_defaults():
    sim = FluidSim()
    assert "viscosity=1.0" in sim.simulate()

def test_fluid_sim_custom_values():
    sim = FluidSim(viscosity=2.5, flow_rate=1.2)
    assert "viscosity=2.5" in sim.simulate()
from scene_env import Scene, FluidSim
from ml_pipeline import train_model

def test_scene_with_fluid_pipeline():
    # Create a scene with fluid simulation data
    scene = Scene(name="FluidScene")
    fluid = FluidSim(viscosity=2.0, flow_rate=1.5)
    scene.add_object({"id": 1, "type": "fluid", "properties": fluid.simulate()})

    # Mock data for ML pipeline
    data = [[0.2, 0.5], [0.3, 0.7]]
    labels = [1, 0]

    result = train_model(data, labels)

    assert result["status"] == "success"
    assert result["accuracy"] == 0.95
    assert "fluid" in scene.objects[0]["type"]
from scene_env import Scene, FluidSim, HumanEnv
from quantum_env import QuantumEnv
from ml_pipeline import train_model

def test_combined_scene_and_quantum_pipeline():
    # Classical scene setup
    scene = Scene(name="HybridScene")
    fluid = FluidSim(viscosity=3.0, flow_rate=2.0)
    human_env = HumanEnv(population=20, behavior_model="adaptive")

    scene.add_object({"id": 1, "type": "fluid", "properties": fluid.simulate()})
    scene.add_object({"id": 2, "type": "agents", "properties": human_env.simulate()})

    # Quantum environment setup
    q_env = QuantumEnv(qubits=5)
    quantum_output = q_env.simulate()

    # Mock ML pipeline data: combine classical + quantum features
    data = [
        [len(scene.objects), len(quantum_output)],   # feature vector from scene + quantum
        [scene.environment.get("gravity", 9.8), q_env.qubits]
    ]
    labels = [1, 0]

    result = train_model(data, labels)

    # Assertions
    assert result["status"] == "success"
    assert result["accuracy"] == 0.95
    assert "fluid" in scene.objects[0]["type"]
    assert "agents" in scene.objects[1]["type"]
    assert "qubit" in quantum_output
from quantum_env import QuantumEnv
from ml_pipeline import train_model

def test_quantum_pipeline_integration():
    # Simulate quantum environment
    q_env = QuantumEnv(qubits=4)
    simulation_output = q_env.simulate()

    # Mock data: encode quantum simulation into features
    data = [[len(simulation_output), 4], [len(simulation_output), 2]]
    labels = [1, 0]

    result = train_model(data, labels)

    assert result["status"] == "success"
    assert result["accuracy"] == 0.95
    assert "qubit" in simulation_output
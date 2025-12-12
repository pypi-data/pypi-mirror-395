from quantum_env import QuantumEnv

def test_quantum_simulation():
    q = QuantumEnv(3)
    assert "3 qubit" in q.simulate()
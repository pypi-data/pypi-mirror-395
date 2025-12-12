from scene_env import HumanEnv

def test_human_env_simulation():
    env = HumanEnv(population=50, behavior_model="adaptive")
    result = env.simulate()
    assert "50 agents" in result
    assert "adaptive" in result
from scene_env import GameEnv

def test_game_env_launch():
    env = GameEnv(difficulty="hard", physics_enabled=False)
    result = env.launch()
    assert "hard" in result
    assert "physics=False" in result
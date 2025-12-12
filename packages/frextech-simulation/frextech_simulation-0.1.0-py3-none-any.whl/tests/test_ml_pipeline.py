from ml_pipeline import train_model

def test_train_model_success():
    data = [[0.1, 0.2], [0.3, 0.4]]
    labels = [0, 1]
    result = train_model(data, labels)
    assert result["status"] == "success"
    assert result["accuracy"] == 0.95

def test_train_model_empty_input():
    try:
        train_model([], [])
    except ValueError as e:
        assert str(e) == "Training data and labels must not be empty."
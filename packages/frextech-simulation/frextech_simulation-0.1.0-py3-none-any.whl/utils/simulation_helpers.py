import logging

logging.basicConfig(level=logging.INFO)

def normalize_data(data: list) -> list:
    """Normalize a list of numerical values to [0, 1] range."""
    if not data:
        logging.warning("Empty dataset provided for normalization")
        return []
    min_val, max_val = min(data), max(data)
    normalized = [(x - min_val) / (max_val - min_val) if max_val != min_val else 0 for x in data]
    logging.info("Data normalized successfully")
    return normalized

def calculate_simulation_score(metrics: dict) -> float:
    """Compute a weighted simulation score from metrics."""
    weights = {"accuracy": 0.5, "efficiency": 0.3, "stability": 0.2}
    score = sum(metrics.get(k, 0) * w for k, w in weights.items())
    logging.info(f"Calculated simulation score: {score}")
    return score

def summarize_simulation(metrics: dict) -> str:
    """Generate a summary string from simulation metrics."""
    score = calculate_simulation_score(metrics)
    summary = (
        f"Simulation Score: {score:.2f} | "
        f"Accuracy: {metrics.get('accuracy', 0):.2f} | "
        f"Efficiency: {metrics.get('efficiency', 0):.2f} | "
        f"Stability: {metrics.get('stability', 0):.2f}"
    )
    logging.info("Generated simulation summary")
    return summary
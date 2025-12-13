from levelapp.aspects.monitor import FunctionMonitor, APICallTracker
from levelapp.clients import ClientRegistry
from levelapp.metrics import MetricRegistry


monitoring_aspect = FunctionMonitor()


@monitoring_aspect.monitor(
    name="api_call",
    cached=True,
    maxsize=100,
    enable_timing=True,
    track_memory=True,
    metadata={"category": "api_call"},
    collectors=[APICallTracker()]
)
def call_client(message: str) -> str:
    model_id = "0b6c4a15-bb8d-4092-82b0-f357b77c59fd"
    ionos_base_url = "https://inference.de-txl.ionos.com/models"
    client_registry = ClientRegistry()
    client = client_registry.get(provider="ionos", base_url=f"{ionos_base_url}/{model_id}")
    response = client.call(message)
    return response.get("result", "No result found.")


@monitoring_aspect.monitor(
    name="compute_score",
    enable_timing=True,
    track_memory=True,
    metadata={"category": "scoring"}
)
def compute_score(s1: str, s2: str):
    metrics_registry = MetricRegistry()
    scorer = metrics_registry.get("levenshtein")
    score = scorer.compute(generated=s1, reference=s2)
    return score


if __name__ == '__main__':
    reference_reply = "Hello, how are you doing?"
    client_reply = call_client(message="Hello, how are you?")
    computed_score = compute_score(s1="Hello, how are you?", s2="Hello, how are you doing?")

    stats = monitoring_aspect.get_all_stats()
    print(f"Monitoring Stats:\n{stats}\n\n")

    for func_name in monitoring_aspect.list_monitored_functions().keys():
        func_history = monitoring_aspect.get_execution_history(name=func_name)
        print(f"Execution History for {func_name}:\n{func_history}\n")

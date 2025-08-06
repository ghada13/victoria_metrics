import requests
import time
import random
from core import config


def push_sample_cpu_usage(
    num_points: int = 20,
    interval_seconds: int = 1,
    metric_name: str = "cpu_usage",
    labels: dict = {"host": "server-1", "env": "prod"},
):
    """
    Pushes sample cpu_usage metrics to VictoriaMetrics.

    Args:
        num_points (int): Number of metrics to push.
        interval_seconds (int): Interval between points (simulated time gap).
        metric_name (str): Name of the metric.
        labels (dict): Labels to attach to the metric.
    """

    current_time = int(time.time())

    for i in range(num_points):
        # Simulate CPU usage between 20% and 90%
        cpu_value = round(random.uniform(20, 90), 2)

        # Labels formatting
        labels_str = ",".join(f'{k}="{v}"' for k, v in labels.items())
        labels_formatted = f"{{{labels_str}}}" if labels else ""

        # Calculate timestamp in seconds (simulated over time)
        timestamp = current_time + i * interval_seconds

        # Form the metric line
        metric_line = f'{metric_name}{labels_formatted} {cpu_value} {timestamp}\n'

        print(f"Pushing: {metric_line.strip()}")

        try:
            response = requests.post(
                config.VICTORIADB_PUSH_ENDPOINT,
                data=metric_line,
                headers={"Content-Type": "text/plain"},
                timeout=5,
            )
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"❌ Failed to push metric: {e}")
            print(f"Response: {getattr(e.response, 'text', None)}")
            break

    print(f"✅ Successfully pushed {num_points} cpu_usage points.")


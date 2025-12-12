"""Monitoring and metrics for Sonora."""

import time
from typing import Dict, Any, Optional
from collections import defaultdict


class MetricsCollector:
    """Collects metrics for monitoring."""

    def __init__(self):
        self._metrics: Dict[str, Any] = defaultdict(dict)
        self._start_time = time.time()

    def increment(self, name: str, value: float = 1.0, labels: Optional[Dict[str, str]] = None):
        """Increment a counter metric."""
        key = name
        if labels:
            key += str(sorted(labels.items()))

        if name not in self._metrics:
            self._metrics[name] = {"type": "counter", "value": 0, "labels": labels or {}}

        self._metrics[name]["value"] += value

    def gauge(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Set a gauge metric."""
        key = name
        if labels:
            key += str(sorted(labels.items()))

        self._metrics[key] = {"type": "gauge", "value": value, "labels": labels or {}}

    def histogram(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Record a histogram metric."""
        # Simplified histogram - just track count and sum
        key = name
        if labels:
            key += str(sorted(labels.items()))

        if key not in self._metrics:
            self._metrics[key] = {"type": "histogram", "count": 0, "sum": 0, "labels": labels or {}}

        self._metrics[key]["count"] += 1
        self._metrics[key]["sum"] += value

    def get_metrics(self) -> Dict[str, Any]:
        """Get all metrics."""
        return dict(self._metrics)

    def to_prometheus(self) -> str:
        """Export metrics in Prometheus format."""
        lines = []

        for name, data in self._metrics.items():
            metric_name = name.replace(".", "_").replace("-", "_")

            if data["type"] == "counter":
                lines.append(f"# TYPE {metric_name} counter")
                if data["labels"]:
                    label_str = ",".join(f'{k}="{v}"' for k, v in data["labels"].items())
                    lines.append(f"{metric_name}{{{label_str}}} {data['value']}")
                else:
                    lines.append(f"{metric_name} {data['value']}")

            elif data["type"] == "gauge":
                lines.append(f"# TYPE {metric_name} gauge")
                if data["labels"]:
                    label_str = ",".join(f'{k}="{v}"' for k, v in data["labels"].items())
                    lines.append(f"{metric_name}{{{label_str}}} {data['value']}")
                else:
                    lines.append(f"{metric_name} {data['value']}")

            elif data["type"] == "histogram":
                lines.append(f"# TYPE {metric_name} histogram")
                if data["labels"]:
                    label_str = ",".join(f'{k}="{v}"' for k, v in data["labels"].items())
                    lines.append(f"{metric_name}_count{{{label_str}}} {data['count']}")
                    lines.append(f"{metric_name}_sum{{{label_str}}} {data['sum']}")
                else:
                    lines.append(f"{metric_name}_count {data['count']}")
                    lines.append(f"{metric_name}_sum {data['sum']}")

        return "\n".join(lines)


# Global metrics collector
metrics = MetricsCollector()
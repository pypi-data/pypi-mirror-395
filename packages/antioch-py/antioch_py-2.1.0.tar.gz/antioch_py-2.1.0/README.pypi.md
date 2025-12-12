# antioch-py

Python SDK for the [Antioch](https://antioch.com) autonomy simulation platform.

## Overview

The antioch-py package provides two components:

### Module SDK (`antioch.module`)

The Module SDK is a framework for building Antioch modules in Python. Modules are containerized components that run alongside your simulation, processing sensor data and producing outputs. Each module runs in its own Docker container and communicates with the simulation through the Antioch runtime. Install the SDK in your module's Dockerfile to read sensors, run inference, and publish results.

```python
from antioch.module import Execution, Module

def process_radar(execution: Execution) -> None:
    scan = execution.read_radar("sensor")
    if scan is not None and len(scan.detections) > 0:
        execution.output("detections").set(scan)

if __name__ == "__main__":
    module = Module()
    module.register("radar_node", process_radar)
    module.spin()
```

### Session SDK (`antioch.session`)

The Session SDK is a client library for orchestrating Antioch simulations. Use it from Python scripts or Jupyter notebooks to programmatically build scenes, load assets, spawn robots, control simulation playback, and record data. The Session SDK connects to your Antioch deployment and provides a high-level API for automation and experimentation.

```python
from antioch.session import Scene, Session, Task, TaskOutcome

session = Session()
scene = Scene()

# Load environment and robot
scene.add_asset(path="/World/environment", name="warehouse", version="1.0.0")
ark = scene.add_ark(name="my_robot", version="0.1.0")

# Run simulation
task = Task()
task.start(mcap_path="/tmp/recording.mcap")

scene.play()
scene.step(1_000_000)  # step 1 second
scene.pause()

task.finish(outcome=TaskOutcome.SUCCESS)
```

## Installation

To install in your Python environment:

```bash
pip install antioch-py
```

To install in your Python-based Docker image (e.g. for an Antioch module):

```dockerfile
FROM python:3.12-slim

RUN pip install antioch-py

COPY . /app
WORKDIR /app

CMD ["python", "module.py"]
```

## Documentation

Visit [antioch.com](https://antioch.com) for full documentation.

## License

MIT

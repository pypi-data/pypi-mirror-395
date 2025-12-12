# Experiment Config Saver

Automatically save all your experiment constants to JSON for reproducibility.

## Usage

### Simple usage
```python
from pyzyconfig import save_config_to_json

# Your experiment constants
RUN_NAME = "my_experiment"
BATCH_SIZE = 32
LEARNING_RATE = 0.001
EPOCHS = 100

# Save all UPPERCASE variables
save_config_to_json("./outputs")
```

### With exclusions
```python
from pyzyconfig import save_config_to_json

DEVICE = "cuda"  # Don't want to save this
RUN_NAME = "my_experiment"
BATCH_SIZE = 32

# Exclude DEVICE from being saved
save_config_to_json("./outputs", exclude=['DEVICE'])
```

### Class-based usage
```python
from pyzyconfig import ConfigSaver

saver = ConfigSaver(exclude=['DEVICE', 'DEBUG'])
saver.save("./outputs")
```

### Load config
```python
from exp_config_saver import load_config_from_json

config = load_config_from_json("./outputs/config.json")
print(config['BATCH_SIZE'])  # 32
```

## Output example
```json
{
    "BATCH_SIZE": 32,
    "EPOCHS": 100,
    "LEARNING_RATE": 0.001,
    "RUN_NAME": "my_experiment",
    "_config_version": "0.1.0",
    "_saved_at": "2025-12-03T15:30:45.123456"
}
```
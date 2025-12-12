# Data Formats and File Specifications

**Purpose**: Document data structures, file formats, and serialization used in Argus.

## Remote ID Message Format

### Structure

Based on FAA 14 CFR Part 89 Remote ID standard (simplified for simulation):

```python
@dataclass
class RemoteIDMessage:
    uav_id: str                              # UAV identifier
    timestamp: float                         # Unix timestamp
    latitude: float                          # GPS latitude (-90 to 90)
    longitude: float                         # GPS longitude (-180 to 180)
    altitude: float                          # Altitude in meters (>= 0)
    velocity: tuple[float, float, float]     # (vx, vy, vz) in m/s
    signature: Optional[bytes]               # 64-byte Ed25519 signature
    is_spoofed: bool                         # Ground truth label
```

### Serialization (to_bytes)

**Format**: Fixed-width numeric fields + variable-length ID

| Field     | Type   | Bytes    | Offset | Description       |
| --------- | ------ | -------- | ------ | ----------------- |
| timestamp | double | 8        | 0-7    | Unix timestamp    |
| latitude  | double | 8        | 8-15   | GPS latitude      |
| longitude | double | 8        | 16-23  | GPS longitude     |
| altitude  | double | 8        | 24-31  | Altitude (meters) |
| vx        | double | 8        | 32-39  | Velocity X        |
| vy        | double | 8        | 40-47  | Velocity Y        |
| vz        | double | 8        | 48-55  | Velocity Z        |
| uav_id    | UTF-8  | variable | 56+    | UAV identifier    |

**Total size**: 56 + len(uav_id) bytes (unsigned)

**With signature**: Total + 64 bytes

**Example**:

```
Unsigned:  63 bytes  (56 fixed + "UAV-001" = 7 bytes)
Signed:    127 bytes (63 + 64-byte signature)
Overhead:  101.6%
```

---

## Configuration Files (YAML)

### Experiment Configuration

```yaml
# Experiment metadata
experiment_name: "phantom_attack_baseline" # Human-readable name
random_seed: 42 # For reproducibility

# Swarm parameters
swarm_size: 50 # Number of legitimate UAVs
comm_range: 100.0 # Communication range (meters)
simulation_duration: 120.0 # Total time (seconds)
update_frequency: 1.0 # Hz (updates per second)

# Attack configuration (optional)
attack_scenario:
  attack_type: "phantom" # phantom | position | coordinated
  start_time: 30.0 # When attack starts (seconds)
  duration: 60.0 # Attack duration (seconds)
  intensity: 0.1 # Attack intensity (0.0-1.0)

  # Type-specific parameters
  phantom_count: 5 # For phantom attacks
  falsification_magnitude: 75.0 # For position attacks (meters)
  coordination_pattern: "circle" # For coordinated attacks

# Defense configuration
enable_crypto: false # Enable Ed25519 signing

# Detection methods
detection_methods: # List of detectors to run
  - "spectral"
  - "centrality"
  - "crypto"

# Output
output_dir: "results/my_experiment" # Where to save results
```

### Attack Types

**Phantom**:

```yaml
attack_scenario:
  attack_type: "phantom"
  phantom_count: 5 # Number of phantom UAVs
  start_time: 30.0
  duration: 60.0
```

**Position Falsification**:

```yaml
attack_scenario:
  attack_type: "position"
  intensity: 0.15 # 15% of UAVs compromised
  falsification_magnitude: 75.0 # Offset up to 75 meters
  start_time: 30.0
  duration: 60.0
```

**Coordinated**:

```yaml
attack_scenario:
  attack_type: "coordinated"
  phantom_count: 8 # Phantoms in formation
  coordination_pattern: "circle" # circle | line | random
  start_time: 30.0
  duration: 60.0
```

---

## Results Files (JSON)

### metrics.json

```json
{
  "spectral": {
    "tpr": 0.85,
    "fpr": 0.08,
    "precision": 0.89,
    "recall": 0.85,
    "f1": 0.87,
    "detection_time": 0.00057,
    "tp": 17,
    "fp": 2,
    "tn": 28,
    "fn": 3
  },
  "centrality": {
    "tpr": 0.78,
    "fpr": 0.12,
    ...
  },
  "crypto": {
    "tpr": 1.0,
    "fpr": 0.0,
    ...
  }
}
```

**Fields**:

- `tpr`: True Positive Rate (0.0-1.0)
- `fpr`: False Positive Rate (0.0-1.0)
- `precision`: TP / (TP + FP)
- `recall`: Same as TPR
- `f1`: F1 score
- `detection_time`: Average detection latency (seconds)
- `tp`, `fp`, `tn`, `fn`: Confusion matrix counts

---

## Graph Snapshots (Pickle)

### Format

Python pickle of dictionary mapping timestamps to NetworkX graphs:

```python
{
    't=0': nx.Graph(...),
    't=30': nx.Graph(...),  # Attack start
    't=90': nx.Graph(...),  # Attack end
    't=120': nx.Graph(...)  # Final state
}
```

### Loading

```python
import pickle

with open('graph_snapshots.pkl', 'rb') as f:
    snapshots = pickle.load(f)

# Access specific snapshot
initial_graph = snapshots['t=0']
print(f"Nodes: {initial_graph.number_of_nodes()}")
print(f"Edges: {initial_graph.number_of_edges()}")
```

---

## Visualization Outputs

### File Naming Convention

```
results/<experiment_name>/figures/
├── roc_comparison.png          # All ROC curves on one plot
├── roc_comparison.pdf          # Vector version for LaTeX
├── roc_spectral.png            # Individual ROC curves
├── roc_centrality.png
├── roc_crypto.png
├── detection_comparison.png    # Bar charts: TPR, FPR, Precision, F1
├── performance_comparison.png  # Speed vs accuracy scatter
├── metrics_heatmap.png         # All metrics for all detectors
├── confusion_spectral.png      # Confusion matrix heatmaps
├── confusion_centrality.png
└── confusion_crypto.png
```

### Plot Specifications

**Resolution**: 300 DPI (publication quality)

**Formats**:

- PNG: For viewing, presentations, websites
- PDF: Vector graphics for LaTeX, scalable

**Color Palette**: Colorblind-friendly (seaborn 'colorblind')

**Style**: Academic paper style (seaborn-v0_8-paper)

---

## Summary Table (Markdown)

### results_table.md

```markdown
# Detection Performance Summary

| Detector      | TPR   | FPR   | Precision | Recall | F1    | Detection Time (ms) |
| ------------- | ----- | ----- | --------- | ------ | ----- | ------------------- |
| Spectral      | 0.850 | 0.080 | 0.890     | 0.850  | 0.870 | 0.57                |
| Centrality    | 0.780 | 0.120 | 0.810     | 0.780  | 0.795 | 0.95                |
| Cryptographic | 1.000 | 0.000 | 1.000     | 1.000  | 1.000 | 59.12               |
```

**Usage**:

- Copy directly into research papers
- Convert to LaTeX with pandoc
- Import into spreadsheets for analysis

---

## Type Definitions

### Python Type Hints

```python
Position = tuple[float, float, float]       # (x, y, z) in meters
Velocity = tuple[float, float, float]       # (vx, vy, vz) in m/s
Bounds = tuple[float, float, float]         # (x_max, y_max, z_max)
UAV_ID = str                                # Unique identifier
GroundTruth = dict[str, bool]               # {uav_id: is_legitimate}
ConfidenceScores = dict[str, float]         # {uav_id: anomaly_score}
```

### Validation Rules

**UAV ID**: Non-empty string, unique within swarm

**Position**:

- All components must be finite floats
- Within bounds: `0 <= x <= x_max`, etc.

**Velocity**:

- Magnitude typically < 20 m/s (reasonable for UAVs)
- No validation enforced (allows testing edge cases)

**Remote ID**:

- Latitude: -90 to 90 degrees
- Longitude: -180 to 180 degrees
- Altitude: >= 0 meters
- Timestamp: Unix time (positive float)

**Signature**:

- Exactly 64 bytes if present
- None for unsigned messages

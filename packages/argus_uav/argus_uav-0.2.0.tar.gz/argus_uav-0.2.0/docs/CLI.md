# Argus CLI User Guide

## Overview

`argus_cli.py` is the main command-line interface for the Argus UAV Swarm Security Testing Framework. It provides an easy way to test different attack scenarios and detection methods, either interactively or via command-line arguments.

## Installation

To use the `argus` command, install the package:

```bash
# Install in development mode
pip install -e .
# or
uv pip install -e .

# Now you can use the 'argus' command from anywhere
argus --help
```

If you're using a virtual environment (recommended), activate it first:

```bash
# Activate venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Then install
pip install -e .
```

## Quick Start

### Interactive Mode (Recommended)

```bash
# After installation, use the 'argus' command
argus

# Or run the script directly
python argus_cli.py
# or
uv run argus_cli.py
```

### Command-Line Mode

```bash
# See all options
argus --help

# Quick visualization
argus --attack phantom --detectors spectral --mode live

# Full comparison
argus --attack phantom --detectors all --mode comparison

# Both modes
argus --attack coordinated --detectors all --mode both
```

## Available Components

### Attacks (3 types)

1. **Phantom UAV** (`phantom`)

   - Injects 3 fake/non-existent UAVs into the swarm
   - Parameters: number of phantoms, timing
   - ✅ Detectable by: Crypto (100%), Spectral (100% stationary)

2. **Position Falsification** (`position`)

   - ~13% of legitimate UAVs report false GPS coordinates (100m offset)
   - Parameters: offset magnitude, timing
   - ⚠️ **Undetectable by all methods** (topology-preserving attack)

3. **Coordinated Attack** (`coordinated`)
   - 5 phantom UAVs in circular formation
   - Parameters: number of attackers, formation pattern
   - ✅ Detectable by: Crypto (100%), Spectral (100% stationary)

### Detection Methods (4 types)

1. **Cryptographic Detection** (`crypto`) ✅ **RECOMMENDED**

   - Ed25519 signature verification
   - Speed: ~58ms (30× overhead but still real-time)
   - Accuracy: **Perfect** (TPR=1.0, FPR=0.0) for phantom/coordinated
   - Mobility: Invariant (no performance degradation)

2. **Spectral Detection** (`spectral`) ⚠️ Supplementary only

   - Uses graph Laplacian eigenvalue analysis
   - Speed: Fast (~2ms)
   - Accuracy: Perfect in stationary, **degrades under mobility** (FPR up to 62.5%)
   - Use as: Fast alerting, not primary security

3. **Centrality Detection** (`centrality`) ❌ Not recommended

   - Analyzes degree/betweenness/closeness centrality
   - Speed: Fast (~1-3ms)
   - ⚠️ **100% false positive rate** - impractical for production

4. **ML Detection** (`ml`) ❌ Not recommended
   - Node2Vec embeddings + Isolation Forest
   - Speed: Medium (~5ms)
   - ⚠️ **87-97% false positive rate** - impractical for production

### Execution Modes

1. **Live Visualization** (`live`)

   - Real-time animated display
   - Shows UAVs, attacks, and detection in motion
   - Color-coded: green=legitimate, red=malicious, yellow=detected

2. **Performance Comparison** (`comparison`)

   - Runs experiments and generates metrics
   - Creates 4-panel comparison plots
   - Saves results tables and figures

3. **Both** (`both`)
   - First shows live visualization
   - Then generates performance comparison

## Command-Line Options

```
usage: argus_cli.py [-h] [--attack {phantom,position,coordinated}]
                    [--detectors {spectral,centrality,crypto,ml,all,none} [...]]
                    [--mode {live,comparison,both}]
                    [--num-uavs NUM_UAVS]
                    [--comm-range COMM_RANGE]

options:
  --attack            Attack type (phantom, position, coordinated)
  --detectors         Detection methods (one or more, or 'all'/'none')
  --mode              Execution mode (live, comparison, both)
  --num-uavs          Number of UAVs in swarm (default: 30)
  --comm-range        Communication range in meters (default: 200)
```

## Usage Examples

### Example 1: First-Time Exploration

```bash
# Interactive mode guides you through all options
argus
```

### Example 2: Quick Visualization

```bash
# Watch phantom attack with spectral detection
argus --attack phantom --detectors spectral --mode live
```

### Example 3: Compare All Methods

```bash
# Test all detectors against phantom attack
argus --attack phantom --detectors all --mode comparison
```

### Example 4: Crypto Baseline Test

```bash
# Crypto should achieve perfect detection
argus --attack coordinated --detectors crypto --mode both
```

### Example 5: Large Swarm Test

```bash
# Test with 100 UAVs
argus --attack phantom \
  --detectors spectral centrality \
  --mode comparison \
  --num-uavs 100 \
  --comm-range 250
```

### Example 6: Batch Testing

```bash
# Test all attacks with all detectors
for attack in phantom position coordinated; do
    argus --attack $attack --detectors all --mode comparison
done
```

## Output Files

When running in `comparison` or `both` mode, results are saved to:

```
results/<attack_type>_comparison/
├── performance_comparison.png   # 300 DPI comparison plot
├── performance_comparison.pdf   # PDF version
└── results_table.md             # Metrics table
```

### Comparison Plot Contents

The 4-panel plot includes:

1. **TPR vs FPR** - Scatter plot showing detection accuracy
2. **F1 Scores** - Bar chart comparing overall performance
3. **Precision vs Recall** - Trade-off visualization
4. **Detection Time** - Speed comparison

### Results Table Format

```markdown
| Detector | TPR   | FPR   | Precision | Recall | F1    | Detection Time (ms) |
| -------- | ----- | ----- | --------- | ------ | ----- | ------------------- |
| Spectral | 0.850 | 0.050 | 0.850     | 0.850  | 0.850 | 1.50                |
| ...      | ...   | ...   | ...       | ...    | ...   | ...                 |
```

## Performance Metrics Explained

| Metric        | Description                                | Ideal Value     |
| ------------- | ------------------------------------------ | --------------- |
| **TPR**       | True Positive Rate (% of attacks detected) | 1.0 (100%)      |
| **FPR**       | False Positive Rate (% of false alarms)    | 0.0 (0%)        |
| **Precision** | Of flagged UAVs, % actually malicious      | 1.0 (100%)      |
| **Recall**    | Same as TPR                                | 1.0 (100%)      |
| **F1**        | Harmonic mean of Precision & Recall        | 1.0 (100%)      |
| **Time**      | Average detection time in milliseconds     | Lower is better |

### Interpreting Results

**Perfect (Cryptographic - phantom/coordinated):**

```
TPR: 1.00, FPR: 0.00, F1: 1.00
```

✅ No false positives or false negatives - **use this for production**

**Good (Spectral - stationary only):**

```
TPR: 1.00, FPR: 0.00, F1: 1.00
```

⚠️ Works well in stationary swarms but degrades under mobility

**Poor (Centrality, ML):**

```
TPR: variable, FPR: 0.87-1.00, F1: <0.20
```

❌ High false positive rates make these impractical for production

**Position Falsification (all methods):**

```
TPR: 0.00, FPR: 0.00, F1: 0.00
```

⚠️ Topology-preserving attacks are fundamentally undetectable

## Visual Legend

During live visualization:

- 🟢 **Green circle** = Legitimate UAV
- 🔵 **Blue circle** = Legitimate UAV (with crypto enabled)
- 🔴 **Red X** = Malicious/Phantom UAV
- ⚠️ **Yellow outline** = Detected by algorithm

## Interactive Mode Flow

When you run `python argus_cli.py` without arguments:

1. **Swarm Configuration**

   - Number of UAVs (10-100)
   - Communication range (50-500m)

2. **Attack Selection**

   - Choose attack type
   - Set attack parameters (count, magnitude, timing)

3. **Detection Selection**

   - Choose one or more detection methods
   - Option for all methods or no detection

4. **Execution Mode**

   - Live visualization
   - Performance comparison
   - Both

5. **Results**
   - Visualization window opens (live mode)
   - Plots and tables generated (comparison mode)

## Tips & Best Practices

1. **Start with interactive mode** to understand options
2. **Use crypto detector** as perfect baseline for comparison
3. **Test spectral first** for fast initial results
4. **Use comparison mode** to get quantitative metrics
5. **Increase UAV count gradually** (20→50→100) for scalability tests
6. **Save results** for documentation and reporting

## Troubleshooting

### "qt.qpa.wayland" Warning

Harmless warning on Wayland displays. Ignore or run:

```bash
export QT_QPA_PLATFORM=xcb
argus
```

### Import Errors

Ensure dependencies are installed:

```bash
uv sync
# or
pip install -r requirements.txt
```

### Window Not Appearing (Live Mode)

- Check if Qt is installed: `pip list | grep PySide6`
- Try different backend: `export MPLBACKEND=TkAgg`

### Slow Performance

- Reduce UAV count: `--num-uavs 20`
- Use faster detectors: spectral, centrality (avoid ML for large swarms)
- Close other applications

## Comparison with Example Scripts

The CLI consolidates functionality from multiple example scripts:

| Old Scripts                  | New CLI Equivalent                  |
| ---------------------------- | ----------------------------------- |
| `attack_demo.py`             | `--mode live`                       |
| `detection_demo.py`          | `--detectors <method> --mode live`  |
| `live_viz_with_detection.py` | `--detectors all --mode live`       |
| `comprehensive_demo.py`      | `--detectors all --mode comparison` |

**Advantages of CLI:**

- ✅ Single unified interface
- ✅ Interactive mode for beginners
- ✅ Command-line mode for automation
- ✅ Proper thresholds (2.5, 2.0 vs old 1.0, 0.9)
- ✅ Generates proper comparison plots
- ✅ Color-coded terminal output
- ✅ Comprehensive help system

## Advanced Usage

### Custom Configuration in Code

To use custom thresholds or parameters, modify `argus_cli.py`:

```python
# Around line 223-241
if detector_name == "spectral":
    detector = SpectralDetector(threshold=3.0)  # Adjust threshold
elif detector_name == "centrality":
    detector = CentralityDetector(threshold=1.5)
```

### Integration with Scripts

Import and use CLI functions programmatically:

```python
from argus_cli import run_performance_comparison, AttackType

# Run comparison from your script
run_performance_comparison(
    attack_type=AttackType.PHANTOM,
    attack_config={"start_time": 10.0, "duration": 20.0, "phantom_count": 5},
    detector_names=["spectral", "centrality"],
    swarm_config={"num_uavs": 30, "comm_range": 200.0, "bounds": (500, 500, 100)}
)
```

## Summary

**What the CLI Provides:**

- ✨ Easy-to-use interface for all functionality
- 🎬 Live visualization of attacks and detection
- 📊 Automated performance comparison
- 🎯 Test any combination of 3 attacks × 4 detectors
- 📈 Publication-quality plots and metrics
- 🚀 Both interactive and scriptable

**Quick Commands to Remember:**

```bash
# Interactive
argus

# Quick test
argus --attack phantom --detectors spectral --mode live

# Full comparison
argus --attack phantom --detectors all --mode comparison
```

For more information, see:

- [QUICKSTART.md](QUICKSTART.md) - General getting started guide
- [algorithm_details.md](algorithm_details.md) - Detection algorithm theory
- [STATUS.md](STATUS.md) - Complete project status

---

**The CLI is the recommended way to use Argus for testing and demonstrations.**

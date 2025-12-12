# Troubleshooting Guide

Common issues and solutions for Argus.

---

## Visualization Issues

### Wayland Warning (Harmless)

**Issue**:

```
qt.qpa.wayland: Wayland does not support QWindow::requestActivate()
```

**Solution**: This is just a warning, not an error. The visualization still works fine. This appears on some Linux systems using Wayland display server.

**To suppress**: You can ignore it or use X11 instead:

```bash
# Use X11 backend (if available)
export QT_QPA_PLATFORM=xcb
uv run python examples/live_visualization.py
```

### Animation Warning

**Issue**:

```
Animation was deleted without rendering anything
```

**Solution**: Fixed in latest version. The `anim` variable is now properly assigned to prevent garbage collection.

### Plots Don't Appear

**Issue**: matplotlib plots don't show or crash

**Solutions**:

1. Verify PySide6 is installed:

   ```bash
   uv pip install PySide6
   ```

2. Check backend:

   ```bash
   uv run python examples/test_qt_backend.py
   ```

3. Use X11 if on Wayland:
   ```bash
   export QT_QPA_PLATFORM=xcb
   ```

---

## Import Errors

### ModuleNotFoundError: No module named 'argus'

**Solution**:

```bash
# Install in development mode
uv pip install -e .

# Or reinstall
uv pip uninstall argus
uv pip install -e .
```

### ImportError: cannot import name 'X'

**Solution**: Circular import issue. Check that TYPE_CHECKING is used for forward references:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from argus_uav.core.swarm import Swarm
```

---

## Test Issues

### Coverage Failure

**Issue**: `Coverage failure: total of X is less than fail-under=80`

**Solution**: Coverage requirement is commented out in `pytest.ini`. Run without coverage:

```bash
pytest tests/ --no-cov
```

### Tests Fail to Run

**Solution**:

```bash
# Use uv run
uv run pytest tests/

# Or install test dependencies
uv pip install pytest pytest-cov
```

---

## Performance Issues

### Slow Simulations

**Solutions**:

1. Reduce swarm size (30 instead of 100)
2. Increase time step (dt=2.0)
3. Use spectral detection only (fastest)

### Out of Memory

**Solutions**:

1. Don't save all graph snapshots
2. Reduce Node2Vec embedding dimensions
3. Process results in batches

---

## Detection Issues

### Low Detection Accuracy

**Solutions**:

1. Lower detection thresholds (0.5-1.0)
2. Collect more baseline graphs (30-50)
3. Use cryptographic detection for perfect accuracy

### False Positives

**Solutions**:

1. Increase detection thresholds
2. Collect longer baseline
3. Use ensemble voting (multiple methods)

---

## Animation/Visualization Issues

### Animation Doesn't Show

**Check**:

1. PySide6 installed? `uv pip install PySide6`
2. DISPLAY set? (on Linux with SSH)
3. Backend correct? Run `test_qt_backend.py`

**Workaround**: Save to file instead:

```python
visualizer.save_animation("output.gif", frames=50, fps=10)
```

### Slow Animation

**Solution**: Increase interval:

```python
LiveSwarmVisualizer(swarm, update_interval=500)  # 500ms instead of 200ms
```

---

## Consensus Issues

### Consensus Doesn't Converge

**Check**:

1. Is graph connected? Check `swarm.get_statistics()['is_connected']`
2. Step size too large? Try smaller epsilon
3. Enough iterations? May need 100+ steps

---

## Configuration Issues

### YAML Parse Error

**Solution**: Check YAML syntax:

```yaml
# Correct:
attack_scenario:
  attack_type: "phantom"
  phantom_count: 5

# Incorrect (indentation):
attack_scenario:
attack_type: "phantom"  # Wrong indentation
```

### Invalid Config Values

**Solution**: Pydantic will validate. Check error message:

```python
# swarm_size must be >= 10
swarm_size: 50  # ✅ Valid
swarm_size: 5   # ❌ Invalid
```

---

## Node2Vec Issues

### Node2Vec Training Slow

**Expected**: Node2Vec training takes 30-60 seconds. This is normal.

**To speed up**:

```python
Node2VecDetector(
    embedding_dim=32,    # Smaller (was 64)
    num_walks=50,        # Fewer (was 100)
    walk_length=15       # Shorter (was 20)
)
```

### Node2Vec Out of Memory

**Solution**: Reduce parameters or use smaller graph for training.

---

## Git/Version Control

### Large Files in Repo

**Check**: Results directory should be gitignored:

```bash
# Verify results/ is ignored
git check-ignore results/
```

**Solution**: If not ignored:

```bash
# Add to .gitignore
echo "results/" >> .gitignore

# Remove from tracking
git rm -r --cached results/
```

---

## Common Warnings (Harmless)

### Wayland Warning

```
qt.qpa.wayland: Wayland does not support QWindow::requestActivate()
```

✅ Harmless - visualization still works

### UserWarning: Animation was deleted

```
Animation was deleted without rendering anything
```

✅ Fixed in latest version (anim variable assigned)

### FutureWarning from libraries

```
FutureWarning: adjacency_matrix will return...
```

✅ Harmless - library compatibility warnings

---

## Getting Help

1. **Check documentation**: `docs/QUICKSTART.md`, `docs/STATUS.md`
2. **Run examples**: All examples should work out of the box
3. **Check tests**: `pytest tests/` should all pass
4. **Verify installation**: `uv run python -c "import argus; print('OK')"`

---

**Last Updated**: December 2025

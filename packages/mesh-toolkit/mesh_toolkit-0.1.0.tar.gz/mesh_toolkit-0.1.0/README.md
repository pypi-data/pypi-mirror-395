# mesh-toolkit

Python SDK for [Meshy AI](https://www.meshy.ai/) 3D asset generation API.

## Installation

```bash
pip install mesh-toolkit
```

## Usage

```python
from mesh_toolkit import text3d, rigging, animate, retexture

# Generate a 3D model
model = text3d.generate("a medieval sword with ornate handle")

# Rig it for animation
rigged = rigging.rig(model.id)

# Apply an animation (678 available)
animated = animate.apply(rigged.id, animation_id=0)  # Idle

# Or retexture it
gold = retexture.apply(model.id, "golden with embedded gems")
```

## Modules

### text3d

```python
from mesh_toolkit import text3d

# Generate model
result = text3d.generate("a wooden chest", art_style="realistic")
print(result.model_urls.glb)

# Or manually control the workflow
task_id = text3d.create(request)  # Returns immediately
result = text3d.get(task_id)      # Check status
result = text3d.poll(task_id)     # Wait for completion
```

### rigging

```python
from mesh_toolkit import rigging

result = rigging.rig(model_id)
# Or from URL
result = rigging.rig_from_url("https://example.com/model.glb")
```

### animate

```python
from mesh_toolkit import animate
from mesh_toolkit.animations import ANIMATIONS

# Apply animation
result = animate.apply(rigged_id, animation_id=0)

# Browse 678 animations
for anim in ANIMATIONS.values():
    print(f"{anim.id}: {anim.name} ({anim.category})")
```

### retexture

```python
from mesh_toolkit import retexture

result = retexture.apply(model_id, "rusty metal with scratches")
# Or from reference image
result = retexture.apply_from_image(model_id, "https://example.com/style.png")
```

## Architecture

```
mesh_toolkit/
├── base.py         # HTTP infrastructure (auth, retries, rate limiting)
├── text3d.py       # Text-to-3D API
├── rigging.py      # Rigging API  
├── animate.py      # Animation API
├── retexture.py    # Retexture API
├── animations.py   # 678 animation catalog
├── models.py       # Pydantic models
└── jobs.py         # Batch workflow orchestration
```

Each API module imports `base` and implements its endpoints directly. No monolithic client class.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `MESHY_API_KEY` | Your Meshy API key (required) |

## License

MIT

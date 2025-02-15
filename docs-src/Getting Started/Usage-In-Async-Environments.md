# Usage in Async Environments

SwiftShadow's default `update` function uses `asyncio.run()` to run its provider coroutines. This can lead to issues when using async frameworks like **FastAPI** or **Quart**, which already manage their own event loops.

!!! warning "Avoid `asyncio.run()` in Async Apps"
    Running `asyncio.run()` inside an existing event loop (like those in FastAPI or Quart) may cause errors or unexpected behavior.

## The Simple Solution

Instead of using `update`, call `async_update()` to refresh your proxies. This makes sure your proxies are up to date and safe to use in your async app.

!!! tip "Keep Proxies Fresh"
    Create a background task that periodically calls `async_update()` so your proxies are always valid.

## FastAPI Example

Use this example in FastAPI to update proxies every 5 seconds:

```python
from fastapi import FastAPI
import asyncio
from swiftshadow.classes import ProxyInterface

app = FastAPI()

# Create the ProxyInterface with autoUpdate disabled.
swift = ProxyInterface(autoUpdate=False, autoRotate=True)

async def background_task():
    """Update proxies every 5 seconds."""
    while True:
        print("Updating proxies...")
        await swift.async_update()
        await asyncio.sleep(5)

@app.on_event("startup")
async def startup_event():
    """Start the background task when the app starts."""
    asyncio.create_task(background_task())
    print("Background task started!")

@app.get("/")
async def home():
    """Return a refreshed proxy."""
    proxy = swift.get()
    return {
        "message": "Hello, FastAPI! Here is a proxy.",
        "proxy": proxy.as_string()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, debug=True)
```

## Quart Example

Below is a similar example for Quart. In this updated example, we disable automatic rotation (i.e. `autoRotate=False`) and instead call `rotate(validate_cache=False)` manually within the route. This avoids errors related to the event loop in Quart.

```python
from quart import Quart
import asyncio
from swiftshadow.classes import ProxyInterface

app = Quart(__name__)
swift = ProxyInterface(autoUpdate=False, autoRotate=False)  # manual update and rotation

async def background_task():
    """Update proxies every 5 seconds."""
    while True:
        print("Updating proxies...")
        await swift.async_update()
        await asyncio.sleep(5)

@app.before_serving
async def startup():
    """Start the background task when the server starts."""
    app.add_background_task(background_task)
    print("Background task started!")

@app.route("/")
async def home():
    """Return a refreshed proxy."""
    swift.rotate(validate_cache=False)  # manually rotate without cache validation
    return "Hello, Quart! Here is a proxy: " + swift.get().as_string()

if __name__ == "__main__":
    app.run(debug=True)
```

## Summary

By calling `async_update()` in a background task, you ensure that your proxies are refreshed safely within your app's own event loop.  
**Note:** In some async frameworks (e.g., Quart), if you encounter issues with auto-rotation, consider disabling `autoRotate` and manually calling `rotate(validate_cache=False)` to avoid event loop conflicts.

!!! note "Remember"
    Always call `async_update()` before accessing a proxy to keep it up to date and avoid potential issues with event loops.

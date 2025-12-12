# Async Support Status Summary

## Current Implementation Status

### ✅ What Works

1. **Synchronous agents** - Fully functional with `on_message` as regular methods
2. **Rust code compilation** - All async-related code compiles successfully
3. **Basic infrastructure** - Event loop detection and initialization logic is in place
4. **Python API** - `send_message_async` exposed for `LlmAgent`

### ⚠️ What Doesn't Work Yet

**Async `on_message` handlers** - Runtime error: "no running event loop"

## The Core Problem

When a message is sent via `mesh.send_to()`:

1. The Python call enters Rust via PyO3
2. Rust spawns/uses a Tokio runtime thread to handle the message
3. The Tokio thread calls back into Python to invoke `on_message`
4. If `on_message` is async, it returns a coroutine
5. **PROBLEM**: The coroutine needs to run on an asyncio event loop, but:
   - The Tokio thread doesn't have a compatible asyncio loop
   - Creating a new loop doesn't help because the coroutine was created in a different context
   - `py.allow_threads()` causes "Python interpreter not initialized" errors

## Why This Is Complex

This is a fundamental async runtime bridging problem:

- **Tokio** (Rust async runtime) and **asyncio** (Python async runtime) are incompatible
- `pyo3-async-runtimes` helps bridge them, but only when:
  - The Python coroutine originates from a function called with proper event loop context
  - The event loop is running and accessible in the current thread

## Possible Solutions (Not Yet Implemented)

### Option 1: Thread-local Event Loop (Complex)

- Ensure each Tokio worker thread has its own asyncio event loop
- Use `pyo3_async_runtimes::TaskLocals` to manage thread-local state
- Requires significant refactoring of how messages are dispatched

### Option 2: Bridge to Python's Event Loop (Preferred)

- Instead of `RUNTIME.block_on()`, spawn tasks that acquire GIL asynchronously
- Use `tokio::task::spawn_blocking` to call into Python
- Let Python's event loop handle async execution
- Would require restructuring the mesh's message processing

### Option 3: Hybrid Approach

- Keep synchronous `on_message` as the primary interface
- Add separate async methods like `on_message_async` that can be explicitly awaited
- Document that async actions work but async message handlers have limitations

## Demo Files Created

1. **`demo_simple_agent.py`** ✅ - Works perfectly

   - Demonstrates synchronous message handling
   - Shows basic agent functionality

2. **`demo_async_agent.py`** ⚠️ - Has event loop issues

   - Demonstrates intended async usage
   - Fails with "no running event loop" error
   - Shows the limitation of current implementation

3. **`test_async_agent.py`** ⚠️ - pytest-based tests
   - Same event loop issues as demo
   - Works for testing the structure but not execution

## Recommendation

For practical use, I recommend:

1. **Use synchronous `on_message`** handlers for now - they work reliably
2. **Use `send_message_async`** for LLM agents - this works because it's called from Python's side
3. **Async actions** may work if invoked from the right context, but need more testing
4. Document the limitation and revisit async message handlers as a future enhancement

The async infrastructure is in place and compiles, but making it fully functional requires deeper integration between Tokio and asyncio event loops - a non-trivial engineering challenge.

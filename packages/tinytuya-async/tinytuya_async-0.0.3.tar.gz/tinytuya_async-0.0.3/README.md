## tinytuya_async

**`tinytuya_async`** is a minimal, **`asyncio`** implementation derived from the popular `tinytuya` library.

The main `tinytuya` project is currently preparing for a major version **2.0** release with **native async support**. This effort involves significant changes to support the wide variety of devices, protocol versions, new features like callbacks, and device type handling already supported by `tinytuya`, which will take time.

Therefore, **`tinytuya_async`** is a **minimal change** library that focuses only on replacing the core **socket I/O** of a single device with an asynchronous implementation (`DeviceAsync`). This repository is intended to be used as a stopgap solution until the official `tinytuya` 2.0 release is available.

-----

### 📥 Installation

Install the library using pip:

```bash
pip install tinytuya-async
```

### 💡 Usage Example

A complete example demonstrating asynchronous connection and status monitoring is located at **[examples/monitor_async.py](examples/monitor_async.py)**.

-----

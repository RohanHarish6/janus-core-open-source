---
trigger: always_on
description: "Hardware constraints and thermal throttling rules for Dell Inspiron 5410."
---
# Hardware Guardrails (Dell Inspiron 5410)

1. Memory:
   - Cap resident process memory at 4.5 GB.
   - Run garbage collection and cache flushing after large MoE streaming operations.

2. Thermal & Power:
   - Monitor simulated CPU package temperature.
   - If CPU temp >= 85.0°C, throttle worker pool concurrency from 4 threads to 2 threads.
   - Detect AC vs Battery state: default to Battery Saver mode (2 threads, low power) when disconnected from mains.

3. Disk Streaming:
   - Use sequential asynchronous buffered I/O for NVMe expert streaming.
   - Maintain prefetch cache hit rate target above 90%.

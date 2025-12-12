# ByteShare

> 🚀 A lightweight, distributed tensor store for ML inference
> 
> The spiritual successor to Apache Plasma, without the Ray dependency.

[![PyPI version](https://badge.fury.io/py/byteshare.svg)](https://badge.fury.io/py/byteshare)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## Why ByteShare?

- **Apache Plasma is dead** - Removed from Arrow 12.0.0 (May 2023)
- **Ray is too heavy** - You just want object sharing, not a full cluster (~150MB)
- **Redis doesn't understand tensors** - Serialization overhead kills performance
- **SharedMemory is local only** - No cross-node support

ByteShare fills this gap: **a lightweight, zero-dependency distributed tensor store**.

## Features

- ✅ **Zero external dependencies** - Pure Python + PyZMQ (optional backends available)
- ✅ **Pass by Reference** - ObjectRef contains only metadata, data transferred on `get()`
- ✅ **Same-node zero-copy** - SharedMemory backend for multi-process sharing
- ✅ **Cross-node efficient transfer** - ZMQ ROUTER/DEALER with connection pooling
- ✅ **Auto lifecycle management** - TTL expiration, optional reference counting
- ✅ **Native Tensor support** - PyTorch, NumPy, with optimal serialization

## Installation

```bash
pip install byteshare

# Optional backends
pip install byteshare[zmq]     # ZMQ transport (recommended for distributed)
pip install byteshare[redis]   # Redis backend
pip install byteshare[s3]      # S3 backend
pip install byteshare[all]     # All optional dependencies
```

## Quick Start

```python
from byteshare import ByteStore, ObjectRef
import torch

# Create a store
store = ByteStore()

# Store a tensor
tensor = torch.randn(1, 16, 125, 96, 96, dtype=torch.float16)
ref: ObjectRef = store.put(tensor, name="embeddings", ttl=120)

# Retrieve it (zero-copy if same process/node)
tensor = store.get(ref)

# Delete when done
store.delete(ref)
```

## Use Cases

- **Disaggregated ML inference** - Share embeddings/latents between pipeline stages
- **Multi-process ML** - Zero-copy tensor sharing between workers
- **Distributed pipelines** - Pass tensors across nodes without serialization pain

## Roadmap

- [ ] v0.1.0 - MVP: ObjectRef, LocalMemory, SharedMemory backends
- [ ] v0.2.0 - Distributed: ZMQ transport, cross-node get
- [ ] v0.3.0 - Production: Async API, Prometheus metrics, disk spill
- [ ] v0.4.0 - Extensions: Redis/S3 backends, UCX RDMA transport

## License

Apache 2.0

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) first.


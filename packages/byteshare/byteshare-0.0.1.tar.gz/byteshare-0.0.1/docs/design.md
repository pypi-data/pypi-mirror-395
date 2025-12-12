# SGLang Disaggregated Diffusion Serving 架构设计

> 一个面向大规模视频/图像生成的分布式推理架构

---

## 目录

1. [背景与问题](#1-背景与问题)
2. [设计目标](#2-设计目标)
3. [整体架构](#3-整体架构)
4. [核心组件设计](#4-核心组件设计)
   - [4.1 ObjectRef 与 TensorStore](#41-objectref-与-tensorstore)
   - [4.2 RequestContext 与 ExecutionPlan](#42-requestcontext-与-executionplan)
   - [4.3 Scheduler 与 TaskQueue](#43-scheduler-与-taskqueue)
   - [4.4 Worker Pool](#44-worker-pool)
5. [通信机制](#5-通信机制)
6. [高可用设计](#6-高可用设计)
7. [生产特性](#7-生产特性)
8. [Kubernetes 部署方案](#8-kubernetes-部署方案)
9. [性能评估](#9-性能评估)
10. [实现路径](#10-实现路径)

---

## 1. 背景与问题

### 1.1 当前 SGLang Diffusion 架构

```
┌─────────────────────────────────────────────────────────┐
│                    单机 Pipeline                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Request → [Text Encoder] → [Conditioning] →            │
│            [Timestep Prep] → [Latent Prep] →            │
│            [Denoising ×50] → [VAE Decode] → Output      │
│                                                         │
│            ↑ 所有阶段在同一台机器顺序执行 ↑              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 1.2 核心问题

| 问题 | 说明 | 影响 |
|------|------|------|
| **资源利用率低** | Encoder/Decoder 只在请求开始/结束时使用 | GPU 闲置率高达 60%+ |
| **吞吐受限** | 单机顺序执行，无法流水线并行 | 难以线性扩展 |
| **硬件要求高** | 大模型需要高配单机 (8×H100) | 部署成本高 |
| **弹性差** | 各阶段耦合，无法独立扩缩容 | 无法应对流量波动 |

### 1.3 参考方案

- **vLLM PD 分离**: Prefill 和 Decode 阶段分离到不同 Worker Pool
- **Ray Object Store**: 分布式对象存储，Pass by Reference
- **AIBrix**: vLLM 的 Kubernetes 部署方案

---

## 2. 设计目标

### 2.1 核心目标

1. **Stage 解耦**: 各阶段独立部署、独立扩缩容
2. **流水线并行**: 多请求并发处理，提升吞吐
3. **零外部依赖**: 默认配置不依赖 Redis/外部存储
4. **渐进增强**: 生产环境可选择增强组件

### 2.2 量化目标

| 指标 | 当前 | 目标 |
|------|------|------|
| GPU 利用率 | ~40% | ~80% |
| 吞吐 (同等资源) | 1x | 4-10x |
| 扩展性 | 单机 | 线性扩展 |

---

## 3. 整体架构

### 3.1 架构图

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         Disaggregated Diffusion Serving                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│    ┌─────────────┐                                                              │
│    │   Client    │                                                              │
│    └──────┬──────┘                                                              │
│           │                                                                     │
│           ▼                                                                     │
│    ┌─────────────┐      ┌──────────────────────────────────────────────────┐   │
│    │  Scheduler  │◄────►│              TaskQueue (Pluggable)               │   │
│    │  (Stateless)│      │  [memory] / [sqlite] / [redis]                   │   │
│    └──────┬──────┘      └──────────────────────────────────────────────────┘   │
│           │                                                                     │
│           │ Pull Model (Workers pull tasks when idle)                          │
│           │                                                                     │
│    ┌──────┴──────────────────────────────────────────────────────────────┐     │
│    │                                                                      │     │
│    │   ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐ │     │
│    │   │  Encoder Pool   │    │  Denoising Pool │    │  Decoder Pool   │ │     │
│    │   │  ┌───┐ ┌───┐    │    │  ┌───┐ ┌───┐    │    │  ┌───┐ ┌───┐    │ │     │
│    │   │  │W1 │ │W2 │    │    │  │W1 │ │W2 │    │    │  │W1 │ │W2 │    │ │     │
│    │   │  └───┘ └───┘    │    │  └───┘ └───┘    │    │  └───┘ └───┘    │ │     │
│    │   │  ┌───┐ ┌───┐    │    │  ┌───┐ ┌───┐    │    │  ┌───┐          │ │     │
│    │   │  │W3 │ │W4 │    │    │  │W3 │ │...│    │    │  │W3 │          │ │     │
│    │   │  └───┘ └───┘    │    │  └───┘ └───┘    │    │  └───┘          │ │     │
│    │   └─────────────────┘    └─────────────────┘    └─────────────────┘ │     │
│    │                                                                      │     │
│    └──────────────────────────────────────────────────────────────────────┘     │
│                                                                                 │
│    ┌──────────────────────────────────────────────────────────────────────┐     │
│    │                    TensorStore (Pluggable)                           │     │
│    │    [memory] / [shared_memory] / [redis] / [s3] / [disk_spill]       │     │
│    │                                                                      │     │
│    │    Workers 之间通过 ObjectRef 传递引用，点对点获取数据              │     │
│    └──────────────────────────────────────────────────────────────────────┘     │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 请求流转

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                              请求生命周期                                       │
├────────────────────────────────────────────────────────────────────────────────┤
│                                                                                │
│  1. Client 发送请求到 Scheduler                                                │
│     └─→ Scheduler 根据 model 生成 ExecutionPlan                               │
│                                                                                │
│  2. Scheduler 将任务放入 encoder-pool 的 TaskQueue                            │
│     └─→ Encoder Worker pull 任务，执行编码                                    │
│     └─→ 结果存入 TensorStore，返回 ObjectRef                                  │
│     └─→ 更新 RequestContext，推进到下一 stage                                 │
│                                                                                │
│  3. Scheduler 将任务放入 denoising-pool 的 TaskQueue                          │
│     └─→ Denoising Worker pull 任务                                            │
│     └─→ 通过 ObjectRef 从 TensorStore 获取 embeddings                         │
│     └─→ 执行 50 步去噪，结果存入 TensorStore                                  │
│     └─→ 更新 RequestContext，推进到下一 stage                                 │
│                                                                                │
│  4. Scheduler 将任务放入 decoder-pool 的 TaskQueue                            │
│     └─→ Decoder Worker pull 任务                                              │
│     └─→ 通过 ObjectRef 获取 latents                                           │
│     └─→ VAE 解码，生成最终视频/图像                                           │
│     └─→ 返回结果给 Scheduler                                                  │
│                                                                                │
│  5. Scheduler 将结果返回给 Client                                              │
│     └─→ 清理 TensorStore 中的临时数据                                         │
│                                                                                │
└────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. 核心组件设计

### 4.1 ObjectRef 与 TensorStore

#### 4.1.1 ObjectRef 定义

```python
@dataclass(frozen=True)
class ObjectRef:
    """
    对象引用，不包含实际数据，只包含获取数据所需的元信息
    类似 Ray ObjectRef，实现 Pass by Reference
    """
    object_id: str           # 唯一标识，格式: {request_id}:{name}:{timestamp}
    owner_address: str       # 数据所在节点地址，如 "192.168.1.10:5555"
    owner_node_id: str       # 节点 ID
    shape: tuple             # Tensor 形状，如 (1, 16, 125, 96, 96)
    dtype: str               # 数据类型，如 "float16"
    size_bytes: int          # 数据大小，用于传输预估
    created_at: float        # 创建时间戳
    name: str                # 语义名称，如 "text_embeddings", "latents"

    def to_dict(self) -> dict:
        """序列化为字典，便于 JSON 传输"""
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "ObjectRef":
        """从字典反序列化"""
        return cls(**d)
```

#### 4.1.2 TensorStore 接口

```python
class TensorStore:
    """
    Tensor 存储层，支持多种后端
    - 同节点: 零拷贝 (共享内存)
    - 跨节点: ZMQ 点对点传输
    """

    def __init__(
        self,
        node_id: str,
        port: int = 5555,
        backend: StorageBackend = None,
        enable_spill: bool = False,
        spill_threshold: float = 0.8,
        spill_dir: str = "/tmp/tensor_spill"
    ):
        self.node_id = node_id
        self.backend = backend or LocalMemoryBackend()
        self.server = ZMQServer(port)  # 响应远程请求
        self.spill_backend = DiskSpillBackend(spill_dir) if enable_spill else None

    def put(
        self,
        tensor: torch.Tensor,
        request_id: str,
        name: str,
        ttl: int = 120
    ) -> ObjectRef:
        """
        存储 Tensor，返回 ObjectRef

        Args:
            tensor: 要存储的 Tensor
            request_id: 请求 ID
            name: 语义名称
            ttl: 生存时间（秒），超时自动清理

        Returns:
            ObjectRef: 对象引用
        """
        object_id = f"{request_id}:{name}:{time.time()}"

        # 序列化存储
        data = self._serialize(tensor)
        self.backend.store(object_id, data, ttl)

        return ObjectRef(
            object_id=object_id,
            owner_address=f"{self.local_ip}:{self.port}",
            owner_node_id=self.node_id,
            shape=tuple(tensor.shape),
            dtype=str(tensor.dtype),
            size_bytes=tensor.nbytes,
            created_at=time.time(),
            name=name
        )

    def get(self, ref: ObjectRef) -> torch.Tensor:
        """
        根据 ObjectRef 获取 Tensor
        - 本地: 直接从 backend 读取
        - 远程: 通过 ZMQ 请求
        """
        if ref.owner_node_id == self.node_id:
            # 本地获取
            data = self.backend.load(ref.object_id)
        else:
            # 远程获取
            data = self._fetch_remote(ref)

        return self._deserialize(data, ref.shape, ref.dtype)

    def delete(self, ref: ObjectRef) -> None:
        """删除对象，释放内存"""
        if ref.owner_node_id == self.node_id:
            self.backend.delete(ref.object_id)

    @classmethod
    def create(cls, backend_type: str = "auto", **kwargs) -> "TensorStore":
        """
        工厂方法，根据配置创建 TensorStore

        Args:
            backend_type: "memory", "shared_memory", "redis", "s3", "auto"
        """
        backends = {
            "memory": LocalMemoryBackend,
            "shared_memory": SharedMemoryBackend,
            "redis": RedisBackend,
            "s3": S3Backend,
        }

        if backend_type == "auto":
            # 自动选择: 优先共享内存，fallback 到普通内存
            try:
                backend = SharedMemoryBackend(**kwargs)
            except:
                backend = LocalMemoryBackend()
        else:
            backend = backends[backend_type](**kwargs)

        return cls(backend=backend, **kwargs)
```

#### 4.1.3 存储后端

```python
class StorageBackend(ABC):
    """存储后端抽象接口"""

    @abstractmethod
    def store(self, object_id: str, data: bytes, ttl: int = 0) -> None:
        """存储数据"""
        pass

    @abstractmethod
    def load(self, object_id: str) -> Optional[bytes]:
        """加载数据"""
        pass

    @abstractmethod
    def delete(self, object_id: str) -> None:
        """删除数据"""
        pass

    @abstractmethod
    def exists(self, object_id: str) -> bool:
        """检查是否存在"""
        pass


class LocalMemoryBackend(StorageBackend):
    """
    本地内存存储 (默认)
    - 零依赖
    - 最简单
    - 进程内共享
    """
    def __init__(self):
        self._store: Dict[str, bytes] = {}
        self._expiry: Dict[str, float] = {}

    def store(self, object_id: str, data: bytes, ttl: int = 0) -> None:
        self._store[object_id] = data
        if ttl > 0:
            self._expiry[object_id] = time.time() + ttl

    def load(self, object_id: str) -> Optional[bytes]:
        if object_id in self._expiry:
            if time.time() > self._expiry[object_id]:
                self.delete(object_id)
                return None
        return self._store.get(object_id)

    def delete(self, object_id: str) -> None:
        self._store.pop(object_id, None)
        self._expiry.pop(object_id, None)


class SharedMemoryBackend(StorageBackend):
    """
    共享内存存储
    - 同机器多进程零拷贝
    - 适合多 Worker 单机部署
    """
    def __init__(self, shm_prefix: str = "/sglang_tensor_"):
        self.shm_prefix = shm_prefix
        self._shm_handles: Dict[str, SharedMemory] = {}

    def store(self, object_id: str, data: bytes, ttl: int = 0) -> None:
        shm_name = self.shm_prefix + hashlib.md5(object_id.encode()).hexdigest()[:16]
        shm = SharedMemory(name=shm_name, create=True, size=len(data))
        shm.buf[:len(data)] = data
        self._shm_handles[object_id] = shm

    def load(self, object_id: str) -> Optional[bytes]:
        shm = self._shm_handles.get(object_id)
        if shm:
            return bytes(shm.buf)
        return None


class RedisBackend(StorageBackend):
    """
    Redis 存储 (可选)
    - 分布式共享
    - 自动过期
    - 需要外部 Redis
    """
    def __init__(self, host: str = "localhost", port: int = 6379):
        import redis
        self.client = redis.Redis(host=host, port=port)

    def store(self, object_id: str, data: bytes, ttl: int = 0) -> None:
        if ttl > 0:
            self.client.setex(object_id, ttl, data)
        else:
            self.client.set(object_id, data)


class S3Backend(StorageBackend):
    """
    S3 存储 (可选)
    - 大容量
    - 持久化
    - 适合调试/checkpoint
    """
    def __init__(self, bucket: str, prefix: str = "tensors/"):
        import boto3
        self.s3 = boto3.client('s3')
        self.bucket = bucket
        self.prefix = prefix
```

### 4.2 RequestContext 与 ExecutionPlan

#### 4.2.1 ExecutionPlan

```python
# 模型到执行计划的映射配置
PIPELINE_REGISTRY = {
    # Wan 系列
    "Wan-AI/Wan2.1-T2V-1.3B-Diffusers": {
        "stages": [
            {"name": "text_encoding", "pool": "wan-t5-encoder-pool"},
            {"name": "denoising", "pool": "wan-1.3b-t2v-dit-pool"},
            {"name": "vae_decoding", "pool": "wan-vae-pool"},
        ]
    },
    "Wan-AI/Wan2.1-T2V-14B-Diffusers": {
        "stages": [
            {"name": "text_encoding", "pool": "wan-t5-encoder-pool"},
            {"name": "denoising", "pool": "wan-14b-t2v-dit-pool"},
            {"name": "vae_decoding", "pool": "wan-vae-pool"},
        ]
    },
    "Wan-AI/Wan2.1-I2V-14B-720P-Diffusers": {
        "stages": [
            {"name": "text_encoding", "pool": "wan-t5-encoder-pool"},
            {"name": "image_encoding", "pool": "wan-clip-encoder-pool"},
            {"name": "denoising", "pool": "wan-14b-i2v-dit-pool"},
            {"name": "vae_decoding", "pool": "wan-vae-pool"},
        ]
    },

    # HunyuanVideo 系列
    "hunyuanvideo-community/HunyuanVideo": {
        "stages": [
            {"name": "text_encoding", "pool": "llama-encoder-pool"},
            {"name": "text_encoding_2", "pool": "clip-encoder-pool"},
            {"name": "denoising", "pool": "hunyuan-dit-pool"},
            {"name": "vae_decoding", "pool": "hunyuan-vae-pool"},
        ]
    },

    # FLUX 系列 (图像生成)
    "black-forest-labs/FLUX.1-dev": {
        "stages": [
            {"name": "text_encoding", "pool": "t5-encoder-pool"},
            {"name": "text_encoding_2", "pool": "clip-encoder-pool"},
            {"name": "denoising", "pool": "flux-dit-pool"},
            {"name": "vae_decoding", "pool": "flux-vae-pool"},
        ]
    },

    # 通用匹配模式
    "_patterns": [
        {
            "match": lambda path: "Wan" in path and "T2V" in path,
            "stages": [
                {"name": "text_encoding", "pool": "wan-t5-encoder-pool"},
                {"name": "denoising", "pool": "wan-dit-pool"},
                {"name": "vae_decoding", "pool": "wan-vae-pool"},
            ]
        },
    ]
}


def get_execution_plan(model_path: str) -> List[Dict[str, Any]]:
    """根据模型路径获取执行计划"""
    # 精确匹配
    if model_path in PIPELINE_REGISTRY:
        return PIPELINE_REGISTRY[model_path]["stages"]

    # 模式匹配
    for pattern in PIPELINE_REGISTRY.get("_patterns", []):
        if pattern["match"](model_path):
            return pattern["stages"]

    raise ValueError(f"Unknown model: {model_path}")
```

#### 4.2.2 RequestContext

```python
@dataclass
class RequestContext:
    """
    请求上下文，包含请求的全部状态
    状态随请求流转，Scheduler 无需持久化存储
    """
    # 基本信息
    req_id: str
    model: str
    params: dict                                    # 生成参数

    # 执行计划
    execution_plan: List[Dict[str, Any]]           # 完整的 stage 列表
    current_stage_index: int = 0                   # 当前执行到第几个 stage

    # 中间结果引用
    refs: Dict[str, dict] = field(default_factory=dict)  # name -> ObjectRef.to_dict()

    # 状态信息
    status: str = "pending"                        # pending, running, completed, failed
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

    # 可选字段
    priority: int = 0                              # 优先级，数值越大越优先
    timeout: float = 300                           # 超时时间
    retry_count: int = 0                           # 重试次数
    error: Optional[str] = None                    # 错误信息

    @property
    def current_stage(self) -> Optional[Dict[str, Any]]:
        """获取当前 stage"""
        if self.current_stage_index < len(self.execution_plan):
            return self.execution_plan[self.current_stage_index]
        return None

    @property
    def next_stage(self) -> Optional[Dict[str, Any]]:
        """获取下一个 stage"""
        next_idx = self.current_stage_index + 1
        if next_idx < len(self.execution_plan):
            return self.execution_plan[next_idx]
        return None

    @property
    def is_completed(self) -> bool:
        """是否已完成所有 stage"""
        return self.current_stage_index >= len(self.execution_plan)

    def advance(self) -> None:
        """推进到下一个 stage"""
        self.current_stage_index += 1
        self.updated_at = time.time()

    def add_ref(self, name: str, ref: ObjectRef) -> None:
        """添加中间结果引用"""
        self.refs[name] = ref.to_dict()
        self.updated_at = time.time()

    def get_ref(self, name: str) -> Optional[ObjectRef]:
        """获取中间结果引用"""
        if name in self.refs:
            return ObjectRef.from_dict(self.refs[name])
        return None

    def to_dict(self) -> dict:
        """序列化为字典"""
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "RequestContext":
        """从字典反序列化"""
        return cls(**d)

    @classmethod
    def create(
        cls,
        req_id: str,
        model: str,
        params: dict,
        priority: int = 0
    ) -> "RequestContext":
        """创建新的请求上下文"""
        return cls(
            req_id=req_id,
            model=model,
            params=params,
            execution_plan=get_execution_plan(model),
            priority=priority
        )
```

### 4.3 Scheduler 与 TaskQueue

#### 4.3.1 TaskQueue 后端

```python
class TaskQueueBackend(ABC):
    """任务队列后端抽象接口"""

    @abstractmethod
    async def push(self, pool: str, ctx: dict, priority: int = 0) -> None:
        """将任务推入指定 pool 的队列"""
        pass

    @abstractmethod
    async def pop(self, pool: str, timeout: float = 30) -> Optional[dict]:
        """从指定 pool 的队列取出任务 (阻塞)"""
        pass

    @abstractmethod
    async def peek(self, pool: str) -> Optional[dict]:
        """查看队首任务但不取出"""
        pass

    @abstractmethod
    async def size(self, pool: str) -> int:
        """获取队列大小"""
        pass

    @abstractmethod
    async def cancel(self, pool: str, req_id: str) -> bool:
        """取消指定任务"""
        pass


class MemoryQueueBackend(TaskQueueBackend):
    """
    内存队列 (默认)
    - 零依赖
    - 非持久化
    - 适合开发/测试
    """
    def __init__(self):
        self._queues: Dict[str, asyncio.PriorityQueue] = defaultdict(asyncio.PriorityQueue)
        self._cancelled: Set[str] = set()

    async def push(self, pool: str, ctx: dict, priority: int = 0) -> None:
        # PriorityQueue 按 (priority, timestamp) 排序，priority 越小越优先
        # 所以我们用 -priority 来实现数值越大越优先
        await self._queues[pool].put((-priority, time.time(), ctx))

    async def pop(self, pool: str, timeout: float = 30) -> Optional[dict]:
        try:
            _, _, ctx = await asyncio.wait_for(
                self._queues[pool].get(),
                timeout=timeout
            )
            # 检查是否已被取消
            if ctx.get("req_id") in self._cancelled:
                self._cancelled.discard(ctx.get("req_id"))
                return await self.pop(pool, timeout)  # 跳过已取消的任务
            return ctx
        except asyncio.TimeoutError:
            return None

    async def size(self, pool: str) -> int:
        return self._queues[pool].qsize()

    async def cancel(self, pool: str, req_id: str) -> bool:
        self._cancelled.add(req_id)
        return True


class SQLiteQueueBackend(TaskQueueBackend):
    """
    SQLite 队列 (零外部依赖持久化)
    - 本地持久化
    - 重启不丢失
    - 适合单机生产
    """
    def __init__(self, db_path: str = "/tmp/sglang_queue.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pool TEXT NOT NULL,
                req_id TEXT NOT NULL,
                priority INTEGER DEFAULT 0,
                created_at REAL NOT NULL,
                ctx TEXT NOT NULL,
                status TEXT DEFAULT 'pending'
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_pool_status ON tasks(pool, status)")
        conn.commit()
        conn.close()

    async def push(self, pool: str, ctx: dict, priority: int = 0) -> None:
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO tasks (pool, req_id, priority, created_at, ctx) VALUES (?, ?, ?, ?, ?)",
            (pool, ctx.get("req_id"), priority, time.time(), json.dumps(ctx))
        )
        conn.commit()
        conn.close()

    async def pop(self, pool: str, timeout: float = 30) -> Optional[dict]:
        start = time.time()
        while time.time() - start < timeout:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.execute(
                """
                SELECT id, ctx FROM tasks
                WHERE pool = ? AND status = 'pending'
                ORDER BY priority DESC, created_at ASC
                LIMIT 1
                """,
                (pool,)
            )
            row = cursor.fetchone()
            if row:
                task_id, ctx_json = row
                conn.execute("UPDATE tasks SET status = 'processing' WHERE id = ?", (task_id,))
                conn.commit()
                conn.close()
                return json.loads(ctx_json)
            conn.close()
            await asyncio.sleep(0.1)
        return None


class RedisQueueBackend(TaskQueueBackend):
    """
    Redis 队列 (分布式持久化)
    - 分布式共享
    - 多 Scheduler 协同
    - 适合大规模生产
    """
    def __init__(self, host: str = "localhost", port: int = 6379, prefix: str = "sglang:queue:"):
        import redis.asyncio as redis
        self.client = redis.Redis(host=host, port=port)
        self.prefix = prefix

    async def push(self, pool: str, ctx: dict, priority: int = 0) -> None:
        key = f"{self.prefix}{pool}"
        # 使用 ZADD，score = -priority (越大越优先)
        await self.client.zadd(key, {json.dumps(ctx): -priority})

    async def pop(self, pool: str, timeout: float = 30) -> Optional[dict]:
        key = f"{self.prefix}{pool}"
        # BZPOPMIN: 阻塞获取最小 score (最高优先级)
        result = await self.client.bzpopmin(key, timeout=timeout)
        if result:
            _, ctx_json, _ = result
            return json.loads(ctx_json)
        return None
```

#### 4.3.2 Scheduler

```python
class Scheduler:
    """
    中心调度器
    - 无状态设计，状态在 RequestContext 中
    - 支持水平扩展 (多 Scheduler 配合 Redis Queue)
    """

    def __init__(
        self,
        queue_backend: str = "memory",  # "memory", "sqlite", "redis"
        queue_config: dict = None,
        max_queue_size: int = 1000,     # 最大队列长度 (背压)
    ):
        # 初始化队列后端
        backends = {
            "memory": MemoryQueueBackend,
            "sqlite": SQLiteQueueBackend,
            "redis": RedisQueueBackend,
        }
        self.queue = backends[queue_backend](**(queue_config or {}))
        self.max_queue_size = max_queue_size

        # 指标
        self.metrics = SchedulerMetrics()

    async def submit(self, request: dict) -> str:
        """
        提交新请求

        Args:
            request: 包含 model, params 等信息的请求

        Returns:
            req_id: 请求 ID
        """
        # 创建 RequestContext
        req_id = str(uuid.uuid4())
        ctx = RequestContext.create(
            req_id=req_id,
            model=request["model"],
            params=request.get("params", {}),
            priority=request.get("priority", 0)
        )

        # 获取第一个 stage 的 pool
        first_stage = ctx.current_stage
        if not first_stage:
            raise ValueError("Empty execution plan")

        pool = first_stage["pool"]

        # 背压检查
        queue_size = await self.queue.size(pool)
        if queue_size >= self.max_queue_size:
            raise ServiceOverloadError(f"Queue {pool} is full")

        # 入队
        await self.queue.push(pool, ctx.to_dict(), ctx.priority)
        self.metrics.requests_submitted.inc()

        return req_id

    async def stage_completed(self, ctx_dict: dict, result_refs: Dict[str, dict]) -> None:
        """
        Worker 完成一个 stage 后回调

        Args:
            ctx_dict: 当前 RequestContext
            result_refs: 产出的 ObjectRef 字典
        """
        ctx = RequestContext.from_dict(ctx_dict)

        # 添加结果引用
        for name, ref_dict in result_refs.items():
            ctx.refs[name] = ref_dict

        # 推进到下一个 stage
        ctx.advance()

        if ctx.is_completed:
            # 所有 stage 完成，通知客户端
            await self._notify_completion(ctx)
        else:
            # 继续下一个 stage
            next_pool = ctx.current_stage["pool"]
            await self.queue.push(next_pool, ctx.to_dict(), ctx.priority)

    async def get_task(self, pool: str, timeout: float = 30) -> Optional[dict]:
        """
        Worker 拉取任务 (Pull 模式)

        Args:
            pool: Worker 所属的 pool 名称
            timeout: 等待超时

        Returns:
            RequestContext dict 或 None
        """
        ctx_dict = await self.queue.pop(pool, timeout)
        if ctx_dict:
            self.metrics.tasks_dispatched.labels(pool=pool).inc()
        return ctx_dict

    async def cancel(self, req_id: str) -> bool:
        """取消请求"""
        # 需要在所有可能的 pool 中取消
        # 实际实现中可能需要维护 req_id -> pool 的映射
        pass

    async def _notify_completion(self, ctx: RequestContext) -> None:
        """通知客户端请求完成"""
        # 通过 WebSocket / 回调 / 写入结果存储
        pass
```

### 4.4 Worker Pool

```python
class StageWorker:
    """
    Stage 执行器
    - 从 Scheduler 拉取任务
    - 执行模型推理
    - 将结果存入 TensorStore
    - 上报完成状态
    """

    def __init__(
        self,
        pool_name: str,
        stage_type: str,                # "text_encoding", "denoising", "vae_decoding"
        scheduler_address: str,
        model_path: str,
        device: str = "cuda:0",
        tensor_store_config: dict = None,
    ):
        self.pool_name = pool_name
        self.stage_type = stage_type
        self.scheduler = SchedulerClient(scheduler_address)
        self.tensor_store = TensorStore.create(**(tensor_store_config or {}))

        # 加载模型
        self.model = self._load_model(stage_type, model_path, device)

    def _load_model(self, stage_type: str, model_path: str, device: str):
        """根据 stage 类型加载对应模型"""
        loaders = {
            "text_encoding": load_text_encoder,
            "image_encoding": load_image_encoder,
            "denoising": load_dit_model,
            "vae_decoding": load_vae_decoder,
        }
        return loaders[stage_type](model_path, device)

    async def run(self):
        """主循环: 拉取任务 -> 执行 -> 上报"""
        while True:
            # Pull 模式: 主动拉取任务
            ctx_dict = await self.scheduler.get_task(self.pool_name)
            if ctx_dict is None:
                continue

            try:
                # 执行 stage
                result_refs = await self._execute_stage(ctx_dict)

                # 上报完成
                await self.scheduler.stage_completed(ctx_dict, result_refs)

            except Exception as e:
                # 错误处理
                await self.scheduler.stage_failed(ctx_dict, str(e))

    async def _execute_stage(self, ctx_dict: dict) -> Dict[str, dict]:
        """执行具体的 stage 逻辑"""
        ctx = RequestContext.from_dict(ctx_dict)
        result_refs = {}

        if self.stage_type == "text_encoding":
            # 文本编码
            prompt = ctx.params.get("prompt", "")
            embeddings = self.model.encode(prompt)

            # 存入 TensorStore
            ref = self.tensor_store.put(embeddings, ctx.req_id, "text_embeddings")
            result_refs["text_embeddings"] = ref.to_dict()

        elif self.stage_type == "denoising":
            # 获取依赖的 embeddings
            emb_ref = ctx.get_ref("text_embeddings")
            embeddings = self.tensor_store.get(emb_ref)

            # 执行去噪
            latents = self.model.denoise(
                embeddings=embeddings,
                num_steps=ctx.params.get("num_inference_steps", 50),
                guidance_scale=ctx.params.get("guidance_scale", 7.5),
            )

            # 存入 TensorStore
            ref = self.tensor_store.put(latents, ctx.req_id, "latents")
            result_refs["latents"] = ref.to_dict()

        elif self.stage_type == "vae_decoding":
            # 获取 latents
            latents_ref = ctx.get_ref("latents")
            latents = self.tensor_store.get(latents_ref)

            # VAE 解码
            output = self.model.decode(latents)

            # 最终结果可以直接返回或存储
            ref = self.tensor_store.put(output, ctx.req_id, "output")
            result_refs["output"] = ref.to_dict()

        return result_refs
```

---

## 5. 通信机制

### 5.1 Pull 模式

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              Pull 模式工作流                                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│                    ┌─────────────┐                                              │
│                    │  Scheduler  │                                              │
│                    │  TaskQueue  │                                              │
│                    └──────┬──────┘                                              │
│                           │                                                     │
│          ┌────────────────┼────────────────┐                                   │
│          │                │                │                                   │
│          ▼                ▼                ▼                                   │
│    ┌──────────┐     ┌──────────┐     ┌──────────┐                              │
│    │ Worker 1 │     │ Worker 2 │     │ Worker 3 │                              │
│    │  (idle)  │     │ (busy)   │     │  (idle)  │                              │
│    └────┬─────┘     └──────────┘     └────┬─────┘                              │
│         │                                  │                                    │
│         │ get_task()                       │ get_task()                         │
│         │────────────────►                 │────────────────►                   │
│         │◄────────────────                 │◄────────────────                   │
│         │   ctx_dict                       │   ctx_dict                         │
│                                                                                 │
│  优点:                                                                          │
│  • 天然负载均衡: 空闲 Worker 主动拉取                                           │
│  • 不会过载: Worker 处理完才拉新任务                                            │
│  • 异构友好: 快 Worker 多拉，慢 Worker 少拉                                     │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 数据传输

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         ObjectRef 点对点传输                                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  场景 1: 同节点传输 (零拷贝)                                                    │
│  ───────────────────────────                                                    │
│                                                                                 │
│    Worker A                          Worker B                                   │
│    (Node 1)                          (Node 1)                                   │
│       │                                 │                                       │
│       │  put(tensor) ──► SharedMemory   │                                       │
│       │  return ObjectRef               │                                       │
│       │ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─│                                       │
│       │         ctx with ObjectRef      │                                       │
│       │                                 │                                       │
│       │                    get(ref) ◄───│                                       │
│       │                    零拷贝读取    │                                       │
│                                                                                 │
│  场景 2: 跨节点传输 (ZMQ)                                                       │
│  ────────────────────────                                                       │
│                                                                                 │
│    Worker A                          Worker C                                   │
│    (Node 1)                          (Node 2)                                   │
│       │                                 │                                       │
│       │  put(tensor) ──► LocalMemory    │                                       │
│       │  return ObjectRef               │                                       │
│       │ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─│                                       │
│       │         ctx with ObjectRef      │                                       │
│       │                                 │                                       │
│       │◄────────── ZMQ Request ─────────│  get(ref)                             │
│       │─────────── ZMQ Response ───────►│  收到 tensor                          │
│                                                                                 │
│  关键: 元数据通过 Scheduler 流转，实际数据点对点传输                            │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. 高可用设计

### 6.1 Scheduler 高可用

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           Scheduler HA (Redis 后端)                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│                         ┌─────────────────┐                                     │
│                         │  Load Balancer  │                                     │
│                         └────────┬────────┘                                     │
│                                  │                                              │
│               ┌──────────────────┼──────────────────┐                          │
│               │                  │                  │                          │
│               ▼                  ▼                  ▼                          │
│        ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                   │
│        │ Scheduler 1 │    │ Scheduler 2 │    │ Scheduler 3 │                   │
│        │ (Stateless) │    │ (Stateless) │    │ (Stateless) │                   │
│        └──────┬──────┘    └──────┬──────┘    └──────┬──────┘                   │
│               │                  │                  │                          │
│               └──────────────────┼──────────────────┘                          │
│                                  │                                              │
│                                  ▼                                              │
│                         ┌─────────────────┐                                     │
│                         │   Redis Cluster │                                     │
│                         │   (TaskQueue)   │                                     │
│                         └─────────────────┘                                     │
│                                                                                 │
│  • 多个 Scheduler 实例共享同一个 Redis Queue                                    │
│  • 任何一个 Scheduler 挂掉，其他继续工作                                        │
│  • Worker 可以连接任意 Scheduler                                                │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Worker 故障恢复

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              Worker 故障恢复                                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  1. 心跳检测                                                                    │
│     • Worker 定期向 Scheduler 发送心跳                                          │
│     • 超时未收到心跳标记为不健康                                                │
│                                                                                 │
│  2. 任务超时                                                                    │
│     • 任务有执行超时时间                                                        │
│     • 超时未完成的任务重新入队                                                  │
│                                                                                 │
│  3. 任务幂等                                                                    │
│     • 使用 req_id + stage_index 作为任务唯一标识                                │
│     • 重复执行不会产生副作用                                                    │
│                                                                                 │
│  4. TensorStore 清理                                                            │
│     • ObjectRef 有 TTL                                                          │
│     • 超时自动清理孤儿数据                                                      │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. 生产特性

### 7.1 背压与限流

```python
class Scheduler:
    async def submit(self, request: dict) -> str:
        # 全局限流
        if self.metrics.active_requests >= self.max_concurrent:
            raise ServiceOverloadError("Too many concurrent requests")

        # 队列背压
        pool = ctx.current_stage["pool"]
        queue_size = await self.queue.size(pool)
        if queue_size >= self.max_queue_size:
            raise ServiceOverloadError(f"Queue {pool} is full")

        # 通过，提交任务
        ...
```

### 7.2 优先级队列

```python
# 请求提交时指定优先级
await scheduler.submit({
    "model": "Wan-AI/Wan2.1-T2V-14B-Diffusers",
    "params": {"prompt": "..."},
    "priority": 10,  # VIP 用户
})

# TaskQueue 按优先级排序
# priority 越大越优先
```

### 7.3 任务取消

```python
# 客户端取消
await scheduler.cancel(req_id)

# 实现机制
# 1. 标记 req_id 为 cancelled
# 2. Worker 拉取任务时检查，跳过已取消的
# 3. 清理相关 ObjectRef
```

### 7.4 监控指标

```python
class SchedulerMetrics:
    # 请求维度
    requests_submitted = Counter("requests_submitted_total")
    requests_completed = Counter("requests_completed_total")
    requests_failed = Counter("requests_failed_total")

    # 队列维度
    queue_size = Gauge("queue_size", labels=["pool"])

    # 延迟维度
    request_latency = Histogram("request_latency_seconds")
    stage_latency = Histogram("stage_latency_seconds", labels=["stage"])

    # Worker 维度
    worker_active = Gauge("worker_active", labels=["pool"])
    worker_idle = Gauge("worker_idle", labels=["pool"])
```

---

## 8. Kubernetes 部署方案

### 8.1 CRD 设计

```yaml
# DiffusionPipeline CRD
apiVersion: sglang.io/v1alpha1
kind: DiffusionPipeline
metadata:
  name: wan-t2v-pipeline
spec:
  model: "Wan-AI/Wan2.1-T2V-14B-Diffusers"

  scheduler:
    replicas: 2
    queueBackend: redis
    redis:
      host: redis-master
      port: 6379

  stages:
    - name: text-encoding
      pool: wan-t5-encoder-pool
      replicas: 2
      resources:
        limits:
          nvidia.com/gpu: 1
          memory: "16Gi"
      model:
        path: "google/t5-v1_1-xxl"

    - name: denoising
      pool: wan-14b-t2v-dit-pool
      replicas: 4
      resources:
        limits:
          nvidia.com/gpu: 8
          memory: "320Gi"
      model:
        path: "Wan-AI/Wan2.1-T2V-14B-Diffusers"
        component: transformer

    - name: vae-decoding
      pool: wan-vae-pool
      replicas: 2
      resources:
        limits:
          nvidia.com/gpu: 1
          memory: "32Gi"
      model:
        path: "Wan-AI/Wan2.1-T2V-14B-Diffusers"
        component: vae

  autoscaling:
    enabled: true
    minReplicas: 1
    maxReplicas: 10
    metrics:
      - type: Custom
        custom:
          name: queue_size
          target:
            type: Value
            value: "100"
```

### 8.2 部署架构

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         Kubernetes 部署架构                                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│    ┌──────────────────────────────────────────────────────────────────────┐    │
│    │                          Kubernetes Cluster                          │    │
│    ├──────────────────────────────────────────────────────────────────────┤    │
│    │                                                                      │    │
│    │   ┌────────────────────────────────────────────────────────────┐    │    │
│    │   │                    Control Plane                           │    │    │
│    │   │  ┌─────────────────┐     ┌─────────────────┐               │    │    │
│    │   │  │    Operator     │────►│ DiffusionPipeline│               │    │    │
│    │   │  │ (sglang-operator)│     │      CRD        │               │    │    │
│    │   │  └─────────────────┘     └─────────────────┘               │    │    │
│    │   └────────────────────────────────────────────────────────────┘    │    │
│    │                                                                      │    │
│    │   ┌────────────────────────────────────────────────────────────┐    │    │
│    │   │                    Data Plane                              │    │    │
│    │   │                                                            │    │    │
│    │   │   Namespace: sglang-wan-t2v                                │    │    │
│    │   │   ┌─────────────────────────────────────────────────────┐  │    │    │
│    │   │   │ Deployment: scheduler (replicas: 2)                 │  │    │    │
│    │   │   │   ┌─────────┐ ┌─────────┐                           │  │    │    │
│    │   │   │   │ sched-0 │ │ sched-1 │ ──► Service: scheduler    │  │    │    │
│    │   │   │   └─────────┘ └─────────┘                           │  │    │    │
│    │   │   └─────────────────────────────────────────────────────┘  │    │    │
│    │   │                                                            │    │    │
│    │   │   ┌─────────────────────────────────────────────────────┐  │    │    │
│    │   │   │ StatefulSet: encoder-pool (replicas: 2)             │  │    │    │
│    │   │   │   ┌─────────┐ ┌─────────┐                           │  │    │    │
│    │   │   │   │ enc-0   │ │ enc-1   │  GPU: 1x per pod          │  │    │    │
│    │   │   │   └─────────┘ └─────────┘                           │  │    │    │
│    │   │   └─────────────────────────────────────────────────────┘  │    │    │
│    │   │                                                            │    │    │
│    │   │   ┌─────────────────────────────────────────────────────┐  │    │    │
│    │   │   │ StatefulSet: dit-pool (replicas: 4)                 │  │    │    │
│    │   │   │   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │  │    │    │
│    │   │   │   │ dit-0   │ │ dit-1   │ │ dit-2   │ │ dit-3   │   │  │    │    │
│    │   │   │   │ 8xH100  │ │ 8xH100  │ │ 8xH100  │ │ 8xH100  │   │  │    │    │
│    │   │   │   └─────────┘ └─────────┘ └─────────┘ └─────────┘   │  │    │    │
│    │   │   └─────────────────────────────────────────────────────┘  │    │    │
│    │   │                                                            │    │    │
│    │   │   ┌─────────────────────────────────────────────────────┐  │    │    │
│    │   │   │ StatefulSet: vae-pool (replicas: 2)                 │  │    │    │
│    │   │   │   ┌─────────┐ ┌─────────┐                           │  │    │    │
│    │   │   │   │ vae-0   │ │ vae-1   │  GPU: 1x per pod          │  │    │    │
│    │   │   │   └─────────┘ └─────────┘                           │  │    │    │
│    │   │   └─────────────────────────────────────────────────────┘  │    │    │
│    │   │                                                            │    │    │
│    │   └────────────────────────────────────────────────────────────┘    │    │
│    │                                                                      │    │
│    │   ┌────────────────────────────────────────────────────────────┐    │    │
│    │   │                    Infrastructure                          │    │    │
│    │   │  ┌─────────────────┐     ┌─────────────────┐               │    │    │
│    │   │  │  Redis Cluster  │     │   Prometheus    │               │    │    │
│    │   │  │  (optional)     │     │   + Grafana     │               │    │    │
│    │   │  └─────────────────┘     └─────────────────┘               │    │    │
│    │   └────────────────────────────────────────────────────────────┘    │    │
│    │                                                                      │    │
│    └──────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 8.3 Helm Chart 结构

```
sglang-diffusion/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── _helpers.tpl
│   ├── scheduler-deployment.yaml
│   ├── scheduler-service.yaml
│   ├── encoder-statefulset.yaml
│   ├── dit-statefulset.yaml
│   ├── vae-statefulset.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── hpa.yaml
│   └── servicemonitor.yaml
└── crds/
    └── diffusionpipeline-crd.yaml
```

---

## 9. 性能评估

### 9.1 吞吐对比

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              吞吐对比 (估算)                                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  场景: Wan-14B T2V, 125 帧, 720P, 50 步                                         │
│  硬件: 32 × H100 GPU                                                            │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                                                                         │   │
│  │  当前架构 (单机 Pipeline):                                               │   │
│  │  ────────────────────────                                               │   │
│  │  • 4 台 8×H100 机器，每台运行完整 Pipeline                               │   │
│  │  • 吞吐: ~4 videos/min (每台 1 video/min)                               │   │
│  │  • GPU 利用率: ~40%                                                     │   │
│  │                                                                         │   │
│  │  新架构 (Disaggregated):                                                │   │
│  │  ────────────────────────                                               │   │
│  │  • Encoder Pool: 2 GPU                                                  │   │
│  │  • Denoising Pool: 28 GPU (4 × 7, 每个 Worker 7 GPU)                    │   │
│  │  • VAE Pool: 2 GPU                                                      │   │
│  │  • 吞吐: ~16-20 videos/min                                              │   │
│  │  • GPU 利用率: ~80%                                                     │   │
│  │                                                                         │   │
│  │  提升: 4-5x 🚀                                                          │   │
│  │                                                                         │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 9.2 延迟分析

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              延迟分析                                           │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  单请求延迟 (E2E):                                                              │
│  ─────────────────                                                              │
│  • Text Encoding:  ~2s                                                          │
│  • Denoising:      ~55s (50 steps × 1.1s/step)                                 │
│  • VAE Decoding:   ~3s                                                          │
│  • 数据传输开销:   ~1s (ObjectRef 传输)                                         │
│  • 总延迟:         ~61s (vs 当前 ~60s)                                          │
│                                                                                 │
│  结论: 单请求延迟基本持平，但吞吐大幅提升                                       │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. 实现路径

### 10.1 阶段规划

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              实现路径                                           │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Phase 1: MVP (2-3 周)                                                          │
│  ─────────────────────                                                          │
│  • ObjectRef + Memory TensorStore                                               │
│  • Memory TaskQueue + Scheduler                                                 │
│  • 单模型 Pipeline (Wan-T2V-1.3B)                                               │
│  • 本地多进程验证                                                               │
│                                                                                 │
│  Phase 2: 分布式 (2-3 周)                                                       │
│  ─────────────────────────                                                      │
│  • 跨节点 TensorStore (ZMQ)                                                     │
│  • SQLite/Redis TaskQueue                                                       │
│  • 多模型 Pipeline Registry                                                     │
│  • 多机部署验证                                                                 │
│                                                                                 │
│  Phase 3: 生产化 (2-3 周)                                                       │
│  ─────────────────────────                                                      │
│  • 优先级队列、取消、超时                                                       │
│  • Prometheus 指标                                                              │
│  • 错误处理完善                                                                 │
│  • 性能调优                                                                     │
│                                                                                 │
│  Phase 4: 云原生 (3-4 周)                                                       │
│  ─────────────────────────                                                      │
│  • Kubernetes Operator                                                          │
│  • DiffusionPipeline CRD                                                        │
│  • 自动扩缩容 (HPA)                                                             │
│  • Helm Chart                                                                   │
│                                                                                 │
│  总计: ~10-13 周 (2-3 个月)                                                      │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 10.2 文件结构

```
sglang/python/sglang/multimodal_gen/
├── distributed/                     # 新增: 分布式组件
│   ├── __init__.py
│   ├── object_ref.py               # ObjectRef 定义
│   ├── tensor_store/               # TensorStore 实现
│   │   ├── __init__.py
│   │   ├── base.py                 # 抽象接口
│   │   ├── memory.py               # 内存后端
│   │   ├── shared_memory.py        # 共享内存后端
│   │   ├── redis.py                # Redis 后端
│   │   └── s3.py                   # S3 后端
│   ├── task_queue/                 # TaskQueue 实现
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── memory.py
│   │   ├── sqlite.py
│   │   └── redis.py
│   ├── scheduler.py                # 分布式 Scheduler
│   ├── worker.py                   # Stage Worker
│   └── context.py                  # RequestContext
├── runtime/
│   ├── ...                         # 现有代码
│   └── pipelines/
│       └── execution_plan.py       # Pipeline Registry
└── k8s/                            # Kubernetes 部署
    ├── operator/
    ├── helm/
    └── examples/
```

---

## 附录

### A. 与 vLLM PD 分离对比

| 维度 | vLLM PD 分离 | SGLang Diffusion 分离 |
|------|-------------|---------------------|
| 分离粒度 | Prefill / Decode | Encoder / Denoising / Decoder |
| 中间数据 | KV Cache | Embeddings / Latents |
| 传输方式 | TCP/NCCL/Mooncake | ObjectRef + TensorStore |
| 调度模式 | 中心调度 | 中心调度 (Pull) |

### B. 参考资料

- [vLLM 官方文档](https://docs.vllm.ai/)
- [vLLM PD 分离设计](https://github.com/vllm-project/vllm/blob/main/docs/design/disaggregated_prefill.md)
- [AIBrix 项目](https://github.com/vllm-project/aibrix)
- [Ray Object Store 设计](https://docs.ray.io/en/latest/ray-core/objects.html)

---

> 文档版本: v1.0
> 最后更新: 2024-12


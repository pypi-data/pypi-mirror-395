# XWSystem Caching - Complete Usage Guide

**Company:** eXonware.com  
**Author:** Eng. Muhammad AlShehri  
**Version:** 0.0.1.388  
**Date:** 01-Nov-2025

---

## 📚 Table of Contents

1. [Quick Start](#quick-start)
2. [Core Cache Types](#core-cache-types)
3. [Advanced Cache Types](#advanced-cache-types)
4. [Decorators](#decorators)
5. [Security Features](#security-features)
6. [Performance Optimization](#performance-optimization)
7. [Integration Patterns](#integration-patterns)
8. [Best Practices](#best-practices)

---

## Quick Start

### Installation

```python
# Already included in xwsystem
from exonware.xwsystem.caching import LRUCache
```

### Basic Usage

```python
# Create cache
cache = LRUCache(capacity=100)

# Store data
cache.put('user:123', {'name': 'Alice'})

# Retrieve data
user = cache.get('user:123')

# Dictionary-style access
cache['product:456'] = {'name': 'Widget'}
product = cache['product:456']
```

---

## Core Cache Types

### LRU Cache (Least Recently Used)

**Best For:** General-purpose caching

```python
from exonware.xwsystem.caching import LRUCache

cache = LRUCache(capacity=1000, ttl=300.0)  # Optional TTL
cache.put('key', 'value')
value = cache.get('key')
```

**Features:**
- O(1) get/put operations
- Thread-safe
- Optional TTL support
- Statistics tracking

### LFU Cache (Least Frequently Used)

**Best For:** Data with varying access patterns

⚠️ **Note:** Use `OptimizedLFUCache` for better performance!

```python
from exonware.xwsystem.caching import OptimizedLFUCache

cache = OptimizedLFUCache(capacity=1000)
```

**Performance:**
- Optimized: O(1) eviction (100x+ faster)
- Standard: O(n) eviction (slow for large caches)

### TTL Cache (Time To Live)

**Best For:** Time-sensitive data (sessions, tokens)

```python
from exonware.xwsystem.caching import TTLCache

cache = TTLCache(capacity=1000, ttl=300.0, cleanup_interval=60.0)
cache.put('session:abc', session_data, ttl=600.0)  # Per-entry TTL
```

---

## Advanced Cache Types

### ReadThroughCache

**Auto-loads from storage on cache miss**

```python
from exonware.xwsystem.caching import ReadThroughCache

def load_user(user_id):
    return database.users.find_one({'id': user_id})

cache = ReadThroughCache(capacity=1000, loader=load_user)

# Automatically loads from DB if not cached
user = cache.get('user:123')
```

### WriteThroughCache

**Auto-persists to storage on cache write**

```python
from exonware.xwsystem.caching import WriteThroughCache

def save_user(key, value):
    database.users.update({'id': key}, value)

cache = WriteThroughCache(capacity=1000, writer=save_user)

# Automatically saves to DB when caching
cache.put('user:123', user_data)
```

### TaggedCache

**Tag-based bulk invalidation**

```python
from exonware.xwsystem.caching import TaggedCache

cache = TaggedCache(capacity=1000)

# Tag entries
cache.put('user:1', data, tags=['user', 'active'])
cache.put('user:2', data, tags=['user', 'inactive'])
cache.put('admin:1', data, tags=['admin', 'active'])

# Bulk invalidation by tag
cache.invalidate_by_tag('user')  # Clears all user entries

# Query by tag
user_keys = cache.get_keys_by_tag('user')
all_tags = cache.get_all_tags()
```

### WriteBehindCache

**Delayed persistence for high throughput**

```python
from exonware.xwsystem.caching import WriteBehindCache

def persist_to_db(key, value):
    database.save(key, value)

cache = WriteBehindCache(
    capacity=1000,
    writer=persist_to_db,
    flush_interval=5.0  # Flush every 5 seconds
)

# Writes cached immediately, persisted in background
cache.put('key', 'value')

# Force immediate flush
cache.flush()
```

### BloomFilterCache

**Fast negative lookups**

```python
from exonware.xwsystem.caching import BloomFilterCache

cache = BloomFilterCache(capacity=10000)

# Fast check without cache lookup
if not cache.might_contain('user:999'):
    return None  # Definitely not in cache

# Actual lookup
value = cache.get('user:999')
```

### SerializableCache

**Save/load cache state**

```python
from exonware.xwsystem.caching import SerializableCache

# Create and populate cache
cache = SerializableCache(capacity=1000)
cache.put('key1', 'value1')
cache.put('key2', 'value2')

# Save to disk
cache.save_to_file('cache_backup.pkl')

# Later... load from disk
cache2 = SerializableCache.load_from_file('cache_backup.pkl')
assert cache2.get('key1') == 'value1'
```

### ConditionalEvictionCache

**Custom eviction rules**

```python
from exonware.xwsystem.caching import ConditionalEvictionCache

# Protect entries starting with 'protected:'
def can_evict(key, value):
    return not str(key).startswith('protected:')

cache = ConditionalEvictionCache(
    capacity=100,
    eviction_policy=can_evict
)

cache.put('protected:admin', admin_data)  # Won't be evicted
cache.put('temp:data', temp_data)  # Can be evicted
```

---

## Decorators

### @xwcached - Simple Function Caching

```python
from exonware.xwsystem.caching import xwcached

@xwcached(ttl=300)
def get_user_profile(user_id):
    # Expensive database query
    return db.query(f"SELECT * FROM users WHERE id = {user_id}")

# First call - queries database
profile = get_user_profile(123)

# Second call - uses cache
profile = get_user_profile(123)  # Instant!
```

### @xwcached - Advanced with Hooks

```python
from exonware.xwsystem.caching import xwcached

hits = []
misses = []

@xwcached(
    namespace="user_api",
    condition=lambda args, kwargs: args[0] > 0,  # Only cache positive IDs
    on_hit=lambda k, v: hits.append(k),
    on_miss=lambda k, v: misses.append(k),
    key_builder=lambda f, a, kw: f"user:{a[0]}"
)
def get_user(user_id):
    return database.get_user(user_id)
```

### @xw_async_cached - Async Functions

```python
from exonware.xwsystem.caching import xw_async_cached

@xw_async_cached(ttl=60)
async def fetch_api_data(endpoint):
    async with httpx.AsyncClient() as client:
        response = await client.get(endpoint)
        return response.json()

# Automatic caching
data = await fetch_api_data("https://api.example.com/data")
```

---

## Security Features

### SecureLRUCache - Production Caching

```python
from exonware.xwsystem.caching import SecureLRUCache

cache = SecureLRUCache(
    capacity=1000,
    enable_integrity=True,        # Checksum verification
    enable_rate_limit=True,        # DoS protection
    max_ops_per_second=10000,      # Rate limit
    max_key_size=1024,             # Max key size (1KB)
    max_value_size_mb=10.0         # Max value size (10MB)
)

# Automatic validation
cache.put('api_response', large_data)  # Validates size
value = cache.get('api_response')       # Verifies integrity

# Security stats
stats = cache.get_security_stats()
print(f"Integrity violations: {stats['integrity_violations']}")
```

### Input Validation

```python
from exonware.xwsystem.caching import validate_cache_key, validate_cache_value

# Validate before caching
validate_cache_key(user_input_key)
validate_cache_value(user_data)

# Sanitize keys
from exonware.xwsystem.caching import sanitize_key
safe_key = sanitize_key(complex_object)
```

---

## Performance Optimization

### Memory-Bounded Caching

```python
from exonware.xwsystem.caching import MemoryBoundedLRUCache

# Cache limited by memory, not entry count
cache = MemoryBoundedLRUCache(
    capacity=10000,           # Fallback limit
    memory_budget_mb=500.0    # Primary: 500MB
)

# Automatically evicts to stay under budget
cache.put('large_dataset', huge_dataframe)
```

### Batch Operations

```python
from exonware.xwsystem.caching import OptimizedLFUCache

cache = OptimizedLFUCache(capacity=1000)

# Efficient batch operations
items = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
cache.put_many(items)

keys = ['key1', 'key2', 'key3']
results = cache.get_many(keys)

cache.delete_many(['key1', 'key2'])
```

### Prometheus Metrics

```python
from exonware.xwsystem.caching import LRUCache, PrometheusExporter

cache = LRUCache(capacity=1000, name="user_cache")
exporter = PrometheusExporter(cache)

# Export metrics
metrics = exporter.export_metrics()

# Use with Flask/FastAPI
@app.get("/metrics")
def metrics_endpoint():
    return Response(exporter.export_metrics(), media_type="text/plain")
```

---

## Integration Patterns

### Cache-Aside Pattern

```python
from exonware.xwsystem.caching import LRUCache

cache = LRUCache(capacity=1000)

def get_user(user_id):
    # 1. Try cache
    user = cache.get(f'user:{user_id}')
    if user:
        return user
    
    # 2. Load from DB
    user = db.users.find_one({'id': user_id})
    
    # 3. Store in cache
    if user:
        cache.put(f'user:{user_id}', user)
    
    return user
```

### Multi-Tier Caching

```python
from exonware.xwsystem.caching import LRUCache, TTLCache

# L1: Hot data (fast, small)
l1 = LRUCache(capacity=100)

# L2: Warm data (medium)
l2 = TTLCache(capacity=1000, ttl=3600)

def get_with_tiers(key):
    value = l1.get(key)
    if value: return value
    
    value = l2.get(key)
    if value:
        l1.put(key, value)  # Promote to L1
        return value
    
    value = expensive_load(key)
    l2.put(key, value)
    return value
```

### Async Patterns

```python
from exonware.xwsystem.caching import AsyncLRUCache

cache = AsyncLRUCache(capacity=500)

# Async context manager
async with AsyncLRUCache(100) as temp_cache:
    await temp_cache.put('temp', data)

# Async iteration
async for key in cache:
    value = await cache.get(key)
    print(f"{key}: {value}")

async for key, value in cache.items_async():
    print(f"{key}: {value}")
```

---

## Best Practices

### 1. Choose the Right Cache Type

| Use Case | Recommended Cache | Reason |
|----------|------------------|--------|
| API responses | TTLCache | Auto-expiration |
| Database queries | ReadThroughCache | Auto-loading |
| User sessions | TTLCache + Secure | Time-based + security |
| ML models | MemoryBoundedLRUCache | Control memory |
| Hot paths | OptimizedLFUCache | Frequency-based |
| High writes | WriteBehindCache | Better throughput |
| High misses | BloomFilterCache | Fast negative lookup |

### 2. Set Appropriate Capacity

```python
# Too small - frequent evictions
cache = LRUCache(capacity=10)  # ❌ Bad

# Reasonable size
cache = LRUCache(capacity=1000)  # ✅ Good

# Very large - use optimized version
cache = OptimizedLFUCache(capacity=100000)  # ✅ Use optimized for large
```

### 3. Use Security Features in Production

```python
# Development
cache = LRUCache(capacity=100)  # ✅ OK for dev

# Production
cache = SecureLRUCache(  # ✅ Use secure in production
    capacity=1000,
    enable_integrity=True,
    enable_rate_limit=True
)
```

### 4. Monitor Performance

```python
from exonware.xwsystem.caching import PrometheusExporter

cache = LRUCache(capacity=1000, name="my_cache")
exporter = PrometheusExporter(cache)

# Regular monitoring
stats = cache.get_stats()
if stats['hit_rate'] < 0.5:
    print("Low hit rate - consider adjusting capacity or TTL")
```

### 5. Handle Errors Gracefully

```python
from exonware.xwsystem.caching import CacheError

try:
    cache.put(large_key, large_value)
except CacheKeySizeError:
    # Use hash of key instead
    cache.put(hash(large_key), large_value)
except CacheValueSizeError:
    # Store reference instead of full value
    cache.put(key, {'ref': value_id})
```

---

## Common Use Cases

### Web API Caching

```python
from exonware.xwsystem.caching import TTLCache, xwcached

response_cache = TTLCache(capacity=5000, ttl=300)

@app.get("/users/{user_id}")
@xwcached(cache=response_cache, ttl=300)
def get_user_endpoint(user_id: int):
    return db.users.get(user_id)
```

### Database Query Caching

```python
from exonware.xwsystem.caching import ReadThroughCache

query_cache = ReadThroughCache(
    capacity=1000,
    loader=lambda query_id: execute_query(query_id)
)

result = query_cache.get('complex_query_123')  # Auto-executes if not cached
```

### Session Management

```python
from exonware.xwsystem.caching import SecureTTLCache

session_cache = SecureTTLCache(
    capacity=10000,
    ttl=1800.0,  # 30 minutes
    enable_rate_limit=True
)

session_cache.put(session_id, session_data)
```

### ML Model Caching

```python
from exonware.xwsystem.caching import MemoryBoundedLRUCache, xwcached

model_cache = MemoryBoundedLRUCache(
    capacity=10,
    memory_budget_mb=2000.0  # 2GB for models
)

@xwcached(cache=model_cache)
def load_model(model_name):
    return torch.load(f"models/{model_name}.pth")
```

### Configuration Caching

```python
from exonware.xwsystem.caching import TTLCache, xwcached

config_cache = TTLCache(capacity=50, ttl=600)

@xwcached(cache=config_cache)
def load_config(config_name):
    return yaml.safe_load(open(f"configs/{config_name}.yaml"))
```

---

## Performance Tips

### 1. Use Optimized Versions

```python
# ❌ Slow for large caches
cache = LFUCache(capacity=10000)  # O(n) eviction

# ✅ Fast for any size
cache = OptimizedLFUCache(capacity=10000)  # O(1) eviction
```

### 2. Batch Operations

```python
# ❌ Slow - multiple lock acquisitions
for key, value in items.items():
    cache.put(key, value)

# ✅ Fast - single lock
cache.put_many(items)
```

### 3. Use Bloom Filters for High Miss Rates

```python
from exonware.xwsystem.caching import BloomFilterCache

cache = BloomFilterCache(capacity=10000)

# Fast rejection without locking
if not cache.might_contain(key):
    return None  # Skip expensive lookup
```

### 4. Async for Async Code

```python
# ❌ Don't use sync cache in async code
cache = LRUCache(capacity=100)
value = cache.get(key)  # Blocks event loop

# ✅ Use async cache
cache = AsyncLRUCache(capacity=100)
value = await cache.get(key)  # Non-blocking
```

---

## Monitoring & Observability

### Statistics Collection

```python
stats = cache.get_stats()

print(f"Hit Rate: {stats['hit_rate']:.2%}")
print(f"Size: {stats['size']}/{stats['capacity']}")
print(f"Evictions: {stats['evictions']}")
```

### Multi-Cache Monitoring

```python
from exonware.xwsystem.caching import StatsCollector

collector = StatsCollector()
collector.register('users', user_cache)
collector.register('products', product_cache)
collector.register('sessions', session_cache)

# Collect all stats
all_stats = collector.collect_all()

# Export for Prometheus
metrics = collector.export_prometheus()
```

---

## Migration Guide

### From functools.lru_cache

```python
# Before
from functools import lru_cache

@lru_cache(maxsize=128)
def my_function(x):
    return x * 2

# After
from exonware.xwsystem.caching import xwcache

@xwcache
def my_function(x):
    return x * 2

# Benefits: hooks, TTL, statistics, custom key builders
```

### From cachetools

```python
# Before
from cachetools import LRUCache, cached

cache = LRUCache(maxsize=100)

@cached(cache)
def my_function(x):
    return x * 2

# After
from exonware.xwsystem.caching import LRUCache, xwcached

cache = LRUCache(capacity=100)

@xwcached(cache=cache)
def my_function(x):
    return x * 2

# Benefits: security features, better stats, async support
```

---

## Error Handling

```python
from exonware.xwsystem.caching import (
    CacheError,
    CacheKeySizeError,
    CacheValueSizeError,
    CacheRateLimitError,
    CacheIntegrityError,
)

try:
    cache.put(key, value)
except CacheKeySizeError:
    # Key too large
    cache.put(hash(key), value)
except CacheValueSizeError:
    # Value too large
    cache.put(key, compress(value))
except CacheRateLimitError:
    # Rate limit exceeded
    time.sleep(0.1)
except CacheIntegrityError:
    # Integrity check failed
    cache.delete(key)
```

---

## See Also

- [Examples Directory](../../../examples/caching/)
- [Test Suite](../../../tests/)
- [API Reference](./contracts.py)
- [GUIDELINES_DEV.md](../../../docs/GUIDELINES_DEV.md)
- [GUIDELINES_TEST.md](../../../docs/GUIDELINES_TEST.md)

---

## Support

**Company:** eXonware.com  
**Email:** connect@exonware.com  
**Documentation:** https://exonware.com/docs/xwsystem/caching

---

**Last Updated:** 01-Nov-2025  
**Version:** 0.0.1.388


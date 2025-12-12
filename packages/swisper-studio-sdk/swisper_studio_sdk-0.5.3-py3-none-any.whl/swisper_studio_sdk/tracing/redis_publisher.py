"""
Redis Streams publisher for non-blocking observability.

Publishes trace events to Redis Streams with 1-2ms latency.

Architecture:
- SDK publishes events via Redis XADD (fire-and-forget)
- SwisperStudio consumer reads from stream and stores in DB
- Heartbeat mechanism for connection verification

v0.5.1: ROBUST FAILURE HANDLING
- All operations have timeouts (DEFAULT_TIMEOUT = 3 seconds)
- SDK NEVER blocks Swisper, even with misconfiguration
- Graceful degradation - if Redis fails, tracing is disabled silently
- All exceptions caught and logged, never propagated

v0.4.0: Redis Streams migration from HTTP
"""

import redis.asyncio as redis
import json
import time
import asyncio
import logging
from typing import Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

# ============================================================================
# CRITICAL DESIGN PRINCIPLE:
# The SDK must NEVER block or crash Swisper, even if:
# - Redis is misconfigured
# - Redis is unreachable
# - SwisperStudio is down
# - Any timeout occurs
#
# All operations have timeouts and fail silently.
# ============================================================================

# Default timeout for ALL Redis operations (seconds)
DEFAULT_TIMEOUT = 3.0

# Connection timeout (shorter for fast fail)
CONNECTION_TIMEOUT = 5.0

# Global state
_redis_client: Optional[redis.Redis] = None
_stream_name: str = "observability:events"
_max_stream_length: int = 100000
_project_id: str = ""
_initialized: bool = False
_initialization_failed: bool = False


async def initialize_redis_publisher(
    redis_url: str,
    stream_name: str = "observability:events",
    project_id: str = "",
    max_stream_length: int = 100000,
    verify_consumer: bool = True,
    connection_timeout: float = CONNECTION_TIMEOUT,
) -> Dict[str, bool]:
    """
    Initialize Redis publisher for observability events.
    
    ROBUST: This function NEVER raises exceptions.
    If initialization fails, tracing is silently disabled.

    Args:
        redis_url: Redis connection URL (e.g., "redis://redis:6379")
        stream_name: Stream name for events
        project_id: SwisperStudio project ID
        max_stream_length: Max events to keep in stream (FIFO eviction)
        verify_consumer: If True, check that consumer is running
        connection_timeout: Timeout for connection (default: 5s)

    Returns:
        dict: Verification results (never raises)
            {
                "redis": bool,      # Redis connectivity OK
                "write": bool,      # Write permission OK
                "consumer": bool,   # Consumer detected and healthy
                "initialized": bool # Overall initialization status
            }
    """
    global _redis_client, _stream_name, _max_stream_length, _project_id
    global _initialized, _initialization_failed

    verification_results = {
        "redis": False,
        "write": False,
        "consumer": False,
        "initialized": False,
    }

    try:
        # Create Redis client with socket timeout
        _redis_client = redis.from_url(
            redis_url,
            decode_responses=False,
            socket_timeout=connection_timeout,
            socket_connect_timeout=connection_timeout,
        )
        _stream_name = stream_name
        _max_stream_length = max_stream_length
        _project_id = project_id

        # Test connection WITH TIMEOUT
        try:
            await asyncio.wait_for(
                _redis_client.ping(),
                timeout=connection_timeout
            )
            verification_results["redis"] = True
            logger.info("✅ Redis connectivity: OK")
        except asyncio.TimeoutError:
            logger.warning(f"⚠️ Redis connection timed out after {connection_timeout}s")
            logger.warning("   Tracing will be DISABLED (Swisper continues normally)")
            _redis_client = None
            _initialization_failed = True
            return verification_results
        except Exception as e:
            logger.warning(f"⚠️ Redis connection failed: {e}")
            logger.warning("   Tracing will be DISABLED (Swisper continues normally)")
            _redis_client = None
            _initialization_failed = True
            return verification_results

        # Test write permission WITH TIMEOUT
        try:
            await asyncio.wait_for(
                _redis_client.xadd(
                    "observability:health_check",
                    {b"test": b"ping", b"timestamp": str(time.time()).encode()},
                    maxlen=10
                ),
                timeout=DEFAULT_TIMEOUT
            )
            verification_results["write"] = True
            logger.info("✅ Redis write permission: OK")
        except asyncio.TimeoutError:
            logger.warning("⚠️ Redis write timed out")
            logger.warning("   Tracing will be DISABLED")
            _redis_client = None
            _initialization_failed = True
            return verification_results
        except Exception as e:
            logger.warning(f"⚠️ Redis write failed: {e}")
            logger.warning("   Tracing will be DISABLED")
            _redis_client = None
            _initialization_failed = True
            return verification_results

        # Check consumer heartbeat (if requested) - non-critical
        if verify_consumer:
            consumer_healthy = await _verify_consumer_health(_redis_client)
            verification_results["consumer"] = consumer_healthy
            
            if consumer_healthy:
                logger.info("✅ Consumer detected: HEALTHY")
            else:
                logger.warning("⚠️ Consumer not detected")
                logger.warning("   Events will queue until consumer starts")
                # Don't fail initialization - events will queue

        logger.info(f"✅ Redis publisher initialized successfully")
        logger.info(f"   Stream: {stream_name}")
        logger.info(f"   Project: {project_id}")

        _initialized = True
        verification_results["initialized"] = True
        return verification_results

    except Exception as e:
        # CATCH-ALL: Any unexpected error disables tracing silently
        logger.warning(f"⚠️ Redis publisher initialization failed: {e}")
        logger.warning("   Tracing will be DISABLED (Swisper continues normally)")
        _redis_client = None
        _initialization_failed = True
        return verification_results


async def _verify_consumer_health(
    redis_client: redis.Redis,
    timeout: float = DEFAULT_TIMEOUT
) -> bool:
    """
    Verify SwisperStudio consumer is running and healthy.

    Checks for consumer heartbeat written every 5 seconds.
    Returns True if consumer active, False otherwise.
    
    NEVER raises - always returns bool.
    """
    try:
        # Check for heartbeat key WITH TIMEOUT
        heartbeat_data = await asyncio.wait_for(
            redis_client.get("swisper_studio:consumer:heartbeat"),
            timeout=timeout
        )

        if not heartbeat_data:
            logger.debug("⚠️ SwisperStudio consumer heartbeat not found")
            return False

        # Parse heartbeat (decode if bytes)
        if isinstance(heartbeat_data, bytes):
            heartbeat_data = heartbeat_data.decode('utf-8')
        
        heartbeat = json.loads(heartbeat_data)
        timestamp = datetime.fromisoformat(heartbeat["timestamp"])
        age_seconds = (datetime.utcnow() - timestamp).total_seconds()

        if age_seconds > 10:
            logger.debug(f"⚠️ Consumer heartbeat stale ({age_seconds:.0f}s old)")
            return False

        logger.debug(f"   Last seen: {age_seconds:.1f} seconds ago")
        return True

    except asyncio.TimeoutError:
        logger.debug("⚠️ Timeout checking consumer heartbeat")
        return False
    except Exception as e:
        logger.debug(f"⚠️ Failed to verify consumer: {e}")
        return False


def get_redis_client() -> Optional[redis.Redis]:
    """
    Get the global Redis client.
    
    Returns None if:
    - Not initialized
    - Initialization failed
    - Client was disabled due to errors
    """
    if _initialization_failed:
        return None
    return _redis_client


def is_tracing_initialized() -> bool:
    """Check if tracing was successfully initialized."""
    return _initialized and not _initialization_failed


def get_project_id() -> str:
    """Get the configured project ID"""
    return _project_id


async def publish_event(
    event_type: str,
    trace_id: Optional[str],
    observation_id: Optional[str] = None,
    data: Optional[Dict[str, Any]] = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> bool:
    """
    Publish observability event to Redis Stream.

    Non-blocking - returns in 1-2ms typically.
    
    ROBUST: NEVER raises exceptions, NEVER blocks indefinitely.
    Returns True if published, False if failed (silently).

    Args:
        event_type: Event type (trace_start, observation_start, observation_end, etc.)
        trace_id: Trace identifier (can be None for heartbeats)
        observation_id: Observation identifier (if applicable)
        data: Event data (will be JSON serialized)
        timeout: Max time to wait for Redis (default: 3s)

    Returns:
        bool: True if published successfully, False otherwise
    """
    client = get_redis_client()
    if not client:
        # Tracing disabled or not initialized - silent no-op
        return False

    try:
        # Build event payload (all fields as bytes for Redis)
        event = {
            b"event_type": event_type.encode(),
            b"project_id": _project_id.encode(),
            b"timestamp": str(time.time()).encode(),
        }
        
        if trace_id:
            event[b"trace_id"] = trace_id.encode()

        if observation_id:
            event[b"observation_id"] = observation_id.encode()

        if data:
            # Serialize data to JSON
            event[b"data"] = json.dumps(data, default=str).encode()

        # XADD with TIMEOUT - publish to stream (1-2ms typically)
        await asyncio.wait_for(
            client.xadd(
                _stream_name,
                event,
                maxlen=_max_stream_length,  # Prevent unbounded growth
            ),
            timeout=timeout
        )

        logger.debug(f"Published {event_type} event to {_stream_name}")
        return True

    except asyncio.TimeoutError:
        # Timeout - log and continue (don't block Swisper)
        logger.debug(f"Timeout publishing {event_type} event (>{timeout}s)")
        return False
    except Exception as e:
        # Any error - log and continue (don't block Swisper)
        logger.debug(f"Failed to publish event: {e}")
        return False


async def is_tracing_enabled_for_project(
    project_id: str,
    timeout: float = DEFAULT_TIMEOUT
) -> bool:
    """
    Check if tracing is enabled for this project (Q2: Tracing Toggle).
    
    Uses Redis cache for speed (1-2ms).
    Cache is managed by SwisperStudio backend.
    
    ROBUST: NEVER blocks indefinitely, defaults to enabled on failure.
    
    Performance:
    - Cache hit: ~1ms (Redis GET)
    - Cache miss: Defaults to enabled (fail-open)
    - Timeout/Error: Defaults to enabled (fail-open)
    
    Args:
        project_id: Project UUID
        timeout: Max time to wait for Redis (default: 3s)
        
    Returns:
        True if tracing enabled (or if unable to check), False if disabled
    """
    client = get_redis_client()
    if not client:
        # Tracing not initialized, default to disabled (no point checking)
        return False
    
    cache_key = f"tracing:{project_id}:enabled"
    
    try:
        # GET with TIMEOUT
        cached = await asyncio.wait_for(
            client.get(cache_key),
            timeout=timeout
        )
        
        # Cached value
        if cached == b"true":
            logger.debug(f"Tracing enabled for project {project_id[:8]}...")
            return True
        elif cached == b"false":
            logger.debug(f"Tracing disabled for project {project_id[:8]}...")
            return False
        
        # Cache miss - default to enabled (fail-open)
        logger.debug(f"Cache miss for project {project_id[:8]}..., defaulting to enabled")
        return True
    
    except asyncio.TimeoutError:
        # Timeout - default to enabled (fail-open, don't block Swisper)
        logger.debug(f"Timeout checking tracing status, defaulting to enabled")
        return True
    except Exception as e:
        # Redis error - default to enabled (fail-open)
        logger.debug(f"Error checking tracing status: {e}, defaulting to enabled")
        return True


async def close_redis_publisher() -> None:
    """
    Close Redis connection gracefully.

    Call this on application shutdown.
    NEVER raises exceptions.
    """
    global _redis_client, _initialized, _initialization_failed

    if _redis_client:
        try:
            await asyncio.wait_for(
                _redis_client.close(),
                timeout=DEFAULT_TIMEOUT
            )
            logger.info("✅ Redis publisher closed")
        except Exception as e:
            logger.debug(f"⚠️ Error closing Redis publisher: {e}")
        finally:
            _redis_client = None
            _initialized = False
            _initialization_failed = False


def disable_tracing() -> None:
    """
    Manually disable tracing (for emergency use).
    
    Call this if you need to disable tracing at runtime.
    """
    global _redis_client, _initialization_failed
    
    _redis_client = None
    _initialization_failed = True
    logger.info("🔴 Tracing manually disabled")

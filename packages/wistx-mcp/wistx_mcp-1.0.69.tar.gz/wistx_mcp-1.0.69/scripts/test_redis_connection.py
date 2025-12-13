"""Test Redis connection for local development."""

import asyncio
import logging
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_redis_connection():
    """Test Redis connection with various configurations."""
    logger.info("=" * 60)
    logger.info("Redis Connection Test")
    logger.info("=" * 60)

    redis_url = os.getenv("REDIS_URL")
    memorystore_host = os.getenv("MEMORYSTORE_HOST")
    memorystore_port = int(os.getenv("MEMORYSTORE_PORT", "6379"))
    memorystore_enabled = os.getenv("MEMORYSTORE_ENABLED", "false").lower() == "true"
    redis_password = os.getenv("REDIS_PASSWORD")

    logger.info("\n📋 Configuration:")
    logger.info(f"  REDIS_URL: {redis_url or 'Not set'}")
    logger.info(f"  MEMORYSTORE_HOST: {memorystore_host or 'Not set'}")
    logger.info(f"  MEMORYSTORE_PORT: {memorystore_port}")
    logger.info(f"  MEMORYSTORE_ENABLED: {memorystore_enabled}")
    logger.info(f"  REDIS_PASSWORD: {'Set' if redis_password else 'Not set'}")

    try:
        import redis.asyncio as redis
        logger.info("\n✅ redis package is installed")
    except ImportError:
        logger.error("\n❌ redis package not installed")
        logger.info("Install with: pip install redis")
        return False

    client = None
    connection_method = None

    try:
        if redis_url:
            logger.info("\n🔌 Attempting connection via REDIS_URL...")
            client = redis.from_url(
                redis_url,
                encoding="utf-8",
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
            )
            connection_method = "REDIS_URL"
        elif memorystore_enabled and memorystore_host:
            logger.info(f"\n🔌 Attempting connection via Memorystore config...")
            logger.info(f"  Host: {memorystore_host}:{memorystore_port}")
            redis_kwargs = {
                "host": memorystore_host,
                "port": memorystore_port,
                "encoding": "utf-8",
                "decode_responses": True,
                "socket_connect_timeout": 10,
                "socket_timeout": 10,
            }
            if redis_password:
                redis_kwargs["password"] = redis_password
                logger.info("  Using password authentication")
            client = redis.Redis(**redis_kwargs)
            connection_method = "MEMORYSTORE"
        else:
            logger.warning("\n⚠️  No Redis configuration found")
            logger.info("Set one of:")
            logger.info("  - REDIS_URL=redis://localhost:6379")
            logger.info("  - MEMORYSTORE_ENABLED=true MEMORYSTORE_HOST=localhost")
            return False

        logger.info(f"\n🧪 Testing connection ({connection_method})...")

        ping_result = await asyncio.wait_for(client.ping(), timeout=5)
        if ping_result:
            logger.info("✅ PING successful - Redis is connected!")

        logger.info("\n🧪 Testing basic operations...")

        test_key = "wistx:test:connection"
        test_value = "test_value_12345"

        await client.set(test_key, test_value, ex=60)
        logger.info(f"✅ SET operation successful")

        retrieved_value = await client.get(test_key)
        if retrieved_value == test_value:
            logger.info(f"✅ GET operation successful (value: {retrieved_value})")
        else:
            logger.error(f"❌ GET operation failed (expected: {test_value}, got: {retrieved_value})")
            return False

        await client.delete(test_key)
        logger.info(f"✅ DELETE operation successful")

        logger.info("\n🧪 Testing subscription cache operations...")

        cache_key = "subscription:test_user_123"
        cache_data = {
            "subscription_id": "sub_test_123",
            "status": "active",
            "plan": "professional",
            "current_period_start": 1234567890,
            "current_period_end": 1234567890,
        }

        import json
        await client.setex(
            cache_key,
            60,
            json.dumps(cache_data, default=str),
        )
        logger.info(f"✅ Cache SET operation successful")

        cached_data = await client.get(cache_key)
        if cached_data:
            parsed_data = json.loads(cached_data)
            if parsed_data["subscription_id"] == cache_data["subscription_id"]:
                logger.info(f"✅ Cache GET operation successful")
            else:
                logger.error(f"❌ Cache data mismatch")
                return False
        else:
            logger.error(f"❌ Cache GET returned None")
            return False

        await client.delete(cache_key)
        logger.info(f"✅ Cache DELETE operation successful")

        logger.info("\n🧪 Testing Redis info...")
        info = await client.info("server")
        redis_version = info.get("redis_version", "unknown")
        logger.info(f"  Redis version: {redis_version}")

        info_memory = await client.info("memory")
        used_memory = info_memory.get("used_memory_human", "unknown")
        logger.info(f"  Used memory: {used_memory}")

        logger.info("\n" + "=" * 60)
        logger.info("✅ ALL TESTS PASSED - Redis is working correctly!")
        logger.info("=" * 60)
        logger.info("\n💡 Your application can now use Redis for:")
        logger.info("   - Subscription caching")
        logger.info("   - Webhook event processing")
        logger.info("   - Rate limiting")
        logger.info("   - Distributed caching")

        return True

    except asyncio.TimeoutError:
        logger.error("\n❌ Connection timeout - Redis is not reachable")
        logger.info("\n🔍 Troubleshooting:")
        logger.info("  1. Check if Docker container is running:")
        logger.info("     docker ps | grep redis")
        logger.info("  2. Check if Redis is listening on port 6379:")
        logger.info("     docker port <container_id>")
        logger.info("  3. Try connecting manually:")
        logger.info("     docker exec -it <container_id> redis-cli ping")
        return False

    except redis.ConnectionError as e:
        logger.error(f"\n❌ Connection error: {e}")
        logger.info("\n🔍 Troubleshooting:")
        logger.info("  1. Verify Docker container is running:")
        logger.info("     docker ps")
        logger.info("  2. Check container logs:")
        logger.info("     docker logs <container_id>")
        logger.info("  3. Verify port mapping:")
        logger.info("     docker port <container_id>")
        logger.info("  4. Test connection from host:")
        logger.info("     redis-cli -h localhost -p 6379 ping")
        return False

    except Exception as e:
        logger.error(f"\n❌ Unexpected error: {e}", exc_info=True)
        return False

    finally:
        if client:
            try:
                await client.aclose()
                logger.info("\n🔌 Connection closed")
            except Exception as e:
                logger.warning(f"Error closing connection: {e}")


async def test_application_redis_manager():
    """Test using the application's Redis client manager."""
    logger.info("\n" + "=" * 60)
    logger.info("Testing Application Redis Manager")
    logger.info("=" * 60)

    try:
        from api.database.redis_client import get_redis_manager

        manager = await get_redis_manager()
        if not manager:
            logger.warning("⚠️  Redis manager not initialized (Redis not configured)")
            return False

        client = await manager.get_client()
        if not client:
            logger.warning("⚠️  Redis client not available")
            return False

        ping_result = await manager.ping()
        if ping_result:
            logger.info("✅ Application Redis manager is working!")
            logger.info("\n📊 Health Status:")
            health = manager.get_health_status()
            logger.info(f"  Healthy: {health['healthy']}")
            logger.info(f"  Circuit State: {health['circuit_state']}")
            logger.info(f"  Client Initialized: {health['client_initialized']}")
            return True
        else:
            logger.error("❌ Application Redis manager ping failed")
            return False

    except Exception as e:
        logger.error(f"❌ Error testing application Redis manager: {e}", exc_info=True)
        return False


async def main():
    """Run all Redis tests."""
    logger.info("\n🚀 Starting Redis Connection Tests\n")

    test1_result = await test_redis_connection()
    test2_result = await test_application_redis_manager()

    logger.info("\n" + "=" * 60)
    logger.info("Test Summary")
    logger.info("=" * 60)
    logger.info(f"Direct Redis Connection: {'✅ PASS' if test1_result else '❌ FAIL'}")
    logger.info(f"Application Redis Manager: {'✅ PASS' if test2_result else '❌ FAIL'}")

    if test1_result and test2_result:
        logger.info("\n🎉 All tests passed! Redis is ready for use.")
        return 0
    else:
        logger.error("\n⚠️  Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)


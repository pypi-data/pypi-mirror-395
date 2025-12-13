"""Simple Redis connection test without application dependencies."""

import asyncio
import os
import sys

async def test_redis():
    """Test Redis connection."""
    try:
        import redis.asyncio as redis
        print("✅ redis package is installed")
    except ImportError:
        print("❌ redis package not installed")
        print("Install with: pip install redis")
        return False

    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    print(f"\n🔌 Connecting to: {redis_url}")

    try:
        client = redis.from_url(
            redis_url,
            encoding="utf-8",
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
        )

        print("🧪 Testing PING...")
        result = await client.ping()
        if result:
            print("✅ PING successful!")

        print("\n🧪 Testing SET/GET...")
        await client.set("wistx:test", "working", ex=60)
        value = await client.get("wistx:test")
        if value == "working":
            print("✅ SET/GET successful!")
        else:
            print(f"❌ GET failed (expected 'working', got '{value}')")
            return False

        await client.delete("wistx:test")
        print("✅ DELETE successful!")

        print("\n🧪 Testing subscription cache format...")
        import json
        cache_data = {
            "subscription_id": "sub_test",
            "status": "active",
            "plan": "professional",
        }
        cache_key = "subscription:test_user"
        await client.setex(cache_key, 60, json.dumps(cache_data))
        cached = await client.get(cache_key)
        if cached:
            parsed = json.loads(cached)
            if parsed["subscription_id"] == cache_data["subscription_id"]:
                print("✅ Cache operations successful!")
            else:
                print("❌ Cache data mismatch")
                return False
        else:
            print("❌ Cache GET returned None")
            return False

        await client.delete(cache_key)

        info = await client.info("server")
        print(f"\n📊 Redis Info:")
        print(f"  Version: {info.get('redis_version', 'unknown')}")
        print(f"  OS: {info.get('os', 'unknown')}")

        await client.aclose()
        print("\n🎉 All tests passed! Redis is working correctly.")
        print("\n💡 To use in your application, set:")
        print("   REDIS_URL=redis://localhost:6379")
        print("   # Or")
        print("   MEMORYSTORE_ENABLED=true")
        print("   MEMORYSTORE_HOST=localhost")
        print("   MEMORYSTORE_PORT=6379")
        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n🔍 Troubleshooting:")
        print("  1. Check if Redis is running: docker ps | grep redis")
        print("  2. Check port: docker port redis-session")
        print("  3. Test manually: docker exec redis-session redis-cli ping")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_redis())
    sys.exit(0 if success else 1)


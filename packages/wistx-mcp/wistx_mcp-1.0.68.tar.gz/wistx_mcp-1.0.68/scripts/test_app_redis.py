"""Test application's Redis client manager."""

import asyncio
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

os.environ.setdefault("REDIS_URL", "redis://localhost:6379")

async def test_app_redis():
    """Test application Redis client manager."""
    print("=" * 60)
    print("Testing Application Redis Client Manager")
    print("=" * 60)
    
    try:
        from api.database.redis_client import get_redis_manager
        
        print("\n🔌 Initializing Redis manager...")
        manager = await get_redis_manager()
        
        if not manager:
            print("⚠️  Redis manager not initialized (Redis not configured)")
            print("💡 Set REDIS_URL=redis://localhost:6379")
            return False
        
        print("✅ Redis manager initialized")
        
        print("\n🧪 Testing connection...")
        ping_result = await manager.ping()
        if ping_result:
            print("✅ PING successful!")
        else:
            print("❌ PING failed")
            return False
        
        print("\n🧪 Testing operations via manager...")
        client = await manager.get_client()
        if not client:
            print("❌ Could not get Redis client")
            return False
        
        import json
        test_key = "wistx:test:app"
        test_data = {"test": "data", "number": 123}
        
        await manager.execute(
            lambda c, *args, **kwargs: c.setex(
                test_key, 60, json.dumps(test_data)
            ),
            test_key,
            60,
            json.dumps(test_data)
        )
        print("✅ SET operation via manager successful")
        
        result = await manager.execute(
            lambda c, *args: c.get(test_key),
            test_key
        )
        
        if result:
            parsed = json.loads(result)
            if parsed == test_data:
                print("✅ GET operation via manager successful")
            else:
                print(f"❌ Data mismatch: {parsed} != {test_data}")
                return False
        else:
            print("❌ GET returned None")
            return False
        
        await manager.execute(lambda c, *args: c.delete(test_key), test_key)
        print("✅ DELETE operation via manager successful")
        
        print("\n📊 Health Status:")
        health = manager.get_health_status()
        print(f"  Healthy: {health['healthy']}")
        print(f"  Circuit State: {health['circuit_state']}")
        print(f"  Client Initialized: {health['client_initialized']}")
        print(f"  Failure Count: {health['failure_count']}")
        
        print("\n📈 Statistics:")
        stats = manager.get_stats()
        print(f"  Total Operations: {stats['metrics']['total_operations']}")
        print(f"  Successful: {stats['metrics']['successful_operations']}")
        print(f"  Failed: {stats['metrics']['failed_operations']}")
        print(f"  Retries: {stats['metrics']['retries']}")
        
        print("\n" + "=" * 60)
        print("✅ Application Redis Manager is working correctly!")
        print("=" * 60)
        print("\n💡 Your application can now use Redis for:")
        print("   - Subscription caching")
        print("   - Webhook event processing")
        print("   - Rate limiting")
        print("   - Distributed caching")
        
        await manager.close()
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're in the project directory and dependencies are installed")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_app_redis())
    sys.exit(0 if success else 1)


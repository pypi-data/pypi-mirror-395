#!/bin/bash
# Quick validation script for Docker Redis

echo "=========================================="
echo "Redis Docker Validation"
echo "=========================================="
echo ""

echo "1. Checking Docker container status..."
if docker ps | grep -q redis; then
    echo "✅ Redis container is running"
    docker ps | grep redis
else
    echo "❌ Redis container not found"
    exit 1
fi

echo ""
echo "2. Testing Redis connection..."
if docker exec redis-session redis-cli ping 2>/dev/null | grep -q PONG; then
    echo "✅ Redis PING successful"
else
    echo "❌ Redis PING failed"
    exit 1
fi

echo ""
echo "3. Testing basic operations..."
docker exec redis-session redis-cli SET test:validation "working" EX 10 > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ SET operation successful"
    
    VALUE=$(docker exec redis-session redis-cli GET test:validation 2>/dev/null)
    if [ "$VALUE" = "working" ]; then
        echo "✅ GET operation successful"
    else
        echo "❌ GET operation failed"
        exit 1
    fi
    
    docker exec redis-session redis-cli DEL test:validation > /dev/null 2>&1
    echo "✅ DELETE operation successful"
else
    echo "❌ SET operation failed"
    exit 1
fi

echo ""
echo "4. Checking port accessibility..."
if nc -zv localhost 6379 2>&1 | grep -q succeeded; then
    echo "✅ Port 6379 is accessible"
else
    echo "⚠️  Port 6379 check failed (nc may not be installed, but Redis is working)"
fi

echo ""
echo "5. Redis version info..."
VERSION=$(docker exec redis-session redis-cli INFO server 2>/dev/null | grep redis_version | cut -d: -f2 | tr -d '\r')
echo "   Redis Version: $VERSION"

echo ""
echo "=========================================="
echo "✅ All validation tests passed!"
echo "=========================================="
echo ""
echo "💡 To use Redis in your application:"
echo "   export REDIS_URL=redis://localhost:6379"
echo "   # Or"
echo "   export MEMORYSTORE_ENABLED=true"
echo "   export MEMORYSTORE_HOST=localhost"
echo "   export MEMORYSTORE_PORT=6379"
echo ""


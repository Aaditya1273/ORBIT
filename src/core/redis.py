"""
ORBIT Redis Configuration
Redis client setup for caching and session management
"""

import redis.asyncio as redis
import json
from typing import Any, Optional, Dict
from datetime import datetime, timedelta
import structlog

from .config import settings

logger = structlog.get_logger(__name__)

# Global Redis client
redis_client: Optional[redis.Redis] = None


async def init_redis():
    """Initialize Redis connection"""
    global redis_client
    
    try:
        # Parse Redis URL
        redis_url = settings.REDIS_URL
        
        # Create Redis client
        redis_client = redis.from_url(
            redis_url,
            encoding="utf-8",
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
            retry_on_timeout=True,
            health_check_interval=30
        )
        
        # Test connection
        await redis_client.ping()
        
        logger.info("Redis connection established", url=redis_url.split('@')[0] + '@***')
        
    except Exception as e:
        logger.error("Failed to connect to Redis", error=str(e))
        raise


async def get_redis() -> redis.Redis:
    """Get Redis client instance"""
    global redis_client
    
    if redis_client is None:
        await init_redis()
    
    return redis_client


class RedisCache:
    """Redis-based caching utility for ORBIT"""
    
    def __init__(self):
        self.client = None
    
    async def _get_client(self):
        """Get Redis client"""
        if self.client is None:
            self.client = await get_redis()
        return self.client
    
    async def set(
        self, 
        key: str, 
        value: Any, 
        expire: Optional[int] = None,
        namespace: str = "orbit"
    ) -> bool:
        """
        Set a value in Redis cache
        
        Args:
            key: Cache key
            value: Value to cache (will be JSON serialized)
            expire: Expiration time in seconds
            namespace: Key namespace
        """
        try:
            client = await self._get_client()
            
            # Add namespace prefix
            full_key = f"{namespace}:{key}"
            
            # Serialize value
            if isinstance(value, (dict, list)):
                serialized_value = json.dumps(value)
            else:
                serialized_value = str(value)
            
            # Set with expiration
            if expire:
                await client.setex(full_key, expire, serialized_value)
            else:
                await client.set(full_key, serialized_value)
            
            return True
            
        except Exception as e:
            logger.error("Redis set failed", key=key, error=str(e))
            return False
    
    async def get(
        self, 
        key: str, 
        namespace: str = "orbit",
        default: Any = None
    ) -> Any:
        """
        Get a value from Redis cache
        
        Args:
            key: Cache key
            namespace: Key namespace
            default: Default value if key not found
        """
        try:
            client = await self._get_client()
            
            # Add namespace prefix
            full_key = f"{namespace}:{key}"
            
            # Get value
            value = await client.get(full_key)
            
            if value is None:
                return default
            
            # Try to deserialize JSON
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return value
                
        except Exception as e:
            logger.error("Redis get failed", key=key, error=str(e))
            return default
    
    async def delete(self, key: str, namespace: str = "orbit") -> bool:
        """Delete a key from Redis cache"""
        try:
            client = await self._get_client()
            full_key = f"{namespace}:{key}"
            
            result = await client.delete(full_key)
            return result > 0
            
        except Exception as e:
            logger.error("Redis delete failed", key=key, error=str(e))
            return False
    
    async def exists(self, key: str, namespace: str = "orbit") -> bool:
        """Check if a key exists in Redis cache"""
        try:
            client = await self._get_client()
            full_key = f"{namespace}:{key}"
            
            result = await client.exists(full_key)
            return result > 0
            
        except Exception as e:
            logger.error("Redis exists check failed", key=key, error=str(e))
            return False
    
    async def increment(
        self, 
        key: str, 
        amount: int = 1, 
        namespace: str = "orbit",
        expire: Optional[int] = None
    ) -> int:
        """Increment a counter in Redis"""
        try:
            client = await self._get_client()
            full_key = f"{namespace}:{key}"
            
            # Increment
            result = await client.incrby(full_key, amount)
            
            # Set expiration if specified
            if expire and result == amount:  # First time setting
                await client.expire(full_key, expire)
            
            return result
            
        except Exception as e:
            logger.error("Redis increment failed", key=key, error=str(e))
            return 0
    
    async def set_hash(
        self, 
        key: str, 
        mapping: Dict[str, Any], 
        namespace: str = "orbit",
        expire: Optional[int] = None
    ) -> bool:
        """Set a hash in Redis"""
        try:
            client = await self._get_client()
            full_key = f"{namespace}:{key}"
            
            # Serialize values in mapping
            serialized_mapping = {}
            for k, v in mapping.items():
                if isinstance(v, (dict, list)):
                    serialized_mapping[k] = json.dumps(v)
                else:
                    serialized_mapping[k] = str(v)
            
            # Set hash
            await client.hset(full_key, mapping=serialized_mapping)
            
            # Set expiration
            if expire:
                await client.expire(full_key, expire)
            
            return True
            
        except Exception as e:
            logger.error("Redis hash set failed", key=key, error=str(e))
            return False
    
    async def get_hash(
        self, 
        key: str, 
        field: Optional[str] = None,
        namespace: str = "orbit"
    ) -> Any:
        """Get a hash or hash field from Redis"""
        try:
            client = await self._get_client()
            full_key = f"{namespace}:{key}"
            
            if field:
                # Get specific field
                value = await client.hget(full_key, field)
                if value is None:
                    return None
                
                try:
                    return json.loads(value)
                except (json.JSONDecodeError, TypeError):
                    return value
            else:
                # Get entire hash
                hash_data = await client.hgetall(full_key)
                
                # Deserialize values
                result = {}
                for k, v in hash_data.items():
                    try:
                        result[k] = json.loads(v)
                    except (json.JSONDecodeError, TypeError):
                        result[k] = v
                
                return result
                
        except Exception as e:
            logger.error("Redis hash get failed", key=key, field=field, error=str(e))
            return None
    
    async def list_keys(self, pattern: str = "*", namespace: str = "orbit") -> list:
        """List keys matching a pattern"""
        try:
            client = await self._get_client()
            full_pattern = f"{namespace}:{pattern}"
            
            keys = await client.keys(full_pattern)
            
            # Remove namespace prefix
            return [key.replace(f"{namespace}:", "") for key in keys]
            
        except Exception as e:
            logger.error("Redis keys list failed", pattern=pattern, error=str(e))
            return []


# Global cache instance
cache = RedisCache()


class SessionManager:
    """Redis-based session management for ORBIT"""
    
    def __init__(self):
        self.cache = cache
        self.session_prefix = "session"
        self.default_expire = 24 * 60 * 60  # 24 hours
    
    async def create_session(
        self, 
        user_id: str, 
        session_data: Dict[str, Any],
        expire: Optional[int] = None
    ) -> str:
        """Create a new session"""
        import uuid
        
        session_id = str(uuid.uuid4())
        session_key = f"{self.session_prefix}:{session_id}"
        
        # Add metadata
        session_data.update({
            "user_id": user_id,
            "created_at": datetime.utcnow().isoformat(),
            "last_accessed": datetime.utcnow().isoformat()
        })
        
        # Store session
        await self.cache.set(
            session_key, 
            session_data, 
            expire=expire or self.default_expire
        )
        
        return session_id
    
    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data"""
        session_key = f"{self.session_prefix}:{session_id}"
        session_data = await self.cache.get(session_key)
        
        if session_data:
            # Update last accessed
            session_data["last_accessed"] = datetime.utcnow().isoformat()
            await self.cache.set(session_key, session_data, expire=self.default_expire)
        
        return session_data
    
    async def update_session(
        self, 
        session_id: str, 
        updates: Dict[str, Any]
    ) -> bool:
        """Update session data"""
        session_key = f"{self.session_prefix}:{session_id}"
        session_data = await self.cache.get(session_key)
        
        if session_data:
            session_data.update(updates)
            session_data["last_accessed"] = datetime.utcnow().isoformat()
            
            return await self.cache.set(
                session_key, 
                session_data, 
                expire=self.default_expire
            )
        
        return False
    
    async def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        session_key = f"{self.session_prefix}:{session_id}"
        return await self.cache.delete(session_key)
    
    async def cleanup_expired_sessions(self):
        """Clean up expired sessions (called by background task)"""
        try:
            # This is handled automatically by Redis TTL
            # But we can add custom cleanup logic here if needed
            pass
        except Exception as e:
            logger.error("Session cleanup failed", error=str(e))


# Global session manager
session_manager = SessionManager()


async def health_check_redis() -> Dict[str, Any]:
    """Health check for Redis connection"""
    try:
        client = await get_redis()
        
        # Test basic operations
        test_key = "health_check"
        await client.set(test_key, "ok", ex=10)
        result = await client.get(test_key)
        await client.delete(test_key)
        
        if result == "ok":
            return {
                "status": "healthy",
                "message": "Redis connection successful",
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            return {
                "status": "unhealthy", 
                "message": "Redis test failed",
                "timestamp": datetime.utcnow().isoformat()
            }
            
    except Exception as e:
        return {
            "status": "unhealthy",
            "message": f"Redis error: {str(e)}",
            "timestamp": datetime.utcnow().isoformat()
        }
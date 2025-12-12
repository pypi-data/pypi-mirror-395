# cc_toolkit/redis_utils.py - Redis utility functions for the cc_toolkit package
import redis
from typing import Any, Optional, Union, List, Dict


class RedisClient:
    """
    A simple Redis client wrapper for common Redis operations.
    """
    
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0, password: Optional[str] = None, **kwargs):
        """
        Initialize Redis client connection.
        
        Args:
            host (str): Redis server hostname.
            port (int): Redis server port.
            db (int): Redis database index.
            password (Optional[str]): Redis password if authentication is enabled.
            **kwargs: Additional parameters for redis.Redis.
        """
        self.client = redis.Redis(host=host, port=port, db=db, password=password, **kwargs)
    
    def set(self, key: str, value: Any, ex: Optional[int] = None, px: Optional[int] = None) -> bool:
        """
        Set a key-value pair in Redis.
        
        Args:
            key (str): The key to set.
            value (Any): The value to set.
            ex (Optional[int]): Expiration time in seconds.
            px (Optional[int]): Expiration time in milliseconds.
            
        Returns:
            bool: True if the operation succeeded, False otherwise.
        """
        return self.client.set(key, value, ex=ex, px=px)
    
    def get(self, key: str) -> Optional[str]:
        """
        Get a value from Redis by key.
        
        Args:
            key (str): The key to get.
            
        Returns:
            Optional[str]: The value if the key exists, None otherwise.
        """
        return self.client.get(key)
    
    def delete(self, *keys: str) -> int:
        """
        Delete one or more keys from Redis.
        
        Args:
            *keys (str): The keys to delete.
            
        Returns:
            int: The number of keys deleted.
        """
        return self.client.delete(*keys)
    
    def exists(self, *keys: str) -> int:
        """
        Check if one or more keys exist in Redis.
        
        Args:
            *keys (str): The keys to check.
            
        Returns:
            int: The number of keys that exist.
        """
        return self.client.exists(*keys)
    
    def expire(self, key: str, seconds: int) -> bool:
        """
        Set expiration time for a key in seconds.
        
        Args:
            key (str): The key to set expiration for.
            seconds (int): Expiration time in seconds.
            
        Returns:
            bool: True if the operation succeeded, False otherwise.
        """
        return self.client.expire(key, seconds)
    
    def ttl(self, key: str) -> int:
        """
        Get the time to live for a key in seconds.
        
        Args:
            key (str): The key to check.
            
        Returns:
            int: TTL in seconds, -1 if key exists but has no expiration, -2 if key does not exist.
        """
        return self.client.ttl(key)
    
    def incr(self, key: str, amount: int = 1) -> int:
        """
        Increment a key by a given amount.
        
        Args:
            key (str): The key to increment.
            amount (int): The amount to increment by.
            
        Returns:
            int: The value after incrementing.
        """
        return self.client.incr(key, amount)
    
    def decr(self, key: str, amount: int = 1) -> int:
        """
        Decrement a key by a given amount.
        
        Args:
            key (str): The key to decrement.
            amount (int): The amount to decrement by.
            
        Returns:
            int: The value after decrementing.
        """
        return self.client.decr(key, amount)
    
    def hset(self, name: str, key: str, value: Any) -> int:
        """
        Set a field in a hash stored at key.
        
        Args:
            name (str): The hash name.
            key (str): The field name.
            value (Any): The field value.
            
        Returns:
            int: The number of fields that were added.
        """
        return self.client.hset(name, key, value)
    
    def hget(self, name: str, key: str) -> Optional[str]:
        """
        Get a field from a hash stored at key.
        
        Args:
            name (str): The hash name.
            key (str): The field name.
            
        Returns:
            Optional[str]: The field value if the field exists, None otherwise.
        """
        return self.client.hget(name, key)
    
    def hgetall(self, name: str) -> Dict[str, str]:
        """
        Get all fields and values from a hash.
        
        Args:
            name (str): The hash name.
            
        Returns:
            Dict[str, str]: A dictionary of field-value pairs.
        """
        return self.client.hgetall(name)
    
    def hdel(self, name: str, *keys: str) -> int:
        """
        Delete one or more fields from a hash.
        
        Args:
            name (str): The hash name.
            *keys (str): The fields to delete.
            
        Returns:
            int: The number of fields deleted.
        """
        return self.client.hdel(name, *keys)
    
    def lpush(self, name: str, *values: Any) -> int:
        """
        Push one or more values onto the head of a list.
        
        Args:
            name (str): The list name.
            *values (Any): The values to push.
            
        Returns:
            int: The length of the list after the push operation.
        """
        return self.client.lpush(name, *values)
    
    def rpush(self, name: str, *values: Any) -> int:
        """
        Push one or more values onto the tail of a list.
        
        Args:
            name (str): The list name.
            *values (Any): The values to push.
            
        Returns:
            int: The length of the list after the push operation.
        """
        return self.client.rpush(name, *values)
    
    def lpop(self, name: str) -> Optional[str]:
        """
        Remove and return the first element of a list.
        
        Args:
            name (str): The list name.
            
        Returns:
            Optional[str]: The first element, or None if the list is empty.
        """
        return self.client.lpop(name)
    
    def rpop(self, name: str) -> Optional[str]:
        """
        Remove and return the last element of a list.
        
        Args:
            name (str): The list name.
            
        Returns:
            Optional[str]: The last element, or None if the list is empty.
        """
        return self.client.rpop(name)
    
    def lrange(self, name: str, start: int, end: int) -> List[str]:
        """
        Get a range of elements from a list.
        
        Args:
            name (str): The list name.
            start (int): The starting index.
            end (int): The ending index (inclusive). Use -1 for the last element.
            
        Returns:
            List[str]: A list of elements in the specified range.
        """
        return self.client.lrange(name, start, end)
    
    def sadd(self, name: str, *values: Any) -> int:
        """
        Add one or more members to a set.
        
        Args:
            name (str): The set name.
            *values (Any): The values to add.
            
        Returns:
            int: The number of members added to the set.
        """
        return self.client.sadd(name, *values)
    
    def smembers(self, name: str) -> List[str]:
        """
        Get all members of a set.
        
        Args:
            name (str): The set name.
            
        Returns:
            List[str]: A list of all members in the set.
        """
        return list(self.client.smembers(name))
    
    def sismember(self, name: str, value: Any) -> bool:
        """
        Check if a value is a member of a set.
        
        Args:
            name (str): The set name.
            value (Any): The value to check.
            
        Returns:
            bool: True if the value is a member, False otherwise.
        """
        return self.client.sismember(name, value)
    
    def srem(self, name: str, *values: Any) -> int:
        """
        Remove one or more members from a set.
        
        Args:
            name (str): The set name.
            *values (Any): The values to remove.
            
        Returns:
            int: The number of members removed from the set.
        """
        return self.client.srem(name, *values)
    
    def close(self) -> None:
        """
        Close the Redis connection.
        """
        self.client.close()
    
    def __enter__(self):
        """
        Support for context manager protocol.
        """
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Support for context manager protocol. Closes the connection when exiting the context.
        """
        self.close()

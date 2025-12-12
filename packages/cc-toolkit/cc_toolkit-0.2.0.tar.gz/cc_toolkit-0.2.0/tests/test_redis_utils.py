import unittest
from unittest.mock import patch, MagicMock
from cc_toolkit.redis_utils import RedisClient


class TestRedisClient(unittest.TestCase):
    """Test cases for RedisClient class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.host = "localhost"
        self.port = 6379
        self.db = 0
        self.password = None
        
    @patch('redis.Redis')
    def test_init(self, mock_redis):
        """Test initialization of RedisClient"""
        client = RedisClient(host=self.host, port=self.port, db=self.db, password=self.password)
        mock_redis.assert_called_once_with(
            host=self.host, port=self.port, db=self.db, password=self.password
        )
    
    @patch('redis.Redis')
    def test_set(self, mock_redis):
        """Test set method"""
        mock_client = MagicMock()
        mock_client.set.return_value = True
        mock_redis.return_value = mock_client
        
        client = RedisClient()
        result = client.set("test_key", "test_value", ex=3600)
        
        mock_client.set.assert_called_once_with("test_key", "test_value", ex=3600, px=None)
        self.assertTrue(result)
    
    @patch('redis.Redis')
    def test_get(self, mock_redis):
        """Test get method"""
        mock_client = MagicMock()
        mock_client.get.return_value = "test_value"
        mock_redis.return_value = mock_client
        
        client = RedisClient()
        result = client.get("test_key")
        
        mock_client.get.assert_called_once_with("test_key")
        self.assertEqual(result, "test_value")
    
    @patch('redis.Redis')
    def test_delete(self, mock_redis):
        """Test delete method"""
        mock_client = MagicMock()
        mock_client.delete.return_value = 1
        mock_redis.return_value = mock_client
        
        client = RedisClient()
        result = client.delete("test_key")
        
        mock_client.delete.assert_called_once_with("test_key")
        self.assertEqual(result, 1)
    
    @patch('redis.Redis')
    def test_exists(self, mock_redis):
        """Test exists method"""
        mock_client = MagicMock()
        mock_client.exists.return_value = 1
        mock_redis.return_value = mock_client
        
        client = RedisClient()
        result = client.exists("test_key")
        
        mock_client.exists.assert_called_once_with("test_key")
        self.assertEqual(result, 1)
    
    @patch('redis.Redis')
    def test_expire(self, mock_redis):
        """Test expire method"""
        mock_client = MagicMock()
        mock_client.expire.return_value = True
        mock_redis.return_value = mock_client
        
        client = RedisClient()
        result = client.expire("test_key", 3600)
        
        mock_client.expire.assert_called_once_with("test_key", 3600)
        self.assertTrue(result)
    
    @patch('redis.Redis')
    def test_incr(self, mock_redis):
        """Test incr method"""
        mock_client = MagicMock()
        mock_client.incr.return_value = 1
        mock_redis.return_value = mock_client
        
        client = RedisClient()
        result = client.incr("test_key")
        
        mock_client.incr.assert_called_once_with("test_key", 1)
        self.assertEqual(result, 1)
    
    @patch('redis.Redis')
    def test_decr(self, mock_redis):
        """Test decr method"""
        mock_client = MagicMock()
        mock_client.decr.return_value = 0
        mock_redis.return_value = mock_client
        
        client = RedisClient()
        result = client.decr("test_key")
        
        mock_client.decr.assert_called_once_with("test_key", 1)
        self.assertEqual(result, 0)
    
    @patch('redis.Redis')
    def test_hset(self, mock_redis):
        """Test hset method"""
        mock_client = MagicMock()
        mock_client.hset.return_value = 1
        mock_redis.return_value = mock_client
        
        client = RedisClient()
        result = client.hset("test_hash", "field", "value")
        
        mock_client.hset.assert_called_once_with("test_hash", "field", "value")
        self.assertEqual(result, 1)
    
    @patch('redis.Redis')
    def test_hget(self, mock_redis):
        """Test hget method"""
        mock_client = MagicMock()
        mock_client.hget.return_value = "value"
        mock_redis.return_value = mock_client
        
        client = RedisClient()
        result = client.hget("test_hash", "field")
        
        mock_client.hget.assert_called_once_with("test_hash", "field")
        self.assertEqual(result, "value")
    
    @patch('redis.Redis')
    def test_hgetall(self, mock_redis):
        """Test hgetall method"""
        mock_client = MagicMock()
        mock_client.hgetall.return_value = {"field1": "value1", "field2": "value2"}
        mock_redis.return_value = mock_client
        
        client = RedisClient()
        result = client.hgetall("test_hash")
        
        mock_client.hgetall.assert_called_once_with("test_hash")
        self.assertEqual(result, {"field1": "value1", "field2": "value2"})
    
    @patch('redis.Redis')
    def test_lpush(self, mock_redis):
        """Test lpush method"""
        mock_client = MagicMock()
        mock_client.lpush.return_value = 3
        mock_redis.return_value = mock_client
        
        client = RedisClient()
        result = client.lpush("test_list", "value1", "value2", "value3")
        
        mock_client.lpush.assert_called_once_with("test_list", "value1", "value2", "value3")
        self.assertEqual(result, 3)
    
    @patch('redis.Redis')
    def test_rpush(self, mock_redis):
        """Test rpush method"""
        mock_client = MagicMock()
        mock_client.rpush.return_value = 3
        mock_redis.return_value = mock_client
        
        client = RedisClient()
        result = client.rpush("test_list", "value1", "value2", "value3")
        
        mock_client.rpush.assert_called_once_with("test_list", "value1", "value2", "value3")
        self.assertEqual(result, 3)
    
    @patch('redis.Redis')
    def test_sadd(self, mock_redis):
        """Test sadd method"""
        mock_client = MagicMock()
        mock_client.sadd.return_value = 2
        mock_redis.return_value = mock_client
        
        client = RedisClient()
        result = client.sadd("test_set", "value1", "value2")
        
        mock_client.sadd.assert_called_once_with("test_set", "value1", "value2")
        self.assertEqual(result, 2)
    
    @patch('redis.Redis')
    def test_smembers(self, mock_redis):
        """Test smembers method"""
        mock_client = MagicMock()
        mock_client.smembers.return_value = {"value1", "value2"}
        mock_redis.return_value = mock_client
        
        client = RedisClient()
        result = client.smembers("test_set")
        
        mock_client.smembers.assert_called_once_with("test_set")
        self.assertEqual(set(result), {"value1", "value2"})
    
    @patch('redis.Redis')
    def test_context_manager(self, mock_redis):
        """Test context manager support"""
        mock_client = MagicMock()
        mock_redis.return_value = mock_client
        
        with RedisClient() as client:
            client.set("test_key", "test_value")
        
        mock_client.set.assert_called_once()
        mock_client.close.assert_called_once()
    
    @patch('redis.Redis')
    def test_close(self, mock_redis):
        """Test close method"""
        mock_client = MagicMock()
        mock_redis.return_value = mock_client
        
        client = RedisClient()
        client.close()
        
        mock_client.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()

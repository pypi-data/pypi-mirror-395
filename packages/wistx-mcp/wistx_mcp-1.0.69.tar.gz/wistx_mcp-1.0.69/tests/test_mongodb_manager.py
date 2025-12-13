import unittest
from unittest.mock import MagicMock, patch
import time
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure

from api.database.mongodb import MongoDBManager
from api.database.circuit_breaker import CircuitBreaker, CircuitState
from api.database.exceptions import MongoDBConnectionError, MongoDBCircuitBreakerOpenError

class TestMongoDBManager(unittest.TestCase):
    def setUp(self):
        # Reset singleton for each test
        MongoDBManager._instance = None
        MongoDBManager._client = None
        self.manager = MongoDBManager()

    def tearDown(self):
        if self.manager:
            self.manager.close()

    @patch("api.database.mongodb.MongoClient")
    def test_connect_success(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client_cls.return_value = mock_client
        
        client = self.manager.connect()
        
        self.assertIsNotNone(client)
        self.assertEqual(client, mock_client)
        mock_client.admin.command.assert_called_with("ping")

    @patch("api.database.mongodb.MongoClient")
    def test_connect_failure(self, mock_client_cls):
        mock_client_cls.side_effect = ConnectionFailure("Connection failed")
        
        with self.assertRaises(MongoDBConnectionError):
            self.manager.connect()

    def test_circuit_breaker_open(self):
        cb = CircuitBreaker(failure_threshold=2, recovery_timeout=1)
        
        # Fail twice to open circuit
        with self.assertRaises(Exception):
            cb.call(lambda: (_ for _ in ()).throw(Exception("Fail 1")))
            
        with self.assertRaises(Exception):
            cb.call(lambda: (_ for _ in ()).throw(Exception("Fail 2")))
            
        self.assertEqual(cb.state, CircuitState.OPEN)
        
        # Should raise CircuitBreakerOpenError immediately
        with self.assertRaises(MongoDBCircuitBreakerOpenError):
            cb.call(lambda: "success")

    def test_circuit_breaker_recovery(self):
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout=0.1)
        
        # Fail to open
        with self.assertRaises(Exception):
            cb.call(lambda: (_ for _ in ()).throw(Exception("Fail")))
            
        self.assertEqual(cb.state, CircuitState.OPEN)
        
        # Wait for recovery timeout
        time.sleep(0.2)
        
        # Should be half-open now and allow call
        result = cb.call(lambda: "success")
        self.assertEqual(result, "success")
        
        # Should need one more success to close (if threshold was higher, but logic says 2 successes in half-open)
        # Let's check the logic in circuit_breaker.py: 
        # if self.success_count >= 2: state = CLOSED
        
        result = cb.call(lambda: "success")
        self.assertEqual(cb.state, CircuitState.CLOSED)

if __name__ == "__main__":
    unittest.main()

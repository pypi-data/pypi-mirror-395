"""Tests for pynhc2 package.

This module contains comprehensive tests for all main classes and their core functionality.
"""

import os
import tempfile
import sqlite3
import zipfile
import json
from unittest.mock import Mock, MagicMock, patch, call
import pytest

from pynhc2 import MQTTConnector, Device, Lamp, MessageHandler, MultiMessageHandler, NHC2FileReader


class TestMQTTConnector:
    """Tests for MQTTConnector class."""
    
    def test_init_missing_broker(self):
        """Test that ValueError is raised when broker is missing."""
        with pytest.raises(ValueError, match="Missing broker"):
            MQTTConnector(broker=None, jwt="token", ca_cert="cert.pem")
    
    def test_init_missing_jwt(self):
        """Test that ValueError is raised when jwt is missing."""
        with pytest.raises(ValueError, match="Missing broker"):
            MQTTConnector(broker="localhost", jwt=None, ca_cert="cert.pem")
    
    def test_init_missing_ca_cert(self):
        """Test that ValueError is raised when ca_cert is missing."""
        with pytest.raises(ValueError, match="Missing broker"):
            MQTTConnector(broker="localhost", jwt="token", ca_cert=None)
    
    @patch('paho.mqtt.client.Client')
    def test_init_success(self, mock_mqtt_client):
        """Test successful initialization."""
        # Create a temporary certificate file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.pem') as f:
            f.write("dummy cert")
            cert_path = f.name
        
        try:
            conn = MQTTConnector(broker="localhost", jwt="token", ca_cert=cert_path)
            assert conn.broker == "localhost"
            assert conn.jwt == "token"
            assert conn.username == "hobby"
            assert conn.port == 8884
            assert conn.handlers == []
        finally:
            os.unlink(cert_path)
    
    @patch('paho.mqtt.client.Client')
    def test_register_handler_success(self, mock_mqtt_client):
        """Test successful handler registration."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.pem') as f:
            f.write("dummy cert")
            cert_path = f.name
        
        try:
            conn = MQTTConnector(broker="localhost", jwt="token", ca_cert=cert_path)
            
            # Create a mock handler
            handler = Mock()
            handler.handle_message = Mock()
            handler.input_uuids = ["uuid-123"]
            
            conn.register_handler(handler)
            assert len(conn.handlers) == 1
            assert conn.handlers[0] == handler
        finally:
            os.unlink(cert_path)
    
    @patch('paho.mqtt.client.Client')
    def test_register_handler_missing_method(self, mock_mqtt_client):
        """Test that TypeError is raised when handler lacks handle_message."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.pem') as f:
            f.write("dummy cert")
            cert_path = f.name
        
        try:
            conn = MQTTConnector(broker="localhost", jwt="token", ca_cert=cert_path)
            
            handler = Mock()
            handler.input_uuids = ["uuid-123"]
            delattr(handler, 'handle_message')
            
            with pytest.raises(TypeError, match="handle_message"):
                conn.register_handler(handler)
        finally:
            os.unlink(cert_path)
    
    @patch('paho.mqtt.client.Client')
    def test_register_handler_missing_input_uuids(self, mock_mqtt_client):
        """Test that TypeError is raised when handler lacks input_uuids."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.pem') as f:
            f.write("dummy cert")
            cert_path = f.name
        
        try:
            conn = MQTTConnector(broker="localhost", jwt="token", ca_cert=cert_path)
            
            handler = Mock(spec=['handle_message'])  # Only has handle_message, no input_uuids
            handler.handle_message = Mock()
            
            with pytest.raises(TypeError, match="input_uuid"):
                conn.register_handler(handler)
        finally:
            os.unlink(cert_path)
    
    @patch('paho.mqtt.client.Client')
    def test_on_connect_callback(self, mock_mqtt_client):
        """Test _on_connect callback subscribes to topics."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.pem') as f:
            f.write("dummy cert")
            cert_path = f.name
        
        try:
            conn = MQTTConnector(broker="localhost", jwt="token", ca_cert=cert_path)
            mock_client = Mock()
            
            # Call the on_connect callback
            conn._on_connect(mock_client, None, None, 0, None)
            
            # Verify subscribe was called
            mock_client.subscribe.assert_called_once_with("hobby/control/#")
        finally:
            os.unlink(cert_path)
    
    @patch('paho.mqtt.client.Client')
    def test_on_message_callback_valid_message(self, mock_mqtt_client):
        """Test _on_message callback processes valid messages."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.pem') as f:
            f.write("dummy cert")
            cert_path = f.name
        
        try:
            conn = MQTTConnector(broker="localhost", jwt="token", ca_cert=cert_path)
            
            # Create a mock handler that mimics MultiMessageHandler
            handler = Mock()
            handler.input_uuids = ["uuid-123"]
            handler.handle_message = Mock()
            type(handler).__name__ = "MultiMessageHandler"
            conn.handlers.append(handler)
            
            # Create a mock message
            mock_msg = Mock()
            mock_msg.topic = "hobby/control/devices/evt"
            mock_msg.mid = 1
            mock_msg.timestamp = 1234567890.0
            mock_msg.payload = json.dumps({
                "Method": "devices.status",
                "Params": [{
                    "Devices": [{
                        "Uuid": "uuid-123",
                        "Properties": [{"Status": "On"}]
                    }]
                }]
            }).encode()
            
            # Call the callback
            conn._on_message(None, None, mock_msg)
            
            # Verify handler was called with message argument
            handler.handle_message.assert_called_once()
            call_args = handler.handle_message.call_args[0]
            assert len(call_args) == 1
            assert call_args[0]['device_uuid'] == "uuid-123"
            assert conn.last_msg['device_uuid'] == "uuid-123"
        finally:
            os.unlink(cert_path)
    
    @patch('paho.mqtt.client.Client')
    def test_on_message_callback_malformed_message(self, mock_mqtt_client):
        """Test _on_message callback handles malformed messages gracefully."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.pem') as f:
            f.write("dummy cert")
            cert_path = f.name
        
        try:
            conn = MQTTConnector(broker="localhost", jwt="token", ca_cert=cert_path)
            
            # Create a mock message with invalid JSON
            mock_msg = Mock()
            mock_msg.topic = "hobby/control/devices/evt"
            mock_msg.mid = 1
            mock_msg.timestamp = 1234567890.0
            mock_msg.payload = b"invalid json"
            
            # Should not raise an exception
            conn._on_message(None, None, mock_msg)
            
            # last_msg should not be set
            assert conn.last_msg is None
        finally:
            os.unlink(cert_path)
    
    @patch('paho.mqtt.client.Client')
    def test_on_message_callback_handler_error(self, mock_mqtt_client):
        """Test _on_message callback handles handler errors gracefully."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.pem') as f:
            f.write("dummy cert")
            cert_path = f.name
        
        try:
            conn = MQTTConnector(broker="localhost", jwt="token", ca_cert=cert_path)
            
            # Create a handler that raises an exception and mimics MultiMessageHandler
            handler = Mock()
            handler.input_uuids = ["uuid-123"]
            handler.handle_message = Mock(side_effect=Exception("Handler error"))
            type(handler).__name__ = "MultiMessageHandler"
            conn.handlers.append(handler)
            
            # Create a valid message
            mock_msg = Mock()
            mock_msg.topic = "hobby/control/devices/evt"
            mock_msg.mid = 1
            mock_msg.timestamp = 1234567890.0
            mock_msg.payload = json.dumps({
                "Params": [{
                    "Devices": [{
                        "Uuid": "uuid-123"
                    }]
                }]
            }).encode()
            
            # Should not raise an exception
            conn._on_message(None, None, mock_msg)
        finally:
            os.unlink(cert_path)
    
    @patch('paho.mqtt.client.Client')
    def test_on_publish_callback(self, mock_mqtt_client):
        """Test _on_publish callback."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.pem') as f:
            f.write("dummy cert")
            cert_path = f.name
        
        try:
            conn = MQTTConnector(broker="localhost", jwt="token", ca_cert=cert_path)
            
            # Call the callback (should just pass)
            conn._on_publish(None, None, 1, 0, None)
        finally:
            os.unlink(cert_path)
    
    @patch('paho.mqtt.client.Client')
    def test_connect_success(self, mock_mqtt_client):
        """Test successful connection."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.pem') as f:
            f.write("dummy cert")
            cert_path = f.name
        
        try:
            mock_client_instance = Mock()
            mock_mqtt_client.return_value = mock_client_instance
            
            conn = MQTTConnector(broker="localhost", jwt="token", ca_cert=cert_path)
            result = conn.connect()
            
            mock_client_instance.connect.assert_called_once_with("localhost", 8884, keepalive=180)
            mock_client_instance.loop_start.assert_called_once()
            assert result == mock_client_instance
        finally:
            os.unlink(cert_path)
    
    @patch('paho.mqtt.client.Client')
    def test_connect_refused(self, mock_mqtt_client):
        """Test connection refused error."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.pem') as f:
            f.write("dummy cert")
            cert_path = f.name
        
        try:
            mock_client_instance = Mock()
            mock_client_instance.connect.side_effect = ConnectionRefusedError()
            mock_mqtt_client.return_value = mock_client_instance
            
            conn = MQTTConnector(broker="localhost", jwt="token", ca_cert=cert_path)
            
            with pytest.raises(ConnectionError, match="Connection refused"):
                conn.connect()
        finally:
            os.unlink(cert_path)
    
    @patch('paho.mqtt.client.Client')
    def test_connect_os_error(self, mock_mqtt_client):
        """Test network error during connection."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.pem') as f:
            f.write("dummy cert")
            cert_path = f.name
        
        try:
            mock_client_instance = Mock()
            mock_client_instance.connect.side_effect = OSError("Network error")
            mock_mqtt_client.return_value = mock_client_instance
            
            conn = MQTTConnector(broker="localhost", jwt="token", ca_cert=cert_path)
            
            with pytest.raises(OSError, match="Network error"):
                conn.connect()
        finally:
            os.unlink(cert_path)
    
    @patch('paho.mqtt.client.Client')
    def test_connect_generic_error(self, mock_mqtt_client):
        """Test generic error during connection."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.pem') as f:
            f.write("dummy cert")
            cert_path = f.name
        
        try:
            mock_client_instance = Mock()
            mock_client_instance.connect.side_effect = Exception("Generic error")
            mock_mqtt_client.return_value = mock_client_instance
            
            conn = MQTTConnector(broker="localhost", jwt="token", ca_cert=cert_path)
            
            with pytest.raises(ConnectionError, match="Failed to connect"):
                conn.connect()
        finally:
            os.unlink(cert_path)
    
    @patch('paho.mqtt.client.Client')
    def test_publish_topic_with_device_uuid(self, mock_mqtt_client):
        """Test _publish_topic with device UUID."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.pem') as f:
            f.write("dummy cert")
            cert_path = f.name
        
        try:
            mock_client_instance = Mock()
            mock_mqtt_client.return_value = mock_client_instance
            
            conn = MQTTConnector(broker="localhost", jwt="token", ca_cert=cert_path)
            
            conn._publish_topic(
                "hobby/control/devices/cmd",
                "devices.control",
                device_uuid="uuid-123",
                properties=[{"Status": "On"}]
            )
            
            mock_client_instance.publish.assert_called_once()
        finally:
            os.unlink(cert_path)
    
    @patch('paho.mqtt.client.Client')
    @patch('time.sleep', return_value=None)
    @patch('pynhc2.mqttconnector.message', {'payload': json.dumps({"Method": "test", "Params": []})})
    def test_publish_topic_without_device_uuid(self, mock_sleep, mock_mqtt_client):
        """Test _publish_topic without device UUID (query)."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.pem') as f:
            f.write("dummy cert")
            cert_path = f.name
        
        try:
            mock_client_instance = Mock()
            mock_mqtt_client.return_value = mock_client_instance
            
            conn = MQTTConnector(broker="localhost", jwt="token", ca_cert=cert_path)
            
            result = conn._publish_topic("hobby/control/locations/cmd", "locations.list")
            
            mock_client_instance.publish.assert_called_once()
            mock_sleep.assert_called_once_with(1)
            assert result is not None
        finally:
            os.unlink(cert_path)
    
    @patch('paho.mqtt.client.Client')
    @patch('time.sleep', return_value=None)
    @patch('pynhc2.mqttconnector.message', {
        'payload': json.dumps({
            "Params": [{
                "Locations": [
                    {"Uuid": "loc-1", "Name": "Living Room"},
                    {"Uuid": "loc-2", "Name": "Kitchen"}
                ]
            }]
        })
    })
    def test_get_locations(self, mock_sleep, mock_mqtt_client):
        """Test get_locations method."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.pem') as f:
            f.write("dummy cert")
            cert_path = f.name
        
        try:
            mock_client_instance = Mock()
            mock_mqtt_client.return_value = mock_client_instance
            
            conn = MQTTConnector(broker="localhost", jwt="token", ca_cert=cert_path)
            
            locations = conn.get_locations()
            
            assert len(locations) == 2
            assert locations[0]["Uuid"] == "loc-1"
        finally:
            os.unlink(cert_path)
    
    @patch('paho.mqtt.client.Client')
    @patch('time.sleep', return_value=None)
    @patch('pynhc2.mqttconnector.message', {
        'payload': json.dumps({
            "Params": [{
                "Locations": [{
                    "Uuid": "loc-1",
                    "Devices": [
                        {"Uuid": "dev-1", "Name": "Lamp"}
                    ]
                }]
            }]
        })
    })
    def test_get_devices(self, mock_sleep, mock_mqtt_client):
        """Test get_devices method."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.pem') as f:
            f.write("dummy cert")
            cert_path = f.name
        
        try:
            mock_client_instance = Mock()
            mock_mqtt_client.return_value = mock_client_instance
            
            conn = MQTTConnector(broker="localhost", jwt="token", ca_cert=cert_path)
            
            # Mock get_locations response
            with patch.object(conn, 'get_locations', return_value=[
                {"Uuid": "loc-1", "Name": "Living Room"}
            ]):
                devices = conn.get_devices()
                
                assert len(devices) == 1
        finally:
            os.unlink(cert_path)
    
    @patch('paho.mqtt.client.Client')
    def test_create_client_invalid_cert(self, mock_mqtt_client):
        """Test _create_client with invalid certificate."""
        mock_client_instance = Mock()
        mock_client_instance.tls_set.side_effect = ValueError("Invalid cert")
        mock_mqtt_client.return_value = mock_client_instance
        
        with pytest.raises(ValueError, match="Invalid"):
            MQTTConnector(broker="localhost", jwt="token", ca_cert="invalid.pem")


class TestDevice:
    """Tests for Device class."""
    
    def test_init_missing_connector(self):
        """Test that ValueError is raised when mqttconnector is missing."""
        with pytest.raises(ValueError, match="No MQTTconnector"):
            Device(mqttconnector=None, device_uuid="uuid-123")
    
    def test_init_missing_uuid(self):
        """Test that ValueError is raised when device_uuid is missing."""
        conn = Mock()
        with pytest.raises(ValueError, match="Missing device_uuid"):
            Device(mqttconnector=conn, device_uuid=None)
    
    def test_init_success(self):
        """Test successful Device initialization."""
        conn = Mock()
        device = Device(mqttconnector=conn, device_uuid="uuid-123")
        
        assert device.conn == conn
        assert device.device_uuid == "uuid-123"
        assert device.current_status == "Unknown"
        assert device.topic == "hobby/control/devices/cmd"
        assert device.method == "devices.control"
    
    def test_command_invalid_properties(self):
        """Test that ValueError is raised for invalid properties format."""
        conn = Mock()
        device = Device(mqttconnector=conn, device_uuid="uuid-123")
        
        with pytest.raises(ValueError, match="Properties must be a list"):
            device.command("not a list")
    
    def test_command_success(self):
        """Test successful command execution."""
        conn = Mock()
        conn._publish_topic = Mock()
        device = Device(mqttconnector=conn, device_uuid="uuid-123")
        
        properties = [{"Status": "On"}]
        device.command(properties)
        
        conn._publish_topic.assert_called_once_with(
            device.topic,
            device.method,
            device_uuid="uuid-123",
            properties=properties
        )


class TestLamp:
    """Tests for Lamp class."""
    
    def test_init_missing_connector(self):
        """Test that ValueError is raised when mqttconnector is missing."""
        with pytest.raises(ValueError, match="No MQTTconnector"):
            Lamp(mqttconnector=None, device_uuid="uuid-123")
    
    def test_init_missing_uuid(self):
        """Test that ValueError is raised when device_uuid is missing."""
        conn = Mock()
        with pytest.raises(ValueError, match="Missing device_uuid"):
            Lamp(mqttconnector=conn, device_uuid=None)
    
    def test_init_success(self):
        """Test successful Lamp initialization."""
        conn = Mock()
        lamp = Lamp(mqttconnector=conn, device_uuid="uuid-456")
        
        assert lamp.conn == conn
        assert lamp.device_uuid == "uuid-456"
        assert lamp.status is None
        assert lamp.brightness == 0
    
    def test_switch_on(self):
        """Test turning lamp on."""
        conn = Mock()
        conn._publish_topic = Mock()
        lamp = Lamp(mqttconnector=conn, device_uuid="uuid-456")
        
        lamp.switch_on()
        
        assert lamp.status == "On"
        conn._publish_topic.assert_called_once()
    
    def test_switch_off(self):
        """Test turning lamp off."""
        conn = Mock()
        conn._publish_topic = Mock()
        lamp = Lamp(mqttconnector=conn, device_uuid="uuid-456")
        
        lamp.switch_off()
        
        assert lamp.status == "Off"
        conn._publish_topic.assert_called_once()
    
    def test_set_brightness_valid(self):
        """Test setting valid brightness level."""
        conn = Mock()
        conn._publish_topic = Mock()
        lamp = Lamp(mqttconnector=conn, device_uuid="uuid-456")
        
        lamp.set_brightness("75")
        
        assert lamp.status == "On"
        assert lamp.brightness == "75"
    
    def test_set_brightness_invalid(self):
        """Test that ValueError is raised for invalid brightness."""
        conn = Mock()
        lamp = Lamp(mqttconnector=conn, device_uuid="uuid-456")
        
        with pytest.raises(ValueError, match="Brightness must be between 0 and 100"):
            lamp.set_brightness("150")
    
    def test_switch_no_status(self):
        """Test that ValueError is raised when status is not set."""
        conn = Mock()
        lamp = Lamp(mqttconnector=conn, device_uuid="uuid-456")
        
        with pytest.raises(ValueError, match="Lamp status is not set"):
            lamp.switch()
    
    def test_switch_toggles_state(self):
        """Test that switch toggles between on and off."""
        conn = Mock()
        conn._publish_topic = Mock()
        lamp = Lamp(mqttconnector=conn, device_uuid="uuid-456")
        
        lamp.status = "Off"
        lamp.switch()
        assert lamp.status == "On"
        
        lamp.switch()
        assert lamp.status == "Off"


class TestMessageHandler:
    """Tests for MessageHandler class."""
    
    def test_init_missing_connector(self):
        """Test that ValueError is raised when mqttconnector is missing."""
        device = Mock()
        device.device_uuid = "uuid-123"
        
        with pytest.raises(ValueError, match="mqttconnector is required"):
            MessageHandler(mqttconnector=None, input_device=device, output_actions=[lambda: None])
    
    def test_init_missing_input_device(self):
        """Test that ValueError is raised when input_device is missing."""
        conn = Mock()
        
        with pytest.raises(ValueError, match="input_device cannot be empty"):
            MessageHandler(mqttconnector=conn, input_device=None, output_actions=[lambda: None])
    
    def test_init_missing_output_actions(self):
        """Test that ValueError is raised when output_actions is empty."""
        conn = Mock()
        device = Mock()
        device.device_uuid = "uuid-123"
        
        with pytest.raises(ValueError, match="output_actions cannot be empty"):
            MessageHandler(mqttconnector=conn, input_device=device, output_actions=[])
    
    def test_init_non_callable_action(self):
        """Test that TypeError is raised for non-callable output action."""
        conn = Mock()
        device = Mock()
        device.device_uuid = "uuid-123"
        
        with pytest.raises(TypeError, match="not callable"):
            MessageHandler(mqttconnector=conn, input_device=device, output_actions=["not callable"])
    
    def test_init_device_without_uuid(self):
        """Test that AttributeError is raised when device lacks device_uuid."""
        conn = Mock()
        device = Mock(spec=[])  # No attributes
        
        with pytest.raises(AttributeError, match="device_uuid"):
            MessageHandler(mqttconnector=conn, input_device=device, output_actions=[lambda: None])
    
    def test_handle_message_executes_actions(self):
        """Test that handle_message executes all output actions."""
        conn = Mock()
        device = Mock()
        device.device_uuid = "uuid-123"
        
        action1 = Mock()
        action2 = Mock()
        
        handler = MessageHandler(mqttconnector=conn, input_device=device, output_actions=[action1, action2])
        handler.handle_message()
        
        action1.assert_called_once()
        action2.assert_called_once()


class TestMultiMessageHandler:
    """Tests for MultiMessageHandler class."""
    
    def test_init_success(self):
        """Test successful MultiMessageHandler initialization."""
        conn = Mock()
        device1 = Mock()
        device1.device_uuid = "uuid-1"
        device2 = Mock()
        device2.device_uuid = "uuid-2"
        
        action = Mock()
        
        handler = MultiMessageHandler(
            mqttconnector=conn,
            input_devices=[device1, device2],
            output_actions=[action],
            seconds_window=0.5
        )
        
        assert handler.input_uuids == ["uuid-1", "uuid-2"]
        assert handler.seconds_window == 0.5
        assert handler.received == []
    
    def test_init_missing_connector(self):
        """Test that ValueError is raised when mqttconnector is missing."""
        device = Mock()
        device.device_uuid = "uuid-123"
        
        with pytest.raises(ValueError, match="mqttconnector is required"):
            MultiMessageHandler(mqttconnector=None, input_devices=[device], output_actions=[lambda: None])
    
    def test_handle_message_within_window(self):
        """Test that actions execute when all devices message within time window."""
        conn = Mock()
        device1 = Mock()
        device1.device_uuid = "uuid-1"
        device2 = Mock()
        device2.device_uuid = "uuid-2"
        
        action = Mock()
        
        handler = MultiMessageHandler(
            mqttconnector=conn,
            input_devices=[device1, device2],
            output_actions=[action],
            seconds_window=1.0
        )
        
        # Simulate messages from both devices within time window
        msg1 = {"device_uuid": "uuid-1", "timestamp": 1000.0}
        msg2 = {"device_uuid": "uuid-2", "timestamp": 1000.2}
        
        handler.handle_message(msg1)
        handler.handle_message(msg2)
        
        action.assert_called_once()
        assert handler.received == []  # Buffer should be cleared
    
    def test_handle_message_outside_window(self):
        """Test that actions don't execute when messages are outside time window."""
        conn = Mock()
        device1 = Mock()
        device1.device_uuid = "uuid-1"
        device2 = Mock()
        device2.device_uuid = "uuid-2"
        
        action = Mock()
        
        handler = MultiMessageHandler(
            mqttconnector=conn,
            input_devices=[device1, device2],
            output_actions=[action],
            seconds_window=0.5
        )
        
        # Simulate messages from both devices outside time window
        msg1 = {"device_uuid": "uuid-1", "timestamp": 1000.0}
        msg2 = {"device_uuid": "uuid-2", "timestamp": 1002.0}
        
        handler.handle_message(msg1)
        handler.handle_message(msg2)
        
        action.assert_not_called()


class TestNHC2FileReader:
    """Tests for NHC2FileReader class."""
    
    def test_init_missing_path(self):
        """Test that ValueError is raised when path is missing."""
        with pytest.raises(ValueError, match="No config file path"):
            NHC2FileReader(nhc2_file_path=None)
    
    def test_init_file_not_found(self):
        """Test that FileNotFoundError is raised when file doesn't exist."""
        with pytest.raises(FileNotFoundError, match="Configuration file not found"):
            NHC2FileReader(nhc2_file_path="nonexistent.nhc2")
    
    def test_init_success(self, tmp_path):
        """Test successful initialization with valid .nhc2 file."""
        # Create a mock SQLite database
        db_path = tmp_path / "test.sqlite"
        conn_db = sqlite3.connect(str(db_path))
        cursor = conn_db.cursor()
        
        # Create tables
        cursor.execute("""
            CREATE TABLE Location (
                Id INTEGER PRIMARY KEY,
                CreationId TEXT,
                Name TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE Action (
                Id INTEGER PRIMARY KEY,
                FifthplayId TEXT,
                Name TEXT,
                LocationId INTEGER
            )
        """)
        cursor.execute("""
            CREATE TABLE Actor (
                Id INTEGER PRIMARY KEY,
                Name TEXT,
                ActorTypeCode TEXT
            )
        """)
        
        conn_db.commit()
        conn_db.close()
        
        # Create a .nhc2 file (zip with sqlite)
        nhc2_file = tmp_path / "test.nhc2"
        with zipfile.ZipFile(nhc2_file, 'w') as zf:
            zf.write(str(db_path), "config.sqlite")
        
        # Test initialization
        reader = NHC2FileReader(str(nhc2_file))
        assert reader.nhc2_file_path == str(nhc2_file)
        assert os.path.exists(reader.db_name)
    
    def test_unzip_file_no_sqlite(self, tmp_path):
        """Test that ValueError is raised when .nhc2 has no SQLite file."""
        # Create a .nhc2 file without sqlite
        nhc2_file = tmp_path / "test.nhc2"
        with zipfile.ZipFile(nhc2_file, 'w') as zf:
            zf.writestr("dummy.txt", "no sqlite here")
        
        with pytest.raises(ValueError, match="No SQLite database found"):
            NHC2FileReader(str(nhc2_file))
    
    def test_unzip_file_io_error(self, tmp_path):
        """Test that IOError is raised on extraction failure."""
        # Create an invalid .nhc2 file (not a valid zip)
        nhc2_file = tmp_path / "test.nhc2"
        nhc2_file.write_text("not a zip file")
        
        with pytest.raises((IOError, zipfile.BadZipFile)):
            NHC2FileReader(str(nhc2_file))
    
    def test_get_locations(self, tmp_path):
        """Test get_locations method."""
        # Create a mock database with locations
        db_path = tmp_path / "test.sqlite"
        conn_db = sqlite3.connect(str(db_path))
        cursor = conn_db.cursor()
        
        cursor.execute("""
            CREATE TABLE Location (
                Id INTEGER PRIMARY KEY,
                CreationId TEXT,
                Name TEXT
            )
        """)
        cursor.execute("""
            INSERT INTO Location (CreationId, Name) VALUES 
            ('loc-1', 'Living Room'),
            ('loc-2', 'Kitchen')
        """)
        cursor.execute("""
            CREATE TABLE Action (
                Id INTEGER PRIMARY KEY,
                FifthplayId TEXT,
                Name TEXT,
                LocationId INTEGER
            )
        """)
        cursor.execute("""
            CREATE TABLE Actor (
                Id INTEGER PRIMARY KEY,
                Name TEXT,
                ActorTypeCode TEXT
            )
        """)
        
        conn_db.commit()
        conn_db.close()
        
        # Create .nhc2 file
        nhc2_file = tmp_path / "test.nhc2"
        with zipfile.ZipFile(nhc2_file, 'w') as zf:
            zf.write(str(db_path), "config.sqlite")
        
        # Test get_locations
        reader = NHC2FileReader(str(nhc2_file))
        locations = reader.get_locations()
        
        assert len(locations) == 2
        assert locations[0]['location_uuid'] == 'loc-1'
        assert locations[0]['location_name'] == 'Living Room'
        assert locations[1]['location_uuid'] == 'loc-2'
        assert locations[1]['location_name'] == 'Kitchen'
    
    def test_get_locations_database_error(self, tmp_path):
        """Test get_locations with corrupted database."""
        # Create an invalid database
        db_path = tmp_path / "test.sqlite"
        db_path.write_text("corrupted database")
        
        nhc2_file = tmp_path / "test.nhc2"
        with zipfile.ZipFile(nhc2_file, 'w') as zf:
            zf.write(str(db_path), "config.sqlite")
        
        reader = NHC2FileReader(str(nhc2_file))
        
        with pytest.raises(sqlite3.DatabaseError):
            reader.get_locations()
    
    def test_get_locations_missing_table(self, tmp_path):
        """Test get_locations with missing Location table."""
        # Create a database without Location table
        db_path = tmp_path / "test.sqlite"
        conn_db = sqlite3.connect(str(db_path))
        cursor = conn_db.cursor()
        cursor.execute("CREATE TABLE Dummy (id INTEGER)")
        conn_db.commit()
        conn_db.close()
        
        nhc2_file = tmp_path / "test.nhc2"
        with zipfile.ZipFile(nhc2_file, 'w') as zf:
            zf.write(str(db_path), "config.sqlite")
        
        reader = NHC2FileReader(str(nhc2_file))
        
        with pytest.raises(sqlite3.OperationalError, match="table may not exist"):
            reader.get_locations()
    
    def test_get_devices(self, tmp_path):
        """Test get_devices method."""
        # Create a full mock database
        db_path = tmp_path / "test.sqlite"
        conn_db = sqlite3.connect(str(db_path))
        cursor = conn_db.cursor()
        
        cursor.execute("""
            CREATE TABLE Location (
                Id INTEGER PRIMARY KEY,
                CreationId TEXT,
                Name TEXT
            )
        """)
        cursor.execute("""
            INSERT INTO Location (Id, CreationId, Name) VALUES (1, 'loc-1', 'Living Room')
        """)
        
        cursor.execute("""
            CREATE TABLE Action (
                Id INTEGER PRIMARY KEY,
                FifthplayId TEXT,
                Name TEXT,
                LocationId INTEGER
            )
        """)
        cursor.execute("""
            INSERT INTO Action (FifthplayId, Name, LocationId) VALUES 
            ('dev-1', 'Lamp 1', 1)
        """)
        
        cursor.execute("""
            CREATE TABLE Actor (
                Id INTEGER PRIMARY KEY,
                Name TEXT,
                ActorTypeCode TEXT
            )
        """)
        cursor.execute("""
            INSERT INTO Actor (Name, ActorTypeCode) VALUES ('Lamp 1', 'DimmableLamp')
        """)
        
        conn_db.commit()
        conn_db.close()
        
        # Create .nhc2 file
        nhc2_file = tmp_path / "test.nhc2"
        with zipfile.ZipFile(nhc2_file, 'w') as zf:
            zf.write(str(db_path), "config.sqlite")
        
        # Test get_devices
        reader = NHC2FileReader(str(nhc2_file))
        devices = reader.get_devices()
        
        assert len(devices) == 1
        assert devices[0]['device_uuid'] == 'dev-1'
        assert devices[0]['device_name'] == 'Lamp 1'
        assert devices[0]['device_type'] == 'DimmableLamp'
        assert devices[0]['location_uuid'] == 'loc-1'
        assert devices[0]['location_name'] == 'Living Room'
    
    def test_get_devices_with_type_filter(self, tmp_path):
        """Test get_devices with device_type filter."""
        # Create database with multiple device types
        db_path = tmp_path / "test.sqlite"
        conn_db = sqlite3.connect(str(db_path))
        cursor = conn_db.cursor()
        
        cursor.execute("""
            CREATE TABLE Location (
                Id INTEGER PRIMARY KEY,
                CreationId TEXT,
                Name TEXT
            )
        """)
        cursor.execute("INSERT INTO Location (Id, CreationId, Name) VALUES (1, 'loc-1', 'Living Room')")
        
        cursor.execute("""
            CREATE TABLE Action (
                Id INTEGER PRIMARY KEY,
                FifthplayId TEXT,
                Name TEXT,
                LocationId INTEGER
            )
        """)
        cursor.execute("""
            INSERT INTO Action (FifthplayId, Name, LocationId) VALUES 
            ('dev-1', 'Lamp 1', 1),
            ('dev-2', 'Switch 1', 1)
        """)
        
        cursor.execute("""
            CREATE TABLE Actor (
                Id INTEGER PRIMARY KEY,
                Name TEXT,
                ActorTypeCode TEXT
            )
        """)
        cursor.execute("""
            INSERT INTO Actor (Name, ActorTypeCode) VALUES 
            ('Lamp 1', 'DimmableLamp'),
            ('Switch 1', 'Switch')
        """)
        
        conn_db.commit()
        conn_db.close()
        
        nhc2_file = tmp_path / "test.nhc2"
        with zipfile.ZipFile(nhc2_file, 'w') as zf:
            zf.write(str(db_path), "config.sqlite")
        
        reader = NHC2FileReader(str(nhc2_file))
        devices = reader.get_devices(device_type='DimmableLamp')
        
        assert len(devices) == 1
        assert devices[0]['device_type'] == 'DimmableLamp'
    
    def test_get_devices_with_location_uuid_filter(self, tmp_path):
        """Test get_devices with location_uuid filter."""
        db_path = tmp_path / "test.sqlite"
        conn_db = sqlite3.connect(str(db_path))
        cursor = conn_db.cursor()
        
        cursor.execute("CREATE TABLE Location (Id INTEGER PRIMARY KEY, CreationId TEXT, Name TEXT)")
        cursor.execute("INSERT INTO Location (Id, CreationId, Name) VALUES (1, 'loc-1', 'Living Room'), (2, 'loc-2', 'Kitchen')")
        
        cursor.execute("CREATE TABLE Action (Id INTEGER PRIMARY KEY, FifthplayId TEXT, Name TEXT, LocationId INTEGER)")
        cursor.execute("INSERT INTO Action (FifthplayId, Name, LocationId) VALUES ('dev-1', 'Lamp 1', 1), ('dev-2', 'Lamp 2', 2)")
        
        cursor.execute("CREATE TABLE Actor (Id INTEGER PRIMARY KEY, Name TEXT, ActorTypeCode TEXT)")
        cursor.execute("INSERT INTO Actor (Name, ActorTypeCode) VALUES ('Lamp 1', 'DimmableLamp'), ('Lamp 2', 'DimmableLamp')")
        
        conn_db.commit()
        conn_db.close()
        
        nhc2_file = tmp_path / "test.nhc2"
        with zipfile.ZipFile(nhc2_file, 'w') as zf:
            zf.write(str(db_path), "config.sqlite")
        
        reader = NHC2FileReader(str(nhc2_file))
        devices = reader.get_devices(location_uuid='loc-1')
        
        assert len(devices) == 1
        assert devices[0]['location_uuid'] == 'loc-1'
    
    def test_get_devices_with_location_name_filter(self, tmp_path):
        """Test get_devices with location_name filter."""
        db_path = tmp_path / "test.sqlite"
        conn_db = sqlite3.connect(str(db_path))
        cursor = conn_db.cursor()
        
        cursor.execute("CREATE TABLE Location (Id INTEGER PRIMARY KEY, CreationId TEXT, Name TEXT)")
        cursor.execute("INSERT INTO Location (Id, CreationId, Name) VALUES (1, 'loc-1', 'Living Room'), (2, 'loc-2', 'Kitchen')")
        
        cursor.execute("CREATE TABLE Action (Id INTEGER PRIMARY KEY, FifthplayId TEXT, Name TEXT, LocationId INTEGER)")
        cursor.execute("INSERT INTO Action (FifthplayId, Name, LocationId) VALUES ('dev-1', 'Lamp 1', 1), ('dev-2', 'Lamp 2', 2)")
        
        cursor.execute("CREATE TABLE Actor (Id INTEGER PRIMARY KEY, Name TEXT, ActorTypeCode TEXT)")
        cursor.execute("INSERT INTO Actor (Name, ActorTypeCode) VALUES ('Lamp 1', 'DimmableLamp'), ('Lamp 2', 'DimmableLamp')")
        
        conn_db.commit()
        conn_db.close()
        
        nhc2_file = tmp_path / "test.nhc2"
        with zipfile.ZipFile(nhc2_file, 'w') as zf:
            zf.write(str(db_path), "config.sqlite")
        
        reader = NHC2FileReader(str(nhc2_file))
        devices = reader.get_devices(location_name='Kitchen')
        
        assert len(devices) == 1
        assert devices[0]['location_name'] == 'Kitchen'
    
    def test_get_devices_database_error(self, tmp_path):
        """Test get_devices with database error."""
        db_path = tmp_path / "test.sqlite"
        db_path.write_text("corrupted")
        
        nhc2_file = tmp_path / "test.nhc2"
        with zipfile.ZipFile(nhc2_file, 'w') as zf:
            zf.write(str(db_path), "config.sqlite")
        
        reader = NHC2FileReader(str(nhc2_file))
        
        with pytest.raises(sqlite3.DatabaseError):
            reader.get_devices()
    
    def test_get_devices_missing_table(self, tmp_path):
        """Test get_devices with missing tables."""
        db_path = tmp_path / "test.sqlite"
        conn_db = sqlite3.connect(str(db_path))
        cursor = conn_db.cursor()
        cursor.execute("CREATE TABLE Dummy (id INTEGER)")
        conn_db.commit()
        conn_db.close()
        
        nhc2_file = tmp_path / "test.nhc2"
        with zipfile.ZipFile(nhc2_file, 'w') as zf:
            zf.write(str(db_path), "config.sqlite")
        
        reader = NHC2FileReader(str(nhc2_file))
        
        with pytest.raises(sqlite3.OperationalError, match="tables may not exist"):
            reader.get_devices()
    
    def test_get_device_types(self, tmp_path):
        """Test get_device_types method."""
        db_path = tmp_path / "test.sqlite"
        conn_db = sqlite3.connect(str(db_path))
        cursor = conn_db.cursor()
        
        cursor.execute("CREATE TABLE Location (Id INTEGER PRIMARY KEY, CreationId TEXT, Name TEXT)")
        cursor.execute("INSERT INTO Location (Id, CreationId, Name) VALUES (1, 'loc-1', 'Living Room')")
        
        cursor.execute("CREATE TABLE Action (Id INTEGER PRIMARY KEY, FifthplayId TEXT, Name TEXT, LocationId INTEGER)")
        cursor.execute("INSERT INTO Action (FifthplayId, Name, LocationId) VALUES ('dev-1', 'Lamp 1', 1), ('dev-2', 'Switch 1', 1)")
        
        cursor.execute("CREATE TABLE Actor (Id INTEGER PRIMARY KEY, Name TEXT, ActorTypeCode TEXT)")
        cursor.execute("INSERT INTO Actor (Name, ActorTypeCode) VALUES ('Lamp 1', 'DimmableLamp'), ('Switch 1', 'Switch')")
        
        conn_db.commit()
        conn_db.close()
        
        nhc2_file = tmp_path / "test.nhc2"
        with zipfile.ZipFile(nhc2_file, 'w') as zf:
            zf.write(str(db_path), "config.sqlite")
        
        reader = NHC2FileReader(str(nhc2_file))
        device_types = reader.get_device_types()
        
        assert len(device_types) == 2
        assert 'DimmableLamp' in device_types
        assert 'Switch' in device_types
    
    def test_get_device_types_database_error(self, tmp_path):
        """Test get_device_types with database error."""
        db_path = tmp_path / "test.sqlite"
        db_path.write_text("corrupted")
        
        nhc2_file = tmp_path / "test.nhc2"
        with zipfile.ZipFile(nhc2_file, 'w') as zf:
            zf.write(str(db_path), "config.sqlite")
        
        reader = NHC2FileReader(str(nhc2_file))
        
        with pytest.raises(sqlite3.DatabaseError):
            reader.get_device_types()
    
    def test_get_device_types_missing_table(self, tmp_path):
        """Test get_device_types with missing tables."""
        db_path = tmp_path / "test.sqlite"
        conn_db = sqlite3.connect(str(db_path))
        cursor = conn_db.cursor()
        cursor.execute("CREATE TABLE Dummy (id INTEGER)")
        conn_db.commit()
        conn_db.close()
        
        nhc2_file = tmp_path / "test.nhc2"
        with zipfile.ZipFile(nhc2_file, 'w') as zf:
            zf.write(str(db_path), "config.sqlite")
        
        reader = NHC2FileReader(str(nhc2_file))
        
        with pytest.raises(sqlite3.OperationalError, match="tables may not exist"):
            reader.get_device_types()


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])

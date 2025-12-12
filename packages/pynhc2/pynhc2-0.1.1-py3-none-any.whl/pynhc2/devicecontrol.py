"""Device control classes for Niko Home Control 2.

This module provides classes for controlling devices and creating
automation handlers based on device state changes.
"""

from datetime import datetime as dt

class Device:
    """Base class for Niko Home Control devices.
    
    Provides basic device control functionality for any Niko Home Control device.
    
    Attributes:
        conn (MQTTConnector): MQTT connector instance.
        device_uuid (str): Unique identifier for the device.
        topic (str): MQTT topic for device commands.
        method (str): Control method name.
        current_status (str): Current device status.
    """
    
    def __init__(self, mqttconnector=None, device_uuid=None):
        """Initialize a Device instance.
        
        Args:
            mqttconnector (MQTTConnector, optional): MQTT connector instance.
            device_uuid (str, optional): Unique device identifier.
            
        Raises:
            ValueError: If mqttconnector or device_uuid is not provided.
        """
        if not mqttconnector:
            raise ValueError("No MQTTconnector object was provided")
        if not device_uuid:
            raise ValueError("Missing device_uuid")

        self.conn = mqttconnector
        self.device_uuid = device_uuid

        self.topic = "hobby/control/devices/cmd"
        self.method = "devices.control"

        self.current_status = "Unknown"

    def command(self, properties):
        """Send a command to the device.
        
        Sends control properties to the device via MQTT.
        Properties are lowerkey versions of the Niko camelcase properties.
        
        Args:
            properties (list): List of property dictionaries to send to the device.
            
        Raises:
            ConnectionError: If MQTT connection is lost.
            ValueError: If properties format is invalid.
        """
        if not isinstance(properties, list):
            raise ValueError("Properties must be a list")
        
        self.conn._publish_topic(self.topic, self.method, device_uuid = self.device_uuid, properties = properties)


class Lamp:
    """Lamp device controller for Niko Home Control.
    
    Provides control methods for lamp devices including on/off switching
    and brightness control.
    
    Attributes:
        conn (MQTTConnector): MQTT connector instance.
        device_uuid (str): Unique identifier for the lamp.
        topic (str): MQTT topic for device commands.
        method (str): Control method name.
        status (str): Current lamp status ("On", "Off", or None).
        brightness (int): Current brightness level (0-100).
    """
    
    def __init__(self, mqttconnector=None, device_uuid=None):
        """Initialize a Lamp instance.
        
        Args:
            mqttconnector (MQTTConnector, optional): MQTT connector instance.
            device_uuid (str, optional): Unique lamp identifier.
            
        Raises:
            ValueError: If mqttconnector or device_uuid is not provided.
        """
        if not mqttconnector:
            raise ValueError("No MQTTconnector object was provided")
        if not device_uuid:
            raise ValueError("Missing device_uuid")

        self.conn = mqttconnector
        self.device_uuid = device_uuid

        self.topic = "hobby/control/devices/cmd"
        self.method = "devices.control"

        self.status = None
        self.brightness = 0

    def command(self, properties):
        """Send a command to the lamp.
        
        Sends control properties to the lamp via MQTT.
        
        Args:
            properties (list): List of property dictionaries to send to the lamp.
                Each property dict should have CamelCase keys (e.g., {"Status": "On"}).
                
        Raises:
            ConnectionError: If MQTT connection is lost.
            ValueError: If properties format is invalid.
        """
        if not isinstance(properties, list):
            raise ValueError("Properties must be a list")
        
        self.conn._publish_topic(self.topic, self.method, device_uuid = self.device_uuid, properties = properties)

    def switch(self):
        """Toggle lamp between on and off states.
        
        Switches the lamp to the opposite of its current state.
        
        Raises:
            ValueError: If lamp status has not been set yet.
        """
        if not self.status:
            raise ValueError("Lamp status is not set yet.")

        if self.status == "Off":
            self.switch_on()
        else:
            self.switch_off()

    def switch_on(self):
        """Turn the lamp on.
        
        Sends an 'On' command to the lamp and updates the status attribute.
        
        Raises:
            ConnectionError: If MQTT connection is lost.
        """
        properties = [{"Status":"On"}]
        self.conn._publish_topic(self.topic, self.method, device_uuid = self.device_uuid, properties = properties)
        self.status = "On"

    def switch_off(self):
        """Turn the lamp off.
        
        Sends an 'Off' command to the lamp and updates the status attribute.
        
        Raises:
            ConnectionError: If MQTT connection is lost.
        """
        properties = [{"Status":"Off"}]
        self.conn._publish_topic(self.topic, self.method, device_uuid = self.device_uuid, properties = properties)
        self.status = "Off"

    def set_brightness(self, brightness="50"):
        """Set lamp brightness level.
        
        Turns the lamp on (if off) and sets the brightness to the specified level.
        
        Args:
            brightness (str, optional): Brightness level (0-100). Defaults to "50".
        
        Raises:
            ValueError: If brightness is not between 0 and 100.
            ConnectionError: If MQTT connection is lost.
            
        Note:
            Currently always sends 'On' status with brightness.
            TODO: Send brightness only if lamp is already on.
        """
        try:
            brightness_int = int(brightness)
            if not 0 <= brightness_int <= 100:
                raise ValueError(f"Brightness must be between 0 and 100, got {brightness}")
        except ValueError as e:
            if "invalid literal" in str(e):
                raise ValueError(f"Brightness must be a valid integer, got {brightness}")
            raise
        
        properties = [
            {"Status":"On"}, 
            {"Brightness": brightness}
        ]
        self.conn._publish_topic(self.topic, self.method, device_uuid = self.device_uuid, properties = properties)
        self.status = "On"
        self.brightness = brightness


class MessageHandler:
    """Automation handler that triggers actions based on one device input.
    
    Monitors an input devices and triggers one or more output actions when all input
    devices have sent messages within a specified time window. This enables
    NHC-devices to control non-NHC devices e.g. Shelly using pyShelly.
    
    Attributes:
        conn (MQTTConnector): MQTT connector instance.
        input_device (object): Device object to monitor.
        input_uuid (str): Device UUID extracted from input_device.
        output_actions (list): List of callable actions to execute.
    """
    
    def __init__(self, mqttconnector, input_device, output_actions):
        """Initialize a MultiMessageHandler.
        
        Args:
            mqttconnector (MQTTConnector): MQTT connector instance.
            input_device (object): Device object to monitor.
            output_actions (list): List of callable actions (methods or lambdas) to execute.
                
        Raises:
            ValueError: If input_device or output_actions is empty.
            TypeError: If output_actions contains non-callable items.
            AttributeError: If input device doesn't have a device_uuid attribute.
        """
        if not mqttconnector:
            raise ValueError("mqttconnector is required")
        if not input_device:
            raise ValueError("input_device cannot be empty")
        if not output_actions:
            raise ValueError("output_actions cannot be empty")
        
        # Validate that all output actions are callable
        for i, action in enumerate(output_actions):
            if not callable(action):
                raise TypeError(f"output_actions[{i}] is not callable")
        
        # Validate that input device has device_uuid
        if not hasattr(input_device, 'device_uuid'):
            raise AttributeError("input_device does not have device_uuid attribute")
        
        self.conn = mqttconnector
        self.input_device = input_device
        self.input_uuid = input_device.device_uuid
        self.output_actions = output_actions

    def handle_message(self):
        """Process incoming MQTT messages for automation logic. 
        Execution of all configured output actions.
        
        The message is send to this object through the MQTT connector by checking the input_uuid.
        """

        # execute actions
        for action in self.output_actions:
            action()
        return


class MultiMessageHandler:
    """Automation handler that triggers actions based on multiple device inputs.
    
    Monitors multiple input devices and triggers output actions when all input
    devices have sent messages within a specified time window. This enables
    complex automation scenarios like "turn on scene when two switches are pressed".
    
    Attributes:
        conn (MQTTConnector): MQTT connector instance.
        input_devices (list): List of device objects to monitor.
        input_uuids (list): List of device UUIDs extracted from input_devices.
        seconds_window (float): Time window in seconds for input matching.
        output_actions (list): List of callable actions to execute.
        received (list): Buffer of received messages within the time window.
    """
    
    def __init__(self, mqttconnector, input_devices, output_actions, seconds_window=0.5):
        """Initialize a MultiMessageHandler.
        
        Args:
            mqttconnector (MQTTConnector): MQTT connector instance.
            input_devices (list): List of device objects (e.g., Lamp instances) to monitor.
            output_actions (list): List of callable actions (methods or lambdas) to execute.
            seconds_window (float, optional): Time window in seconds for matching inputs.
                Defaults to 0.5.
                
        Raises:
            ValueError: If input_devices or output_actions is empty.
            TypeError: If output_actions contains non-callable items.
            AttributeError: If input devices don't have device_uuid attribute.
        """
        if not mqttconnector:
            raise ValueError("mqttconnector is required")
        if not input_devices:
            raise ValueError("input_devices cannot be empty")
        if not output_actions:
            raise ValueError("output_actions cannot be empty")
        
        # Validate that all output actions are callable
        for i, action in enumerate(output_actions):
            if not callable(action):
                raise TypeError(f"output_actions[{i}] is not callable")
        
        # Validate that all input devices have device_uuid
        for i, device in enumerate(input_devices):
            if not hasattr(device, 'device_uuid'):
                raise AttributeError(f"input_devices[{i}] does not have device_uuid attribute")
        
        self.conn = mqttconnector
        self.input_devices = input_devices
        self.input_uuids = [dev.device_uuid for dev in input_devices]
        self.seconds_window = seconds_window
        self.output_actions = output_actions
        self.received = []

    def handle_message(self, message):
        """Process incoming MQTT message for automation logic.
        
        Checks if all input devices have sent messages within the time window.
        If so, executes all configured output actions.
        
        Args:
            message (dict): MQTT message dictionary containing:
                - device_uuid (str): UUID of the device that sent the message.
                - timestamp (float): Message timestamp in seconds.
                - Other message metadata.
        """

        # remove old messages
        if self.received:
            newest_timestamp = self.received[-1]['timestamp']
        else:
            newest_timestamp = message['timestamp']

        self.received = [
            msg for msg in self.received
            if (newest_timestamp - msg['timestamp']) < (self.seconds_window * 2)
        ]

        # add new message
        self.received.append(message)

        # collect timestamps for each input device uuid
        device_timestamps = {}
        for msg in self.received:
            device_timestamps[msg.get('device_uuid')] = msg.get('timestamp')

        # check if commands have been sent for all input_devices
        if sorted(list(device_timestamps.keys())) == sorted(self.input_uuids):
            timestamps = [device_timestamps[uuid] for uuid in self.input_uuids]
            differences = [
                abs(timestamps[i] - timestamps[(i + 1) % len(timestamps)])
                for i in range(len(timestamps))
            ]
            # check if all entries are within window and publish
            if all(diff < self.seconds_window for diff in differences):
                # Call output actions
                for action in self.output_actions:
                    action()
                self.received = []
                return


"""MQTT connector for Niko Home Control 2.

This module provides the MQTTConnector class for managing MQTT connections
to Niko Home Control 2 systems.
"""

import ssl
import paho.mqtt.client as mqtt
import time
import json

class MQTTConnector:
    """MQTT Connector for Niko Home Control 2.

    This class manages MQTT connections to the Niko Home Control 2 broker,
    handling authentication, TLS encryption, and message routing to registered handlers.

    Attributes:
        broker (str): MQTT broker hostname or IP address.
        jwt (str): JSON Web Token for authentication.
        ca_cert (str): Path to CA certificate file for TLS.
        username (str): MQTT username (default: "hobby").
        port (int): MQTT broker port (default: 8884).
        client: Paho MQTT client instance.
        last_msg (dict): Last received MQTT message.
        handlers (list): List of registered message handlers.
    """

    def __init__(self, broker, jwt, ca_cert, username="hobby"):
        """Initialize MQTT connector.

        Args:
            broker (str): MQTT broker hostname or IP address.
            jwt (str): JSON Web Token for authentication.
            ca_cert (str): Path to CA certificate file for TLS verification.
            username (str, optional): MQTT username. Defaults to "hobby".

        Raises:
            ValueError: If broker, jwt, or ca_cert is missing or empty.
        """
        if not (broker and jwt and ca_cert):
            raise ValueError("Missing broker, jwt, or ca_cert")

        self.broker = broker
        self.jwt = jwt
        self.ca_cert = ca_cert
        self.username = username
        self.port = 8884
        self.stored_kwargs = {}

        # create & configure client
        self.client = self._create_client()

        self.last_msg = None
        self.handlers = []


    def _create_client(self):
        """Create and configure MQTT client.

        Creates a Paho MQTT client with TLS encryption and authentication,
        and registers callback handlers.

        Returns:
            mqtt.Client: Configured MQTT client instance.

        Raises:
            FileNotFoundError: If the CA certificate file does not exist.
            ValueError: If the CA certificate file is invalid.
        """
        client = mqtt.Client(
            protocol=mqtt.MQTTv311,
            transport="tcp",
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2
        )

        # credentials
        client.username_pw_set(self.username, self.jwt)

        # TLS
        try:
            client.tls_set(
                ca_certs=self.ca_cert,
                tls_version=ssl.PROTOCOL_TLSv1_2
            )
        except FileNotFoundError:
            raise FileNotFoundError(f"CA certificate file not found: {self.ca_cert}")
        except Exception as e:
            raise ValueError(f"Invalid CA certificate file: {e}")

        client.tls_insecure_set(False)

        # callbacks
        client.on_connect = self._on_connect
        client.on_message = self._on_message
        client.on_publish = self._on_publish

        return client

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        """Callback for when connection to MQTT broker is established.

        Subscribes to all Niko Home Control topics upon successful connection.

        Args:
            client: MQTT client instance.
            userdata: User data passed during client creation.
            flags: Connection flags.
            reason_code: Connection result code.
            properties: MQTT v5 properties.
        """
        #print("Connected. Reason:", reason_code)
        client.subscribe("hobby/control/#")

    def _on_message(self, client, userdata, msg):
        """Callback for when a message is received from MQTT broker.

        Parses the message, extracts device UUID, and routes to registered handlers.
        Silently handles malformed messages to prevent callback failures.

        Args:
            client: MQTT client instance.
            userdata: User data passed during client creation.
            msg: Received MQTT message object.
        """
        global message 
        message = {}
        message['topic'] = msg.topic
        message['mid'] = msg.mid

        try:
            message['payload']= json.loads(msg.payload.decode(errors='ignore'))
            message['device_uuid'] = message['payload'].get('Params', [{}])[0].get('Devices', [])[0].get('Uuid', [])
        except (json.JSONDecodeError, IndexError, KeyError, AttributeError):
            # Silently ignore malformed messages
            return

        message['timestamp'] = msg.timestamp

        self.last_msg = message

        for handler in self.handlers:
            if message['device_uuid'] in handler.input_uuids:
                try:
                    if type(handler).__name__ == "MultiMessageHandler":
                        handler.handle_message(message)
                    elif type(handler).__name__ == "MessageHandler": 
                        handler.handle_message()
                except Exception as e:
                    # Log error but don't break the callback chain
                    print(f"Error in message handler: {e}")     


    def _on_publish(self, client, userdata, mid, reason_code, properties):
        """Callback for when a message is published to MQTT broker.

        Args:
            client: MQTT client instance.
            userdata: User data passed during client creation.
            mid: Message ID.
            reason_code: Publish result code.
            properties: MQTT v5 properties.
        """
        pass

    def connect(self):
        """Connect to MQTT broker and start message loop.

        Establishes connection to the broker and starts the network loop
        in a background thread.

        Returns:
            mqtt.Client: The connected MQTT client instance.

        Raises:
            ConnectionError: If connection to the broker fails.
            OSError: If network connection is unavailable.
        """
        try:
            self.client.connect(self.broker, self.port, keepalive=180)
            self.client.loop_start()
        except ConnectionRefusedError:
            raise ConnectionError(f"Connection refused by broker at {self.broker}:{self.port}")
        except OSError as e:
            raise OSError(f"Network error connecting to {self.broker}:{self.port}: {e}")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to broker: {e}")

        return self.client


    def _publish_topic(self, topic, method, **kwargs):
        """Publish a message to an MQTT topic.

        Formats and publishes control messages or queries to the Niko Home Control broker.

        Args:
            topic (str): MQTT topic to publish to.
            method (str): Niko Home Control method name.
            **kwargs: Additional keyword arguments.
                device_uuid (str, optional): Device UUID for device control.
                properties (list, optional): Device properties to set.

        Returns:
            dict or None: Response data if method requires response, None otherwise.
        """

        if "device_uuid" in kwargs:

            # join with method and device uuid for publishing
            data = {
                "Method": method,
                "Params": [{
                    "Devices": [{
                        "Uuid": kwargs.get("device_uuid"), "Properties": kwargs.get("properties")
                    }]
                }]
            }

            # publish
            ret= self.client.publish(topic, json.dumps(data))

        # create loop to receive subscriptions in response to publish + only method
        else:
            data = {"Method" : method}
            # publish in order for broker to publish message
            ret= self.client.publish(topic, json.dumps(data))
            time.sleep(1)

            return json.loads(message['payload'])

        # Check if the publish was sent to the broker successfully
        if ret.rc == mqtt.MQTT_ERR_SUCCESS:
            pass
        else:
            print("Publish failed with error:", ret.rc)



    def get_locations(self):
        """Get all locations from Niko Home Control system.

        Queries the broker for all configured locations/rooms.

        Returns:
            list: List of location dictionaries containing location information.
        """
        topic = "hobby/control/locations/cmd"
        method = "locations.list"

        locations = self._publish_topic(topic, method)

        return locations.get('Params')[0].get('Locations')


    def get_devices(self, device_type=None, location_uuid=None, location_name=None):
        """Get devices from Niko Home Control system.

        Queries the broker for all devices, optionally filtered by type or location.

        Args:
            device_type (str, optional): Filter by device type. Defaults to None.
            location_uuid (str, optional): Filter by location UUID. Defaults to None.
            location_name (str, optional): Filter by location name. Defaults to None.

        Returns:
            list: List of location dictionaries, each containing device information.
        """
        topic = "hobby/control/locations/cmd"
        method = "locations.listitems"

        locations = self.get_locations()

        if location_uuid:
            loc_lst = [{"Uuid": location_uuid}]
        else:
            loc_lst = []
            for loc in locations:
                loc_dict = {}
                loc_uuid = loc.get("Uuid")
                loc_dict["Uuid"] = loc_uuid
                loc_lst.append(loc_dict)

        ### change publish_topic function to allow other data structures!!
        data = {
        "Method": method,
        "Params": [{"Locations": loc_lst}]
        }

        # start loop to receive messages
        # publish in order for broker to publish 
        ret= self.client.publish(topic, json.dumps(data))
        time.sleep(1)

        return json.loads(message['payload']).get('Params')[0]['Locations']


    def register_handler(self, handler):
        """Register a message handler.

        Adds a handler that will receive MQTT messages matching its input devices.

        Args:
            handler: Handler object with handle_message method and input_uuids attribute.

        Raises:
            TypeError: If handler does not have required attributes or methods.
        """
        if not hasattr(handler, 'handle_message') or not callable(handler.handle_message):
            raise TypeError("Handler must have a callable 'handle_message' method")
        if not hasattr(handler, 'input_uuids') and not hasattr(handler, 'input_uuid'):
            raise TypeError("Handler must have 'input_uuid(s)' attribute")

        self.handlers.append(handler)

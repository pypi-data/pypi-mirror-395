#! /usr/bin/env python3
import argparse
import json
import os
import sys
import types
import logging
from typing import Dict, Any, Optional

from cloudevents.conversion import to_json
from cloudevents.http import CloudEvent

# Ensure that CloudEvent is correctly instantiated in the send_message method
def send_message(self, topic: str, event_type: str, source: str, data: Dict[str, Any]) -> None:
    if not self.is_connected():
        self.logger.warning("Connection to Kafka broker lost, reconnecting...")
        try:
            self._create_producer()
            if not self.is_connected():
                raise ConnectionError("Failed to connect to Kafka broker")
        except Exception as e:
            self.logger.error(f"Failed to reconnect: {e}")
            raise ConnectionError(f"Failed to connect to Kafka broker: {e}")

    attributes = {
        "type": event_type,
        "source": source,
    }
    event = CloudEvent(attributes, data)
    message = to_json(event)
    self.producer.send(topic, message.encode('utf-8'))  # Ensure message is encoded to bytes
    self.producer.flush()  # Ensure message is sent

# Define a proper kafka helper class instead of using globals
class KafkaMessageProducer:
    def __init__(self, broker: str, sasl_un: str, sasl_pw: str):
        import ssl
        # Still need the module hack for kafka six.moves import
        m = types.ModuleType('kafka.vendor.six.moves', 'Mock module')
        setattr(m, 'range', range)
        sys.modules['kafka.vendor.six.moves'] = m
        from kafka import KafkaProducer
        
        self.broker = broker
        self.sasl_un = sasl_un
        self.sasl_pw = sasl_pw
        self.logger = logging.getLogger('kafka')
        
        # Create producer once
        self._create_producer()
    
    def _create_producer(self):
        import ssl
        from kafka import KafkaProducer
        
        context = ssl._create_unverified_context()
        self.producer = KafkaProducer(bootstrap_servers=self.broker, 
                             sasl_mechanism="SCRAM-SHA-512", 
                             sasl_plain_username=self.sasl_un,
                             sasl_plain_password=self.sasl_pw, 
                             security_protocol="SASL_SSL", 
                             ssl_context=context)
    
    def is_connected(self) -> bool:
        try:
            return self.producer.bootstrap_connected()
        except:
            return False
    
    def send_message(self, topic: str, event_type: str, source: str, data: Dict[str, Any]) -> None:
        if not self.is_connected():
            self.logger.warning("Connection to Kafka broker lost, reconnecting...")
            try:
                self._create_producer()
                if not self.is_connected():
                    raise ConnectionError("Failed to connect to Kafka broker")
            except Exception as e:
                self.logger.error(f"Failed to reconnect: {e}")
                raise ConnectionError(f"Failed to connect to Kafka broker: {e}")
        
        attributes = {
            "type": event_type,
            "source": source,
        }
        event = CloudEvent(attributes, data)
        message = to_json(event)
        
        # Fix: Check if message is already bytes, if not, encode it
        if isinstance(message, str):
            message = message.encode('utf-8')
            
        self.producer.send(topic, message)  # No need to encode if already bytes
        self.producer.flush()  # Ensure message is sent

def create_producer() -> KafkaMessageProducer:
    broker = os.environ.get('BROKER_ADDR')
    sasl_un = os.environ.get('SASL_UN')
    sasl_pw = os.environ.get('SASL_PW')
    
    if not all([broker, sasl_un, sasl_pw]):
        raise ValueError("Missing required environment variables: BROKER_ADDR, SASL_UN, SASL_PW")
        
    return KafkaMessageProducer(broker, sasl_un, sasl_pw)

def main():
    # Set up logging at the entry point
    logger = logging.getLogger('kafka')
    logger.setLevel(logging.WARN)
    
    parser = argparse.ArgumentParser(description='Send messages to Kafka using CloudEvents format')
    parser.add_argument("topic", help="Kafka topic to publish to")
    parser.add_argument("-t", "--type", help="Cloud event type to publish", required=True)
    parser.add_argument("-s", "--source", help="Origin of the event", required=True)
    parser.add_argument("-d", "--data", help="Data to publish (JSON format)", required=True)
    args = parser.parse_args()
    
    try:
        data = json.loads(args.data)
        producer = create_producer()
        producer.send_message(args.topic, args.type, args.source, data)
        print(f"Message successfully sent to topic: {args.topic}")
        return 0
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in data argument: {args.data}")
        return 1
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Error sending message: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

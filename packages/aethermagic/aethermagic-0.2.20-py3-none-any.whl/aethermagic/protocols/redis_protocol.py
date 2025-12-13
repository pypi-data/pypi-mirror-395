"""
Simplified Redis Protocol Implementation for AetherMagic
Uses only Redis Pub/Sub but with separate connections for publishing and subscribing
"""

import asyncio
import inspect
import json
from typing import Optional, Callable, Dict, Any, List
import redis.asyncio as redis
from redis.asyncio.client import PubSub

from . import ProtocolInterface, ConnectionConfig, AetherMessage, ProtocolType


class RedisProtocol(ProtocolInterface):
    """Redis protocol with Pub/Sub + Lists for load balancing"""
    
    def __init__(self, config: ConnectionConfig):
        super().__init__(config)
        self.publish_client: Optional[redis.Redis] = None
        self.subscribe_client: Optional[redis.Redis] = None
        self.pubsub: Optional[PubSub] = None
        self.subscribed_channels: set = set()
        self.subscribed_queues: set = set()  # For load balancing queues
        self._reconnect_delay = 1  # Start with 1 second
        self._max_reconnect_delay = 30  # Max 30 seconds
        self._reconnecting = False
        self._pending_resubscribe_channels: set = set()
        self._pending_resubscribe_queues: set = set()
    
    def _is_connection_error(self, error: Exception) -> bool:
        """Check if exception is a connection-related error that requires reconnect"""
        error_str = str(error).lower()
        connection_keywords = [
            'timeout', 'timed out', 'connection', 'closed', 'disconnect',
            'errno 60', 'errno 61', 'errno 54', 'errno 104',  # Socket errors
            'operation timed out', 'connection refused', 'connection reset',
            'broken pipe', 'network is unreachable', 'no route to host'
        ]
        return any(keyword in error_str for keyword in connection_keywords)
        
    async def connect(self) -> bool:
        """Connect to Redis server"""
        try:
            # Create Redis connection parameters
            connection_params = {
                'host': self.config.host,
                'port': self.config.port,
                'decode_responses': True,
                'socket_timeout': self.config.timeout,
                'socket_keepalive': True,
                'socket_keepalive_options': {}
            }
            
            # Add SSL if needed
            if self.config.ssl:
                connection_params['ssl'] = True
                connection_params['ssl_cert_reqs'] = None
            
            # Add auth if provided
            if self.config.username and self.config.password:
                connection_params['username'] = self.config.username
                connection_params['password'] = self.config.password
            elif self.config.password:
                connection_params['password'] = self.config.password
                
            # Add extra parameters
            connection_params.update(self.config.extra_params)
            
            # Create single client for both publishing and subscribing
            self.client = redis.Redis(**connection_params)
            self.publish_client = self.client  # Alias for backward compatibility
            self.subscribe_client = self.client  # Alias for backward compatibility
            
            # Test connection - handle async/sync ping
            ping_result = self.client.ping()
            if inspect.isawaitable(ping_result):
                await ping_result
            
            # Create pub/sub connection
            self.pubsub = self.client.pubsub()
            
            self.connected = True
            print(f"Redis: Connected (channel: {self.config.channel})")
            return True
            
        except Exception as e:
            print(f"Redis: Connection failed - {e}")
            self.connected = False
            return False
    
    async def disconnect(self) -> bool:
        """Disconnect from Redis"""
        try:
            if self.pubsub:
                await self.pubsub.close()
            if self.client:
                await self.client.close()
            self.connected = False
            return True
        except Exception as e:
            print(f"Redis: Disconnect failed - {e}")
            return False
    
    async def _reconnect(self) -> bool:
        """Attempt to reconnect to Redis with exponential backoff"""
        if self._reconnecting:
            return False
        
        self._reconnecting = True
        print(f"Redis: Connection lost, attempting reconnect...")
        
        # Store subscriptions to restore
        self._pending_resubscribe_channels = self.subscribed_channels.copy()
        self._pending_resubscribe_queues = self.subscribed_queues.copy()
        
        # Try to disconnect cleanly
        try:
            if self.pubsub:
                await self.pubsub.close()
            if self.client:
                await self.client.close()
        except:
            pass
        
        self.client = None
        self.publish_client = None
        self.subscribe_client = None
        self.pubsub = None
        self.connected = False
        
        # Attempt reconnection with exponential backoff
        delay = self._reconnect_delay
        while not self.connected:
            print(f"Redis: Reconnecting in {delay}s...")
            await asyncio.sleep(delay)
            
            try:
                success = await self.connect()
                if success:
                    print(f"Redis: Reconnected successfully!")
                    # Restore subscriptions
                    for channel in self._pending_resubscribe_channels:
                        try:
                            if '*' in channel or '?' in channel or '[' in channel:
                                await self.pubsub.psubscribe(channel)
                            else:
                                await self.pubsub.subscribe(channel)
                            print(f"Redis: Resubscribed to {channel}")
                        except Exception as e:
                            print(f"Redis: Failed to resubscribe to {channel}: {e}")
                    
                    # Restore queue subscriptions
                    self.subscribed_queues = self._pending_resubscribe_queues.copy()
                    
                    self._pending_resubscribe_channels.clear()
                    self._pending_resubscribe_queues.clear()
                    self._reconnect_delay = 1  # Reset delay
                    self._reconnecting = False
                    return True
            except Exception as e:
                print(f"Redis: Reconnect attempt failed - {e}")
            
            delay = min(delay * 2, self._max_reconnect_delay)
        
        self._reconnecting = False
        return False
    
    async def publish(self, topic: str, message: AetherMessage, retain: bool = False) -> bool:
        """Publish message to Redis channel or list for load balancing"""
        try:
            if not self.publish_client or not self.connected:
                # Try to reconnect
                reconnected = await self._reconnect()
                if not reconnected:
                    return False
            
            # Check if this is a perform action for load balancing
            if topic.endswith(':perform'):
                # Use Redis List with LPUSH for load balancing (FIFO queue)
                queue_key = f"queue:{topic}"
                lpush_result = self.client.lpush(queue_key, message.to_json())
                
                # Handle async/sync result
                if inspect.isawaitable(lpush_result):
                    result = await lpush_result
                else:
                    result = lpush_result
                    
                print(f"Redis: Queued {topic} -> {queue_key} (len={result}) (channel: {self.config.channel})")
            else:
                # Use regular pub/sub for other messages
                await self.client.publish(topic, message.to_json())
                print(f"Redis: Published {topic} (channel: {self.config.channel})")
            
            return True
            
        except Exception as e:
            if self._is_connection_error(e):
                print(f"Redis: Publish failed (disconnected) - {e}")
                self.connected = False
                asyncio.create_task(self._reconnect())
            else:
                print(f"Redis: Publish failed - {e}")
            return False
    
    async def subscribe(self, topic: str, callback: Optional[Callable] = None) -> bool:
        """Subscribe to Redis channel or queue for load balancing"""
        try:
            if not self.pubsub or not self.connected:
                # Add to pending and try reconnect
                redis_topic = topic.replace('+', '*').replace('#', '*')
                if topic.endswith(':perform') or ('+:perform' in topic):
                    self._pending_resubscribe_queues.add(f"queue:{redis_topic}")
                else:
                    self._pending_resubscribe_channels.add(redis_topic)
                reconnected = await self._reconnect()
                if not reconnected:
                    return False
            
            # Check if this is a perform subscription for load balancing
            if topic.endswith(':perform') or ('+:perform' in topic):
                # Subscribe to queue instead of pub/sub for load balancing
                queue_key = f"queue:{topic.replace('+', '*')}"  # Convert wildcard for queue naming
                self.subscribed_queues.add(queue_key)
                print(f"Redis: Queue subscribed to {queue_key} (original: {topic}) (channel: {self.config.channel})")
                return True
            
            # Convert MQTT wildcards to Redis wildcards  
            redis_topic = topic.replace('+', '*')  # MQTT single-level -> Redis wildcard
            redis_topic = redis_topic.replace('#', '*')  # MQTT multi-level -> Redis wildcard
                
            # Handle wildcard patterns (Redis uses * for wildcards)
            if '*' in redis_topic or '?' in redis_topic or '[' in redis_topic:
                await self.pubsub.psubscribe(redis_topic)
                print(f"Redis: Pattern subscribed to {redis_topic} (original: {topic}) (channel: {self.config.channel})")
            else:
                await self.pubsub.subscribe(redis_topic)
                print(f"Redis: Subscribed to {redis_topic} (channel: {self.config.channel})")
                
            self.subscribed_channels.add(redis_topic)
            return True
            
        except Exception as e:
            if self._is_connection_error(e):
                print(f"Redis: Subscribe failed (disconnected) - {e}")
                self.connected = False
                redis_topic = topic.replace('+', '*').replace('#', '*')
                if topic.endswith(':perform') or ('+:perform' in topic):
                    self._pending_resubscribe_queues.add(f"queue:{redis_topic}")
                else:
                    self._pending_resubscribe_channels.add(redis_topic)
                asyncio.create_task(self._reconnect())
            else:
                print(f"Redis: Subscribe failed - {e}")
            return False
    
    async def unsubscribe(self, topic: str) -> bool:
        """Unsubscribe from Redis channel"""
        try:
            if not self.pubsub or not self.connected:
                return False
            
            # Convert MQTT wildcards to Redis wildcards
            redis_topic = topic.replace('+', '*')  # MQTT single-level -> Redis wildcard
            redis_topic = redis_topic.replace('#', '*')  # MQTT multi-level -> Redis wildcard
                
            if '*' in redis_topic or '?' in redis_topic or '[' in redis_topic:
                await self.pubsub.punsubscribe(redis_topic)
            else:
                await self.pubsub.unsubscribe(redis_topic)
                
            self.subscribed_channels.discard(redis_topic)
            return True
            
        except Exception as e:
            print(f"Redis: Unsubscribe failed - {e}")
            return False
    
    async def receive_messages(self) -> List[Dict[str, Any]]:
        """Receive messages from subscribed channels and queues"""
        messages = []
        
        if not self.connected:
            return messages
        
        # Check queues first (for load balancing)  
        if self.subscribed_queues:
            try:
                # Find all actual queues matching our patterns
                for queue_pattern in self.subscribed_queues:
                    # Use SCAN to find matching queue keys
                    scan_result = self.client.scan(match=queue_pattern, count=100)
                    if inspect.isawaitable(scan_result):
                        cursor, keys = await scan_result
                    else:
                        cursor, keys = scan_result
                    
                    # Try to pop from each found queue
                    for queue_key in keys:
                        if isinstance(queue_key, bytes):
                            queue_key = queue_key.decode('utf-8')
                            
                        rpop_result = self.client.rpop(queue_key)
                        if inspect.isawaitable(rpop_result):
                            data = await rpop_result
                        else:
                            data = rpop_result
                            
                        if data:
                            if isinstance(data, bytes):
                                data = data.decode('utf-8')
                                
                            # Convert queue key back to topic
                            topic = queue_key.replace('queue:', '').replace('*', '+')  # Convert back to MQTT wildcard
                            print(f"Redis: Dequeued from {queue_key} -> {topic} (channel: {self.config.channel})")
                            messages.append({
                                'topic': topic,
                                'payload': data
                            })
                            return messages  # Return immediately after processing one message
                    
            except Exception as e:
                if self._is_connection_error(e):
                    print(f"Redis: Queue receive failed (disconnected) - {e}")
                    self.connected = False
                    asyncio.create_task(self._reconnect())
                else:
                    print(f"Redis: Queue receive failed - {e}")
        
        # Check pub/sub channels
        if self.pubsub and self.subscribed_channels:
            try:
                # Get message with timeout to avoid blocking
                message = await asyncio.wait_for(
                    self.pubsub.get_message(ignore_subscribe_messages=True),
                    timeout=0.1
                )
                
                if message and message['type'] in ['message', 'pmessage']:
                    channel = message['channel']
                    data = message['data']
                    
                    if data:
                        print(f"Redis: Received {channel} (channel: {self.config.channel})")
                        messages.append({
                            'topic': channel,
                            'payload': data
                        })
                        
            except asyncio.TimeoutError:
                pass  # No pub/sub messages available
            except Exception as e:
                if self._is_connection_error(e):
                    print(f"Redis: Pub/Sub receive failed (disconnected) - {e}")
                    self.connected = False
                    asyncio.create_task(self._reconnect())
                else:
                    print(f"Redis: Pub/Sub receive failed - {e}")
            
        return messages
    
    def generate_topic(self, job: str, task: str, context: str, tid: str, action: str, shared: bool = False, workgroup: str = "") -> str:
        """Generate Redis channel name - use colon format for Redis"""
        return f"{self.config.union}:{job}:{task}:{context}:{tid}:{action}"
    
    def parse_topic(self, topic: str) -> Dict[str, str]:
        """Parse Redis channel name with colon separators"""
        parts = topic.split(':')
        
        if len(parts) >= 6:
            return {
                'union': parts[0],
                'job': parts[1], 
                'task': parts[2],
                'context': parts[3],
                'tid': parts[4],
                'action': parts[5]
            }
        return {}
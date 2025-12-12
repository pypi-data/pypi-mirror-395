"""Main user statistics tracking application."""

import asyncio
import json
import logging
import signal
from pathlib import Path
from typing import Optional

from kryten import KrytenClient, ChatMessageEvent, UserJoinEvent, UserLeaveEvent, ChangeMediaEvent

from .database import StatsDatabase
from .activity_tracker import ActivityTracker
from .kudos_detector import KudosDetector
from .emote_detector import EmoteDetector
from .metrics_server import MetricsServer
from .query_endpoints import QueryEndpoints


class UserStatsApp:
    """User statistics tracking microservice.
    
    Tracks:
    - User message counts (public and PM)
    - Channel population snapshots every 5 minutes
    - Media title changes
    - User activity time (total and not-AFK)
    - Emote usage
    - Kudos system (++ and phrase-based)
    """
    
    def __init__(self, config_path: str):
        """Initialize the application.
        
        Args:
            config_path: Path to configuration JSON file
        """
        self.config_path = Path(config_path)
        self.logger = logging.getLogger(__name__)
        
        # Components
        self.client: Optional[KrytenClient] = None
        self.db: Optional[StatsDatabase] = None
        self.activity_tracker: Optional[ActivityTracker] = None
        self.kudos_detector: Optional[KudosDetector] = None
        self.emote_detector: Optional[EmoteDetector] = None
        self.metrics_server: Optional[MetricsServer] = None
        self.query_endpoints: Optional[QueryEndpoints] = None
        
        # State
        self._running = False
        self._shutdown_event = asyncio.Event()
        self._snapshot_task: Optional[asyncio.Task] = None
        
        # Load configuration
        self._load_config()
        
    def _load_config(self) -> None:
        """Load configuration from file."""
        with open(self.config_path) as f:
            self.config = json.load(f)
            
        self.logger.info(f"Configuration loaded from {self.config_path}")
        
    async def start(self) -> None:
        """Start the application."""
        self.logger.info("Starting User Statistics Tracker")
        
        # Initialize database
        db_path = self.config.get("database", {}).get("path", "data/userstats.db")
        self.db = StatsDatabase(db_path, self.logger)
        await self.db.initialize()
        
        # Initialize activity tracker (no longer needs AFK threshold)
        self.activity_tracker = ActivityTracker(self.logger)
        await self.activity_tracker.start()
        
        # Initialize kudos detector
        self.kudos_detector = KudosDetector(self.logger)
        trigger_phrases = await self.db.get_trigger_phrases()
        if not trigger_phrases:
            # Load default phrases if none configured
            trigger_phrases = self.config.get("kudos", {}).get("default_phrases", ["lol", "rofl", "haha"])
            for phrase in trigger_phrases:
                await self.db.add_trigger_phrase(phrase)
        self.kudos_detector.set_trigger_phrases(trigger_phrases)
        
        # Initialize emote detector
        self.emote_detector = EmoteDetector(self.logger)
        # Emote list will be populated from emoteList events
        
        # Initialize Kryten client
        self.client = KrytenClient(self.config)
        
        # Register event handlers
        @self.client.on("chatmsg")
        async def handle_chat(event: ChatMessageEvent):
            await self._handle_chat_message(event)
            
        @self.client.on("pm")
        async def handle_pm(event):
            await self._handle_pm(event)
            
        @self.client.on("adduser")
        async def handle_user_join(event: UserJoinEvent):
            await self._handle_user_join(event)
            
        @self.client.on("userleave")
        async def handle_user_leave(event: UserLeaveEvent):
            await self._handle_user_leave(event)
            
        @self.client.on("changemedia")
        async def handle_media_change(event: ChangeMediaEvent):
            await self._handle_media_change(event)
            
        @self.client.on("emotelist")
        async def handle_emote_list(event):
            await self._handle_emote_list(event)
            
        @self.client.on("setafk")
        async def handle_set_afk(event):
            await self._handle_set_afk(event)
            
        # Connect to NATS
        await self.client.connect()
        
        # Initialize metrics server
        metrics_port = self.config.get("metrics", {}).get("port", 28282)
        self.metrics_server = MetricsServer(self, metrics_port)
        await self.metrics_server.start()
        
        # Initialize NATS query endpoints
        domain = self.config["channels"][0]["domain"]  # Use first configured domain
        self.query_endpoints = QueryEndpoints(self, domain)
        await self.query_endpoints.start()
        
        # Start population snapshot task
        snapshot_interval = self.config.get("snapshots", {}).get("interval_seconds", 300)
        self._snapshot_task = asyncio.create_task(self._periodic_snapshots(snapshot_interval))
        
        # Start event processing
        self._running = True
        await self.client.run()
        
    async def stop(self) -> None:
        """Stop the application."""
        self.logger.info("Stopping User Statistics Tracker")
        self._running = False
        
        # Stop snapshot task
        if self._snapshot_task:
            self._snapshot_task.cancel()
            try:
                await self._snapshot_task
            except asyncio.CancelledError:
                pass
        
        # Stop query endpoints
        if self.query_endpoints:
            await self.query_endpoints.stop()
        
        # Stop metrics server
        if self.metrics_server:
            await self.metrics_server.stop()
                
        # Stop components
        if self.activity_tracker:
            await self.activity_tracker.stop()
            
        if self.client:
            await self.client.disconnect()
            
        self.logger.info("User Statistics Tracker stopped")
        
    async def _handle_chat_message(self, event: ChatMessageEvent) -> None:
        """Handle chat message event."""
        try:
            # Track user
            await self.db.track_user(event.username)
            
            # Increment message count
            await self.db.increment_message_count(event.username, event.channel, event.domain)
            
            # Record activity
            self.activity_tracker.user_activity(event.domain, event.channel, event.username)
            
            # Check for ++ kudos
            plusplus_users = self.kudos_detector.detect_plusplus_kudos(event.message)
            for username in plusplus_users:
                resolved = await self.db.resolve_username(username)
                await self.db.increment_kudos_plusplus(resolved, event.channel, event.domain)
                self.logger.debug(f"++ kudos for {resolved} in {event.channel}")
                
            # Check for phrase kudos
            phrase_kudos = self.kudos_detector.detect_phrase_kudos(event.message)
            for username, phrase in phrase_kudos:
                resolved = await self.db.resolve_username(username)
                await self.db.increment_kudos_phrase(resolved, event.channel, event.domain, phrase)
                self.logger.debug(f"Phrase kudos '{phrase}' for {resolved} in {event.channel}")
                
            # Check for emotes
            emotes = self.emote_detector.detect_emotes(event.message)
            for emote in emotes:
                await self.db.increment_emote_usage(event.username, event.channel, event.domain, emote)
                
        except Exception as e:
            self.logger.error(f"Error handling chat message: {e}", exc_info=True)
            
    async def _handle_pm(self, event) -> None:
        """Handle private message event."""
        try:
            # Extract username from payload
            username = event.payload.get("from") or event.payload.get("username")
            if not username:
                return
                
            # Track user
            await self.db.track_user(username)
            
            # Increment PM count
            await self.db.increment_pm_count(username)
            
        except Exception as e:
            self.logger.error(f"Error handling PM: {e}", exc_info=True)
            
    async def _handle_user_join(self, event: UserJoinEvent) -> None:
        """Handle user join event."""
        try:
            # Track user
            await self.db.track_user(event.username)
            
            # Start activity tracking
            self.activity_tracker.user_joined(event.domain, event.channel, event.username)
            
        except Exception as e:
            self.logger.error(f"Error handling user join: {e}", exc_info=True)
            
    async def _handle_user_leave(self, event: UserLeaveEvent) -> None:
        """Handle user leave event."""
        try:
            # Calculate activity time
            times = self.activity_tracker.user_left(event.domain, event.channel, event.username)
            
            if times:
                total_seconds, not_afk_seconds = times
                await self.db.update_user_activity(
                    event.username, event.channel, event.domain, total_seconds, not_afk_seconds
                )
                self.logger.debug(
                    f"User {event.username} left {event.channel}: "
                    f"{total_seconds}s total, {not_afk_seconds}s active"
                )
                
        except Exception as e:
            self.logger.error(f"Error handling user leave: {e}", exc_info=True)
            
    async def _handle_media_change(self, event: ChangeMediaEvent) -> None:
        """Handle media change event."""
        try:
            await self.db.log_media_change(
                event.channel,
                event.domain,
                event.title,
                event.media_type,
                event.media_id
            )
            
        except Exception as e:
            self.logger.error(f"Error handling media change: {e}", exc_info=True)
            
    async def _handle_emote_list(self, event) -> None:
        """Handle emote list event."""
        try:
            # Extract emote names from payload
            emote_list = event.payload
            if isinstance(emote_list, list):
                emote_names = [e.get("name") for e in emote_list if isinstance(e, dict) and e.get("name")]
                self.emote_detector.set_emote_list(emote_names)
            elif isinstance(emote_list, dict):
                # Sometimes emotes are in a dict format
                emote_names = list(emote_list.keys())
                self.emote_detector.set_emote_list(emote_names)
                
        except Exception as e:
            self.logger.error(f"Error handling emote list: {e}", exc_info=True)
            
    async def _handle_set_afk(self, event) -> None:
        """Handle setAFK event from CyTube."""
        try:
            # Extract username and AFK status from payload
            # Payload format: {"name": "username", "afk": true/false}
            username = event.payload.get("name")
            is_afk = event.payload.get("afk", False)
            
            if not username:
                return
            
            # Update activity tracker with AFK status
            self.activity_tracker.set_afk_status(event.domain, event.channel, username, is_afk)
            
        except Exception as e:
            self.logger.error(f"Error handling setAFK: {e}", exc_info=True)
            
    async def _periodic_snapshots(self, interval: int) -> None:
        """Periodically save population snapshots."""
        while self._running:
            try:
                await asyncio.sleep(interval)
                
                # Get active sessions from activity tracker
                sessions = self.activity_tracker.get_active_sessions()
                
                for (domain, channel), usernames in sessions.items():
                    # Count connected users (all in session)
                    connected_count = len(usernames)
                    
                    # Count chat users (not AFK)
                    # For simplicity, we'll use connected count for both
                    # A more sophisticated approach would track AFK status
                    chat_count = connected_count
                    
                    await self.db.save_population_snapshot(
                        channel, domain, connected_count, chat_count
                    )
                    
                    self.logger.debug(
                        f"Population snapshot for {channel}: "
                        f"{connected_count} connected, {chat_count} in chat"
                    )
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in periodic snapshots: {e}", exc_info=True)


async def main():
    """Main entry point."""
    import argparse
    import sys
    
    # Parse arguments
    parser = argparse.ArgumentParser(description="User Statistics Tracker for CyTube")
    parser.add_argument("--config", default="config.json", help="Configuration file path")
    parser.add_argument("--log-level", default="INFO", help="Logging level")
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(
        level=getattr(logging, args.log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    logger = logging.getLogger(__name__)
    
    # Create application
    app = UserStatsApp(args.config)
    
    # Setup signal handlers
    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}, shutting down...")
        asyncio.create_task(app.stop())
        
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Run application
    try:
        await app.start()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

"""NATS query endpoints for user statistics."""

import asyncio
import json
import logging
from typing import Optional


class QueryEndpoints:
    """NATS query endpoints for exposing statistics data."""
    
    def __init__(self, app_reference, domain: str):
        """Initialize query endpoints.
        
        Args:
            app_reference: Reference to UserStatsApp for accessing database
            domain: CyTube domain (e.g., "cytu.be")
        """
        self.app = app_reference
        self.domain = domain
        self.logger = logging.getLogger(__name__)
        
        self._subscriptions = []
        
    async def start(self) -> None:
        """Start NATS query endpoints."""
        if not self.app.client or not self.app.client.nats_client:
            self.logger.error("Cannot start query endpoints: NATS client not available")
            return
            
        nats = self.app.client.nats_client
        
        # Subscribe to query subjects
        # Format: cytube.query.userstats.{domain}.{query_type}
        base = f"cytube.query.userstats.{self.domain}"
        
        # User queries
        self._subscriptions.append(
            await nats.subscribe(f"{base}.user.stats", cb=self._handle_user_stats)
        )
        self._subscriptions.append(
            await nats.subscribe(f"{base}.user.messages", cb=self._handle_user_messages)
        )
        self._subscriptions.append(
            await nats.subscribe(f"{base}.user.activity", cb=self._handle_user_activity)
        )
        self._subscriptions.append(
            await nats.subscribe(f"{base}.user.kudos", cb=self._handle_user_kudos)
        )
        
        # Channel queries
        self._subscriptions.append(
            await nats.subscribe(f"{base}.channel.top_users", cb=self._handle_top_users)
        )
        self._subscriptions.append(
            await nats.subscribe(f"{base}.channel.population", cb=self._handle_population)
        )
        self._subscriptions.append(
            await nats.subscribe(f"{base}.channel.media_history", cb=self._handle_media_history)
        )
        
        # Leaderboard queries
        self._subscriptions.append(
            await nats.subscribe(f"{base}.leaderboard.messages", cb=self._handle_leaderboard_messages)
        )
        self._subscriptions.append(
            await nats.subscribe(f"{base}.leaderboard.kudos", cb=self._handle_leaderboard_kudos)
        )
        self._subscriptions.append(
            await nats.subscribe(f"{base}.leaderboard.emotes", cb=self._handle_leaderboard_emotes)
        )
        
        # System queries
        self._subscriptions.append(
            await nats.subscribe(f"{base}.system.health", cb=self._handle_system_health)
        )
        self._subscriptions.append(
            await nats.subscribe(f"{base}.system.stats", cb=self._handle_system_stats)
        )
        
        self.logger.info(f"NATS query endpoints registered under {base}.*")
        
    async def stop(self) -> None:
        """Stop NATS query endpoints."""
        for sub in self._subscriptions:
            try:
                await sub.unsubscribe()
            except Exception as e:
                self.logger.error(f"Error unsubscribing: {e}")
                
        self._subscriptions.clear()
        self.logger.info("Query endpoints stopped")
        
    async def _handle_user_stats(self, msg) -> None:
        """Handle user.stats query - comprehensive user statistics."""
        try:
            # Parse request: {"username": "foo", "channel": "bar"}
            request = json.loads(msg.data.decode())
            username = request.get("username")
            channel = request.get("channel")
            
            if not username:
                await msg.respond(json.dumps({"error": "username required"}).encode())
                return
                
            # Resolve username via aliases
            resolved = await self.app.db.resolve_username(username)
            
            # Get comprehensive stats
            stats = {
                "username": resolved,
                "aliases": await self.app.db.get_user_aliases(resolved),
                "messages": {},
                "pms": 0,
                "activity": {},
                "kudos_plusplus": 0,
                "kudos_phrases": [],
                "emotes": []
            }
            
            # Message counts
            if channel:
                msg_count = await self.app.db.get_user_message_count(resolved, channel, self.domain)
                stats["messages"][channel] = msg_count
            else:
                # All channels
                all_messages = await self.app.db.get_user_all_message_counts(resolved, self.domain)
                stats["messages"] = {row["channel"]: row["count"] for row in all_messages}
                
            # PM count
            pm_count = await self.app.db.get_user_pm_count(resolved)
            stats["pms"] = pm_count
            
            # Activity time
            if channel:
                activity = await self.app.db.get_user_activity_stats(resolved, channel, self.domain)
                if activity:
                    stats["activity"][channel] = {
                        "total_seconds": activity["total_seconds"],
                        "active_seconds": activity["active_seconds"]
                    }
            else:
                # All channels
                all_activity = await self.app.db.get_user_all_activity(resolved, self.domain)
                for row in all_activity:
                    stats["activity"][row["channel"]] = {
                        "total_seconds": row["total_seconds"],
                        "active_seconds": row["active_seconds"]
                    }
                    
            # Kudos
            kudos_pp = await self.app.db.get_user_kudos_plusplus(resolved, self.domain)
            stats["kudos_plusplus"] = kudos_pp
            
            kudos_phrases = await self.app.db.get_user_kudos_phrases(resolved, self.domain)
            stats["kudos_phrases"] = [{"phrase": row["phrase"], "count": row["count"]} for row in kudos_phrases]
            
            # Emotes
            emotes = await self.app.db.get_user_emote_usage(resolved, self.domain)
            stats["emotes"] = [{"emote": row["emote"], "count": row["count"]} for row in emotes]
            
            await msg.respond(json.dumps(stats).encode())
            
        except Exception as e:
            self.logger.error(f"Error handling user.stats query: {e}", exc_info=True)
            await msg.respond(json.dumps({"error": str(e)}).encode())
            
    async def _handle_user_messages(self, msg) -> None:
        """Handle user.messages query - message counts."""
        try:
            request = json.loads(msg.data.decode())
            username = request.get("username")
            channel = request.get("channel")
            
            if not username:
                await msg.respond(json.dumps({"error": "username required"}).encode())
                return
                
            resolved = await self.app.db.resolve_username(username)
            
            if channel:
                count = await self.app.db.get_user_message_count(resolved, channel, self.domain)
                response = {"username": resolved, "channel": channel, "count": count}
            else:
                all_counts = await self.app.db.get_user_all_message_counts(resolved, self.domain)
                response = {"username": resolved, "channels": {row["channel"]: row["count"] for row in all_counts}}
                
            await msg.respond(json.dumps(response).encode())
            
        except Exception as e:
            self.logger.error(f"Error handling user.messages query: {e}", exc_info=True)
            await msg.respond(json.dumps({"error": str(e)}).encode())
            
    async def _handle_user_activity(self, msg) -> None:
        """Handle user.activity query - time spent in channel."""
        try:
            request = json.loads(msg.data.decode())
            username = request.get("username")
            channel = request.get("channel")
            
            if not username or not channel:
                await msg.respond(json.dumps({"error": "username and channel required"}).encode())
                return
                
            resolved = await self.app.db.resolve_username(username)
            activity = await self.app.db.get_user_activity_stats(resolved, channel, self.domain)
            
            if activity:
                response = {
                    "username": resolved,
                    "channel": channel,
                    "total_seconds": activity["total_seconds"],
                    "active_seconds": activity["active_seconds"]
                }
            else:
                response = {
                    "username": resolved,
                    "channel": channel,
                    "total_seconds": 0,
                    "active_seconds": 0
                }
                
            await msg.respond(json.dumps(response).encode())
            
        except Exception as e:
            self.logger.error(f"Error handling user.activity query: {e}", exc_info=True)
            await msg.respond(json.dumps({"error": str(e)}).encode())
            
    async def _handle_user_kudos(self, msg) -> None:
        """Handle user.kudos query - kudos received."""
        try:
            request = json.loads(msg.data.decode())
            username = request.get("username")
            
            if not username:
                await msg.respond(json.dumps({"error": "username required"}).encode())
                return
                
            resolved = await self.app.db.resolve_username(username)
            
            kudos_pp = await self.app.db.get_user_kudos_plusplus(resolved, self.domain)
            kudos_phrases = await self.app.db.get_user_kudos_phrases(resolved, self.domain)
            
            response = {
                "username": resolved,
                "plusplus": kudos_pp,
                "phrases": [{"phrase": row["phrase"], "count": row["count"]} for row in kudos_phrases]
            }
            
            await msg.respond(json.dumps(response).encode())
            
        except Exception as e:
            self.logger.error(f"Error handling user.kudos query: {e}", exc_info=True)
            await msg.respond(json.dumps({"error": str(e)}).encode())
            
    async def _handle_top_users(self, msg) -> None:
        """Handle channel.top_users query - leaderboard for channel."""
        try:
            request = json.loads(msg.data.decode())
            channel = request.get("channel")
            limit = request.get("limit", 10)
            
            if not channel:
                await msg.respond(json.dumps({"error": "channel required"}).encode())
                return
                
            top_users = await self.app.db.get_top_message_senders(channel, self.domain, limit)
            
            response = {
                "channel": channel,
                "top_users": [{"username": row["username"], "count": row["count"]} for row in top_users]
            }
            
            await msg.respond(json.dumps(response).encode())
            
        except Exception as e:
            self.logger.error(f"Error handling channel.top_users query: {e}", exc_info=True)
            await msg.respond(json.dumps({"error": str(e)}).encode())
            
    async def _handle_population(self, msg) -> None:
        """Handle channel.population query - recent population snapshots."""
        try:
            request = json.loads(msg.data.decode())
            channel = request.get("channel")
            hours = request.get("hours", 24)
            
            if not channel:
                await msg.respond(json.dumps({"error": "channel required"}).encode())
                return
                
            snapshots = await self.app.db.get_recent_population_snapshots(channel, self.domain, hours)
            
            response = {
                "channel": channel,
                "hours": hours,
                "snapshots": [
                    {
                        "timestamp": row["timestamp"],
                        "connected": row["connected_count"],
                        "chatting": row["chat_count"]
                    }
                    for row in snapshots
                ]
            }
            
            await msg.respond(json.dumps(response).encode())
            
        except Exception as e:
            self.logger.error(f"Error handling channel.population query: {e}", exc_info=True)
            await msg.respond(json.dumps({"error": str(e)}).encode())
            
    async def _handle_media_history(self, msg) -> None:
        """Handle channel.media_history query - recent media changes."""
        try:
            request = json.loads(msg.data.decode())
            channel = request.get("channel")
            limit = request.get("limit", 20)
            
            if not channel:
                await msg.respond(json.dumps({"error": "channel required"}).encode())
                return
                
            media_history = await self.app.db.get_recent_media_changes(channel, self.domain, limit)
            
            response = {
                "channel": channel,
                "media_history": [
                    {
                        "timestamp": row["timestamp"],
                        "title": row["title"],
                        "type": row["media_type"],
                        "id": row["media_id"]
                    }
                    for row in media_history
                ]
            }
            
            await msg.respond(json.dumps(response).encode())
            
        except Exception as e:
            self.logger.error(f"Error handling channel.media_history query: {e}", exc_info=True)
            await msg.respond(json.dumps({"error": str(e)}).encode())
            
    async def _handle_leaderboard_messages(self, msg) -> None:
        """Handle leaderboard.messages query - global message leaderboard."""
        try:
            request = json.loads(msg.data.decode())
            limit = request.get("limit", 20)
            
            leaderboard = await self.app.db.get_global_message_leaderboard(self.domain, limit)
            
            response = {
                "leaderboard": [{"username": row["username"], "count": row["count"]} for row in leaderboard]
            }
            
            await msg.respond(json.dumps(response).encode())
            
        except Exception as e:
            self.logger.error(f"Error handling leaderboard.messages query: {e}", exc_info=True)
            await msg.respond(json.dumps({"error": str(e)}).encode())
            
    async def _handle_leaderboard_kudos(self, msg) -> None:
        """Handle leaderboard.kudos query - global kudos leaderboard."""
        try:
            request = json.loads(msg.data.decode())
            limit = request.get("limit", 20)
            
            leaderboard = await self.app.db.get_global_kudos_leaderboard(self.domain, limit)
            
            response = {
                "leaderboard": [{"username": row["username"], "count": row["count"]} for row in leaderboard]
            }
            
            await msg.respond(json.dumps(response).encode())
            
        except Exception as e:
            self.logger.error(f"Error handling leaderboard.kudos query: {e}", exc_info=True)
            await msg.respond(json.dumps({"error": str(e)}).encode())
            
    async def _handle_leaderboard_emotes(self, msg) -> None:
        """Handle leaderboard.emotes query - most used emotes."""
        try:
            request = json.loads(msg.data.decode())
            limit = request.get("limit", 20)
            
            leaderboard = await self.app.db.get_top_emotes(self.domain, limit)
            
            response = {
                "leaderboard": [{"emote": row["emote"], "count": row["count"]} for row in leaderboard]
            }
            
            await msg.respond(json.dumps(response).encode())
            
        except Exception as e:
            self.logger.error(f"Error handling leaderboard.emotes query: {e}", exc_info=True)
            await msg.respond(json.dumps({"error": str(e)}).encode())
            
    async def _handle_system_health(self, msg) -> None:
        """Handle system.health query - service health status."""
        try:
            health = {
                "service": "userstats",
                "status": "healthy" if self.app._running else "unhealthy",
                "database_connected": bool(self.app.db and self.app.db.db_path),
                "nats_connected": bool(self.app.client and self.app.client._running),
                "uptime_seconds": 0  # Could track this
            }
            
            await msg.respond(json.dumps(health).encode())
            
        except Exception as e:
            self.logger.error(f"Error handling system.health query: {e}", exc_info=True)
            await msg.respond(json.dumps({"error": str(e)}).encode())
            
    async def _handle_system_stats(self, msg) -> None:
        """Handle system.stats query - overall statistics."""
        try:
            stats = {
                "total_users": await self.app.db.get_total_users(),
                "total_messages": await self.app.db.get_total_messages(),
                "total_pms": await self.app.db.get_total_pms(),
                "total_kudos": await self.app.db.get_total_kudos_plusplus(),
                "total_emotes": await self.app.db.get_total_emote_usage(),
                "total_media_changes": await self.app.db.get_total_media_changes(),
                "active_sessions": self.app.activity_tracker.get_active_session_count() if self.app.activity_tracker else 0
            }
            
            await msg.respond(json.dumps(stats).encode())
            
        except Exception as e:
            self.logger.error(f"Error handling system.stats query: {e}", exc_info=True)
            await msg.respond(json.dumps({"error": str(e)}).encode())

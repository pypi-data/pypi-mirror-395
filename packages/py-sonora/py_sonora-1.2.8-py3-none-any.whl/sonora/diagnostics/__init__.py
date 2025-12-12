"""Advanced diagnostics and developer experience tools."""

import asyncio
import cProfile
import io
import pstats
import time
import tracemalloc
from typing import Any, Dict, List, Optional, TextIO

from ..events import EventType, event_manager
from ..performance import performance_monitor


class PerformanceProfiler:
    """Built-in performance profiler."""

    def __init__(self):
        self.profiler: Optional[cProfile.Profile] = None
        self._profiling = False
        self._profile_data: Optional[io.StringIO] = None

    def start_profiling(self) -> None:
        """Start performance profiling."""
        if self._profiling:
            return

        self.profiler = cProfile.Profile()
        self.profiler.enable()
        self._profiling = True
        tracemalloc.start()

    def stop_profiling(self) -> Dict[str, Any]:
        """Stop profiling and return results."""
        if not self._profiling or not self.profiler:
            return {}

        self.profiler.disable()
        self._profiling = False

        # Get profile stats
        self._profile_data = io.StringIO()
        stats = pstats.Stats(self.profiler, stream=self._profile_data)
        stats.sort_stats('cumulative')
        stats.print_stats(20)  # Top 20 functions

        # Get memory stats
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return {
            "profile_stats": self._profile_data.getvalue(),
            "memory_current_mb": current / 1024 / 1024,
            "memory_peak_mb": peak / 1024 / 1024,
            "timestamp": time.time()
        }

    def is_profiling(self) -> bool:
        """Check if profiling is active."""
        return self._profiling


class StructuredLogger:
    """JSON structured logging for debugging."""

    def __init__(self, enabled: bool = False, log_file: Optional[str] = None):
        self.enabled = enabled
        self.log_file = log_file
        self._log_buffer: List[Dict[str, Any]] = []
        self._max_buffer_size = 1000

    def enable(self) -> None:
        """Enable structured logging."""
        self.enabled = True

    def disable(self) -> None:
        """Disable structured logging."""
        self.enabled = False

    def log_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Log a structured event."""
        if not self.enabled:
            return

        log_entry = {
            "timestamp": time.time(),
            "event_type": event_type,
            "data": data
        }

        self._log_buffer.append(log_entry)

        # Maintain buffer size
        if len(self._log_buffer) > self._max_buffer_size:
            self._log_buffer = self._log_buffer[-self._max_buffer_size:]

    def get_logs(self, event_type: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get logged events."""
        logs = self._log_buffer

        if event_type:
            logs = [log for log in logs if log["event_type"] == event_type]

        return logs[-limit:]

    def clear_logs(self) -> None:
        """Clear the log buffer."""
        self._log_buffer.clear()

    def export_logs(self, filepath: str) -> None:
        """Export logs to file."""
        import json
        with open(filepath, 'w') as f:
            json.dump(self._log_buffer, f, indent=2, default=str)


class WiretapDebugger:
    """Wire-level debugging for Lavalink protocol."""

    def __init__(self):
        self.enabled = False
        self.captured_packets: List[Dict[str, Any]] = []
        self._max_packets = 1000
        self._listener_id: Optional[int] = None

    def enable(self) -> None:
        """Enable wiretap debugging."""
        if self.enabled:
            return

        self.enabled = True
        # This would hook into the websocket layer
        # For now, this is a placeholder

    def disable(self) -> None:
        """Disable wiretap debugging."""
        self.enabled = False
        if self._listener_id:
            event_manager.remove_all_listeners()
            self._listener_id = None

    def get_captured_packets(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get captured packets."""
        return self.captured_packets[-limit:]

    def clear_packets(self) -> None:
        """Clear captured packets."""
        self.captured_packets.clear()

    def export_packets(self, filepath: str) -> None:
        """Export captured packets to file."""
        import json
        with open(filepath, 'w') as f:
            json.dump(self.captured_packets, f, indent=2, default=str)


class PlayerIntrospector:
    """Introspection tools for player state and decision making."""

    def __init__(self):
        self.decision_log: List[Dict[str, Any]] = []
        self._max_log_size = 500

    def log_decision(self, decision_type: str, context: Dict[str, Any], result: Any) -> None:
        """Log a player decision."""
        entry = {
            "timestamp": time.time(),
            "decision_type": decision_type,
            "context": context,
            "result": result
        }

        self.decision_log.append(entry)

        if len(self.decision_log) > self._max_log_size:
            self.decision_log = self.decision_log[-self._max_log_size:]

    def get_decisions(self, decision_type: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Get logged decisions."""
        decisions = self.decision_log

        if decision_type:
            decisions = [d for d in decisions if d["decision_type"] == decision_type]

        return decisions[-limit:]

    def analyze_decision_patterns(self) -> Dict[str, Any]:
        """Analyze decision patterns."""
        if not self.decision_log:
            return {}

        # Group by decision type
        by_type = {}
        for decision in self.decision_log:
            d_type = decision["decision_type"]
            if d_type not in by_type:
                by_type[d_type] = []
            by_type[d_type].append(decision)

        analysis = {}
        for d_type, decisions in by_type.items():
            analysis[d_type] = {
                "count": len(decisions),
                "avg_context_size": sum(len(d["context"]) for d in decisions) / len(decisions),
                "time_range": {
                    "start": min(d["timestamp"] for d in decisions),
                    "end": max(d["timestamp"] for d in decisions)
                }
            }

        return analysis


class PlaybackTimelineDebugger:
    """Timeline debugging for playback events."""

    def __init__(self):
        self.timeline: List[Dict[str, Any]] = []
        self._max_events = 2000

    def record_event(self, event_type: str, guild_id: int, data: Dict[str, Any]) -> None:
        """Record a playback event."""
        event = {
            "timestamp": time.time(),
            "event_type": event_type,
            "guild_id": guild_id,
            "data": data
        }

        self.timeline.append(event)

        if len(self.timeline) > self._max_events:
            self.timeline = self.timeline[-self._max_events:]

    def get_timeline(self, guild_id: Optional[int] = None, event_types: Optional[List[str]] = None,
                    time_range: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Get timeline events with filtering."""
        events = self.timeline

        if guild_id is not None:
            events = [e for e in events if e["guild_id"] == guild_id]

        if event_types:
            events = [e for e in events if e["event_type"] in event_types]

        if time_range:
            start_time, end_time = time_range
            events = [e for e in events if start_time <= e["timestamp"] <= end_time]

        return events

    def generate_timeline_report(self, guild_id: int) -> Dict[str, Any]:
        """Generate a timeline report for analysis."""
        events = self.get_timeline(guild_id)

        if not events:
            return {"error": "No events found for guild"}

        # Analyze event patterns
        event_counts = {}
        time_gaps = []

        for i, event in enumerate(events[1:], 1):
            prev_event = events[i-1]
            gap = event["timestamp"] - prev_event["timestamp"]
            time_gaps.append(gap)

            event_type = event["event_type"]
            event_counts[event_type] = event_counts.get(event_type, 0) + 1

        return {
            "total_events": len(events),
            "time_span": events[-1]["timestamp"] - events[0]["timestamp"],
            "event_counts": event_counts,
            "avg_time_between_events": sum(time_gaps) / len(time_gaps) if time_gaps else 0,
            "max_gap": max(time_gaps) if time_gaps else 0,
            "min_gap": min(time_gaps) if time_gaps else 0
        }


class ReproduciblePlaybackEngine:
    """Engine for reproducible playback testing."""

    def __init__(self):
        self.recorded_sessions: Dict[str, List[Dict[str, Any]]] = {}
        self._current_session: Optional[str] = None
        self._session_events: List[Dict[str, Any]] = []

    def start_recording(self, session_id: str) -> None:
        """Start recording a playback session."""
        self._current_session = session_id
        self._session_events = []

    def stop_recording(self) -> Optional[str]:
        """Stop recording and save session."""
        if not self._current_session:
            return None

        session_id = self._current_session
        self.recorded_sessions[session_id] = self._session_events.copy()
        self._current_session = None
        self._session_events = []
        return session_id

    def record_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Record an event in the current session."""
        if not self._current_session:
            return

        event = {
            "timestamp": time.time(),
            "event_type": event_type,
            "data": data
        }

        self._session_events.append(event)

    async def replay_session(self, session_id: str, speed: float = 1.0) -> None:
        """Replay a recorded session."""
        if session_id not in self.recorded_sessions:
            raise ValueError(f"Session {session_id} not found")

        events = self.recorded_sessions[session_id]
        if not events:
            return

        start_time = time.time()
        session_start = events[0]["timestamp"]

        for event in events:
            # Calculate delay from session start
            event_time = event["timestamp"]
            delay = (event_time - session_start) / speed

            # Wait for the appropriate time
            elapsed = time.time() - start_time
            if delay > elapsed:
                await asyncio.sleep(delay - elapsed)

            # Emit the event
            await event_manager.emit_event(
                EventType(event["event_type"]),
                event["data"]
            )

    def list_sessions(self) -> List[str]:
        """List recorded sessions."""
        return list(self.recorded_sessions.keys())

    def delete_session(self, session_id: str) -> bool:
        """Delete a recorded session."""
        if session_id in self.recorded_sessions:
            del self.recorded_sessions[session_id]
            return True
        return False


# Global diagnostics instances
performance_profiler = PerformanceProfiler()
structured_logger = StructuredLogger()
wiretap_debugger = WiretapDebugger()
player_introspector = PlayerIntrospector()
timeline_debugger = PlaybackTimelineDebugger()
playback_engine = ReproduciblePlaybackEngine()
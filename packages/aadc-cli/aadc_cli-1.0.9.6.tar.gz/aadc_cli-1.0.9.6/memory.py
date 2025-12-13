"""
Memory Module for Gemini Agent
Provides persistent memory and context across sessions
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


MEMORY_DIR = Path.home() / ".gemini-agent" / "memory"
MEMORY_FILE = MEMORY_DIR / "memory.json"
CONTEXT_FILE = MEMORY_DIR / "context.json"
HISTORY_FILE = MEMORY_DIR / "history.json"


@dataclass
class MemoryEntry:
    """A single memory entry."""
    key: str
    value: Any
    category: str  # "fact", "preference", "project", "note"
    created_at: str
    updated_at: str
    source: str = "conversation"  # Where this memory came from


class MemoryManager:
    """Manages persistent memory across sessions."""
    
    def __init__(self):
        self._ensure_memory_dir()
        self.memories: Dict[str, MemoryEntry] = {}
        self.context: Dict[str, Any] = {}
        self.conversation_history: List[Dict] = []
        self._load()
    
    def _ensure_memory_dir(self):
        """Ensure memory directory exists."""
        MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    
    def _load(self):
        """Load memories from disk."""
        # Load memories
        if MEMORY_FILE.exists():
            try:
                with open(MEMORY_FILE, 'r') as f:
                    data = json.load(f)
                    for key, entry_data in data.items():
                        self.memories[key] = MemoryEntry(**entry_data)
            except Exception:
                self.memories = {}
        
        # Load context
        if CONTEXT_FILE.exists():
            try:
                with open(CONTEXT_FILE, 'r') as f:
                    self.context = json.load(f)
            except Exception:
                self.context = {}
        
        # Load conversation history (last 50 conversations)
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, 'r') as f:
                    self.conversation_history = json.load(f)
            except Exception:
                self.conversation_history = []
    
    def _save(self):
        """Save memories to disk."""
        self._ensure_memory_dir()
        
        # Save memories
        memories_data = {k: asdict(v) for k, v in self.memories.items()}
        with open(MEMORY_FILE, 'w') as f:
            json.dump(memories_data, f, indent=2)
        
        # Save context
        with open(CONTEXT_FILE, 'w') as f:
            json.dump(self.context, f, indent=2)
        
        # Save history (keep last 50)
        with open(HISTORY_FILE, 'w') as f:
            json.dump(self.conversation_history[-50:], f, indent=2)
    
    def remember(
        self,
        key: str,
        value: Any,
        category: str = "fact",
        source: str = "conversation"
    ) -> dict:
        """Store a memory."""
        now = datetime.now().isoformat()
        
        if key in self.memories:
            # Update existing memory
            entry = self.memories[key]
            entry.value = value
            entry.updated_at = now
            entry.source = source
        else:
            # Create new memory
            entry = MemoryEntry(
                key=key,
                value=value,
                category=category,
                created_at=now,
                updated_at=now,
                source=source
            )
        
        self.memories[key] = entry
        self._save()
        
        return {
            "success": True,
            "message": f"Remembered: {key}",
            "key": key,
            "value": value
        }
    
    def recall(self, key: str) -> dict:
        """Retrieve a specific memory."""
        if key in self.memories:
            entry = self.memories[key]
            return {
                "success": True,
                "key": key,
                "value": entry.value,
                "category": entry.category,
                "updated_at": entry.updated_at
            }
        return {
            "success": False,
            "error": f"No memory found for: {key}"
        }
    
    def forget(self, key: str) -> dict:
        """Remove a memory."""
        if key in self.memories:
            del self.memories[key]
            self._save()
            return {
                "success": True,
                "message": f"Forgot: {key}"
            }
        return {
            "success": False,
            "error": f"No memory found for: {key}"
        }
    
    def search_memories(self, query: str) -> dict:
        """Search memories by key or value."""
        query_lower = query.lower()
        results = []
        
        for key, entry in self.memories.items():
            if query_lower in key.lower() or query_lower in str(entry.value).lower():
                results.append({
                    "key": key,
                    "value": entry.value,
                    "category": entry.category
                })
        
        return {
            "success": True,
            "count": len(results),
            "results": results
        }
    
    def list_memories(self, category: Optional[str] = None) -> dict:
        """List all memories, optionally filtered by category."""
        memories = []
        
        for key, entry in self.memories.items():
            if category is None or entry.category == category:
                memories.append({
                    "key": key,
                    "value": entry.value,
                    "category": entry.category,
                    "updated_at": entry.updated_at
                })
        
        return {
            "success": True,
            "count": len(memories),
            "memories": memories
        }
    
    def set_context(self, key: str, value: Any) -> dict:
        """Set a context value (session-persistent)."""
        self.context[key] = value
        self._save()
        return {
            "success": True,
            "message": f"Context set: {key}"
        }
    
    def get_context(self, key: str) -> Any:
        """Get a context value."""
        return self.context.get(key)
    
    def get_all_context(self) -> dict:
        """Get all context."""
        return self.context.copy()
    
    def clear_context(self):
        """Clear all context."""
        self.context = {}
        self._save()
    
    def add_conversation(self, role: str, content: str, summary: Optional[str] = None):
        """Add a conversation entry to history."""
        self.conversation_history.append({
            "role": role,
            "content": content[:1000],  # Truncate long content
            "summary": summary,
            "timestamp": datetime.now().isoformat()
        })
        self._save()
    
    def get_recent_history(self, count: int = 10) -> List[Dict]:
        """Get recent conversation history."""
        return self.conversation_history[-count:]
    
    def get_memory_summary(self) -> str:
        """Get a summary of memories for the AI context."""
        if not self.memories:
            return "No memories stored yet."
        
        summary_parts = ["## User Memory & Context\n"]
        
        # Group by category
        by_category: Dict[str, List] = {}
        for key, entry in self.memories.items():
            cat = entry.category
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(f"- {key}: {entry.value}")
        
        for category, items in by_category.items():
            summary_parts.append(f"\n### {category.title()}s:")
            summary_parts.extend(items[:10])  # Limit per category
        
        # Add recent context
        if self.context:
            summary_parts.append("\n### Current Context:")
            for key, value in list(self.context.items())[:5]:
                summary_parts.append(f"- {key}: {value}")
        
        return "\n".join(summary_parts)
    
    def clear_all(self):
        """Clear all memories and context."""
        self.memories = {}
        self.context = {}
        self.conversation_history = []
        self._save()


# Global memory manager instance
memory_manager = MemoryManager()

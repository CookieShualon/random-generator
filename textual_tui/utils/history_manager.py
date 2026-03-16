"""History management for generation results."""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class HistoryEntry:
    """Represents a single generation history entry."""
    timestamp: str
    gen_type: str
    parameters: Dict
    results: List[str]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'HistoryEntry':
        """Create from dictionary."""
        return cls(**data)


class HistoryManager:
    """Manages generation history with persistence."""
    
    def __init__(self, history_file: str = ".random_gen_history.json", max_entries: int = 100):
        """
        Initialize history manager.
        
        Args:
            history_file: Path to history file
            max_entries: Maximum number of entries to keep
        """
        self.history_file = Path.home() / history_file
        self.max_entries = max_entries
        self.entries: List[HistoryEntry] = []
        self.load()
    
    def add_entry(self, gen_type: str, parameters: Dict, results: List[str]) -> None:
        """
        Add a new history entry.
        
        Args:
            gen_type: Type of generation (number, float, color, etc.)
            parameters: Generation parameters
            results: Generated results
        """
        entry = HistoryEntry(
            timestamp=datetime.now().isoformat(),
            gen_type=gen_type,
            parameters=parameters,
            results=results
        )
        
        self.entries.insert(0, entry)  # Add to beginning
        
        # Trim to max entries
        if len(self.entries) > self.max_entries:
            self.entries = self.entries[:self.max_entries]
        
        self.save()
    
    def get_entries(self, gen_type: Optional[str] = None, limit: Optional[int] = None) -> List[HistoryEntry]:
        """
        Get history entries with optional filtering.
        
        Args:
            gen_type: Filter by generation type (None for all)
            limit: Maximum number of entries to return
        
        Returns:
            List of history entries
        """
        entries = self.entries
        
        if gen_type:
            entries = [e for e in entries if e.gen_type == gen_type]
        
        if limit:
            entries = entries[:limit]
        
        return entries
    
    def get_recent(self, count: int = 5) -> List[HistoryEntry]:
        """
        Get most recent entries.
        
        Args:
            count: Number of recent entries to return
        
        Returns:
            List of recent history entries
        """
        return self.entries[:count]
    
    def clear(self) -> None:
        """Clear all history."""
        self.entries = []
        self.save()
    
    def delete_entry(self, index: int) -> bool:
        """
        Delete entry at index.
        
        Args:
            index: Index of entry to delete
        
        Returns:
            True if deleted, False if index invalid
        """
        if 0 <= index < len(self.entries):
            del self.entries[index]
            self.save()
            return True
        return False
    
    def save(self) -> None:
        """Save history to file."""
        try:
            data = [entry.to_dict() for entry in self.entries]
            with open(self.history_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            # Silently fail if can't save
            pass
    
    def load(self) -> None:
        """Load history from file."""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r') as f:
                    data = json.load(f)
                    self.entries = [HistoryEntry.from_dict(entry) for entry in data]
        except Exception as e:
            # Start with empty history if can't load
            self.entries = []
    
    def format_timestamp(self, timestamp: str) -> str:
        """
        Format timestamp for display.
        
        Args:
            timestamp: ISO format timestamp
        
        Returns:
            Human-readable time string
        """
        try:
            dt = datetime.fromisoformat(timestamp)
            now = datetime.now()
            diff = now - dt
            
            if diff.seconds < 60:
                return "Just now"
            elif diff.seconds < 3600:
                minutes = diff.seconds // 60
                return f"{minutes} min ago"
            elif diff.seconds < 86400:
                hours = diff.seconds // 3600
                return f"{hours} hour{'s' if hours > 1 else ''} ago"
            elif diff.days == 1:
                return "Yesterday"
            elif diff.days < 7:
                return f"{diff.days} days ago"
            else:
                return dt.strftime("%Y-%m-%d")
        except:
            return timestamp
    
    def format_parameters(self, entry: HistoryEntry) -> str:
        """
        Format parameters for display.
        
        Args:
            entry: History entry
        
        Returns:
            Formatted parameter string
        """
        params = entry.parameters
        gen_type = entry.gen_type
        
        if gen_type == "number":
            parts = [f"{params.get('min', 1)}-{params.get('max', 100)}"]
            if params.get('exclude'):
                parts.append(f"excl:{len(params['exclude'])}")
            parts.append(f"count={params.get('count', 1)}")
            return ", ".join(parts)
        
        elif gen_type == "float":
            return f"{params.get('min', 0.0)}-{params.get('max', 1.0)}, dec={params.get('decimals', 2)}, count={params.get('count', 1)}"
        
        elif gen_type == "color":
            return f"{params.get('format', 'hex')}, count={params.get('count', 1)}"
        
        elif gen_type == "string":
            return f"len={params.get('length', 10)}, {params.get('pattern', 'alphanumeric')}, count={params.get('count', 1)}"
        
        elif gen_type == "custom":
            template = params.get('template', '')
            if len(template) > 20:
                template = template[:17] + "..."
            return f"{template}, count={params.get('count', 1)}"
        
        elif gen_type == "list":
            return f"{len(params.get('items', []))} items, count={params.get('count', 1)}, unique={params.get('unique', False)}"
        
        return str(params)
    
    def format_results(self, entry: HistoryEntry, max_length: int = 50) -> str:
        """
        Format results for display.
        
        Args:
            entry: History entry
            max_length: Maximum length of result string
        
        Returns:
            Formatted result string
        """
        results_str = ", ".join(str(r) for r in entry.results)
        
        if len(results_str) > max_length:
            results_str = results_str[:max_length - 3] + "..."
        
        return results_str

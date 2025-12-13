"""
alphabit - Hardware-accelerated symbolic stream processing core module.

alphabit - Hardware-accelerated symbolic stream processing
The fundamental unit of symbolic computation.
"""

import re
import logging
import time
from typing import List, Tuple, Optional, Union, Dict, Iterable, TypeAlias
from collections import OrderedDict
from threading import Lock
from abc import ABC, abstractmethod

# Configure module-level logger
logger = logging.getLogger(__name__)

# ============================================================================
# Type Aliases
# ============================================================================

MatchResult: TypeAlias = Tuple[int, int, int]  # (pattern_id, start, end)
QuickMatch: TypeAlias = Tuple[int, int]         # (start, end)

# ============================================================================
# Constants
# ============================================================================

MAX_PATTERN_ID = 1_000_000  # Prevent unbounded growth
MAX_CACHED_PATTERNS = 1000  # Maximum patterns in LRU cache

# ============================================================================
# Module-level state for quick scan function
# ============================================================================

_scan_spu: Optional['SPU'] = None
_scan_spu_lock = Lock()
_loaded_patterns: OrderedDict[str, int] = OrderedDict()  # LRU cache
_pattern_counter = 0
_pattern_counter_lock = Lock()
# Reverse mapping: pattern_id -> pattern (for LRU eviction)
_pattern_id_to_pattern: Dict[int, str] = {}


# ============================================================================
# Hardware Interface - Abstract Base Class
# ============================================================================

class HardwareInterface(ABC):
    """Abstract interface for hardware pattern matching engines."""
    
    @abstractmethod
    def load_pattern(self, pattern_id: int, pattern: str) -> None:
        """Load a pattern into the hardware engine."""
        ...
    
    @abstractmethod
    def unload_pattern(self, pattern_id: int) -> bool:
        """Unload a pattern from the hardware engine."""
        ...
    
    @abstractmethod
    def clear_patterns(self) -> None:
        """Clear all patterns from the hardware engine."""
        ...
    
    @abstractmethod
    def scan(
        self,
        text: Union[str, bytes],
        pattern_ids: Optional[Iterable[int]] = None
    ) -> List[MatchResult]:
        """Scan text for patterns."""
        ...


# ============================================================================
# SimulatedHardware - Core pattern matching engine
# ============================================================================

class SimulatedHardware(HardwareInterface):
    """
    Simulated hardware engine for pattern matching.
    
    This class provides a hardware-accelerated pattern matching interface
    that can be extended to support actual hardware devices in the future.
    """
    
    def __init__(self, simulate_delay: bool = False) -> None:
        """
        Initialize the simulated hardware engine.
        
        Args:
            simulate_delay: If True, adds artificial delay to simulate
                          hardware processing time. Set to False for
                          maximum performance.
        """
        self.patterns: Dict[int, re.Pattern] = {}
        self.simulate_delay = simulate_delay
    
    def load_pattern(self, pattern_id: int, pattern: str) -> None:
        """
        Load a regex pattern into the engine.
        
        Args:
            pattern_id: Unique non-negative identifier for the pattern
            pattern: Regex pattern string to compile
            
        Raises:
            ValueError: If pattern_id is negative, pattern is empty, or
                         pattern is invalid regex
            TypeError: If pattern is not a string
        """
        if pattern_id < 0:
            raise ValueError(
                f"pattern_id must be non-negative, got {pattern_id}"
            )
        
        if not isinstance(pattern, str):
            raise TypeError(
                f"pattern must be a string, got {type(pattern).__name__}"
            )
        
        if not pattern:
            raise ValueError("pattern cannot be empty")
        
        try:
            self.patterns[pattern_id] = re.compile(pattern)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {e}") from e
    
    def unload_pattern(self, pattern_id: int) -> bool:
        """
        Remove a pattern from the engine.
        
        Args:
            pattern_id: Identifier of the pattern to remove
            
        Returns:
            True if pattern was removed, False if it didn't exist
        """
        if pattern_id in self.patterns:
            del self.patterns[pattern_id]
            return True
        return False
    
    def clear_patterns(self) -> None:
        """Clear all loaded patterns from the engine."""
        self.patterns.clear()
    
    def scan(
        self,
        text: Union[str, bytes],
        pattern_ids: Optional[Iterable[int]] = None
    ) -> List[MatchResult]:
        """
        Scan text for matches against loaded patterns.
        
        Args:
            text: Text to scan (string or bytes)
            pattern_ids: Iterable of pattern IDs to search. If None,
                       searches all loaded patterns.
        
        Returns:
            List of tuples (pattern_id, start, end) for each match found.
            Results are ordered by pattern_id, then by position in text.
        
        Raises:
            UnicodeDecodeError: If bytes cannot be decoded as UTF-8
            TypeError: If pattern_ids is not an iterable of integers
        """
        # Early return for empty input
        if not text:
            return []
        
        # Decode bytes to string if needed
        if isinstance(text, bytes):
            try:
                text_str = text.decode('utf-8')
            except UnicodeDecodeError as e:
                raise UnicodeDecodeError(
                    "utf-8",
                    text,
                    e.start,
                    e.end,
                    "Failed to decode bytes as UTF-8"
                ) from e
        else:
            text_str = text
        
        # Simulate hardware processing delay if enabled
        if self.simulate_delay:
            processing_time = min(len(text_str) / 5_000_000, 0.1)
            time.sleep(processing_time)
        
                # Determine which patterns to scan
        if pattern_ids is None:
            pattern_ids = tuple(self.patterns.keys())
        elif isinstance(pattern_ids, str):
            # String is iterable but not what we want
            raise TypeError(
                "pattern_ids must be a list"
            )
        elif not isinstance(pattern_ids, (list, tuple)):
            # Try to convert, but validate first
            try:
                # Check if it's iterable and contains only integers
                pattern_ids = tuple(pattern_ids)
            except TypeError:
                raise TypeError(
                    f"pattern_ids must be a list or tuple, got {type(pattern_ids).__name__}"
                )
        
        # Validate pattern_ids contains integers
        for pid in pattern_ids:
            if not isinstance(pid, int):
                raise TypeError(
                    f"pattern_ids must contain integers, got {type(pid).__name__}"
                )
                
        if self.simulate_delay:
            processing_time = min(len(text_str) / 5_000_000, 0.1)
            time.sleep(processing_time)
        
        # Scan patterns and collect matches
        results: List[MatchResult] = []
        patterns = self.patterns  # Cache reference for performance
        
        for pattern_id in pattern_ids:
            pattern = patterns.get(pattern_id)
            if pattern is None:
                logger.warning(
                    f"Pattern ID {pattern_id} not loaded, skipping"
                )
                continue
            
            # Collect all matches for this pattern
            for match in pattern.finditer(text_str):
                results.append((pattern_id, match.start(), match.end()))
        
        return results
    
    def __len__(self) -> int:
        """Return the number of loaded patterns."""
        return len(self.patterns)
    
    def __contains__(self, pattern_id: int) -> bool:
        """Check if a pattern ID is loaded."""
        return pattern_id in self.patterns


# ============================================================================
# SPU - Symbolic Stream Processor
# ============================================================================

class SPU:
    """
    Symbolic Stream Processor - The alphabit Engine.
    
    This is the main interface for hardware-accelerated pattern matching.
    It provides a high-level API for loading patterns and scanning text.
    """
    
    def __init__(
        self,
        device_path: Optional[str] = None,
        simulate_delay: bool = False
    ) -> None:
        """
        Initialize the SPU device.
        
        Args:
            device_path: Path to hardware device (for future hardware support).
                        If None, uses simulated hardware.
            simulate_delay: If True, adds artificial delay to simulate hardware
        """
        self.device_path = device_path
        self.hw = SimulatedHardware(simulate_delay=simulate_delay)
        
        if device_path is None:
            logger.info(
                "Using simulated alphabit engine "
                "(hardware support coming soon)"
            )
        else:
            logger.info(f"Initializing hardware device at {device_path}")
            # TODO: Initialize actual hardware device
    
    def load_pattern(self, pattern_id: int, pattern: str) -> None:
        """
        Load a pattern into the SPU engine.
        
        Args:
            pattern_id: Unique identifier for the pattern
            pattern: Regex pattern string
            
        Raises:
            ValueError: If pattern is invalid or pattern_id is negative
            TypeError: If pattern is not a string
        """
        self.hw.load_pattern(pattern_id, pattern)
    
    def unload_pattern(self, pattern_id: int) -> bool:
        """
        Unload a pattern from the SPU engine.
        
        Args:
            pattern_id: Pattern identifier to remove
            
        Returns:
            True if pattern was removed, False if it didn't exist
        """
        return self.hw.unload_pattern(pattern_id)
    
    def clear_patterns(self) -> None:
        """Clear all loaded patterns from the SPU engine."""
        self.hw.clear_patterns()
    
    def scan(
        self,
        text: Union[str, bytes],
        pattern_ids: Optional[Iterable[int]] = None
    ) -> List[MatchResult]:
        """
        Scan text for patterns using the SPU engine.
        
        Args:
            text: Text to scan (string or bytes)
            pattern_ids: Iterable of pattern IDs to search. If None,
                        searches all loaded patterns.
        
        Returns:
            List of tuples (pattern_id, start, end) for each match
        """
        return self.hw.scan(text, pattern_ids)
    
    def __enter__(self) -> 'SPU':
        """Context manager entry."""
        return self
    
    def __exit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[Exception],
        exc_tb: Optional[object]
    ) -> bool:
        """
        Context manager exit - cleanup resources.
        
        Returns:
            False to allow exceptions to propagate
        """
        self.clear_patterns()
        return False
    
    def __len__(self) -> int:
        """Return the number of loaded patterns."""
        return len(self.hw)
    
    def __contains__(self, pattern_id: int) -> bool:
        """Check if a pattern ID is loaded."""
        return pattern_id in self.hw

# ============================================================================
# Quick scan function - Convenience API
# ============================================================================

def _get_scan_spu() -> SPU:
    """
    Get or create the shared SPU instance for quick scan function.
    
    Uses thread-safe singleton pattern with double-checked locking.
    
    Returns:
        Shared SPU instance (never None)
    """
    global _scan_spu
    
    if _scan_spu is None:
        with _scan_spu_lock:
            # Double-check after acquiring lock
            if _scan_spu is None:
                _scan_spu = SPU(simulate_delay=False)
    
    return _scan_spu


def _get_pattern_id(pattern: str) -> Tuple[int, SPU]:
    """
    Get or assign a pattern ID for the given pattern.
    
    Thread-safe pattern ID management with LRU caching.
    Returns both pattern_id and SPU instance to avoid double lookup.
    
    Args:
        pattern: Regex pattern string
        
    Returns:
        Tuple of (pattern_id, spu_instance)
        
    Raises:
        ValueError: If pattern is invalid regex
    """
    global _loaded_patterns, _pattern_counter, _pattern_id_to_pattern
    
    # Fast path: pattern already loaded
    if pattern in _loaded_patterns:
        # Move to end (mark as recently used)
        _loaded_patterns.move_to_end(pattern)
        return _loaded_patterns[pattern], _get_scan_spu()
    
    # Slow path: need to load pattern
    with _pattern_counter_lock:
        # Double-check after acquiring lock
        if pattern in _loaded_patterns:
            _loaded_patterns.move_to_end(pattern)
            return _loaded_patterns[pattern], _get_scan_spu()
        
        # Check if we need to reset counter
        if _pattern_counter >= MAX_PATTERN_ID:
            # Reset counter and clear cache to prevent memory leaks
            logger.warning(
                f"Pattern counter reached {MAX_PATTERN_ID}, "
                "resetting cache to prevent memory leaks"
            )
            _pattern_counter = 0
            _loaded_patterns.clear()
            _pattern_id_to_pattern.clear()
            # Also clear the SPU patterns
            _get_scan_spu().clear_patterns()
        
        # Assign new pattern ID
        pattern_id = _pattern_counter
        _pattern_counter += 1
        _loaded_patterns[pattern] = pattern_id
        _pattern_id_to_pattern[pattern_id] = pattern
        _loaded_patterns.move_to_end(pattern)  # Mark as recently used
        
        # LRU eviction: remove least recently used if cache is full
        if len(_loaded_patterns) > MAX_CACHED_PATTERNS:
            # Remove least recently used (first item in OrderedDict)
            oldest_pattern = next(iter(_loaded_patterns))
            oldest_pattern_id = _loaded_patterns[oldest_pattern]
            del _loaded_patterns[oldest_pattern]
            del _pattern_id_to_pattern[oldest_pattern_id]
            # Also unload from SPU
            _get_scan_spu().unload_pattern(oldest_pattern_id)
        
        # Load pattern into SPU
        spu = _get_scan_spu()
        spu.load_pattern(pattern_id, pattern)
        
        return pattern_id, spu


def scan(text: str, pattern: str) -> List[QuickMatch]:
    """
    Quick scan function using the alphabit SPU engine.
    
    This is a convenience function for simple pattern matching use cases.
    It uses a shared SPU instance and automatically caches patterns for
    efficiency. For advanced use cases or multi-threaded applications,
    consider creating your own SPU instance.
    
    Args:
        text: Text to scan (must be a string, not bytes)
        pattern: Regex pattern string to search for
        
    Returns:
        List of tuples (start, end) for each match found.
        Results are ordered by position in text.
        
    Raises:
        ValueError: If pattern is empty or invalid regex
        TypeError: If text is not a string
        
    Example:
        >>> scan("hello world", r"\\w+")
        [(0, 5), (6, 11)]
        
        >>> scan("The price is $99.99", r"\\$\\d+\\.\\d{2}")
        [(12, 18)]
    """
    # Fast path: empty text
    if not text:
        return []
    
    # Validate input types
    if not isinstance(text, str):
        raise TypeError(
            f"text must be a string, got {type(text).__name__}"
        )
    
    if not pattern:
        raise ValueError("pattern cannot be empty")
    
    # Get pattern ID and SPU instance (optimized single call)
    pattern_id, spu = _get_pattern_id(pattern)
    
    # Scan using SPU engine
    results = spu.scan(text, [pattern_id])
    
    # Extract (start, end) tuples, dropping pattern_id
    return [(start, end) for _, start, end in results]
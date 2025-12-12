"""
Progress bar utilities using tqdm.
"""
from tqdm import tqdm
from typing import Iterable, Any


class ProgressBar:
    """Wrapper for tqdm progress bar."""
    
    @staticmethod
    def create(iterable: Iterable, desc: str = "", total: int = None) -> tqdm:
        """
        Create a progress bar.
        
        Args:
            iterable: Iterable to wrap
            desc: Description to display
            total: Total number of items
            
        Returns:
            tqdm: Progress bar object
        """
        return tqdm(iterable, desc=desc, total=total, ncols=80, 
                   bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]')
    
    @staticmethod
    def create_manual(total: int, desc: str = "") -> tqdm:
        """
        Create a manual progress bar (no iterable).
        
        Args:
            total: Total number of items
            desc: Description to display
            
        Returns:
            tqdm: Progress bar object
        """
        return tqdm(total=total, desc=desc, ncols=80,
                   bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]')

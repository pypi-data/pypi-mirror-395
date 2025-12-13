"""
Game state module for grid-based board games.
Represents the complete state of a game at any point in time.

This is a generic GameState for grid-based games (Tic-Tac-Toe, Connect Four, Gomoku, Chess, etc.)
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
import copy


@dataclass
class GameState:
    """Generic representation of grid-based game state for API responses."""

    # Core state
    board: List[List[str]]
    current_player: str
    status: str  # 'active', 'won', 'draw'
    winner: Optional[str] = None

    # Game tracking
    turn_number: int = 0
    move_history: List[Dict[str, Any]] = field(default_factory=list)
    available_moves: List[Tuple[int, int]] = field(default_factory=list)

    # Game configuration
    game_mode: str = 'human_vs_human'
    game_id: Optional[str] = None

    # Win information
    winning_line: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert game state to dictionary for serialization.

        Returns:
            Dictionary representation of game state
        """
        return {
            'board': copy.deepcopy(self.board),
            'current_player': self.current_player,
            'status': self.status,
            'winner': self.winner,
            'turn_number': self.turn_number,
            'move_history': copy.deepcopy(self.move_history),
            'available_moves': list(self.available_moves),
            'game_mode': self.game_mode,
            'game_id': self.game_id,
            'winning_line': copy.deepcopy(self.winning_line) if self.winning_line else None
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GameState':
        """Create GameState from dictionary.

        Args:
            data: Dictionary containing game state fields

        Returns:
            New GameState instance
        """
        return cls(
            board=data.get('board', []),
            current_player=data.get('current_player', 'X'),
            status=data.get('status', 'active'),
            winner=data.get('winner'),
            turn_number=data.get('turn_number', 0),
            move_history=data.get('move_history', []),
            available_moves=data.get('available_moves', []),
            game_mode=data.get('game_mode', 'human_vs_human'),
            game_id=data.get('game_id'),
            winning_line=data.get('winning_line')
        )

    def copy(self) -> 'GameState':
        """Create a deep copy of the game state.

        Returns:
            New GameState instance with same values
        """
        return GameState(
            board=copy.deepcopy(self.board),
            current_player=self.current_player,
            status=self.status,
            winner=self.winner,
            turn_number=self.turn_number,
            move_history=copy.deepcopy(self.move_history),
            available_moves=list(self.available_moves),
            game_mode=self.game_mode,
            game_id=self.game_id,
            winning_line=copy.deepcopy(self.winning_line) if self.winning_line else None
        )

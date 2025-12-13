"""
Data models for the Paircraft API SDK.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class Tournament:
    """Represents a chess tournament."""
    
    id: str
    name: str
    format: str = "swiss"
    rounds: int = 5
    status: str = "created"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    location: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    time_control: Optional[str] = None
    sections: List[str] = field(default_factory=lambda: ["Open"])
    player_count: int = 0
    is_public: bool = True
    uscf_rated: bool = True
    fide_rated: bool = False
    prize_fund: float = 0.0
    organization_name: Optional[str] = None
    organization_slug: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> "Tournament":
        """Create a Tournament from API response data."""
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            format=data.get("format", "swiss"),
            rounds=data.get("rounds", 5),
            status=data.get("status", "created"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            location=data.get("location"),
            city=data.get("city"),
            state=data.get("state"),
            time_control=data.get("time_control"),
            sections=data.get("sections", ["Open"]),
            player_count=data.get("player_count", 0),
            is_public=data.get("is_public", True),
            uscf_rated=data.get("uscf_rated", True),
            fide_rated=data.get("fide_rated", False),
            prize_fund=data.get("prize_fund", 0.0),
            organization_name=data.get("organization_name"),
            organization_slug=data.get("organization_slug"),
        )


@dataclass
class Player:
    """Represents a player in a tournament."""
    
    id: str
    name: str
    rating: int = 0
    section: str = "Open"
    status: str = "active"
    uscf_id: Optional[str] = None
    fide_id: Optional[str] = None
    lichess_username: Optional[str] = None
    chesscom_username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    total_points: float = 0.0
    games_played: int = 0
    
    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        """Create a Player from API response data."""
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            rating=data.get("rating", 0),
            section=data.get("section", "Open"),
            status=data.get("status", "active"),
            uscf_id=data.get("uscf_id"),
            fide_id=data.get("fide_id"),
            lichess_username=data.get("lichess_username"),
            chesscom_username=data.get("chesscom_username"),
            email=data.get("email"),
            phone=data.get("phone"),
            total_points=data.get("total_points", 0.0),
            games_played=data.get("games_played", 0),
        )


@dataclass
class Pairing:
    """Represents a pairing between two players."""
    
    id: str
    round: int
    board: int
    white_player_id: str
    white_name: str
    white_rating: int = 0
    black_player_id: Optional[str] = None
    black_name: Optional[str] = None
    black_rating: int = 0
    result: Optional[str] = None
    section: str = "Open"
    
    @classmethod
    def from_dict(cls, data: dict) -> "Pairing":
        """Create a Pairing from API response data."""
        return cls(
            id=data.get("id", ""),
            round=data.get("round", 1),
            board=data.get("board", 1),
            white_player_id=data.get("white_player_id", ""),
            white_name=data.get("white_name", ""),
            white_rating=data.get("white_rating", 0),
            black_player_id=data.get("black_player_id"),
            black_name=data.get("black_name"),
            black_rating=data.get("black_rating", 0),
            result=data.get("result"),
            section=data.get("section", "Open"),
        )
    
    @property
    def is_bye(self) -> bool:
        """Check if this pairing is a bye."""
        return self.black_player_id is None or self.black_name is None


@dataclass
class Standing:
    """Represents a player's standing in a tournament."""
    
    rank: int
    player_id: str
    name: str
    rating: int = 0
    section: str = "Open"
    total_points: float = 0.0
    games_played: int = 0
    wins: int = 0
    losses: int = 0
    draws: int = 0
    tiebreakers: Dict[str, float] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: dict) -> "Standing":
        """Create a Standing from API response data."""
        return cls(
            rank=data.get("rank", 0),
            player_id=data.get("id", ""),
            name=data.get("name", ""),
            rating=data.get("rating", 0),
            section=data.get("section", "Open"),
            total_points=data.get("total_points", 0.0),
            games_played=data.get("games_played", 0),
            wins=data.get("wins", 0),
            losses=data.get("losses", 0),
            draws=data.get("draws", 0),
            tiebreakers=data.get("tiebreakers", {}),
        )


@dataclass
class Prize:
    """Represents a prize winner."""
    
    player_id: str
    player_name: str
    player_rating: int = 0
    position: int = 1
    prize_name: str = ""
    prize_type: str = "place"
    amount: Optional[float] = None
    is_pooled: bool = False
    tie_group: Optional[int] = None
    total_points: float = 0.0
    
    @classmethod
    def from_dict(cls, data: dict) -> "Prize":
        """Create a Prize from API response data."""
        return cls(
            player_id=data.get("player_id", ""),
            player_name=data.get("player_name", ""),
            player_rating=data.get("player_rating", 0),
            position=data.get("position", 1),
            prize_name=data.get("prize_name", ""),
            prize_type=data.get("prize_type", "place"),
            amount=data.get("amount"),
            is_pooled=data.get("is_pooled", False),
            tie_group=data.get("tie_group"),
            total_points=data.get("total_points", 0.0),
        )


@dataclass
class Section:
    """Represents a tournament section with its prize winners."""
    
    name: str
    winners: List[Prize] = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, data: dict) -> "Section":
        """Create a Section from API response data."""
        return cls(
            name=data.get("name", "Open"),
            winners=[Prize.from_dict(w) for w in data.get("winners", [])],
        )


@dataclass
class RoundStatus:
    """Represents the status of a round."""
    
    round: int
    total_games: int
    completed_games: int
    pending_games: int
    is_complete: bool
    completion_percentage: int
    
    @classmethod
    def from_dict(cls, data: dict) -> "RoundStatus":
        """Create a RoundStatus from API response data."""
        return cls(
            round=data.get("round", 1),
            total_games=data.get("total_games", 0),
            completed_games=data.get("completed_games", 0),
            pending_games=data.get("pending_games", 0),
            is_complete=data.get("is_complete", False),
            completion_percentage=data.get("completion_percentage", 0),
        )


@dataclass
class PaginatedResponse:
    """Represents a paginated API response."""
    
    items: List[Any]
    page: int = 1
    limit: int = 50
    total: int = 0
    total_pages: int = 1
    has_more: bool = False
    has_previous: bool = False
    
    @classmethod
    def from_response(cls, data: dict, items: List[Any]) -> "PaginatedResponse":
        """Create a PaginatedResponse from API response data."""
        pagination = data.get("pagination", {})
        return cls(
            items=items,
            page=pagination.get("page", 1),
            limit=pagination.get("limit", 50),
            total=pagination.get("total", len(items)),
            total_pages=pagination.get("totalPages", 1),
            has_more=pagination.get("hasMore", False),
            has_previous=pagination.get("hasPrevious", False),
        )

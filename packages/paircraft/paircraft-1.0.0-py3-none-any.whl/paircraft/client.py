"""
Main client for the Paircraft API SDK.
"""

import requests
from typing import Optional, List, Dict, Any, Union
from urllib.parse import urljoin

from .exceptions import raise_for_error, NetworkError
from .models import (
    Tournament,
    Player,
    Pairing,
    Standing,
    Section,
    RoundStatus,
    PaginatedResponse,
)


DEFAULT_BASE_URL = "https://chess-tournament-director-6ce5e76147d7.herokuapp.com"
API_VERSION = "v1"


class BaseResource:
    """Base class for API resources."""
    
    def __init__(self, client: "ChessTournamentClient"):
        self._client = client
    
    def _request(
        self,
        method: str,
        endpoint: str,
        params: dict = None,
        json: dict = None,
        **kwargs
    ) -> dict:
        """Make an API request."""
        return self._client._request(method, endpoint, params=params, json=json, **kwargs)


class TournamentsResource(BaseResource):
    """API resource for tournament operations."""
    
    def list(
        self,
        page: int = 1,
        limit: int = 50,
        search: str = None,
        status: str = None,
        format: str = None,
    ) -> PaginatedResponse:
        """
        List tournaments.
        
        Args:
            page: Page number (default: 1)
            limit: Results per page (default: 50, max: 100)
            search: Search by tournament name
            status: Filter by status (created, in_progress, completed)
            format: Filter by format (swiss, round_robin)
        
        Returns:
            PaginatedResponse containing Tournament objects
        """
        params = {"page": page, "limit": limit}
        if search:
            params["search"] = search
        if status:
            params["status"] = status
        if format:
            params["format"] = format
        
        response = self._request("GET", "/tournaments", params=params)
        tournaments = [Tournament.from_dict(t) for t in response.get("data", [])]
        return PaginatedResponse.from_response(response, tournaments)
    
    def get(self, tournament_id: str) -> Tournament:
        """
        Get a tournament by ID.
        
        Args:
            tournament_id: The tournament UUID
        
        Returns:
            Tournament object
        """
        response = self._request("GET", f"/tournaments/{tournament_id}")
        return Tournament.from_dict(response.get("data", {}))
    
    def create(
        self,
        name: str,
        date: str = None,
        rounds: int = 5,
        time_control: str = None,
        location: str = None,
        format: str = "swiss",
        sections: List[str] = None,
        **kwargs
    ) -> Tournament:
        """
        Create a new tournament.
        
        Args:
            name: Tournament name
            date: Start date (YYYY-MM-DD)
            rounds: Number of rounds (default: 5)
            time_control: Time control string (e.g., "G/60+5")
            location: Venue/location name
            format: Tournament format (swiss or round_robin)
            sections: List of section names
            **kwargs: Additional tournament properties
        
        Returns:
            Created Tournament object
        """
        data = {
            "name": name,
            "rounds": rounds,
            "format": format,
        }
        if date:
            data["date"] = date
        if time_control:
            data["time_control"] = time_control
        if location:
            data["location"] = location
        if sections:
            data["sections"] = sections
        data.update(kwargs)
        
        response = self._request("POST", "/tournaments", json=data)
        return Tournament.from_dict(response.get("data", {}))
    
    def update(self, tournament_id: str, **kwargs) -> Tournament:
        """
        Update a tournament.
        
        Args:
            tournament_id: The tournament UUID
            **kwargs: Fields to update
        
        Returns:
            Updated Tournament object
        """
        response = self._request("PUT", f"/tournaments/{tournament_id}", json=kwargs)
        return Tournament.from_dict(response.get("data", {}))
    
    def delete(self, tournament_id: str) -> bool:
        """
        Delete a tournament.
        
        Args:
            tournament_id: The tournament UUID
        
        Returns:
            True if successful
        """
        self._request("DELETE", f"/tournaments/{tournament_id}")
        return True
    
    def standings(
        self,
        tournament_id: str,
        section: str = None,
        round: int = None
    ) -> Dict[str, List[Standing]]:
        """
        Get tournament standings.
        
        Args:
            tournament_id: The tournament UUID
            section: Filter by section name
            round: Get standings as of specific round
        
        Returns:
            Dictionary mapping section names to lists of Standing objects
        """
        params = {}
        if section:
            params["section"] = section
        if round:
            params["round"] = round
        
        response = self._request("GET", f"/tournaments/{tournament_id}/standings", params=params)
        data = response.get("data", {})
        standings_data = data.get("standings", {})
        
        result = {}
        for section_name, players in standings_data.items():
            result[section_name] = [Standing.from_dict(p) for p in players]
        
        return result
    
    def prizes(
        self,
        tournament_id: str,
        section: str = None,
        calculate: bool = False
    ) -> Dict[str, Any]:
        """
        Get prize winners for a tournament.
        
        Args:
            tournament_id: The tournament UUID
            section: Filter by section name
            calculate: Recalculate prizes from current standings
        
        Returns:
            Prize data with sections and winners
        """
        params = {}
        if section:
            params["section"] = section
        if calculate:
            params["calculate"] = "true"
        
        response = self._request("GET", f"/tournaments/{tournament_id}/prizes", params=params)
        data = response.get("data", {})
        
        # Parse sections
        sections = [Section.from_dict(s) for s in data.get("sections", [])]
        
        return {
            "tournament_id": data.get("tournament_id"),
            "tournament_name": data.get("tournament_name"),
            "total_rounds": data.get("total_rounds"),
            "prize_fund": data.get("prize_fund", 0),
            "sections": sections,
            "summary": data.get("summary", {}),
        }
    
    def calculate_prizes(
        self,
        tournament_id: str,
        prize_fund: float = None,
        sections: List[dict] = None
    ) -> Dict[str, Any]:
        """
        Calculate and assign prizes for a tournament.
        
        Args:
            tournament_id: The tournament UUID
            prize_fund: Total prize fund amount
            sections: Custom prize configuration per section
        
        Returns:
            Prize distribution data
        """
        data = {}
        if prize_fund is not None:
            data["prize_fund"] = prize_fund
        if sections:
            data["sections"] = sections
        
        response = self._request("POST", f"/tournaments/{tournament_id}/prizes/calculate", json=data)
        return response.get("data", {})


class PlayersResource(BaseResource):
    """API resource for player operations."""
    
    def list(
        self,
        tournament_id: str,
        page: int = 1,
        limit: int = 50,
        section: str = None,
        status: str = None,
    ) -> PaginatedResponse:
        """
        List players in a tournament.
        
        Args:
            tournament_id: The tournament UUID
            page: Page number
            limit: Results per page
            section: Filter by section
            status: Filter by status (active, withdrawn, inactive)
        
        Returns:
            PaginatedResponse containing Player objects
        """
        params = {"page": page, "limit": limit}
        if section:
            params["section"] = section
        if status:
            params["status"] = status
        
        response = self._request("GET", f"/tournaments/{tournament_id}/players", params=params)
        players = [Player.from_dict(p) for p in response.get("data", [])]
        return PaginatedResponse.from_response(response, players)
    
    def get(self, tournament_id: str, player_id: str) -> Player:
        """
        Get a player by ID.
        
        Args:
            tournament_id: The tournament UUID
            player_id: The player UUID
        
        Returns:
            Player object
        """
        response = self._request("GET", f"/tournaments/{tournament_id}/players/{player_id}")
        return Player.from_dict(response.get("data", {}))
    
    def add(
        self,
        tournament_id: str,
        player: Union[dict, List[dict]]
    ) -> Union[Player, List[Player]]:
        """
        Add one or more players to a tournament.
        
        Args:
            tournament_id: The tournament UUID
            player: Single player dict or list of player dicts
        
        Returns:
            Player object or list of Player objects
        """
        if isinstance(player, list):
            return self.import_players(tournament_id, player)
        
        response = self._request("POST", f"/tournaments/{tournament_id}/players", json=player)
        return Player.from_dict(response.get("data", {}))
    
    def import_players(self, tournament_id: str, players: List[dict]) -> Dict[str, Any]:
        """
        Import multiple players to a tournament.
        
        Args:
            tournament_id: The tournament UUID
            players: List of player dictionaries
        
        Returns:
            Import result with counts and any errors
        """
        response = self._request(
            "POST",
            f"/tournaments/{tournament_id}/players/import",
            json={"players": players}
        )
        return response.get("data", {})
    
    def update(self, tournament_id: str, player_id: str, **kwargs) -> Player:
        """
        Update a player.
        
        Args:
            tournament_id: The tournament UUID
            player_id: The player UUID
            **kwargs: Fields to update
        
        Returns:
            Updated Player object
        """
        response = self._request(
            "PUT",
            f"/tournaments/{tournament_id}/players/{player_id}",
            json=kwargs
        )
        return Player.from_dict(response.get("data", {}))
    
    def delete(self, tournament_id: str, player_id: str) -> bool:
        """
        Remove a player from a tournament.
        
        Args:
            tournament_id: The tournament UUID
            player_id: The player UUID
        
        Returns:
            True if successful
        """
        self._request("DELETE", f"/tournaments/{tournament_id}/players/{player_id}")
        return True
    
    def withdraw(self, tournament_id: str, player_id: str) -> Player:
        """
        Withdraw a player from a tournament.
        
        Args:
            tournament_id: The tournament UUID
            player_id: The player UUID
        
        Returns:
            Updated Player object
        """
        return self.update(tournament_id, player_id, status="withdrawn")


class PairingsResource(BaseResource):
    """API resource for pairing operations."""
    
    def list(
        self,
        tournament_id: str,
        round: int = None,
        section: str = None
    ) -> List[Pairing]:
        """
        Get pairings for a tournament.
        
        Args:
            tournament_id: The tournament UUID
            round: Filter by round number
            section: Filter by section
        
        Returns:
            List of Pairing objects
        """
        params = {}
        if round:
            params["round"] = round
        if section:
            params["section"] = section
        
        response = self._request("GET", f"/tournaments/{tournament_id}/pairings", params=params)
        return [Pairing.from_dict(p) for p in response.get("data", [])]
    
    def generate(
        self,
        tournament_id: str,
        round: int,
        section: str = None,
        algorithm: str = "dutch"
    ) -> List[Pairing]:
        """
        Generate pairings for a round.
        
        Args:
            tournament_id: The tournament UUID
            round: Round number to generate
            section: Section to pair (optional, pairs all sections if not specified)
            algorithm: Pairing algorithm (dutch, burstein)
        
        Returns:
            List of generated Pairing objects
        """
        data = {"round": round, "algorithm": algorithm}
        if section:
            data["section"] = section
        
        response = self._request(
            "POST",
            f"/tournaments/{tournament_id}/pairings/generate",
            json=data
        )
        pairings_data = response.get("data", {}).get("pairings", [])
        return [Pairing.from_dict(p) for p in pairings_data]
    
    def set_result(
        self,
        tournament_id: str,
        pairing_id: str,
        result: str
    ) -> Dict[str, Any]:
        """
        Set the result for a pairing.
        
        Args:
            tournament_id: The tournament UUID
            pairing_id: The pairing UUID
            result: Result string (1-0, 0-1, 1/2-1/2, etc.)
        
        Returns:
            Updated pairing data
        """
        response = self._request(
            "PUT",
            f"/tournaments/{tournament_id}/pairings/{pairing_id}/result",
            json={"result": result}
        )
        return response.get("data", {})
    
    def set_results(
        self,
        tournament_id: str,
        results: List[dict]
    ) -> Dict[str, Any]:
        """
        Set results for multiple pairings.
        
        Args:
            tournament_id: The tournament UUID
            results: List of {"pairing_id": str, "result": str} dicts
        
        Returns:
            Batch result with counts and any errors
        """
        response = self._request(
            "POST",
            f"/tournaments/{tournament_id}/results/batch",
            json={"results": results}
        )
        return response.get("data", {})
    
    def round_status(self, tournament_id: str, round: int) -> RoundStatus:
        """
        Get the status of a round.
        
        Args:
            tournament_id: The tournament UUID
            round: Round number
        
        Returns:
            RoundStatus object
        """
        response = self._request("GET", f"/tournaments/{tournament_id}/rounds/{round}/status")
        return RoundStatus.from_dict(response.get("data", {}))


class ChessTournamentClient:
    """
    Main client for the Paircraft API.
    
    Usage:
        client = ChessTournamentClient(api_key="your-api-key")
        tournaments = client.tournaments.list()
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = 30,
    ):
        """
        Initialize the client.
        
        Args:
            api_key: Your API key
            base_url: API base URL (default: production server)
            timeout: Request timeout in seconds (default: 30)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        
        # Initialize resources
        self.tournaments = TournamentsResource(self)
        self.players = PlayersResource(self)
        self.pairings = PairingsResource(self)
    
    def _get_url(self, endpoint: str) -> str:
        """Build full URL for an endpoint."""
        endpoint = endpoint.lstrip("/")
        return f"{self.base_url}/api/{API_VERSION}/{endpoint}"
    
    def _get_headers(self) -> dict:
        """Get request headers."""
        return {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    
    def _request(
        self,
        method: str,
        endpoint: str,
        params: dict = None,
        json: dict = None,
        **kwargs
    ) -> dict:
        """
        Make an API request.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (e.g., "/tournaments")
            params: Query parameters
            json: JSON body data
            **kwargs: Additional request arguments
        
        Returns:
            Response JSON data
        
        Raises:
            APIError: On API errors
            NetworkError: On network errors
        """
        url = self._get_url(endpoint)
        headers = self._get_headers()
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json,
                timeout=self.timeout,
                **kwargs
            )
        except requests.exceptions.Timeout:
            raise NetworkError("Request timed out", code="TIMEOUT")
        except requests.exceptions.ConnectionError:
            raise NetworkError("Connection failed", code="CONNECTION_ERROR")
        except requests.exceptions.RequestException as e:
            raise NetworkError(str(e), code="REQUEST_ERROR")
        
        try:
            data = response.json()
        except ValueError:
            if response.status_code >= 400:
                raise_for_error(
                    {"error": response.text or "Unknown error"},
                    response.status_code
                )
            return {}
        
        if not response.ok or not data.get("success", True):
            raise_for_error(data, response.status_code)
        
        return data
    
    def health_check(self) -> bool:
        """
        Check if the API is available.
        
        Returns:
            True if the API is healthy
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/{API_VERSION}/health",
                timeout=5
            )
            return response.ok
        except Exception:
            return False

"""
Tests for the Paircraft API SDK.
"""

import pytest
from unittest.mock import Mock, patch

from paircraft import (
    ChessTournamentClient,
    Tournament,
    Player,
    Pairing,
    Standing,
)
from paircraft.exceptions import (
    AuthenticationError,
    NotFoundError,
    ValidationError,
)


@pytest.fixture
def client():
    """Create a test client."""
    return ChessTournamentClient(api_key="test-api-key-full-access")


@pytest.fixture
def mock_response():
    """Create a mock response factory."""
    def _make_response(data, success=True, status_code=200):
        response = Mock()
        response.ok = status_code < 400
        response.status_code = status_code
        response.json.return_value = {"success": success, "data": data}
        return response
    return _make_response


class TestTournamentModel:
    """Tests for Tournament model."""
    
    def test_from_dict(self):
        data = {
            "id": "test-id",
            "name": "Test Tournament",
            "format": "swiss",
            "rounds": 5,
            "status": "created",
        }
        tournament = Tournament.from_dict(data)
        assert tournament.id == "test-id"
        assert tournament.name == "Test Tournament"
        assert tournament.format == "swiss"
        assert tournament.rounds == 5


class TestPlayerModel:
    """Tests for Player model."""
    
    def test_from_dict(self):
        data = {
            "id": "player-id",
            "name": "John Doe",
            "rating": 1500,
            "section": "Open",
        }
        player = Player.from_dict(data)
        assert player.id == "player-id"
        assert player.name == "John Doe"
        assert player.rating == 1500


class TestPairingModel:
    """Tests for Pairing model."""
    
    def test_from_dict(self):
        data = {
            "id": "pairing-id",
            "round": 1,
            "board": 1,
            "white_player_id": "white-id",
            "white_name": "White Player",
            "black_player_id": "black-id",
            "black_name": "Black Player",
        }
        pairing = Pairing.from_dict(data)
        assert pairing.id == "pairing-id"
        assert pairing.round == 1
        assert not pairing.is_bye
    
    def test_is_bye(self):
        data = {
            "id": "pairing-id",
            "round": 1,
            "board": 1,
            "white_player_id": "white-id",
            "white_name": "White Player",
            "black_player_id": None,
            "black_name": None,
        }
        pairing = Pairing.from_dict(data)
        assert pairing.is_bye


class TestClient:
    """Tests for ChessTournamentClient."""
    
    def test_initialization(self, client):
        assert client.api_key == "test-api-key-full-access"
        assert client.tournaments is not None
        assert client.players is not None
        assert client.pairings is not None
    
    def test_get_url(self, client):
        url = client._get_url("/tournaments")
        assert url == f"{client.base_url}/api/v1/tournaments"
    
    def test_get_headers(self, client):
        headers = client._get_headers()
        assert headers["X-API-Key"] == "test-api-key-full-access"
        assert headers["Content-Type"] == "application/json"


class TestTournamentsResource:
    """Tests for tournaments resource."""
    
    @patch("requests.request")
    def test_list(self, mock_request, client, mock_response):
        mock_request.return_value = mock_response([
            {"id": "1", "name": "Tournament 1"},
            {"id": "2", "name": "Tournament 2"},
        ])
        
        result = client.tournaments.list()
        assert len(result.items) == 2
        assert result.items[0].name == "Tournament 1"
    
    @patch("requests.request")
    def test_get(self, mock_request, client, mock_response):
        mock_request.return_value = mock_response({
            "id": "test-id",
            "name": "Test Tournament",
        })
        
        tournament = client.tournaments.get("test-id")
        assert tournament.id == "test-id"
        assert tournament.name == "Test Tournament"
    
    @patch("requests.request")
    def test_create(self, mock_request, client, mock_response):
        mock_request.return_value = mock_response({
            "id": "new-id",
            "name": "New Tournament",
            "rounds": 5,
        })
        
        tournament = client.tournaments.create(
            name="New Tournament",
            rounds=5,
        )
        assert tournament.id == "new-id"
        assert tournament.name == "New Tournament"


class TestPlayersResource:
    """Tests for players resource."""
    
    @patch("requests.request")
    def test_list(self, mock_request, client, mock_response):
        mock_request.return_value = mock_response([
            {"id": "p1", "name": "Player 1"},
            {"id": "p2", "name": "Player 2"},
        ])
        
        result = client.players.list("tournament-id")
        assert len(result.items) == 2
    
    @patch("requests.request")
    def test_add(self, mock_request, client, mock_response):
        mock_request.return_value = mock_response({
            "id": "new-player",
            "name": "New Player",
            "rating": 1500,
        })
        
        player = client.players.add("tournament-id", {
            "name": "New Player",
            "rating": 1500,
        })
        assert player.name == "New Player"


class TestPairingsResource:
    """Tests for pairings resource."""
    
    @patch("requests.request")
    def test_generate(self, mock_request, client, mock_response):
        mock_request.return_value = mock_response({
            "round": 1,
            "pairings": [
                {"id": "pair1", "round": 1, "board": 1, "white_player_id": "w1", "white_name": "White"},
            ]
        })
        
        pairings = client.pairings.generate("tournament-id", round=1)
        assert len(pairings) == 1
        assert pairings[0].round == 1
    
    @patch("requests.request")
    def test_set_result(self, mock_request, client, mock_response):
        mock_request.return_value = mock_response({
            "pairing_id": "pair1",
            "result": "1-0",
        })
        
        result = client.pairings.set_result("tournament-id", "pair1", "1-0")
        assert result["result"] == "1-0"


class TestExceptions:
    """Tests for exception handling."""
    
    @patch("requests.request")
    def test_authentication_error(self, mock_request, client):
        response = Mock()
        response.ok = False
        response.status_code = 401
        response.json.return_value = {
            "success": False,
            "error": "Invalid API key",
            "code": "UNAUTHORIZED",
        }
        mock_request.return_value = response
        
        with pytest.raises(AuthenticationError):
            client.tournaments.list()
    
    @patch("requests.request")
    def test_not_found_error(self, mock_request, client):
        response = Mock()
        response.ok = False
        response.status_code = 404
        response.json.return_value = {
            "success": False,
            "error": "Tournament not found",
            "code": "NOT_FOUND",
        }
        mock_request.return_value = response
        
        with pytest.raises(NotFoundError):
            client.tournaments.get("invalid-id")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

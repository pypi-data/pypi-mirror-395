"""
Tests for the OpenAPI/Swagger documentation.
"""

import unittest

# Import the Flask app from the API Gateway
import fogis_api_gateway


class TestSwagger(unittest.TestCase):
    """Test case for the Swagger documentation."""

    def setUp(self):
        """Set up the test case."""
        # Create a test client
        self.app = fogis_api_gateway.app
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def test_swagger_json_endpoint(self):
        """Test the /api/swagger.json endpoint."""
        # Call the endpoint
        response = self.client.get("/api/swagger.json")

        # Verify the response
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, dict)

        # Check that the OpenAPI version is correct
        self.assertEqual(response.json["openapi"], "3.0.2")

        # Check that the title is correct
        self.assertEqual(response.json["info"]["title"], "FOGIS API Gateway")

        # Check that the paths are defined
        self.assertIn("paths", response.json)
        self.assertIsInstance(response.json["paths"], dict)

        # Check that the components are defined
        self.assertIn("components", response.json)
        self.assertIn("schemas", response.json["components"])

        # Check that all required schemas are defined
        required_schemas = ["Error", "Match", "MatchResult", "Event", "Player", "Official"]
        for schema in required_schemas:
            self.assertIn(schema, response.json["components"]["schemas"])

        # Check that all endpoints are documented
        required_paths = [
            "/",
            "/hello",
            "/matches",
            "/matches/filter",
            "/match/{match_id}",
            "/match/{match_id}/result",
            "/match/{match_id}/events",
            "/match/{match_id}/events/clear",
            "/match/{match_id}/officials",
            "/match/{match_id}/finish",
            "/team/{team_id}/players",
            "/team/{team_id}/officials",
        ]
        for path in required_paths:
            self.assertIn(path, response.json["paths"])

    def test_swagger_ui_endpoint(self):
        """Test the /api/docs endpoint."""
        # Call the endpoint
        response = self.client.get("/api/docs/")

        # Verify the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"swagger-ui", response.data)
        self.assertIn(b"html", response.data)


if __name__ == "__main__":
    unittest.main()

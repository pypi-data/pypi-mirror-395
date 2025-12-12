"""
Tests for Phase 3: JSON API Endpoints with Verification

This test suite validates the new JSON API endpoints that expose
organization reports with checksums and verification for programmatic access.

Endpoints tested:
- /api/reports/organizations - List all organizations
- /api/reports/organization/<name>/json - Full report with checksums
- /api/reports/organization/<name>/verification - Verification only
- /api/docs - API documentation

Phase: MVC Refactoring Phase 3
"""

import json
import unittest

from app import SHEET_DATA, app, load_sheet_data


class TestPhase3API(unittest.TestCase):
    """Test JSON API endpoints with verification"""

    @classmethod
    def setUpClass(cls):
        """Set up test client and load data once for all tests"""
        app.config["TESTING"] = True
        cls.client = app.test_client()

        # Load sheet data if not already loaded
        if not SHEET_DATA:
            print("Loading sheet data for tests...")
            load_sheet_data(verbose=False, use_cache=True)
            print(f"Loaded {len(SHEET_DATA)} sheets")

    def test_01_organizations_list(self):
        """Test organizations list endpoint returns valid JSON"""
        response = self.client.get("/api/reports/organizations")
        self.assertEqual(response.status_code, 200, "Organizations list should return 200 OK")

        # Parse JSON response
        data = json.loads(response.data)

        # Verify structure
        self.assertIn("organizations", data, "Response should contain 'organizations' key")
        self.assertIn(
            "total_organizations", data, "Response should contain 'total_organizations' key"
        )
        self.assertIn("api_version", data, "Response should contain 'api_version' key")
        self.assertIn("generated_at", data, "Response should contain 'generated_at' key")

        # Verify data
        self.assertIsInstance(data["organizations"], list, "Organizations should be a list")
        self.assertGreaterEqual(
            data["total_organizations"], 0, "Total organizations should be non-negative"
        )
        self.assertEqual(
            len(data["organizations"]),
            data["total_organizations"],
            "Organization count should match list length",
        )

        # Verify organization structure
        if data["total_organizations"] > 0:
            org = data["organizations"][0]
            self.assertIn("name", org, "Organization should have 'name' field")
            self.assertIn("report_url", org, "Organization should have 'report_url' field")
            self.assertIn("html_url", org, "Organization should have 'html_url' field")

            # Store first org for later tests
            self.__class__.test_org_name = org["name"]
            print(f"Using '{org['name']}' for subsequent tests")

    def test_02_organization_report_json(self):
        """Test organization report JSON endpoint returns complete report"""
        # Skip if no organizations available
        if not hasattr(self.__class__, "test_org_name"):
            self.skipTest("No organizations available for testing")

        org_name = self.__class__.test_org_name
        url_encoded_name = org_name.replace(" ", "%20")

        response = self.client.get(f"/api/reports/organization/{url_encoded_name}/json")
        self.assertEqual(
            response.status_code, 200, f"Organization report should return 200 OK for {org_name}"
        )

        # Parse JSON response
        data = json.loads(response.data)

        # Verify API metadata
        self.assertIn("api_metadata", data, "Report should contain 'api_metadata'")
        metadata = data["api_metadata"]
        self.assertIn("version", metadata, "Metadata should contain 'version'")
        self.assertIn("generated_at", metadata, "Metadata should contain 'generated_at'")
        self.assertTrue(
            metadata.get("checksums_included", False),
            "Metadata should indicate checksums are included",
        )
        self.assertTrue(
            metadata.get("verification_included", False),
            "Metadata should indicate verification is included",
        )
        self.assertEqual(
            metadata["organization"], org_name, "Metadata should include organization name"
        )

        # Verify report structure
        self.assertIn("maturity", data, "Report should contain 'maturity' data")
        self.assertIn("verification", data, "Report should contain 'verification' data")

        # Verify maturity data has checksums
        if "variance_analysis" in data["maturity"]:
            variance = data["maturity"]["variance_analysis"]
            self.assertIsInstance(variance, dict, "Variance analysis should be a dictionary")

            # Check at least one dimension has checksum
            has_checksum = False
            for dimension, analysis in variance.items():
                if "checksum" in analysis:
                    has_checksum = True
                    checksum_data = analysis["checksum"]
                    self.assertIn(
                        "checksum", checksum_data, "Checksum data should contain 'checksum' field"
                    )
                    self.assertIn(
                        "valid", checksum_data, "Checksum data should contain 'valid' field"
                    )
                    self.assertIn(
                        "calculation",
                        checksum_data,
                        "Checksum data should contain 'calculation' field",
                    )

            self.assertTrue(has_checksum, "At least one dimension should have checksum data")

        print(f"✓ Full report for '{org_name}' validated successfully")

    def test_03_verification_endpoint(self):
        """Test verification-only endpoint returns checksums"""
        # Skip if no organizations available
        if not hasattr(self.__class__, "test_org_name"):
            self.skipTest("No organizations available for testing")

        org_name = self.__class__.test_org_name
        url_encoded_name = org_name.replace(" ", "%20")

        response = self.client.get(f"/api/reports/organization/{url_encoded_name}/verification")
        self.assertEqual(
            response.status_code, 200, f"Verification endpoint should return 200 OK for {org_name}"
        )

        # Parse JSON response
        data = json.loads(response.data)

        # Verify structure
        self.assertIn("verification", data, "Response should contain 'verification' data")
        self.assertIn("organization", data, "Response should contain 'organization' name")
        self.assertIn("dimension_checksums", data, "Response should contain 'dimension_checksums'")
        self.assertIn("summary", data, "Response should contain 'summary'")

        # Verify organization name matches
        self.assertEqual(data["organization"], org_name, "Organization name should match request")

        # Verify checksums structure
        checksums = data["dimension_checksums"]
        self.assertIsInstance(checksums, dict, "Dimension checksums should be a dictionary")

        # Verify at least one checksum exists
        if len(checksums) > 0:
            first_dimension = list(checksums.keys())[0]
            first_checksum = checksums[first_dimension]

            self.assertIn("checksum", first_checksum, "Checksum should have 'checksum' field")
            self.assertIn("valid", first_checksum, "Checksum should have 'valid' field")
            self.assertIn("calculation", first_checksum, "Checksum should have 'calculation' field")
            self.assertIn("score", first_checksum, "Checksum should have 'score' field")

        # Verify summary
        summary = data["summary"]
        self.assertIn("total_dimensions", summary, "Summary should contain 'total_dimensions'")
        self.assertIn(
            "all_checksums_valid", summary, "Summary should contain 'all_checksums_valid'"
        )
        self.assertIn(
            "verification_passed", summary, "Summary should contain 'verification_passed'"
        )

        self.assertEqual(
            summary["total_dimensions"],
            len(checksums),
            "Summary dimension count should match checksums",
        )

        print(f"✓ Verification data for '{org_name}' validated successfully")
        print(f"  - {summary['total_dimensions']} dimensions checked")
        print(f"  - All checksums valid: {summary['all_checksums_valid']}")

    def test_04_api_docs(self):
        """Test API documentation endpoint"""
        response = self.client.get("/api/docs")
        self.assertEqual(response.status_code, 200, "API docs should return 200 OK")

        # Parse JSON response
        data = json.loads(response.data)

        # Verify structure
        self.assertIn("endpoints", data, "Docs should contain 'endpoints'")
        self.assertIn("features", data, "Docs should contain 'features'")
        self.assertIn("data_format", data, "Docs should contain 'data_format'")
        self.assertIn("error_responses", data, "Docs should contain 'error_responses'")
        self.assertIn("usage_examples", data, "Docs should contain 'usage_examples'")

        # Verify all documented endpoints exist
        endpoints = data["endpoints"]
        expected_endpoints = [
            "organizations_list",
            "organization_report",
            "organization_verification",
            "api_docs",
        ]

        for endpoint_name in expected_endpoints:
            self.assertIn(
                endpoint_name, endpoints, f"Docs should document '{endpoint_name}' endpoint"
            )

            endpoint_doc = endpoints[endpoint_name]
            self.assertIn("url", endpoint_doc, f"{endpoint_name} should have 'url'")
            self.assertIn("method", endpoint_doc, f"{endpoint_name} should have 'method'")
            self.assertIn("description", endpoint_doc, f"{endpoint_name} should have 'description'")

        # Verify usage examples
        examples = data["usage_examples"]
        self.assertIn("python", examples, "Should include Python examples")
        self.assertIn("curl", examples, "Should include curl examples")
        self.assertIn("javascript", examples, "Should include JavaScript examples")

        print("✓ API documentation validated successfully")

    def test_05_cors_headers(self):
        """Test CORS headers are present on API responses"""
        endpoints = ["/api/reports/organizations", "/api/docs"]

        for endpoint in endpoints:
            response = self.client.get(endpoint)
            self.assertIn(
                "Access-Control-Allow-Origin",
                response.headers,
                f"CORS header should be present on {endpoint}",
            )
            self.assertEqual(
                response.headers["Access-Control-Allow-Origin"],
                "*",
                f"CORS should allow all origins for {endpoint}",
            )

        print("✓ CORS headers validated on all endpoints")

    def test_06_404_organization(self):
        """Test 404 error for non-existent organization"""
        response = self.client.get("/api/reports/organization/NonExistentOrganization123/json")
        self.assertEqual(response.status_code, 404, "Non-existent organization should return 404")

        # Parse JSON response
        data = json.loads(response.data)
        self.assertIn("error", data, "Error response should contain 'error' field")
        self.assertEqual(
            data["error"],
            "Organization not found",
            "Error message should indicate organization not found",
        )

        print("✓ 404 error handling validated")

    def test_07_content_type(self):
        """Test Content-Type headers are correct"""
        endpoints = ["/api/reports/organizations", "/api/docs"]

        for endpoint in endpoints:
            response = self.client.get(endpoint)
            content_type = response.headers.get("Content-Type", "")
            self.assertIn(
                "application/json", content_type, f"Content-Type should be JSON for {endpoint}"
            )

        print("✓ Content-Type headers validated")

    def test_08_cache_metadata(self):
        """Test that cache metadata is included in responses"""
        if not hasattr(self.__class__, "test_org_name"):
            self.skipTest("No organizations available for testing")

        org_name = self.__class__.test_org_name
        url_encoded_name = org_name.replace(" ", "%20")

        # First request (likely cache miss)
        response1 = self.client.get(f"/api/reports/organization/{url_encoded_name}/json")
        data1 = json.loads(response1.data)

        # Second request (likely cache hit)
        response2 = self.client.get(f"/api/reports/organization/{url_encoded_name}/json")
        data2 = json.loads(response2.data)

        # Both should have api_metadata
        self.assertIn("api_metadata", data1, "First response should have metadata")
        self.assertIn("api_metadata", data2, "Second response should have metadata")

        # Second request should indicate cache hit
        self.assertIn("cached", data2["api_metadata"], "Metadata should indicate cache status")

        print("✓ Cache metadata validated")
        print(f"  - First request cached: {data1['api_metadata'].get('cached', False)}")
        print(f"  - Second request cached: {data2['api_metadata'].get('cached', False)}")

    def test_09_checksum_format(self):
        """Test that checksums follow the expected MD5 format"""
        if not hasattr(self.__class__, "test_org_name"):
            self.skipTest("No organizations available for testing")

        org_name = self.__class__.test_org_name
        url_encoded_name = org_name.replace(" ", "%20")

        response = self.client.get(f"/api/reports/organization/{url_encoded_name}/verification")
        data = json.loads(response.data)

        checksums = data.get("dimension_checksums", {})

        # Verify checksum format (Truncated MD5 is 8 hex characters)
        import re

        checksum_pattern = re.compile(r"^[a-f0-9]{8}$")

        for dimension, checksum_data in checksums.items():
            checksum_value = checksum_data.get("checksum", "")
            self.assertIsNotNone(checksum_value, f"Checksum for {dimension} should not be None")
            self.assertRegex(
                checksum_value,
                checksum_pattern,
                f"Checksum for {dimension} should be 8-character hex hash",
            )

        print(f"✓ Checksum format validated for {len(checksums)} dimensions")


def run_tests():
    """Run the test suite and return results"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestPhase3API)

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 70)
    print("Phase 3 API Test Suite Summary")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)

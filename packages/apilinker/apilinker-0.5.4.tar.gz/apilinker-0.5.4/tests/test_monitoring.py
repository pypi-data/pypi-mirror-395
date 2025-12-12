import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from apilinker.core.monitoring import (
    HealthStatus,
    HealthCheckResult,
    AlertSeverity,
    Alert,
    MonitoringManager,
    ThresholdAlertRule,
    StatusAlertRule,
    PagerDutyIntegration,
    SlackIntegration,
    EmailIntegration,
)
from apilinker.core.connector import ApiConnector


class TestMonitoring:
    def test_health_check_result(self):
        result = HealthCheckResult(
            status=HealthStatus.HEALTHY,
            component="test_component",
            message="All good",
            latency_ms=10.5,
        )
        assert result.status == HealthStatus.HEALTHY
        assert result.component == "test_component"
        assert result.latency_ms == 10.5

    def test_monitoring_manager_health_checks(self):
        manager = MonitoringManager()

        def check_success():
            return True

        def check_fail():
            return False

        def check_result():
            return HealthCheckResult(
                status=HealthStatus.DEGRADED,
                component="custom",
                message="Slow",
                latency_ms=100.0,
            )

        manager.register_health_check("success", check_success)
        manager.register_health_check("fail", check_fail)
        manager.register_health_check("result", check_result)

        results = manager.run_health_checks()

        assert results["success"].status == HealthStatus.HEALTHY
        assert results["fail"].status == HealthStatus.UNHEALTHY
        assert results["result"].status == HealthStatus.DEGRADED
        assert results["result"].latency_ms == 100.0

    def test_threshold_alert_rule(self):
        rule = ThresholdAlertRule(
            name="high_cpu",
            metric="cpu_usage",
            threshold=90.0,
            operator=">",
            severity=AlertSeverity.CRITICAL,
        )

        assert not rule.should_trigger({"cpu_usage": 80.0})
        assert rule.should_trigger({"cpu_usage": 95.0})

        # Test cooldown
        assert not rule.should_trigger({"cpu_usage": 95.0})

    def test_status_alert_rule(self):
        rule = StatusAlertRule(
            name="db_down", component="database", target_status=HealthStatus.UNHEALTHY
        )

        assert not rule.should_trigger({"database_status": HealthStatus.HEALTHY})
        assert rule.should_trigger({"database_status": HealthStatus.UNHEALTHY})

    @patch("apilinker.core.monitoring.httpx.Client")
    def test_pagerduty_integration(self, mock_client_cls):
        mock_client = Mock()
        mock_client_cls.return_value.__enter__.return_value = mock_client

        integration = PagerDutyIntegration(routing_key="test_key")
        alert = Alert(
            id="test_alert",
            rule_name="test_rule",
            severity=AlertSeverity.CRITICAL,
            message="Something went wrong",
        )

        integration.send_alert(alert)

        mock_client.post.assert_called_once()
        args, kwargs = mock_client.post.call_args
        assert kwargs["json"]["routing_key"] == "test_key"
        assert kwargs["json"]["payload"]["severity"] == "critical"

    @patch("apilinker.core.monitoring.httpx.Client")
    def test_slack_integration(self, mock_client_cls):
        mock_client = Mock()
        mock_client_cls.return_value.__enter__.return_value = mock_client

        integration = SlackIntegration(webhook_url="http://slack.com/webhook")
        alert = Alert(
            id="test_alert",
            rule_name="test_rule",
            severity=AlertSeverity.WARNING,
            message="Warning message",
        )

        integration.send_alert(alert)

        mock_client.post.assert_called_once()
        args, kwargs = mock_client.post.call_args
        assert kwargs["json"]["attachments"][0]["color"] == "#ffcc00"

    @patch("apilinker.core.connector.httpx.Client")
    def test_connector_health_check(self, mock_client_cls):
        mock_client = Mock()
        mock_client_cls.return_value = mock_client

        connector = ApiConnector("rest", "http://api.example.com")

        # Test healthy
        mock_client.get.return_value.status_code = 200
        result = connector.check_health()
        assert result.status == HealthStatus.HEALTHY

        # Test unhealthy (500)
        mock_client.get.return_value.status_code = 500
        result = connector.check_health()
        assert result.status == HealthStatus.UNHEALTHY

        # Test exception
        mock_client.get.side_effect = Exception("Connection error")
        result = connector.check_health()
        assert result.status == HealthStatus.UNHEALTHY
        assert "Connection error" in result.message

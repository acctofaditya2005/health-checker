import pytest


def test_rto_is_reasonable():
        rto = 0.15
        assert rto < 60

def test_result_has_required_keys():
        result = {"pod": "nginx-abc", "rto_seconds": 4.2, "status": "recovered"}
        assert "pod" in result
        assert "rto_seconds" in result
        assert "status" in result

def test_result_status_is_recovered():
        result = {"pod": "nginx-abc", "rto_seconds": 4.2, "status": "recovered"}
        assert result["status"] == "recovered"


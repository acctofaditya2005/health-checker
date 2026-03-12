from pydantic import BaseModel
from typing   import Optional , List

class TestResult(BaseModel):
    test_name: str
    passed: bool
    duration: float
    error: Optional[str] = None

class AgentReport(BaseModel):
    total_tests : int
    passed : int
    failed : int
    result : List[TestResult]


r1 = TestResult(test_name="test_login", passed=True, duration=1.2)
r2 = TestResult(test_name="test_logout", passed=False, duration=0.8, error="Element not found")

report = AgentReport(total_tests=2, passed=1, failed=1, result=[r1, r2])
print(report.model_dump())
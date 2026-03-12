import os, subprocess, json
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

class TestResults(BaseModel):
    test_name : str
    passed : bool
    duration : float
    error : Optional[str] = None

class AgentReport(BaseModel):
    total_test : int
    passed : int
    failed : int
    timestamp : str
    results : List[TestResults]


llm = ChatGoogleGenerativeAI(
    model = "gemini-2.0-flash",
    google_api_key = os.environ["GOOGLE_API_KEY"]   
)

@tool
def run_test(test_file:str)->str:
    """ Runs a pytest test file and return the full output including pass/fail results. 
       Use this to execute files and check if test pass or fail."""
    start = datetime.now()
    result = subprocess.run(['py', '-m', 'pytest', test_file, '-v'], capture_output = True, text =True)
    duration = (datetime.now() - start).total_seconds()
    return f"Duration: {duration}s\n {result.stdout}{result.stderr}"


def run_agent():
    llm_with_tools = llm.bind_tools([run_test])
    response = llm_with_tools.invoke("Run the test file test_chaos.py and tell me if all tests passed")
    tool_result = ""
    if response.tool_calls:
        for tool_call in response.tool_calls:
            print(f"Agent calling tools: {tool_call['name']}")
            tool_result = run_test.invoke(tool_call['args'])
            print(f"Tool result \n {tool_result}")
    
    final_response = llm.invoke(
        f"The test results are:\n{tool_result}\n\n Please summarizr whether all tests passed or failed."
    )
    print(f"\nAgent summary:\n{final_response.content}")



if __name__ == "__main__":
    run_agent()

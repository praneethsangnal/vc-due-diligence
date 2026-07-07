from app.agents.market import run_market
from app.schemas.due_diligence import DueDiligenceState


state = DueDiligenceState(
    startup_description="""
AIHire is an AI-powered recruitment platform for software engineers.

The company has raised a $1M pre-seed round and currently generates
$150K ARR by serving B2B SaaS companies.
"""
)

result = run_market(state)

print(result)
print(type(result))
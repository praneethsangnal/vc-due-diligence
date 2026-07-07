from app.agents.planner import run_planner


startup_description = """
Company: AIHire

AIHire is an AI-powered recruitment platform that helps companies
screen software engineers automatically.

The company has $150,000 ARR,
raised a $1M pre-seed round,
and primarily serves B2B SaaS companies.
"""

result = run_planner(startup_description)

print(result)
print(type(result))
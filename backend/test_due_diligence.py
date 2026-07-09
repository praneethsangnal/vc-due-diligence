import asyncio

from app.services.due_diligence_service import DueDiligenceService


async def main():
    service = DueDiligenceService()

    state = await service.run(
        """
AIHire is an AI-powered recruitment platform that helps companies
hire software engineers faster.

The company has raised a $1M pre-seed round,
generates $150K ARR,
and primarily serves B2B SaaS companies.
"""
    )

    print("\n========== PLANNER ==========\n")
    print(state.planner_output)

    print("\n========== MARKET ==========\n")
    print(state.market_analysis)

    print("\n========== FINANCE ==========\n")
    print(state.finance_analysis)

    print("\n========== COMPETITION ==========\n")
    print(state.competition_analysis)

    print("\n========== PRODUCT ==========\n")
    print(state.product_analysis)

    print("\n========== RISK ==========\n")
    print(state.risk_analysis)

    print("\n========== CRITIC ==========\n")
    print(state.critic_review)


if __name__ == "__main__":
    asyncio.run(main())
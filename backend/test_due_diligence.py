import asyncio
import time

from app.services.due_diligence_service import DueDiligenceService


async def main():
    service = DueDiligenceService()

    startup_description = """
AIHire is a recruitment platform generating $150K ARR from a pool of 
exactly two enterprise clients who each pay $5,000 per year. 

The founders claim they have an absolute global monopoly with zero direct 
or indirect competitors in existence, and that their proprietary AI models 
are 100% accurate, completely free of algorithmic bias, and require zero compliance oversight.

They plan to use their $1M pre-seed round to buy a fleet of corporate jets.
"""

    start_time = time.perf_counter()

    state = await service.run(startup_description)

    end_time = time.perf_counter()

    print("\n" + "=" * 60)
    print("DUE DILIGENCE EXECUTION COMPLETED")
    print("=" * 60)

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

    print("\n========== FINAL CRITIC REVIEW ==========\n")
    print(state.critic_review)

    print("\n========== EXECUTION TIME ==========\n")
    print(f"Total execution time: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"

states = pd.read_csv(OUT / "state_delivery.csv")

comparisons = []

for minimum in [500, 1000]:
    ranked = (
        states.loc[states["orders"] >= minimum]
        .sort_values("late_rate_pct", ascending=False)
        .copy()
    )

    ranked.insert(0, "rank", range(1, len(ranked) + 1))
    ranked.insert(0, "minimum_orders", minimum)

    comparisons.append(ranked)

    print(f"\nStates with at least {minimum:,} eligible orders:")
    print(
        ranked[
            ["rank", "customer_state", "orders",
             "late_orders", "late_rate_pct"]
        ].head(10).to_string(index=False)
    )

comparison = pd.concat(comparisons, ignore_index=True)
comparison.to_csv(
    OUT / "state_threshold_comparison.csv",
    index=False
)

print("\nSaved outputs/state_threshold_comparison.csv")
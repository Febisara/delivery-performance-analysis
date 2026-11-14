"""Analyse delivered orders without changing the original files."""
from pathlib import Path
import json
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
RAW = ROOT / 'data' / 'raw'
OUT = ROOT / 'outputs'
OUT.mkdir(exist_ok=True)


def build_analysis(orders, customers):
    # The analysis must keep exactly one row per order.
    for frame, key in [(orders, 'order_id'),
                       (customers, 'customer_id')]:
        if frame[key].isna().any() or frame[key].duplicated().any():
            raise ValueError(f'Missing or duplicated key: {key}')
    dates = ['order_purchase_timestamp',
             'order_delivered_customer_date',
             'order_estimated_delivery_date']
    orders = orders.copy()
    for col in dates:
        orders[col] = pd.to_datetime(orders[col], errors='coerce')
    joined = orders.merge(
        customers[['customer_id', 'customer_state']],
        on='customer_id', how='left', validate='many_to_one',
        indicator=True
    )
    if not joined['_merge'].eq('both').all():
        raise ValueError('Some orders have no matching customer')
    delivered = joined['order_status'].eq('delivered')
    has_dates = joined[dates].notna().all(axis=1)
    chronology = (
        joined['order_delivered_customer_date'] >=
        joined['order_purchase_timestamp']
    ) & (
        joined['order_estimated_delivery_date'].dt.normalize() >=
        joined['order_purchase_timestamp'].dt.normalize()
    )
    eligible = delivered & has_dates & chronology
    rejected = joined.loc[~eligible].copy()
    rejected['exclusion_reason'] = 'invalid_chronology'
    rejected.loc[~has_dates, 'exclusion_reason'] = 'missing_date'
    rejected.loc[~delivered, 'exclusion_reason'] = 'not_delivered'
    clean = joined.loc[eligible].copy()
    # The promise is interpreted as a calendar date, not midnight.
    actual = clean['order_delivered_customer_date'].dt.normalize()
    promised = clean['order_estimated_delivery_date'].dt.normalize()
    clean['late_days'] = (actual - promised).dt.days.clip(lower=0)
    clean['is_late'] = clean['late_days'].gt(0)
    clean['delivery_days'] = (
        clean['order_delivered_customer_date'] -
        clean['order_purchase_timestamp']
    ).dt.total_seconds() / 86400
    clean['purchase_month'] = (
        clean['order_purchase_timestamp'].dt.to_period('M').astype(str)
    )
    return clean, rejected


def summary(frame, column):
    result = frame.groupby(column, dropna=False).agg(
        orders=('order_id', 'size'),
        late_orders=('is_late', 'sum'),
        late_rate_pct=('is_late', lambda x: 100 * x.mean()),
        median_delivery_days=('delivery_days', 'median'),
        p90_delivery_days=('delivery_days', lambda x: x.quantile(.9))
    ).reset_index()
    return result


def main():
    orders = pd.read_csv(RAW / 'olist_orders_dataset.csv')
    customers = pd.read_csv(RAW / 'olist_customers_dataset.csv')
    clean, rejected = build_analysis(orders, customers)
    assert len(clean) + len(rejected) == len(orders)
    assert clean['order_id'].is_unique
    assert clean['late_days'].ge(0).all()
    monthly = summary(clean, 'purchase_month')
    states = summary(clean, 'customer_state')
    states = states.sort_values('late_rate_pct', ascending=False)
    clean.to_csv(OUT / 'analysed_orders.csv', index=False)
    rejected[['order_id', 'exclusion_reason']].to_csv(
        OUT / 'excluded_orders.csv', index=False
    )
    monthly.to_csv(OUT / 'monthly_delivery.csv', index=False)
    states.to_csv(OUT / 'state_delivery.csv', index=False)
    metrics = {
        'raw_orders': len(orders),
        'eligible_delivered_orders': len(clean),
        'excluded_orders': len(rejected),
        'late_orders': int(clean['is_late'].sum()),
        'late_rate_pct': round(100 * clean['is_late'].mean(), 2),
        'median_delivery_days': round(clean['delivery_days'].median(), 2),
        'p90_delivery_days': round(clean['delivery_days'].quantile(.9), 2),
        'exclusions': rejected['exclusion_reason'].value_counts().to_dict()
    }
    (OUT / 'metrics.json').write_text(json.dumps(metrics, indent=2))
    fig, ax = plt.subplots(figsize=(10, 5))
    plot_monthly = monthly.loc[monthly['orders'] >= 100]
    ax.plot(plot_monthly['purchase_month'], plot_monthly['late_rate_pct'],
            marker='o', color='#155e75')
    ax.set(title='Late delivery rate by purchase month (100+ orders)',
           ylabel='Late delivered orders (%)', xlabel='Purchase month')
    ax.tick_params(axis='x', rotation=60)
    ax.grid(axis='y', alpha=.2)
    fig.tight_layout()
    fig.savefig(OUT / 'monthly_lateness.png', dpi=180)
    plt.close(fig)
    # Minimum volume makes the comparison less vulnerable to tiny groups.
    compare = states.loc[states['orders'] >= 500].head(10)
    compare = compare.sort_values('late_rate_pct')
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.barh(compare['customer_state'], compare['late_rate_pct'],
            color='#155e75')
    ax.set(title='Highest late rates among states with 500 or more orders',
           xlabel='Late delivered orders (%)', ylabel='Customer state')
    fig.tight_layout()
    fig.savefig(OUT / 'state_lateness.png', dpi=180)
    plt.close(fig)
    print(json.dumps(metrics, indent=2))


if __name__ == '__main__':
    main()

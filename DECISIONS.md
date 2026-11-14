# Decision log

### 1\. Assess lateness using calendar dates

Decision: An order is late only if its actual delivery calendar date is after its estimated calendar date. Delivery on the estimated day is on time.

Alternative: Comparing exact timestamps could label arrival later on the promised day as late when the estimated timestamp is midnight.

Validation: The calendar-deadline automated test passed.

### 

### 2\. Define the eligible population

Decision: Include delivered orders with usable purchase, actual delivery and estimated delivery dates, and valid chronology. Actual receipt cannot precede purchase; the estimated calendar date cannot precede the purchase calendar date.

Alternative: Using all purchased orders as the denominator would include orders without a completed delivery to assess.

Results:

* Raw orders: 99,441
* Eligible delivered orders: 96,470
* Excluded orders: 2,971
* Not delivered: 2,963
* Delivered but missing a required date: 8

Reconciliation: 96,470 + 2,971 = 99,441; 2,963 + 8 = 2,971.

Limitation: These results describe eligible completed deliveries, not all promised deliveries.

### 

### 3\. Preserve one row per order

Decision: Validate order and customer keys before joining. Reject duplicated customer keys rather than allowing a join to multiply order rows.

Alternative: An unchecked join could inflate counts and distort metrics.

Validation: The duplicate-customer rejection test passed. Both supplied automated tests completed successfully.

### 

### 4\. Check individual dates

|Order ID|Estimated date|Actual date|Comparison|Expected late\_days|Expected is\_late|Matches CSV|
|-|-|-|-|-|-|-|
|e481f51cbdc54678b7cc49136f2d6af7|2017-10-18|2017-10-10|8 days early|0|False|Yes|
|203096f03d82e0dffbc41ebc2e2bcfb7|2017-09-28|2017-10-09|11 days late|11|True|Yes|
|8563039e855156e48fccee4d611a3196|2018-03-20|2018-03-20|Same day|0|False|Yes|

Early arrivals have zero late days. The same-day example arrived at 00:59:25 and correctly counts as on time.

### 

### 5\. Check repeatability

I reran analyse.py with the same input files and environment and confirmed that the summary metrics matched:

* Raw orders: 99,441
* Eligible delivered orders: 96,470
* Excluded orders: 2,971
* Late orders: 6,534
* Late rate: 6.77%
* Median delivery duration: 10.22 days
* 90th-percentile duration: 23.10 days

This demonstrates consistent summary results across two runs, not exhaustive coverage of every possible input.

### 

### 6\. Compare state minimum-volume thresholds

Question: Does raising the minimum eligible order count from 500 to 1,000 change the highest-ranked state?

Method: I ran compare\_thresholds.py using state\_delivery.csv and saved outputs/state\_threshold\_comparison.csv.

Result: At 500 orders, MA ranked highest with 125 late orders out of 717 (17.43%). At 1,000 orders, MA no longer qualified. CE ranked highest with 176 late orders out of 1,279 (13.76%).

Interpretation: Individual state rates stay unchanged. The threshold changes which states qualify and therefore their rankings. A higher threshold focuses on larger groups but excludes signals from smaller states.

Decision: Retain the original 500-order chart and report the 1,000-order comparison as a sensitivity check. Neither threshold establishes statistical significance or the causes of lateness.


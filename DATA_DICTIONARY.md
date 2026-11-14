# Data dictionary

Each row in the orders file represents one order. Customer records link to orders through customer\_id.



## Orders — olist\_orders\_dataset.csv

|Field|Meaning|Treatment|
|-|-|-|
|order\_id|Unique order identifier|Keep as text; reject missing or duplicate keys|
|customer\_id|Key linking an order to its customer record|Keep as text; use for the customer join|
|order\_status|Recorded order status|Only delivered orders qualify for the core analysis|
|order\_purchase\_timestamp|Recorded purchase date and time|Parse as a datetime; required|
|order\_approved\_at|Recorded order approval date and time|Not used in the core metrics|
|order\_delivered\_carrier\_date|Recorded handover date and time to the carrier|Not used in the core metrics|
|order\_delivered\_customer\_date|Recorded customer receipt date and time|Parse as a datetime; required|
|order\_estimated\_delivery\_date|Recorded estimated delivery date|Parse as a datetime; compare calendar dates for lateness|

## 

## Customers — olist\_customers\_dataset.csv

|Field|Meaning|Treatment|
|-|-|-|
|customer\_id|Key linking customer records to orders|Reject missing or duplicate keys before joining|
|customer\_unique\_id|Person-level identifier that can connect repeat purchases|Not used here|
|customer\_zip\_code\_prefix|Customer postal-code prefix|Not used here; treat as an identifier|
|customer\_city|Customer city|Not used here|
|customer\_state|Two-letter Brazilian state code|Used to group destination-state results|

## 

## Calculated fields

|Field|Meaning|
|-|-|
|late\_days|Actual delivery calendar date minus estimated calendar date, with negative values set to zero|
|is\_late|True when actual delivery is after the estimated calendar date|
|delivery\_days|Elapsed seconds from purchase to receipt divided by 86,400|
|purchase\_month|Purchase year and month|
|exclusion\_reason|not\_delivered, missing\_date, or invalid\_chronology|
|\_merge|Join indicator; all orders must match a customer record|

## 

## Summary fields

|Field|Meaning|
|-|-|
|orders|Eligible order count in a group|
|late\_orders|Late eligible order count in a group|
|late\_rate\_pct|100 × late\_orders / orders|
|median\_delivery\_days|Median elapsed delivery duration|
|p90\_delivery\_days|90th percentile of elapsed delivery duration|
|minimum\_orders|Minimum group size used in the threshold comparison|
|rank|Late-rate rank among states meeting that threshold|

## 

## Analysis rules

* Include delivered orders with all three required dates and valid chronology.
* Actual receipt cannot precede purchase. The estimated calendar date cannot precede the purchase calendar date.
* Exclusion reasons use priority: not delivered, then missing date, then invalid chronology.
* Arrival on the estimated calendar date counts as on time.
* The late-rate denominator is eligible delivered orders, not all purchased orders.
* The monthly chart requires at least 100 eligible orders per month.
* The original state chart requires at least 500 eligible orders per state.
* The additional comparison uses thresholds of 500 and 1,000 orders.
* Thresholds are screening rules, not statistical significance tests.
* Source timestamps have no resolved timezone information in this analysis.


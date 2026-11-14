# Delivery performance findings

## 

## Overall result

* Of 96,470 eligible delivered orders, 6,534 arrived after their estimated calendar delivery date, giving a late rate of 6.77%. The analysis excluded 2,971 of the original 99,441 orders: 2,963 were not delivered and eight delivered orders lacked a required date.
* Arrival on the estimated date counts as on time. Eligibility requires delivered status, usable dates and valid chronology. These results describe historical Olist marketplace data from 2016–2018, not current performance.

## 

## Delivery duration

* Median delivery duration was 10.22 days, while the 90th percentile was 23.10 days. Approximately 90% of eligible orders arrived within 23.10 days of purchase. The gap shows that the median alone does not describe slower deliveries.
* Duration and lateness measure different things. A long delivery can meet its estimated date, while a shorter delivery can miss a tighter promise.

## 

## State pattern

* Among states with at least 500 eligible orders, Maranhão (MA) had the highest late rate: 125 of 717 orders, or 17.43%. This was 10.66 percentage points above the overall rate. Its median delivery duration was 19.19 days.
* Alagoas (AL) recorded 21.41%, but its 397 eligible orders did not meet the comparison threshold. This threshold reduces reliance on small groups; it is not a statistical significance test.
* Rio de Janeiro (RJ) merits investigation because of its volume: 1,495 of 12,350 eligible orders were late, or 12.11%. Both rates and affected order counts matter.

## 

## Monthly pattern

* Among purchase months with at least 100 eligible orders, March 2018 had the highest late rate: 1,328 of 7,003 orders, or 18.96%.
* February 2018 also had an elevated rate of 14.13% (926 of 6,555), compared with 4.50% in April 2018 (306 of 6,798). This variation warrants investigation, but the tables alone do not explain its cause.
* September 2016 had a 100% rate based on one order and was excluded from the monthly chart. Months group orders by purchase date, not arrival date.

## 

## Sensitivity check

* Raising the state minimum from 500 to 1,000 orders changed the highest-ranked state from MA to CE. MA no longer qualified. CE had 176 late orders out of 1,279, or 13.76%.
* Individual state rates remained unchanged. The leading state therefore depends on the comparison threshold. The original chart was retained, with the additional comparison saved separately.

## 

## Recommendations and limitations

* Investigate February–March 2018 purchase cohorts and the state patterns above. Compare promised lead times, seller origins, destination routes, carriers and service types before attributing differences to operational causes.
* The core analysis does not establish that a particular courier, capacity issue or event caused delays. Undelivered orders are excluded, so this is not the late rate of all promised deliveries. Boundary months may also reflect incomplete observation windows.
* Request carrier and route information, service levels and full pending-order histories before proposing operational changes. Both automated tests passed, and a second analysis run produced unchanged summary metrics.

## 

## Supporting outputs

* [Summary metrics](outputs/metrics.json)
* [State results](outputs/state_delivery.csv)
* [Monthly results](outputs/monthly_delivery.csv)
* [Threshold comparison](outputs/state_threshold_comparison.csv)
* [State chart](outputs/state_lateness.png)
* [Monthly chart](outputs/monthly_lateness.png)


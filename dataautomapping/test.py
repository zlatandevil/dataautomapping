import markdown
output = r"""
## DMP2: Customer Balance Table 

This mapping will create a table storing balance information for every individual customer.

###  1. CTE Declarations 

| Source Table | Alias | Transformation |
|---|---|---|
| """tcb-prod-curated"".individual_gra_ds1 | idv | SELECT * FROM """tcb-prod-curated"".individual_gra_ds1 |
| """tcb-prod-golden_curated"".au_bal | au | SELECT * FROM """tcb-prod-golden_curated"".au_bal |

### 2. Target Data Mapping

| field_name | field_type | transformation | description |
|---|---|---|---|
| customer_id | STRING | idv.individual_id | Customer ID |
| balance | DECIMAL(38,6) | au.au_bal_value | Customer balance |
| balance_date | DATE | au.balance_date | Date of the balance |
| balance_type | STRING | au.balance_type | Type of balance (e.g., 'Balance', 'Max', 'Min') |

**Explanation:**

This mapping joins the `individual_gra_ds1` and `au_bal` tables on the customer ID (`individual_id`). The resulting table will include the customer ID, balance, balance date, and balance type for each customer. 

**Note:**

* This mapping assumes that the `au_bal` table contains balance information for all customers. If this is not the case, you may need to add a filter to the CTE to select only balances related to individual customers. 
* The `balance_type` field could be further transformed to provide a more user-friendly representation of the balance type. 

This mapping provides a basic structure for storing customer balance information. You can adjust the fields, transformations, and filters to meet your specific requirements. 
"""
markdown.markdown(output)

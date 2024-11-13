import markdown

output = r"""
```markdown
# DMP2 information of organization representative

## 1. Pre-filter Declaration:

| Input Table | Alias | Transformation |
|---|---|---|
| `"""tcb-prod-curated"".organization_gra` | ORGA | SELECT * FROM `"""tcb-prod-curated"".organization_gra` |
| `"""tcb-prod-curated"".individual_gra_ds1` | IDVA | SELECT * FROM `"""tcb-prod-curated"".individual_gra_ds1` |


## 2. Target Data Mapping:

| ID | Field name | Datatype | Transformation | Description |
|---|---|---|---|---|
| 1 | org_id | string | ORGA.org_id | The unique identifier assigned to an Organization. |
| 2 | representative_id | string | ORGA.legal_representative_id |  The unique identifier of the legal representative of the organization. |
| 3 | representative_name | string | IDVA.idv_name_eng  WHERE IDVA.individual_id = ORGA.legal_representative_id | Name of the legal representative (Looked up from IDVA table using representative_id) |
| 4 | representative_phone | string | IDVA.mobile_user_name[0] WHERE IDVA.individual_id = ORGA.legal_representative_id | Phone number of the legal representative (Looked up from IDVA table using representative_id) -  Assumes first element in array is primary contact.  Further clarification needed for multiple phone numbers. | 
| 5 | representative_email | string |  Not Available | Email address of the legal representative. This information is not present in the provided data.  |


```"""
markdown.markdown(output)


## Flow

```mermaid
graph TD;
    A[Set Variables] --> B[Read from SQL Database];
    B --> V[Input Schema Validation];
    V -->|Failure| X[Error Alert];
    V -->|Success| C[Transform KPIs];
    C --> Y[Output Schema Validation];
    Y -->|Failure| Z[Error Alert];
    Y -->|Success| D[Save to DuckDB];
```
Data Contract
::: app.schema.ProductSchema

Transformations
Set Variables
::: app.etl.load_settings

Read from SQL Database
::: app.etl.extract_from_sql

Transform KPIs
::: app.etl.transform
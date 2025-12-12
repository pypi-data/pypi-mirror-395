Nesso CLI in some types of dbt adapters uses non-standard functionalities created by nesso-cli team. Below are the added functionalities with a description of how to use them depending on the adapters.

## dbt sqlserver

### `OPTION()` clause

In some cases we need to use the `OPTION` clause. An example would be a code that, thanks to the `OPTION` clause, will be able to perform an infinite number of recursions. 

```sql
WITH cte
  AS (SELECT [date]
        FROM calendar
       WHERE DATE = '2020-01-01'
      UNION ALL
      SELECT DATEADD(day, 1, [date]) as [date]
        FROM cte
       WHERE DATEADD(day, 1, [date]) 
       < '2021-01-01'
    --    < '2020-02-28'
       )
SELECT *
  FROM cte
  OPTION (MAXRECURSION 0);
```

The equivalent of this expression in dbt will be the utilization of the `option_clause` parameter in the Jinja template.

```sql
{{
    config({
        "materialized": 'table',
        "option_clause": "MAXRECURSION 0"
    })

}}
WITH cte
  AS (SELECT [date]
        FROM calendar
       WHERE DATE = '2020-01-01'
      UNION ALL
      SELECT DATEADD(day, 1, [date]) as [date]
        FROM cte
       WHERE DATEADD(day, 1, [date]) 
    < '2021-01-01'
    -- < '2020-02-28'
       )
SELECT *
  FROM cte
```
>***Note**: The `OPTION` clause can only be used when materializing a model as a table because using the `OPTION` clause when creating a view is not possible in SQL Server.*

In the `option_clause` parameter, you can include multiple values for the `OPTION` field. You should provide them as a single string, as if you were entering them inside parentheses in SQL Server.

```sql
{{
    config({
        "materialized": 'table',
        "option_clause": "HASH JOIN, MAXDOP 4, RECOMPILE"
    })

}}
```
The above example is equivalent to the following code. 
```sql
OPTION(HASH JOIN, MAXDOP 4, RECOMPILE)
```
To learn about all the possibilities of the `OPTION` clause, refer to the [Microsoft documentation](https://learn.microsoft.com/en-us/sql/t-sql/queries/option-clause-transact-sql?view=sql-server-ver16).


### `sql_header`
An optional configuration to inject SQL above the `create table` statements that dbt executes when building models and snapshots.

Example of using `sql_header` for `SET DATEFIRST` command.
```sql
-- Query written in Transact-SQL
SET DATEFIRST 1;

SELECT GETDATE() AS CurrentDate,
       DATEPART(WEEKDAY, GETDATE()) AS DayOfWeek;
```
The equivalent of this expression in dbt will be the utilization of the `sql_header` parameter in the Jinja template.
```sql
{{
    config({
        "materialized": 'table',
        "sql_header": 'SET DATEFIRST 1',
    })

}}
SELECT GETDATE() AS CurrentDate,
       DATEPART(WEEKDAY, GETDATE()) AS DayOfWeek;
```

>***Note**: The `sql_header` clause can only be used when materializing a model as a table.*


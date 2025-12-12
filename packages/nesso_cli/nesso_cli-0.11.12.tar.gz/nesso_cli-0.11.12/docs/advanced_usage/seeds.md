# Seeds

Seeds are CSV and Excel files which `nesso models` can ingest into the data warehouse. For more information about seeds, see the [dbt documentation](https://docs.getdbt.com/docs/build/seeds).

Here are some good use-cases for seeds:  
✅ Mappings  
✅ Fixed lists of items  

Poor use-cases of seeds:  
❌ Loading often changing data  
❌ Loading sensitive information (remember, these files are stored unencrypted in a git repository)

## Registering a seed

To load a seed table into the database, run the following command:

```bash
nesso models seed register <my_seed>
```

This will do two things:

- materialize the seed as a table within the project's database (in the bronze schema; by default, `staging`)
- add seed metadata to the seed [properties file](../reference/glossary.md#property-files) (by default, `seeds/schema.yml`)

In case the seed is an Excel file, it will also be converted to a CSV.

In below example, the `average salary test.xlsx` seed file will be converted to `average_salary_test.csv`. Additionally, metadata about the `average_salary_test` table will be added to the `schema.yml` file.

!!! note  "Metadata matters"
    It's a good idea to edit `schema.yml` manually after running `nesso models seed register` to add the dataset's owner, description, tests, and any other relevant metadata.

Initial file structure:

```bash
└── seeds
    ├── average_salary_test.xlsx
    └── schema.yml
```

Now let's register the `average_salary_test` seed:

```bash
nesso models seed register average_salary_test
```

This will produce the following file structure:

```bash
└── seeds
    ├── average_salary_test.xlsx
    ├── average_salary_test.csv
    └── schema.yml
```

## **Referring to a seed table**

In downstream models, seeds can be referenced using the `ref` variable:

```sql
select * from {{ ref('average_salary_test') }}
```

## **Testing seeds**

Seeds can be tested the same way as models. For more information, see the [User Guide](../user_guide/models.md#tests).

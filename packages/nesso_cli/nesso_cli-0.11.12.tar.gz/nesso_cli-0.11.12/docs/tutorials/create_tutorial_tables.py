import random
from datetime import datetime

import duckdb
import pandas as pd
from faker import Faker
from loguru import logger
from pydantic import BaseModel, Field

fake = Faker()
test_tables_nrows = 100


class Contact(BaseModel):
    Id: int = Field(default_factory=lambda: i)
    AccountId: str = Field(default_factory=lambda: random.randint(1, test_tables_nrows))
    FirstName: str = Field(default_factory=fake.first_name)
    LastName: str = Field(default_factory=fake.last_name)
    ContactEMail: str = Field(default_factory=fake.email)
    MailingCity: str = Field(default_factory=fake.city)
    Country: str = Field(default_factory=fake.country)
    # we need to use alias as pydantic doesn't support fields starting with an underscore
    viadot_downloaded_at_utc: datetime = Field(
        default_factory=datetime.utcnow, alias="_viadot_downloaded_at_utc"
    )


class Account(BaseModel):
    id: int = Field(default_factory=lambda: i)
    name: str = Field(default_factory=fake.company)
    email: str = Field(default_factory=fake.email)
    mobile: str = Field(default_factory=fake.phone_number)
    country: str = Field(default_factory=fake.country)
    # we need to use alias as pydantic doesn't support fields starting with an underscore
    viadot_downloaded_at_utc: datetime = Field(
        default_factory=datetime.utcnow, alias="_viadot_downloaded_at_utc"
    )


contacts = []
accounts = []

for i in range(1, test_tables_nrows + 1):
    contacts.append(Contact(Id=i).dict(by_alias=True))
    accounts.append(Account(id=i).dict(by_alias=True))

contacts_df = pd.DataFrame(contacts)
accounts_df = pd.DataFrame(accounts)

# Materialize the tables in DuckDB.
con = duckdb.connect("nesso.duckdb")
bronze_schema = "staging"
con.execute(f"CREATE SCHEMA {bronze_schema}")

# Contact
contact_table_fqn = f"{bronze_schema}.contact"
con.execute(f"CREATE TABLE {contact_table_fqn} AS SELECT * FROM contacts_df")
logger.info(f"Successfully created table {contact_table_fqn}")

account_table_fqn = f"{bronze_schema}.account"
con.execute(f"CREATE TABLE {account_table_fqn} AS SELECT * FROM accounts_df")
logger.info(f"Successfully created table {account_table_fqn}")

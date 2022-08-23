
import snowflake.connector
import argparse
import json

# context = '{"token": "***"}'
# context = r"""{
#     "token": "***",
#     "job": "validate_deploy",
#     "ref": "refs/pull/238/merge"}"""
parser = argparse.ArgumentParser(description="")
# parser.add_argument(
#     "--context",
#     type=json.loads,
#     required=True,
#     help="sql statement to execute",
# )

parser.add_argument(
    "--context",
    type=str,
    required=True,
    help="sql statement to execute",
)
# args = parser.parse_args(['--context', context])
args = parser.parse_args()
# print(f'args.context: {args.context}')
# print(json.dumps(args.context))
# print(f'json.loads(args.context): {json.loads(args.context)}')
sql = f"INSERT INTO dbt_metrics.artifacts.github_context (content) SELECT PARSE_JSON(column1) as content FROM VALUES ('{args.context}'); "

print(sql)
# exit(1)


# Connect to database
print("Connecting to Snowflake Database")
con = snowflake.connector.connect(
    account='nc87444.ap-south-1',
    user='vimalathi',
    password='Snowflake!2',
    role='accountadmin',
    database='dbt_metrics',
    schema='artifacts',
    warehouse='compute_wh'
)

try:
    cur = con.cursor()
    cur.execute(sql)
    # print(f"Number of rows inserted: {affected_rows}")
    # con.get_query_status(sf_qid=cur.sfqid)
    con.commit()
except snowflake.connector.errors.ProgrammingError as e:
    print(e)
finally:
    if not cur.is_closed():
        cur.close()
        con.close()


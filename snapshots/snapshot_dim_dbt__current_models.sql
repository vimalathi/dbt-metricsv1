{% snapshot snapshot_dim_dbt__current_models %}

    {{
        config(
          target_database='dbt_metrics',
          target_schema='snapshots',

          strategy='check',
          unique_key='node_id',
          check_cols=['checksum'],
          invalidate_hard_deletes=True,
        )
    }}

    select * from {{ ref('dim_dbt__current_models') }}

{% endsnapshot %}
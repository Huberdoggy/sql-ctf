from solutions import instantiate, populate, run_query

engine, tables = instantiate()

# Eventually, might use this to selectively run other tests/imported functions
# Build an evidence trail to the 'flag'
if __name__ == "__main__":
    populate(engine, tables)  # All tables, expanded view
    run_query(engine, db_table='boot_errors')  # 1.2
    run_query(engine, db_table='failed_modules')  # 2.1
    run_query(engine, db_table='ct_investigation')  # 2.2
    run_query(engine, db_table='triple_threat')  # 3.1
    run_query(engine, db_table='temporal_analysis')  # 3.2

from solutions import instantiate, populate, run_query

engine, tables = instantiate()

# Eventually, might use this to selectively run other tests/imported functions
if __name__ == "__main__":
    # populate(engine, tables)
    run_query(engine, key='boot_errors')

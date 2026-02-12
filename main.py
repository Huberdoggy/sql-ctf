from solutions import boot_inspection, instantiate, populate

engine, tables = instantiate()

# Eventually, might use this to selectively run other tests/imported functions
if __name__ == "__main__":
    # populate(engine, tables)
    boot_inspection(engine)

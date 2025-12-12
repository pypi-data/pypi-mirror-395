import tomllib
import inspect
from pympler import asizeof
from . import config as c
from .utils import convert


def save(results):
    # Build output path
    to_write = (
        str(results) + "\n"
    )  # Include new line in the same write call to prevent buffer issues
    with open(c.CONFIG_PATH, "rb") as f:
        config = tomllib.load(f)
        file = config["FILE_NAME"]
    # Append to output file
    with open(file, "a") as out:
        out.write(to_write)
        out.flush()  # Prevent dual entries on a line due to buffer issues


def deets_profile(func, units="mb"):
    def profile(*args, **kwargs):
        # Dont do anything unless profiler is on in the conf file
        with open(c.CONFIG_PATH, "rb") as f:
            config = tomllib.load(f)
        if config["RECORDING"]:
            # Function must have 'self' param

            # Get ordered dict of params
            p_names = inspect.signature(func).parameters
            if "self" not in p_names:
                raise UserWarning(
                    "Invalid usage: decorated function must contain a 'self' parameter"
                )

            # Get the function name that is being decorated
            f_name = func.__name__

            if f_name == "clear":
                cache_data = args[0]._data

                # Transalate cache into useable data
                cache_data = translate_cache(cache_data)

                # Do something here
                if cache_data:
                    save(cache_data)

        # Run the clear function regardless
        return func(*args, **kwargs)

    return profile


def translate_cache(cache_data):
    """
    Remaps cache._data to desired format inorder to create a profiler entry:
    res = {
        model: {
            record_id: {
                field: size (MB)
            }
        },
        ...
    }
    """

    rebuilt = {}

    for k, v in cache_data.items():
        # Extract model & field
        model = str(k)

        field = model.split(".")[-1]
        model = ".".join(model.split(".")[:-1])

        # Add model to dict
        if model not in rebuilt:
            rebuilt[model] = {}

        # Populate record data
        for rec_id, f_val in v.items():
            if type(rec_id) is int or type(rec_id).__name__ == "NewId":
                # Change to string representation of newid if it comes up
                if type(rec_id).__name__ == "NewId":
                    rec_id = "(NewId)"
                f_mem = convert(asizeof.asized(f_val, detail=1).size, "mb")
                rec_id = str(rec_id)
                field = str(field)

                if rec_id not in rebuilt[model]:
                    rebuilt[model][rec_id] = {field: f_mem}
                else:
                    rebuilt[model][rec_id][field] = (
                        rebuilt[model][rec_id].get(field, 0) + f_mem
                    )

            else:
                # Sometimes the _data keys do not refer to a record ID and the expected data is nested, honestly no clue why.
                for rec_id_nested, f_val_nested in f_val.items():
                    f_mem = convert(asizeof.asized(f_val_nested, detail=1).size, "mb")
                    rec_id_nested = str(rec_id_nested)
                    field = str(field)
                    if rec_id_nested not in rebuilt[model]:
                        rebuilt[model][rec_id_nested] = {field: f_mem}
                    else:
                        rebuilt[model][rec_id_nested][field] = (
                            rebuilt[model][rec_id_nested].get(field, 0) + f_mem
                        )

    # Return none if there wasnt actually anything cleared by the cache to keep data clean
    if rebuilt == {}:
        return None

    return rebuilt

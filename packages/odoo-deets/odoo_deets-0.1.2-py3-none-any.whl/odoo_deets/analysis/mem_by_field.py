from odoo_deets.utils import parse_deetsfile
from odoo_deets import config as c
import pygal


def tables(deetsfile):
    data = mem_by_field(deetsfile)
    tables = []
    for model, recs in data.items():
        if len(tables) > c.TABLE_LIMIT:
            break
        m_mem = 0
        bar = pygal.Bar()
        bar.x_labels = ["Cumulative Memory (MB)"]
        for r_id, mem in recs.items():
            bar.add(str(r_id), [mem])
            m_mem += mem

        tables.append((bar.render_table(style=True, transpose=True), model, m_mem))

    tables.sort(key=lambda x: x[2], reverse=True)

    return tables


def mem_by_field(deetsfile):
    """
    Prepare a dict mapping field: cum_memory for all entries which were recorded, grouped by model

    {
        model -> field -> cum_mem,
        model -> field -> cum_mem,
        ...
    }
    """
    entries = parse_deetsfile(deetsfile)

    model_map = {}

    for e in entries:
        for model, recs in e.items():
            if model not in model_map:
                model_map[model] = {}

            # Isolate the list of fields for each record
            for fields in recs.values():
                # Iterate through each accessed field
                for field, mem in fields.items():
                    model_map[model][field] = model_map[model].get(field, 0) + mem

    # Sort both models and recs by mem desc

    # Sort models
    model_map = dict(
        sorted(model_map.items(), key=lambda x: sum(x[1].values()), reverse=True)
    )

    # Round and sort Fields
    for model in model_map:
        model_map[model] = {
            k: round(v, c.DECIMAL_PLACES)
            for k, v in sorted(
                model_map[model].items(), key=lambda x: x[1], reverse=True
            )
        }

    return model_map


# mem_by_field("/home/austin/deets_profiles/tester.deets")

from odoo_deets.utils import parse_deetsfile
from odoo_deets import config as c
import pygal


def tables(deetsfile):
    data = mem_by_record(deetsfile)
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


def mem_by_record(deetsfile):
    """
    Prepare a dict mapping record: cum_memory for all entries which were recorded, grouped by model

    {
        model -> record -> cum_mem,
        model -> record -> cum_mem,
        ...
    }
    """
    entries = parse_deetsfile(deetsfile)

    model_map = {}

    for e in entries:
        for model, recs in e.items():
            if model not in model_map:
                model_map[model] = {}

            for rec_id, fields in recs.items():
                model_map[model][rec_id] = model_map[model].get(rec_id, 0) + sum(
                    fields.values()
                )

    # Sort both models and recs by mem desc

    # Models
    model_map = dict(
        sorted(model_map.items(), key=lambda x: sum(x[1].values()), reverse=True)
    )

    # Records
    for model in model_map:
        model_map[model] = {
            k: round(v, c.DECIMAL_PLACES)
            for k, v in sorted(
                model_map[model].items(), key=lambda x: x[1], reverse=True
            )
        }

    return model_map

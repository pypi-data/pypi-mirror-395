from odoo_deets.utils import parse_deetsfile
from odoo_deets import config as c
import pygal


def pie(deetsfile):
    data, total = mem_by_model(deetsfile)
    pie = pygal.Pie()
    pie.title = f"Cumulative Memory Use ({round(total, c.DECIMAL_PLACES)} MB) by Model"
    for k, v in data.items():
        pie.add(k, v)

    return (pie.render(is_unicode=True), total)


def cum_mem(model_dict):
    """
    Sum up the memory taken by all fields for all records in a model for a given entry
    """
    mem = 0
    for fields in model_dict.values():
        for mem_mb in fields.values():
            mem += mem_mb

    return mem


def mem_by_model(deetsfile):
    """
    Prepare a dict mapping model: cum_memory for all entries which were recorded
    """
    entries = parse_deetsfile(deetsfile)

    model_map = {}

    total_cum = 0

    for e in entries:
        for model in e:
            cm = cum_mem(e[model])
            model_map[model] = model_map.get(model, 0) + cm
            total_cum += cm

    # Sort by mem desc
    model_map = dict(sorted(model_map.items(), key=lambda x: x[1], reverse=True))

    return (
        {m: round(mem, c.DECIMAL_PLACES) for m, mem in model_map.items()},
        total_cum,
    )

from . import analysis as a
from . import config as conf


def render_html(deetsfile: str):
    # Make a bunch of charts
    charts = []

    mem_by_model_data, cum_mem = a.m_b_m_pie(deetsfile)
    charts.append(mem_by_model_data)

    # Make a new path for the HTML output
    html_path = deetsfile[:-5] + "html"
    # Add to HTML page. it works, okay?

    m_b_r_table_html = ""
    m_b_r_tables = a.m_b_r_tables(deetsfile)

    # Memory by record tables
    for c in m_b_r_tables:
        m_b_r_table_html += f"""
            <div>
                <h3>{c[1]}</h3>
                <p class="subtitle">{round(c[2], conf.DECIMAL_PLACES)} MB</p>
                {c[0]}
            </div>
        """

    # Memory by field tables
    m_b_f_table_html = ""
    m_b_f_tables = a.m_b_f_tables(deetsfile)

    for c in m_b_f_tables:
        m_b_f_table_html += f"""
            <div>
                <h3>{c[1]}</h3>
                <p class="subtitle">{round(c[2], conf.DECIMAL_PLACES)} MB</p>
                {c[0]}
            </div>
        """

    html = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <script type="text/javascript" src="http://kozea.github.com/pygal.js/latest/pygal-tooltips.min.js"></script>
                <link rel="stylesheet" type="text/css" href="{conf.CSS_URL}">
            </head>
            <body>
                <div class="titlebar">
                    <h1>The Deets</h1>
                </div>

                <div class="content">
                    <h2>Total cumulative field memory use: {round(cum_mem, conf.DECIMAL_PLACES)} MB</h2>
                    <div class="figcontainer">
                        <figure>
                            {charts[0]}
                        </figure>
                    </div>

                    <h2>Records IDs Ordered by Cumulative Memory Use (by Model, limit {conf.TABLE_LIMIT})</h2>

                    <div class="tablerow">
                        {m_b_r_table_html}
                    </div>

                    <h2>Fields Ordered by Cumulative Memory Use (by Model, limit {conf.TABLE_LIMIT})</h2>

                    <div class="tablerow">
                        {m_b_f_table_html}
                    </div>

                </div>




            </body>
        </html>



"""

    with open(html_path, "a") as out:
        out.write(html)

    return html_path

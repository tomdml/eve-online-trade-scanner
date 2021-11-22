import pandas as pd
import os

url = os.path.join('render', 'output.html')


def render_to_html(summary):
    # Make pretty
    summary.index.name = None
    pd.options.display.float_format = '{:20,.2f}'.format
    formatters = {
        'Margin': '{:,.2%}'.format,
        'typeID': '{:05}'.format,
    }

    summary = summary[[
        'typeID', 'Total Profit', 'Product Cost',
        'Product Revenue', 'Profit', 'Margin',
        'Mean Volume', 'Haul Size'
    ]]

    # Output to HTML table
    with open(url, 'w+') as fp:
        fp.write('<link rel="stylesheet" href="style.css">')
        fp.write(summary.to_html(
            formatters=formatters,
            bold_rows=False
        ))

    return url

from dash import dcc
from dash import html
"""
    Supported Components
    1. Table
    2. Pie Chart
    3. Bar Chart
    4. Dough Nut Chart
    5. Line Chart
"""

"""
    This method is to import basic skeleton of any chart or component
    Supported Charts :
        1. Pie Chart            : pie
        2. Dough Nut Chart      : dough-nut
        3. Bar Chart            : bar
        4. Line Chart           : line
    Supported Components:
        1. Table                : table
        2. Span                 : span
        3. Heading (H1-H6)      : heading

    Inputs are :
        param1: type - defines which type component you want to integrate
            values:
                'table'
                'pie' or 'dough-nut'
                'bar'
                'line'
        param2: id - it should be unique across the component and which is used to refer callback methods: Should Not DUPLICATE values
        param3: title - describes the title of your component
        param4: title_sytle - defines style for the title, accepts (H1 to H6), default='H6'
            values:
                'H1' or 'H2' or 'H3' or 'H4' or 'H5' or 'H6'
        param5: style -  defines the component structure either full or side-by-side
            values:
                For full size:
                    'full'
                    '1x1'
                For side-by-side:
                    'half'
                    'side-by-side'
                    '1x2'
        param6: class_name - define the style of component's div, default='row mx-0' 
"""


def component(type, id, title, title_style='H6', style='Full', class_name='row mx-0'):
    div = html.Div([])
    style = get_style_classname(style)
    if type is not None:
        if type.lower() == 'table':
            div = get_table_component(id, title, title_style, style)
        elif type.lower() == 'bar':
            div = get_chart_component(id, title, title_style, style)
        elif (type.lower() == 'pie' or type.lower() == 'dough-nut'):
            div = get_chart_component(id, title, title_style, style)
        elif (type.lower() == 'line'):
            div = get_chart_component(id, title, title_style, style)
        elif (type.lower() == 'span'):
            return get_span_component(id, title)
        elif (type.lower() == 'heading'):
            return get_header_component(title, title_style, style)
    if style == 'twelve columns':
        full_div = html.Div([
            div,
        ],
            className=class_name,
        )
        return full_div
    return div


def get_table_component(key, title, title_style, style):
    return html.Div(
        [
            get_header_component(title, title_style),
            html.Table(id=key),
        ],
        className=style,
    )


def get_chart_component(key, title, title_style, style):
    return html.Div(
        [
            get_header_component(title, title_style),
            dcc.Graph(
                id=key,
                config={"displayModeBar": False},
            ),
        ],
        className=style,
    )


def get_style_classname(style):
    if style is not None:
        if (style.lower() == 'full' or style.lower() == '1x1'):
            return 'twelve columns'
        elif (style.lower() == 'half' or style.lower() == 'side-by-side' or style.lower() == '1x2'):
            return 'six columns'


def get_header_component(title, style, class_name="subtitle padded"):
    if style is None:
        style = 'H6'

    if style.upper() == 'H1':
        return html.H1(title, className=class_name)
    elif style.upper() == 'H2':
        return html.H2(title, className=class_name)
    elif style.upper() == 'H3':
        return html.H3(title, className=class_name)
    elif style.upper() == 'H4':
        return html.H4(title, className=class_name)
    elif style.upper() == 'H5':
        return html.H5(title, className=class_name)
    else:
        return html.H6(title, className=class_name)


def get_span_component(key, title):
    if title is None or title == '':
        title = "-"
    return html.Span([title], id=key)

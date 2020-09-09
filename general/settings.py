

def init():
    global sql
    sql = None

    global colors
    colors = {
        'Alpha' : {'color_line': 'rgba(255, 0, 0, 1.0)'  , 'color_fill': 'rgba(255, 0, 0, 0.2)'}  ,
        'Beta'  : {'color_line': 'rgba(0, 0, 255, 1.0)'  , 'color_fill': 'rgba(0, 0, 255, 0.2)'}  ,
        'RM'    : {'color_line': 'rgba(0, 0, 255, 1.0)'  , 'color_fill': 'rgba(0, 0, 255, 0.2)'}  ,
        'RF'    : {'color_line': 'rgba(0, 0, 255, 1.0)'  , 'color_fill': 'rgba(0, 0, 255, 0.2)'}  ,
        'c_rate': {'color_line': 'rgba(0, 155, 255, 1.0)', 'color_fill': 'rgba(0, 155, 255, 0.2)'},
        'd_rate': {'color_line': 'rgba(0, 255, 255, 1.0)', 'color_fill': 'rgba(0, 255, 255, 0.2)'},

        'growth_rate' : {'color_line': 'rgba(0, 255, 255, 1.0)', 'color_fill': 'rgba(0, 255, 255, 0.2)'},
        'NAV'         : {'color_line': 'rgba(127, 0, 127, 1.0)', 'color_fill': 'rgba(127, 0, 127, 0.2)'},
        'Unfunded'    : {'color_line': 'rgba(255, 165, 0, 1.0)', 'color_fill': 'rgba(255, 165, 0, 0.2)'},
        'Called'      : {'color_line': 'rgba(255, 100, 0, 1.0)', 'color_fill': 'rgba(255, 100, 0, 0.2)'},
        'Distributed' : {'color_line': 'rgba(255, 200, 0, 1.0)', 'color_fill': 'rgba(255, 200, 0, 0.2)'}

    }

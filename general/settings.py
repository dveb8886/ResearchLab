

def init():
    global sql
    sql = None

    global colors
    colors = {
        'Red'   : {'color_line': 'rgba(255, 0, 0, 1.0)'  , 'color_fill': 'rgba(255, 0, 0, 0.2)'  },
        'Blue'  : {'color_line': 'rgba(0, 0, 255, 1.0)'  , 'color_fill': 'rgba(0, 0, 255, 0.2)'  },
        'Cyan'  : {'color_line': 'rgba(0, 255, 255, 1.0)', 'color_fill': 'rgba(0, 255, 255, 0.2)'},
        'Purple': {'color_line': 'rgba(127, 0, 127, 1.0)', 'color_fill': 'rgba(127, 0, 127, 0.2)'},
        'Orange': {'color_line': 'rgba(255, 165, 0, 1.0)', 'color_fill': 'rgba(255, 165, 0, 0.2)'}
    }

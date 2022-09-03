import PySimpleGUI as sg
from news_parser import news


def gui():
    cnn = news(filtering=True)
    header_list = cnn.section_list
    
    sg.theme('DarkTanBlue')  # Add a touch of color
    # All the stuff inside your window.
    layout = [[sg.Text('This simple GUI is only for experimentation!')],
            [sg.Text('Enter CNN Section: '), sg.Combo(header_list)],
            [sg.Text('Open File with path:'), sg.InputText()],
            [sg.Button('Open file'), sg.Button('NEWS'), sg.Button('Cancel')]]

    # Create the Window
    window = sg.Window('Parsing CNN News - playground', layout)
    
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Cancel':
            # if user closes window or clicks cancel
            break

        if event == 'Open file':
            try:
                f_in = open(values[1], 'r')
                for line in f_in:
                    print(line)
            except FileNotFoundError:
                print('File was not found!')

        if event == 'NEWS':
            section = values[0]
            cnn.set_section(section)
            print(cnn.get_headlines())
            
    window.close()


if __name__ == '__main__':
    gui()
    
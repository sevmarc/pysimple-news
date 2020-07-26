import PySimpleGUI as sg
from news_parser import news


sg.theme('DarkTanBlue')  # Add a touch of color
# All the stuff inside your window.
layout = [[sg.Text('This simple GUI is only for experimentation!')],
          [sg.Text('Enter CNN Section: '), sg.InputText()],
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
        URL_BASE = 'https://edition.cnn.com'
        SECTION = '/' + values[0]
        news(URL_BASE, SECTION)

window.close()

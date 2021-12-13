import PySimpleGUI as sg
import pyqrcode

# Convert from color code to tuple of RGB values plus alpha
def color_code_to_tuple(color_code):
    c = (eval("0x" + color_code[i : i + 2]) for i in (1, 3, 5))
    return tuple(c) + (255,)


input_layout = sg.Frame(
    "Input text", [[sg.InputText(key="-IN-", expand_x=True)]], expand_x=True
)

slider_layout = sg.Frame(
    "Size Setting",
    [
        [
            sg.Frame(
                "Scale",
                [
                    [
                        sg.Slider(
                            range=(1, 10),
                            default_value=5,
                            orientation="h",
                            key="-SCALE-",
                            expand_x=True,
                            tooltip="Scale of the QR code",
                        )
                    ]
                ],
                element_justification="center",
                expand_x=True,
                expand_y=True,
            ),
            sg.Frame(
                "Quiet Zone",
                [
                    [
                        sg.Slider(
                            range=(0, 5),
                            default_value=4,
                            orientation="h",
                            key="-QUIETZONE-",
                            expand_x=True,
                            tooltip="Quiet zone around the QR code",
                        )
                    ]
                ],
                element_justification="center",
                expand_x=True,
                expand_y=True,
            ),
        ]
    ],
    element_justification="center",
    expand_x=True,
    expand_y=True,
)

color_layout = sg.Frame(
    "Color",
    [
        [
            sg.In(key="-FGCOLOR-", visible=False),
            sg.In(key="-BGCOLOR-", visible=False),
            sg.ColorChooserButton("Foreground", target="-FGCOLOR-", tooltip="Foreground color"),
            sg.ColorChooserButton("Background", target="-BGCOLOR-", tooltip="Background color"),
        ]
    ],
    element_justification="center",
    expand_x=True,
)

button_layout = sg.Column(
    [
        [
            sg.Button("Generate", size=(8,), tooltip="Generate QR code"),
            sg.Button("Save", size=(8,), disabled=True, tooltip="Save QR code"),
            sg.Button("Exit", size=(8,), tooltip="Exit application"),
        ]
    ],
    justification="center",
)
image_layout = sg.Frame(
    "Preview",
    [[sg.Image(filename="", key="-IMAGE-")]],
    element_justification="center",
    expand_x=True,
    expand_y=True,
)

layout = [
    [input_layout],
    [slider_layout],
    [color_layout],
    [button_layout],
    [image_layout],
]

# Create the window
window = sg.Window("QR Code Generator", layout)

# Set default colors
fgcolor = (0, 0, 0, 255)
bgcolor = (255, 255, 255, 255)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the Exit button
    if event in ["Exit", None]:
        break
    # Generate QR Code
    if event == "Generate":
        try:
            data = values["-IN-"]
            scale = int(values["-SCALE-"])
            quietzone = int(values["-QUIETZONE-"])
            if data:
                print(data)
                qr = pyqrcode.create(data)
                if values["-FGCOLOR-"]:
                    fgcolor = color_code_to_tuple(values["-FGCOLOR-"])
                if values["-BGCOLOR-"]:
                    bgcolor = color_code_to_tuple(values["-BGCOLOR-"])
                window["-IMAGE-"].update(
                    data=qr.png_as_base64_str(
                        scale=scale,
                        module_color=fgcolor,
                        background=bgcolor,
                        quiet_zone=quietzone,
                    )
                )
                window["Save"].update(disabled=False)
            else:
                sg.popup("Please enter text to encode")
        except:
            window["Save"].update(disabled=True)
            sg.popup_error("Error", "Invalid input")
    # Save QR Code
    if event == "Save":
        try:
            scale = int(values["-SCALE-"])
            quietzone = int(values["-QUIETZONE-"])
            filename = sg.popup_get_file(
                "Save As",
                save_as=True,
                file_types=(("PNG", "*.png"),),
                default_extension=".png",
                no_window=True,
            )
            if filename:
                qr.png(
                    filename,
                    scale=scale,
                    module_color=fgcolor,
                    background=bgcolor,
                    quiet_zone=quietzone,
                )
                sg.popup("Saved", filename)
                print(filename)
        except:
            sg.popup_error("Error", "Invalid input")

window.close()

from pathlib import Path
import json

from wiliot_tools.test_equipment.test_equipment import ZebraPrinter

label = """
^XA

^FX Third section with bar code.
^BY5,2,270
^FO100,550^BC^FD12345078^FS

^FX Fourth section (the two boxes on the bottom).
^FO50,900^GB700,250,3^FS
^FO400,900^GB3,250,3^FS
^CF0,40
^FO100,960^FDCtr. X34B-1^FS
^FO100,1010^FDREF1 F00B47^FS
^FO100,1060^FDREF2 BL4H8^FS
^CF0,190
^FO470,955^FDCA^FS

^XZ
"""

# You can create and edit labels here: https://labelary.com/viewer.html
printer_params = {}
try:
    json_path = Path(__file__).parents[4] / 'pywiliot-testers' / 'wiliot_testers' / 'association_tester' / 'configs' / 'r2r_printer_params.json'
    with open(json_path, 'r') as f:
        printer_params = json.load(f)
except Exception as e:
    print(f"Failed to load printer params from json: {e}")
p = ZebraPrinter(**printer_params)

# print simple label given as ZPL
p.print_label(label)

# print label from label_format_path and label_content_path
s = p.print_next_label()

# save example label to file
with open(printer_params['label_format_path'][:-4] + '_example.txt', 'w') as f:
    f.write(s)

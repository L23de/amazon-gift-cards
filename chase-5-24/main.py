import math
from xml.etree.ElementTree import Element
from pdfquery import PDFQuery
from glob import glob
import dateparser
from datetime import datetime

# Number of cards to show (Defaults to 5 for Chase's 5/24)
NUM_CARDS = 5

experian_pdf_path = glob("**/experian.pdf")[0]

print(f"Loading {experian_pdf_path}...")

pdf = PDFQuery(experian_pdf_path)

pdf.load()

# NOTE: Cannot just use the first, there ae a couple pages that deviate
# Notably the pages that have the headers (E.g. 'Open Accounts' and 'Closed Accounts')
date_opened_labels: list[Element] = pdf.pq(
    "LTTextLineHorizontal:contains('Date opened')"
)

# Calculate the first page where accounts are listed
start_page = next(date_opened_labels[0].iterancestors("LTPage")).layout.pageid

dates: list[datetime] = []

for i, label in enumerate(date_opened_labels):
    attrib = label.attrib

    # 'Date opened' coords
    x0, y0, y1 = attrib.get("x0"), attrib.get("y0"), attrib.get("y1")
    x0, y0, y1 = float(x0), float(y0), float(y1)

    # Some "constants"
    field_width, field_height = 50, y1 - y0
    date_x_offset, date_y_offset = 195, 0
    name_x0_offset, name_y0_offset = 50, 66

    # Date bounding boxes
    x0, y0 = x0 + date_x_offset, y0 + date_y_offset
    x1, y1 = x0 + field_width, y1 + field_height

    # Name bounding boxes
    name_x0 = x0 - name_x0_offset
    name_y0 = y0 + name_y0_offset
    name_y1 = name_y0 + field_height + 1

    extracted: str = pdf.extract(
        [
            ("with_formatter", "text"),
            ("with_parent", f"LTPage[page_index='{i+start_page-1}']"),
            (
                "date",
                ':in_bbox("%s, %s, %s, %s")' % (x0, y0, x1, y1),
            ),
            (
                "name",
                ':in_bbox("%s, %s, %s, %s")' % (name_x0, name_y0, x1, name_y1),
            ),
        ]
    )

    date = extracted.get("date")
    formatted_date = " ".join(date.split(" ")[:3])
    formatted_date = dateparser.parse(formatted_date)

    name = extracted.get("name")
    formatted_name = name[: math.floor(len(name) / 2)]
    formatted_name = " ".join(formatted_name.split(" "))

    dates.append((formatted_name, formatted_date))

last_n_dates = sorted(dates, reverse=True, key=lambda x: x[1])[:5]
formatted_last_n_dates = [
    (name, date.strftime("%m/%d/%Y")) for (name, date) in last_n_dates
]

print("----------------")
print("Last 5 Cards:")
print("----------------")
for card, date in formatted_last_n_dates:
    print(date, "-", card)

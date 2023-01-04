import calendar
import datetime

from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4, letter, landscape

# Config parameters
year = 2023
start_weekday = 6  # 1st day of week; 0: Monday, 6: Sunday
holiday_region = 'DE'  # 'None': other, 'US': USA, 'JP': Japan, etc.
remove_1wk = False  # Remove 1st week if the month consumes 6 week rows
pagesize = 0  # 0: A4, 1: Letter

efont = "Helvetica"
jfont = "HeiseiKakuGo-W5"

fileName = f'cal{year}.pdf'
if holiday_region:
    import holidays

pagesizes = [A4, letter]
height, width = pagesizes[pagesize]
cell_width = (width - 48)/7

calendar.setfirstweekday(start_weekday)

canvas = Canvas(fileName, pagesize=landscape(pagesizes[pagesize]))
canvas.setTitle(str(year))

pdfmetrics.registerFont(UnicodeCIDFont(jfont))

months = ('January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December')
week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
             'Friday', 'Saturday', 'Sunday']
week_days = (week_days[start_weekday:] + week_days[:start_weekday])

for m, month in enumerate(months, start=1):
    weeks = calendar.monthcalendar(year, m)
    if remove_1wk and len(weeks) == 6:  # 6 weeks per the month
        weeks.pop(0)
    cell_height = (height - 108 - 32)/len(weeks)
    canvas.setStrokeColorRGB(0, 0, 0)
    canvas.setFont(efont, 48)
    canvas.drawString(32, height-64, str(m))
    canvas.drawString(width-140, height-64, str(year))
    canvas.setFont(efont, 26)
    canvas.drawString(96, height-60, month)
    canvas.setFont(efont, 16)

    # draw horizontal lines
    for i in range(len(weeks)):
        canvas.line(24, height - 108 - cell_height*i,
                    24 + cell_width*7, height - 108 - cell_height*i)
    canvas.line(24, 32, 24 + cell_width*7, 32)

    # put weekdays and draw vertical lines
    for i, day in enumerate(week_days):
        if day == 'Saturday':
            canvas.setFillColorRGB(0, 0, 1)  # blue
        elif day == 'Sunday':
            canvas.setFillColorRGB(1, 0, 0)  # red
        canvas.drawString(28 + i*cell_width, height - 96, day)
        canvas.setFillColorRGB(0, 0, 0)
        if i != 0:
            canvas.line(24 + i*cell_width, height - 108,
                        24 + i*cell_width, 32)

    canvas.setFont(efont, 26)
    for w, week in enumerate(weeks):
        wd = week_days[:]
        for i, date in enumerate(week):
            if date:
                holiday = None
                if holiday_region:
                    canvas.setFont(efont, 9)
                    if holiday_region == 'JP':
                        canvas.setFont(jfont, 12)
                    holiday = holidays.country_holidays(
                        holiday_region).get(
                        datetime.date(year, m, date))
                if holiday:
                    holiday = holiday[:24]
                    canvas.drawString(28 + i*cell_width,
                                      height - 148 - cell_height*w,
                                      holiday)
                canvas.setFont(efont, 26)
                if wd[i] == 'Saturday':
                    canvas.setFillColorRGB(0, 0, 1)  # blue
                if wd[i] == 'Sunday' or holiday:
                    canvas.setFillColorRGB(1, 0, 0)  # red
                canvas.drawString(28 + i*cell_width,
                                  height - 132 - cell_height*w, str(date))
                canvas.setFillColorRGB(0, 0, 0)
    canvas.showPage()  # next page/month
canvas.save()

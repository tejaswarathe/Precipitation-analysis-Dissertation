import os

periods = ['historical', 'period1', 'period2']



indices = ['CDD', 'CWD', 'SDII', 'PRCPTOT', 'R10mm', 'R20mm', 'R95PTOT', 'R99PTOT', 'Rx1day', 'Rx5day']

for period in periods:
    path = 'Code\Calculations\\' + period

    for index in indices:
        os.system('python ' + path + '\\' + index + '_' + period)
        
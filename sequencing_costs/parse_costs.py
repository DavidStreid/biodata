



def parse(raw):
    return raw.strip().split('\t')

def convert_abbreviated_date(abbreviated_date):
    # Define a dictionary to map month abbreviations to numbers
    month_mapping = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                     'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                     'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

    # Convert the abbreviated date to the corresponding number
    month_abbreviation = abbreviated_date[:3]
    if month_abbreviation in month_mapping:
        month_number = month_mapping[month_abbreviation]
        return month_number
    else:
        return None  # Return None for invalid month abbreviations


def read_tsv():
    with open('SEQUENCING_COST_HISTORY.tsv', 'r') as in_f:
        headers = parse(in_f.readline())

        # "2016-09-19T10:24:08.741Z"
        for line in in_f:
            e = dict(zip(headers, parse(line)))
            # print(e)
            [month, year] = e['Date'].split('-')
            day = '01'
            month = convert_abbreviated_date(month)
            fmt_date = f"{year}-{month}-{day}T00:00:00.000Z"
            fmt_date = f"{month}-{day}-{year}"
            fmt_date = f"20{year}-{month}-{day}"

            cost = int(e['Cost per Genome'].replace('$', '').replace(',', ''))

            graph_dp = {
                'name': f'new Date("{fmt_date}")',
                'value': cost
            }
            print(f'{graph_dp},')


def output_x_ticks():
    ticks = []
    for i in range(1,9):
        ticks.append(f"01-01-0{i}")
    for i in range(10,23):
        ticks.append(f"01-01-{i}")
    print(ticks)




if __name__ == '__main__':
    read_tsv()
    # output_x_ticks()
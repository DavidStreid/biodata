import sys
import subprocess
import json

MONTHS_BACK = 175

def parse_results(result_file):
    result_dic = {}
    with open(result_file, 'r') as in_f:
        results = json.load(in_f)
        for tag, tag_info in results.items():
            ct = tag_info["total"]
            result_dic[tag] = ct
    return result_dic

def send_queries(tag_dic, fname):
    print(f"Retrieving queries from the past ~{int(MONTHS_BACK/12)} years")
    month_list = range(1,MONTHS_BACK)
    for month in month_list:
        out_f = f'results_{month}.json'
        cmd=f'curl -X POST -F "months={month}" -F "tags=@{fname}" https://www.biostars.org/api/tags/list/ > {out_f}'
        subprocess.run(cmd, shell=True, check=True)
        result_dic = parse_results(out_f)
        for tag in tag_dic.keys():
            cumm_ct = result_dic[tag]
            tag_dic[tag]['months'][month] = {
                'cummulative': cumm_ct
            }
            prev = month-1
            if prev in tag_dic[tag]['months']:
                tag_dic[tag]['months'][month]['ct'] = cumm_ct - tag_dic[tag]['months'][prev]['cummulative']
            else:
                tag_dic[tag]['months'][month]['ct'] = cumm_ct

            print(f"{tag}\t{month}\t{cumm_ct}")


def write_tag_dic(tag_dic):
    ct_file = 'biostars_summary.tsv'

    headers = []
    lines = []

    months = set([])

    columns = []
    for tag, tag_info in tag_dic.items():
        col=[]
        col.append(tag)
        # label = tag_info['label']
        # line = [tag, label]
        for month, month_info in tag_info['months'].items():
            # months.add(month)
            month_ct = month_info['ct']
            col.append(str(month_ct))
            # line.append(str(month_ct))
        columns.append(col)
        # lines.append(line)

    headers = [ 'tag', 'label' ]
    for month in sorted(list(months)):
        headers.append(f'm{month}')

    headers = [ 'month' ] + [ c[0] for c in columns ]
    with open(ct_file, 'w') as out_f:
        out_f.write('\t'.join(headers) + '\n')
        for i in range(1, len(columns) - 1):
            vals = '\t'.join(c[i] for c in columns)
            line = f'm{i}\t{vals}\n'
            out_f.write(line)
        # for line in lines:
            # out_f.write('\t'.join(line) + '\n')

def run():
    tag_file = sys.argv[1]
    tag_dic, query_tag_file = read_tsv(tag_file)
    send_queries(tag_dic, query_tag_file)
    write_tag_dic(tag_dic)



def read_tsv(fname):
    tag_dic = {}
    query_tag_file = 'query.txt'
    with open(fname, 'r') as in_f, open(query_tag_file, 'w') as out_f:
        header = in_f.readline().strip('\n').split('\t')
        for raw_line in in_f:
            line = raw_line.strip('\n')
            vals = line.split('\t')
            entry = dict(zip(header, vals))
            label = entry['label']
            tag = entry['tag']
            out_f.write(f'{tag}\n')
            tag_dic[tag] = {
                'label': label,
                'months': {}
            }

    return tag_dic, query_tag_file


if __name__ == '__main__':
    run()
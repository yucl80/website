import sys
import json
import shutil

COUNTER = 1
INFO = 2

INTEGER = 2
STRING = 1
TIMESTAMP = 6

def load_data(filename):
    with open(filename, 'r') as f:
        csv_stats = f.readlines()
    header = csv_stats[0].strip().split(',')
    stats = {}
    for line in csv_stats[1:]:
        parts = line.strip().split(',', 3)
        if len(parts) != 4:
            print parts
        assert len(parts) == 4
        stat = {}
        stat['name'] = parts[header.index('column_name')]
        stat['summary'] = parts[header.index('description')]
        stat['metric_type'] = parts[header.index('metric_type')]
        vartype = parts[header.index('data_type')]
        if vartype == 'oid' or vartype == 'bigint' or vartype == 'double precision' or vartype == 'integer':
            vartype = INTEGER
        elif vartype == 'name' or vartype == 'text':
            vartype = STRING
        elif vartype.startswith('timestamp'):
            vartype = TIMESTAMP
        else:
            raise Exception(vartype)
        stat['vartype'] = vartype
        stats[stat['name']] = stat
    return stats

dbstats = load_data('pg96_database_stats.csv')
gstats = load_data('pg96_global_stats.csv')
istats = load_data('pg96_index_stats.csv')
tstats = load_data('pg96_table_stats.csv')

with open('metrics_sample.json', 'r') as f:
    metrics = json.load(f)

final_metrics = []
vartypes = set()
for view_name, mets in metrics.iteritems():
    if 'database' in view_name:
        scope = 'database'
        stats = dbstats
    elif 'indexes' in view_name:
        scope = 'index'
        stats = istats
    elif 'tables' in view_name:
        scope = 'table'
        stats = tstats
    else:
        scope = 'global'
        stats = gstats

    for metric_name in mets:
        entry = {}
        entry['model'] = 'website.MetricCatalog'
        mstats = stats[metric_name]
        fields = {}
        fields['name'] = '{}.{}'.format(view_name, metric_name)
        fields['vartype'] = mstats['vartype']
        vartypes.add(fields['vartype'])
        fields['summary'] = mstats['summary']
        fields['scope'] = scope
        metric_type = mstats['metric_type']
        if metric_type == 'counter':
            mt = COUNTER
        elif metric_type == 'info':
            mt = INFO
        else:
            raise Exception('Invalid metric type: {}'.format(metric_type))
        fields['metric_type'] = mt
        fields['dbms'] = 1
        entry['fields'] = fields
        final_metrics.append(entry)

with open('postgres-96_metrics.json', 'w') as f:
    json.dump(final_metrics, f, indent=4)

shutil.copy('postgres-96_metrics.json', '../../preload/postgres-96_metrics.json')

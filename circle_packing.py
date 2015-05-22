import csv
import json
import sys

def mtable_to_json(mg_abundance):
    """
    Convert a list of functional abundance data (level1,level2,level3,level4,abundance) into
    a hierarchical JSON file: {name: ..., children: [name:..., size:...]}
    """
    hierarchy = {'name': 'metagenome', 'children':[]}
    for entry in mg_abundance:
        L1_idx = -1
        lvl1, lvl2, lvl3, lvl4, count = entry[0], entry[1], entry[2], entry[3], float(entry[4])
        for i, c in enumerate(hierarchy['children']):
            if c['name'] == lvl1:
                L1_idx = i
                break
        else:
            hierarchy['children'].append({'name':lvl1,
                                          'children':[{'name':lvl2,
                                                       'children':[{'name':lvl3,
                                                                    'children':[{'name':lvl4, 'size':count}]}]}]})
            continue
        if L1_idx > -1:
            L2_idx = -1
            for j, c in enumerate(hierarchy['children'][L1_idx]['children']):
                if c['name'] == lvl2:
                    L2_idx = j
                    break
            else:
                hierarchy['children'][L1_idx]['children'].append({'name': lvl2,
                                                                  'children':[{'name':lvl3,
                                                                               'children':[{'name':lvl4, 'size':count}]}]})
                continue
        if L2_idx > -1:
            for c in hierarchy['children'][L1_idx]['children'][L2_idx]['children']:
                if c['name'] == lvl3:
                    c['children'].append({'name':lvl4, 'size':count})
                    break
            else:
                hierarchy['children'][L1_idx]['children'][L2_idx]['children'].append({'name': lvl3,
                                                                                      'children':[{'name':lvl4, 'size':count}]})

    return hierarchy


def mtable_to_json_3lvls(mg_abundance):
    """
    Convert a list of KEGG orthology abundance data (level1,level2,level3,abundance) into
    a hierarchical JSON file: {name: ..., children: [name:..., size:...]}
    """
    hierarchy = {'name': 'metagenome', 'children':[]}
    for entry in mg_abundance:
        index = -1
        lvl1, lvl2, lvl3, count = entry[0], entry[1], entry[2], sum(map(float,entry[3:]))
        for i,c in enumerate(hierarchy['children']):
            if c['name'] == lvl1:
                index = i
                break
        else:
            hierarchy['children'].append({'name':lvl1, 'children':[{'name':lvl2, 'children':[{'name':lvl3, 'size':count}]}]})
            continue
        if index > -1:
            for c in hierarchy['children'][index]['children']:
                if c['name'] == lvl2:
                    c['children'].append({'name':lvl3, 'size':count})
                    break
            else:
                hierarchy['children'][index]['children'].append({'name': lvl2, 'children':[{'name':lvl3, 'size':count}]})
    return hierarchy


def mtable_to_json_2lvls(mg_abundance):
    """
    Convert a list of KEGG orthology abundance data (level1,level2,abundance) into
    a hierarchical JSON file: {name: ..., children: [name:..., size:...]}
    """
    hierarchy = {'name': 'metagenome', 'children':[]}
    for entry in mg_abundance:
        index = -1
        lvl1, lvl2, count = entry[0], entry[1], sum(map(float,entry[2:]))
        for i,c in enumerate(hierarchy['children']):
            if c['name'] == lvl1:
                index = i
                break
        else:
            hierarchy['children'].append({'name':lvl1, 'children':[{'name':lvl2, 'size':count}]})
            continue
        if index > -1:
            hierarchy['children'][index]['children'].append({'name':lvl2, 'size':count})
    return hierarchy


def process_fc_data(fc_lvl_fp, json_out_fp, delim='\t', levels=4):
    """
    Takes as input a spreadsheet file containing hierarchical pathway/functional
    data and associated fold-changes (pos/neg indicating group A vs group B) and
    writes out a JSON file that can be input into the circle-packing viusalization.

    :type fc_lvl_fp: str
    :param fc_lvl_fp: Path to the fold-change data file.
    :type json_out_fp: str
    :param json_out_fp: Path to the output JSON file.
    :type delim: str
    :param delim: Optional delimiter for use while reading the input file.
                  Defaults to the tab character ('\t')
    :rtype: None
    """
    with open(fc_lvl_fp, 'rU') as in_f:
    	reader = csv.reader(in_f, delimiter=delim)
    	levels = len(reader.next())-1
    	sys.stdout.write(levels)
        fc_lvl_data = [line for line in reader]
    
    lvl_switch = {4: mtable_to_json, 3: mtable_to_json_3lvls, 2: mtable_to_json_2lvls}
	
    with open(json_out_fp, 'w') as out_f:
        json.dump(lvl_switch[levels](fc_lvl_data), out_f)





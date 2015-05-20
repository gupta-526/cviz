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



def process_fc_data(fc_lvl_fp, json_out_fp, delim='\t')
    """
    Takes a tab-delimited spreadsheet file as input with the f
    """
    with open(fc_lvl_fp, 'rU') as in_f:
        fc_lvl_data = [line for line in csv.reader(in_f, delimiter=delim)][1:]

    with open(json_out_fp, 'w') as out_f:
        json.dump(mtable_to_json(fc_lvl_data), out_f)
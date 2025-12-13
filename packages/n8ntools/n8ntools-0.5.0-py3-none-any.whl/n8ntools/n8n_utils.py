
def get_workflow_reg(wf):
    wf_reg=[]
    for i in wf['data']:
        wf_reg.append({"wf_id":i['id'],"wf_name":i['name'],"status":i['active']})
    return wf_reg
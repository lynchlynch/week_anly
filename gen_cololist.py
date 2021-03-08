#讲CU、DP等转化为03，04
def gen_cololist(vendor_list_str):
    vendor_list = []
    for single_vendor in vendor_list_str:
        if single_vendor == 'CT':
            vendor_list.append('01')
        elif single_vendor == 'CM':
            vendor_list.append('02')
        elif single_vendor == 'CU':
            vendor_list.append('03')
        else:
            vendor_list.append('04')
    return vendor_list
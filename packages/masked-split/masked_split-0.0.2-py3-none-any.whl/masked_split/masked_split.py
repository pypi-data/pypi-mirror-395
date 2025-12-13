import re
from intervalop.interval import contains, union, excluding, is_intersecting, remove_overlapping_intervals, complements

def get_delim_locations(s, delims):
    """
    s: text
    delims: ['ab', 'def']

    ..!..!?..!
    xxoxxooxxo
    0123456789
    """
    output = []
    shortest_delim_len = min([len(d) for d in delims])
    skip = 0
    for i in range(len(s) - shortest_delim_len + 1):
        if skip > 0:
            skip -= 1
        else:
            for d in delims:
                if i+(len(d)-1) <= (len(s)-1):
                    if s[i:i+len(d)] == d:
                        output.append([i, d])
                        skip = len(d)-1
                        break
    return output

def filter_out_nodes(nodes, filter_intervals):
    """
    nodes = [x, y, z]
    filter_intervals = [[a, b], [c, d]]
    """
    output = []
    filter_func = lambda x : not contains(filter_intervals, x)
    for n in filter(filter_func, nodes):
        output.append(n)
    return output

# now, get delimiter locations first, or masking first?
# what if there is a delimiter that, if masking is done first, the delimiter will not be detected?

def get_mask_locations(s, masks):
    """
    s: text
    masks: [['ab', 'cd'], ['e', 'fg']]

    .".."..{.}
    xooooxxooo
    0123456789

    ..{(..)}..
    xxooooooxx
    0123456789
    """
    output = []
    try:
        for m in masks:
            suboutput = []
            start = None
            end = None
            skip = 0
            for i in range(len(s)):
                if skip > 0:
                    skip -= 1
                else:
                    if start is None:
                        if i+(len(m[0])-1) <= len(s)-1:
                            if s[i:i+len(m[0])] == m[0]:
                                start = i
                                skip = len(m[0])-1
                    else:
                        if i+(len(m[1])-1) <= len(s)-1:
                            if s[i:i+len(m[1])] == m[1]:
                                end = i
                                skip = len(m[1])-1
                                suboutput.append([start, end])
                                start = None
                                end = None
            if suboutput:
                if output:
                    output = union(output, suboutput)
                else:
                    output = suboutput
    except Exception as e:
        print(f"Exception (get_mask_locations): {e}")
        print(s)
        print(masks)
    return output

def get_delim_intervals(delims):
    """
    delims: [[9, 'cd'], [12, '!'], [21, 'cd'], [26, '.'], [38, 'cd'], [47, '!']]

    ..{(...)}.
    xxooxxxoox
    0123456789
    """
    output = []
    for d in delims:
        output.append([d[0], d[0]+(len(d[1])-1)])
    return output

def get_parsed_region(s, delim_regions, include='none'):
    """
    s: text
    delim_regions = [[a, b], [c, d]]

    xooxxxxxox
    oxxoooooxo
    0123456789
    """
    if delim_regions == []:
        print("hi there!")
        output = [[0, len(s)-1]]
        return output
    U = [0, len(s)-1]
    output = complements(delim_regions, U)
    print(output)
    match include:
        case 'none':
            pass
        case 'left':
            output += delim_regions
            output.sort(key=lambda sublist : sublist[0])
            print("output and delim_regions")
            print(output)
            output2 = output
            output = []
            d = None
            for I in output2:
                print(f"d {d}")
                print(f"I {I}")
                print(output)
                if I in delim_regions:
                    # if d, grow d by I
                    # else d = I
                    if d:
                        d = [d[0], I[1]]
                    else:
                        d = I
                else:
                    # if d, pop out the previous element from output and append prev+d back. then append I.
                    # else, append I
                    if d:
                        if len(output)==0:
                            prev = [0, 0]
                        else:
                            prev = output.pop(-1)
                        output.append([prev[0], d[1]])
                        d = None
                    output.append(I)
            # in case output2 ending with I in delim_regions
            if d:
                prev = output.pop(-1)
                output.append([prev[0], d[1]])
                d = None
        case 'independent':
            output += delim_regions
            output.sort(key=lambda sublist : sublist[0])
            print(output)
        case 'right':
            output += delim_regions
            output.sort(key=lambda sublist : sublist[0])
            output2 = output
            output = []
            d = None
            for I in output2:
                if I in delim_regions:
                    # if d, grow d by I
                    # else d = I
                    # move one
                    if d:
                        d = [d[0], I[1]]
                    else:
                        d = I
                else:
                    # if d, add d+I to output
                    # else, add I to output
                    # move on
                    if d:
                        output.append([d[0], I[1]])
                        d = None
                    else:
                        output.append(I)
            # in case d is the last element of output2
            if d:
                output.append(d)
        case _:
            pass
    return output

def get_parsed_region2(s, delim_region, include='none'):
    """
    s: text
    delim_region = [[a, b], [c, d]]

    xooxxxxxox
    oxxoooooxo
    0123456789
    """
    parsed_region = [[0, 0]]
    prev_d = [0, 0]
    for d in delim_region:
        prev = parsed_region[-1]
        match include:
            case 'none':
                parsed_region.append([prev[1]+(prev_d[1]-prev_d[0]), d[0]])
            case 'left':
                parsed_region.append([prev[1], d[1]])
            case 'independent':
                parsed_region.append([prev[1], d[0]])
                parsed_region.append([d[0], d[1]])
            case 'right':
                parsed_region.append([prev[1], d[0]])
            case _:
                pass
        prev_d = d
    # last element
    prev = parsed_region[-1]
    # prev_d is still valid as the last delimiter
    match include:
        case 'none':
            parsed_region.append([prev[1]+(prev_d[1]-prev_d[0]), len(s)])
        case 'left':
            parsed_region.append([prev[1], len(s)])
        case 'independent':
            parsed_region.append([prev[1], len(s)])
        case 'right':
            parsed_region.append([prev[1], len(s)])
        case _:
            pass
    # Remove possible initial and final duplicates.
    output = parsed_region
    for I in parsed_region:
        if I[0] == I[1]:
            output.pop(output.index(I))
    return output

def masked_split(s, masks, delims, include='none', strip=False, debug=False):
    """
    s: text
    masks: [['\"', '\"'], ['\'', '\''], ['{', '}'], ...]
    delims: ['.', '!', '?', '{newline}', ...]
    include: 'none', 'left', 'independent', 'right'
    """
    try:
        mask_region = get_mask_locations(s, masks)
    except Exception as e:
        print(f"Exception 1 (maskedsplit): {e}")
        print(s)
        print(masks)
    try:
        delim_nodes = get_delim_locations(s, delims)
    except Exception as e:
        print(f"Exception 2 (maskedsplit): {e}")
    # from delimiter locations, create delimiter intervals.
    # from the delimiter intervals, drop disqualified delimiters.
    # disqualified delimiters: those that overlap with each other, and those that also overlap with mask region.
    try:
        delim_regions = get_delim_intervals(delim_nodes)
    except Exception as e:
        print(f"Exception 3 (maskedsplit): {e}")
    if debug:
        print(s)
        print("0....5....10...5....20...5....30...5....40...5....50...5....60...5....70...5....80...5....90...5....100..5....110..5....120..5....130..5....140..5....150..5....160..5....170..5....180..5....190..5....200..5")
        print(f"delim_regions before masked: {delim_regions}")
    try:
        delim_regions = excluding(delim_regions, mask_region)
    except Exception as e:
        print(f"Exception 4 (maskedsplit): {e}")
    if debug:
        print(f"mask_region: {mask_region}")
        print(f"delim_region after masked: {delim_regions}")
    # now delim_region is free from invading masked regions.
    # remove possible overlapping delimiters remaining
    try:
        delim_regions = remove_overlapping_intervals(delim_regions)
    except Exception as e:
        print(f"Exception 5 (maskedsplit): {e}")
    if debug:
        print(f"delim_region after removing overlaps: {delim_regions}")
    try:
        parsed_regions = get_parsed_region(s=s, delim_regions=delim_regions, include=include)
    except Exception as e:
        print(f"Exception 6 (maskedsplit): {e}")
    if debug:
        print(f"parsed_regions: {parsed_regions}")
        print(f"include: {include}")
        print(s)
        print("0....5....10...5....20...5....30...5....40...5....50...5....60...5....70...5....80")
    output = []
    for I in parsed_regions:
        p = s[I[0]:I[1]+1]
        if strip:
            p = p.strip()
        output.append(p)
    if output == []:
        output.append('')
    if debug:
        for o in output:
            print(o+'|')
        print('\n')
    return output

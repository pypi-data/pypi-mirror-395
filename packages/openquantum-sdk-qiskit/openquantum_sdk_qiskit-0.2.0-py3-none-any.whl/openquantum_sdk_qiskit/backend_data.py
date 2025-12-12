
from typing import List, Dict


def adj_to_edges(adj: Dict[str, List[str]], shift: int = 0) -> List[List[int]]:
    edges = []
    seen = set()
    for u_str, neighbors in adj.items():
        u = int(u_str) - shift
        for v_str in neighbors:
            v = int(v_str) - shift
            if u < v:
                pair = (u, v)
            else:
                pair = (v, u)
            if pair not in seen:
                edges.append([pair[0], pair[1]])
                seen.add(pair)
    return sorted(edges)


def fully_connected(n: int) -> List[List[int]]:
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            edges.append([i, j])
    return edges


# --- Rigetti Ankaa-3 ---
RIGETTI_ADJ = {
    '0': ['1', '7'], '1': ['0', '2', '8'], '2': ['1', '3', '9'], '3': ['2', '4', '10'],
    '4': ['3', '5', '11'], '5': ['4', '6', '12'], '6': ['5', '13'], '7': ['0', '8', '14'],
    '8': ['1', '7', '9', '15'], '9': ['2', '8', '10', '16'], '10': ['3', '9', '11', '17'],
    '11': ['4', '10', '12', '18'], '12': ['5', '11', '13', '19'], '13': ['6', '12', '20'],
    '14': ['7', '15', '21'], '15': ['8', '14', '16', '22'], '16': ['9', '15', '17', '23'],
    '17': ['10', '16', '18', '24'], '18': ['11', '17', '19', '25'], '19': ['12', '18', '20', '26'],
    '20': ['13', '19', '27'], '21': ['14', '22', '28'], '22': ['15', '21', '23', '29'],
    '23': ['16', '22', '24', '30'], '24': ['17', '23', '25', '31'], '25': ['18', '24', '26', '32'],
    '26': ['19', '25', '27', '33'], '27': ['20', '26'], '28': ['21', '29', '35'],
    '29': ['22', '28', '30', '36'], '30': ['23', '29', '31', '37'], '31': ['24', '30', '32', '38'],
    '32': ['25', '31', '33', '39'], '33': ['26', '32', '34', '40'], '34': ['33', '41'],
    '35': ['28', '36'], '36': ['29', '35', '37', '43'], '37': ['30', '36', '38', '44'],
    '38': ['31', '37', '39', '45'], '39': ['32', '38', '40', '46'], '40': ['33', '39', '41', '47'],
    '41': ['34', '40'], '43': ['36', '50'], '44': ['37', '45', '51'], '45': ['38', '44', '46', '52'],
    '46': ['39', '45', '47', '53'], '47': ['40', '46', '54'], '49': ['50', '56'],
    '50': ['43', '49', '51', '57'], '51': ['44', '50', '52', '58'], '52': ['45', '51', '53', '59'],
    '53': ['46', '52', '54', '60'], '54': ['47', '53', '55', '61'], '55': ['54', '62'],
    '56': ['49', '57', '63'], '57': ['50', '56', '58', '64'], '58': ['51', '57', '59', '65'],
    '59': ['52', '58', '60', '66'], '60': ['53', '59', '61', '67'], '61': ['54', '60', '62', '68'],
    '62': ['55', '61', '69'], '63': ['56', '64', '70'], '64': ['57', '63', '65', '71'],
    '65': ['58', '64', '66', '72'], '66': ['59', '65', '73'], '67': ['60', '68', '74'],
    '68': ['61', '67', '69', '75'], '69': ['62', '68', '76'], '70': ['63', '71', '77'],
    '71': ['64', '70', '72', '78'], '72': ['65', '71', '73', '79'], '73': ['66', '72', '74', '80'],
    '74': ['67', '73', '75', '81'], '75': ['68', '74', '76', '82'], '76': ['69', '75', '83'],
    '77': ['70', '78'], '78': ['71', '77', '79'], '79': ['72', '78', '80'],
    '80': ['73', '79', '81'], '81': ['74', '80', '82'], '82': ['75', '81', '83'],
    '83': ['76', '82']
}

RIGETTI_ANKAA_3_CAPS = {
    "version": 1,
    "n_qubits": 84,
    "timing": {
        "dt": 1e-9,  # Placeholder
        "durations": []
    },
    "native_ops": [
        {"name": "rx", "arity": 1, "params": ["theta"]},
        {"name": "rz", "arity": 1, "params": ["phi"]},
        {"name": "iswap", "arity": 2},
        {"name": "measure", "arity": 1}
    ],
    "supported_ops": [
        {"name": "cz", "arity": 2}, {"name": "xy", "arity": 2}, {"name": "ccnot", "arity": 3},
        {"name": "cnot", "arity": 2}, {"name": "cphaseshift", "arity": 2}, {"name": "cswap", "arity": 3},
        {"name": "h", "arity": 1}, {"name": "i", "arity": 1}, {"name": "iswap", "arity": 2},
        {"name": "phaseshift", "arity": 1}, {"name": "pswap", "arity": 2}, {"name": "rx", "arity": 1},
        {"name": "ry", "arity": 1}, {"name": "rz", "arity": 1}, {"name": "s", "arity": 1},
        {"name": "si", "arity": 1}, {"name": "swap", "arity": 2}, {"name": "t", "arity": 1},
        {"name": "ti", "arity": 1}, {"name": "x", "arity": 1}, {"name": "y", "arity": 1},
        {"name": "z", "arity": 1}
    ],
    "topology": {
        "directed_edges": False,
        "coupling_map": adj_to_edges(RIGETTI_ADJ, shift=0)
    },
    "noise": {},
    "qubit_properties": [],
    "limits": {"max_circuits": 1024},
    "features": ["measure"]
}

# --- IonQ Aria-1 ---
IONQ_ARIA_1_CAPS = {
    "version": 1,
    "n_qubits": 25,
    "timing": {"dt": None, "durations": []},
    "native_ops": [
        {"name": "gpi", "arity": 1, "params": ["phi"]},
        {"name": "gpi2", "arity": 1, "params": ["phi"]},
        {"name": "ms", "arity": 2, "params": ["phi0", "phi1"]},
        {"name": "measure", "arity": 1}
    ],
    "supported_ops": [
        {"name": "x", "arity": 1}, {"name": "y", "arity": 1}, {"name": "z", "arity": 1},
        {"name": "h", "arity": 1}, {"name": "s", "arity": 1}, {"name": "si", "arity": 1},
        {"name": "t", "arity": 1}, {"name": "ti", "arity": 1}, {"name": "v", "arity": 1},
        {"name": "vi", "arity": 1}, {"name": "rx", "arity": 1}, {"name": "ry", "arity": 1},
        {"name": "rz", "arity": 1}, {"name": "cnot", "arity": 2}, {"name": "swap", "arity": 2},
        {"name": "xx", "arity": 2}, {"name": "yy", "arity": 2}, {"name": "zz", "arity": 2}
    ],
    "topology": {
        "directed_edges": False,
        "coupling_map": fully_connected(25)
    },
    "noise": {},
    "limits": {"max_circuits": 1024},
    "features": ["measure"]
}

# --- IQM Emerald ---
IQM_EMERALD_ADJ = {
    '1': ['2', '5'], '2': ['1', '6'], '5': ['1', '4', '6', '11'], '6': ['2', '5', '7', '12'],
    '3': ['4', '9'], '4': ['3', '5', '10'], '9': ['3', '8', '10', '17'], '10': ['4', '9', '11'],
    '11': ['5', '10', '12', '19'], '7': ['6'], '12': ['6', '11', '13', '20'], '8': ['9', '16'],
    '16': ['8', '15', '17', '24'], '17': ['9', '16', '18', '25'], '19': ['11', '18', '20', '27'],
    '13': ['12', '14', '21'], '20': ['12', '19', '21', '28'], '14': ['13', '22'],
    '21': ['13', '20', '22', '29'], '22': ['14', '21', '30'], '15': ['16', '23'],
    '23': ['15', '24'], '24': ['16', '23', '25', '32'], '18': ['17', '19', '26'],
    '25': ['17', '24', '26', '33'], '26': ['18', '25', '27', '34'], '27': ['19', '26', '28', '35'],
    '28': ['20', '27', '29', '36'], '29': ['21', '28', '30', '37'], '30': ['22', '29', '31'],
    '32': ['24', '33'], '33': ['25', '32', '34', '41'], '34': ['26', '33', '35', '42'],
    '35': ['27', '34', '36', '43'], '36': ['28', '35', '37', '44'], '37': ['29', '36', '38', '45'],
    '31': ['30', '39'], '39': ['31', '38'], '41': ['33', '40', '42', '47'],
    '42': ['34', '41', '43', '48'], '43': ['35', '42'], '44': ['36', '45', '50'],
    '38': ['37', '39', '46'], '45': ['37', '44', '46', '51'], '46': ['38', '45'],
    '40': ['41'], '47': ['41', '48'], '48': ['42', '47', '49', '52'], '50': ['44', '51', '54'],
    '51': ['45', '50'], '49': ['48', '53'], '52': ['48', '53'], '53': ['49', '52', '54'],
    '54': ['50', '53']
}

IQM_EMERALD_CAPS = {
    "version": 1,
    "n_qubits": 54,
    "timing": {"dt": None, "durations": []},
    "native_ops": [
        {"name": "cz", "arity": 2},
        {"name": "prx", "arity": 1, "params": ["theta", "phi"]},
        {"name": "measure", "arity": 1}
    ],
    "supported_ops": [
        {"name": "ccnot", "arity": 3}, {"name": "cnot", "arity": 2}, {"name": "cphaseshift", "arity": 2},
        {"name": "cswap", "arity": 3}, {"name": "swap", "arity": 2}, {"name": "iswap", "arity": 2},
        {"name": "ecr", "arity": 2}, {"name": "cy", "arity": 2}, {"name": "cz", "arity": 2},
        {"name": "xy", "arity": 2}, {"name": "xx", "arity": 2}, {"name": "yy", "arity": 2},
        {"name": "zz", "arity": 2}, {"name": "h", "arity": 1}, {"name": "i", "arity": 1},
        {"name": "rx", "arity": 1}, {"name": "ry", "arity": 1}, {"name": "rz", "arity": 1},
        {"name": "s", "arity": 1}, {"name": "si", "arity": 1}, {"name": "t", "arity": 1},
        {"name": "ti", "arity": 1}, {"name": "v", "arity": 1}, {"name": "vi", "arity": 1},
        {"name": "x", "arity": 1}, {"name": "y", "arity": 1}, {"name": "z", "arity": 1},
        {"name": "prx", "arity": 1}, {"name": "cc_prx", "arity": 2}, {"name": "measure_ff", "arity": 1}
    ],
    "topology": {
        "directed_edges": False,
        "coupling_map": adj_to_edges(IQM_EMERALD_ADJ, shift=1)  # 1-based to 0-based
    },
    "noise": {},
    "limits": {"max_circuits": 1024},
    "features": ["measure"]
}

# --- IQM Garnet ---
IQM_GARNET_ADJ = {
    '1': ['2', '4'], '2': ['1', '5'], '4': ['1', '3', '5', '9'], '5': ['2', '4', '6', '10'],
    '3': ['4', '8'], '8': ['3', '9', '13'], '9': ['4', '8', '10', '14'], '6': ['5', '7', '11'],
    '10': ['5', '9', '11', '15'], '7': ['6', '12'], '11': ['6', '10', '12', '16'],
    '12': ['7', '11', '17'], '13': ['8', '14'], '14': ['9', '13', '15', '18'],
    '15': ['10', '14', '16', '19'], '16': ['11', '15', '17', '20'], '17': ['12', '16'],
    '18': ['14', '19'], '19': ['15', '18', '20'], '20': ['16', '19']
}

IQM_GARNET_CAPS = {
    "version": 1,
    "n_qubits": 20,
    "timing": {"dt": None, "durations": []},
    "native_ops": [
        {"name": "cz", "arity": 2},
        {"name": "prx", "arity": 1, "params": ["theta", "phi"]},
        {"name": "measure", "arity": 1}
    ],
    "supported_ops": [
        {"name": "ccnot", "arity": 3}, {"name": "cnot", "arity": 2}, {"name": "cphaseshift", "arity": 2},
        {"name": "cswap", "arity": 3}, {"name": "swap", "arity": 2}, {"name": "iswap", "arity": 2},
        {"name": "ecr", "arity": 2}, {"name": "cy", "arity": 2}, {"name": "cz", "arity": 2},
        {"name": "xy", "arity": 2}, {"name": "xx", "arity": 2}, {"name": "yy", "arity": 2},
        {"name": "zz", "arity": 2}, {"name": "h", "arity": 1}, {"name": "i", "arity": 1},
        {"name": "rx", "arity": 1}, {"name": "ry", "arity": 1}, {"name": "rz", "arity": 1},
        {"name": "s", "arity": 1}, {"name": "si", "arity": 1}, {"name": "t", "arity": 1},
        {"name": "ti", "arity": 1}, {"name": "v", "arity": 1}, {"name": "vi", "arity": 1},
        {"name": "x", "arity": 1}, {"name": "y", "arity": 1}, {"name": "z", "arity": 1},
        {"name": "prx", "arity": 1}, {"name": "cc_prx", "arity": 2}, {"name": "measure_ff", "arity": 1}
    ],
    "topology": {
        "directed_edges": False,
        "coupling_map": adj_to_edges(IQM_GARNET_ADJ, shift=1)  # 1-based to 0-based
    },
    "noise": {},
    "limits": {"max_circuits": 1024},
    "features": ["measure"]
}

import tempfile
from enum import Enum
from tcheckerpy.utils import call_tchecker

class Algorithm(Enum):
    REACH = 0 # standard reachability algorithm over the zone graph
    CONCUR19 = 1 # reachability algorithm over the local-time zone graph, with sync-subsumption
    COVREACH = 2 # reachability algorithm over the zone graph with inclusion subsumption
    ALU_COVREACH = 3 # reachability algorithm over the zone graph with aLU subsumption

class SearchOrder(Enum):
    BFS = "bfs" # breadth-first search
    DFS = "dfs" # depth-first search

class Certificate(Enum):
    GRAPH = 0 # graph of explored state-space
    SYMBOLIC = 1 # symbolic run to a state with searched labels if any
    CONCRETE = 2 # concrete run to a state with searched labels if any (only for reach and covreach)
    NONE = 3 # no certificate

def reach(sys_decl: str, algorithm: Algorithm, search_order: SearchOrder = SearchOrder.BFS, 
          certificate: Certificate = Certificate.NONE, labels: list[str] = [],
          block_size: int | None = None, table_size: int | None = None) -> tuple[bool, str, str]:
    """
    Checks for reachability of timed automaton.

    :param sys_decl: system declaration of timed automaton
    :param algorithm: algorithm to be used (see `tck_reach.Algorithm`)
    :param search_order: search order to be used (see `tck_reach.SearchOrder`)
    :param certificate: certificate type (see `tck_reach.Certificate`)
    :param labels: list of accepting labels
    :param block_size: block size for internal computation
    :param table_size: table size for internal computation
    :return: result of reachability check, statistics and certificate
    """
    
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(sys_decl.encode('utf-8'))
        temp_file_path = temp_file.name

    # convert list to string
    labels_str = ", ".join(labels)
        
    # call TChecker function
    stats, cert = call_tchecker.call_tchecker_function_in_new_process(
        func_name="tck_reach",
        argtypes=["ctypes.c_char_p", "ctypes.c_char_p", "ctypes.c_int", "ctypes.c_char_p",
                  "ctypes.c_int", "ctypes.POINTER(ctypes.c_int)", "ctypes.POINTER(ctypes.c_int)"],
        has_result=True,
        args=[temp_file_path, labels_str, algorithm.value, search_order.value,
              certificate.value, block_size, table_size]
    )
 
    return "REACHABLE true" in stats, stats, cert

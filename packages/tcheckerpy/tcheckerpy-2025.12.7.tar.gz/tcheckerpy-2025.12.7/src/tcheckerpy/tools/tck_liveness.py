import tempfile
from enum import Enum
from tcheckerpy.utils import call_tchecker

class Algorithm(Enum):
    COUVSCC = 0 # Couvreur's SCC-decomposition-based algorithm (search an accepting cycle that visits all labels)
    NDFS = 1 # nested depth-first search algorithm over the zone graph (search an accepting cycle with a state with all labels)

class Certificate(Enum):
    GRAPH = 0 # graph of explored state-space
    SYMBOLIC = 1 # symbolic lasso run with loop on labels (not for couvscc with multiple labels)
    NONE = 2 # no certificate

def liveness(sys_decl: str, algorithm: Algorithm, certificate: Certificate = Certificate.NONE, 
             labels: list[str] = [], block_size: int | None = None, table_size: int | None = None) -> tuple[bool, str, str]:
    """
    Checks whether timed automaton contains a cycle.

    :param sys_decl: system declaration of timed automaton
    :param algorithm: algorithm to be used (see `tck_liveness.Algorithm`)
    :param certificate: certificate type (see `tck_liveness.Certificate`)
    :param labels: list of accepting labels
    :param block_size: block size for internal computation
    :param table_size: table size for internal computation
    :return: result of liveness check (True iff timed automaton contains cycle), statistics and certificate
    """

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(sys_decl.encode('utf-8'))
        temp_file_path = temp_file.name
    
    # convert list to string
    labels_str = ", ".join(labels)

    # call the TChecker function
    stats, cert = call_tchecker.call_tchecker_function_in_new_process(
        func_name="tck_liveness",
        argtypes=["ctypes.c_char_p", "ctypes.c_char_p", "ctypes.c_int", "ctypes.c_int",
                  "ctypes.POINTER(ctypes.c_int)", "ctypes.POINTER(ctypes.c_int)"],
        has_result=True,
        args=[temp_file_path, labels_str, algorithm.value, certificate.value,
              block_size, table_size]
    )

    return "CYCLE true" in stats, stats, cert

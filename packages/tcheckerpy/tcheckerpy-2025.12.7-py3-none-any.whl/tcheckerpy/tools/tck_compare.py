import tempfile
from enum import Enum
from tcheckerpy.utils import call_tchecker

class Relationship(Enum):
    STRONG_TIMED_BISIM = 0 # strong timed bisimilarity

def compare(first_sys_decl: str, second_sys_decl: str, relationship: Relationship = Relationship.STRONG_TIMED_BISIM, 
            generate_witness = False, block_size: int | None = None, table_size: int | None = None) -> tuple[bool, str, str]:
    """
    Checks for bisimilarity of two timed automata.

    :param first_sys_decl: system declaration of first timed automaton
    :param second_sys_decl: system declaration of second timed automaton
    :param relationship: relationship to be checked (so far only strong timed bisimilarity is supported)
    :param block_size: block size for internal computation
    :param table_size: table size for internal computation
    :return: result of bisimilarity check, statistics and witness
    """
    
    with tempfile.NamedTemporaryFile(delete=False) as temp_file_first_sysdecl:
        temp_file_first_sysdecl.write(first_sys_decl.encode('utf-8'))
        temp_file_path_first_sysdecl = temp_file_first_sysdecl.name
    with tempfile.NamedTemporaryFile(delete=False) as temp_file_second_sysdecl:
        temp_file_second_sysdecl.write(second_sys_decl.encode('utf-8'))
        temp_file_path_second_sysdecl  = temp_file_second_sysdecl.name
        
    # call TChecker function
    stats, witness = call_tchecker.call_tchecker_function_in_new_process(
        func_name="tck_compare",
        argtypes=["ctypes.c_char_p", "ctypes.c_char_p", "ctypes.c_int",
                  "ctypes.POINTER(ctypes.c_int)", "ctypes.POINTER(ctypes.c_int)", "ctypes.c_bool"],
        has_result=True,
        args=[temp_file_path_first_sysdecl, temp_file_path_second_sysdecl, relationship.value, 
              block_size, table_size, generate_witness]
    )

    return "RELATIONSHIP_FULFILLED true" in stats, stats, witness

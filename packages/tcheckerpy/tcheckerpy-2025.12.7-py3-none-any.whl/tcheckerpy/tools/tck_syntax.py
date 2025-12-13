import tempfile
from tcheckerpy.utils import call_tchecker

def __call_tck_syntax(sys_decl: str, func_name: str, process_name: str | None = None) -> str:

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(sys_decl.encode('utf-8'))
        temp_file_path = temp_file.name

    product = func_name == "tck_syntax_create_synchronized_product"
        
    # call TChecker function
    _, result = call_tchecker.call_tchecker_function_in_new_process(
        func_name = func_name,
        argtypes = ["ctypes.c_char_p", "ctypes.c_char_p"] if product else ["ctypes.c_char_p"],
        has_result = True,
        args = [temp_file_path, process_name] if product else [temp_file_path]
    )

    return result

def check(sys_decl: str) -> None:
    """
    Check syntax of timed automaton.

    :param sys_decl: system declaration of timed automaton
    :raises RuntimeError: if syntax is incorrect
    """ 
    __call_tck_syntax(sys_decl, "tck_syntax_check_syntax")

def to_dot(sys_decl: str) -> str:
    """
    Convert timed automaton to DOT graphviz format.

    :param sys_decl: system declaration of timed automaton
    :return: system declaration in DOT graphviz format
    """
    return __call_tck_syntax(sys_decl, "tck_syntax_to_dot")

def to_json(sys_decl: str) -> str:
    """
    Convert timed automaton to JSON format.

    :param sys_decl: system declaration of timed automaton
    :return: system declaration in JSON format
    """
    return __call_tck_syntax(sys_decl, "tck_syntax_to_json")

def create_product(sys_decl: str, process_name: str = "P") -> str:
    """
    Create a synchronized product of timed automaton with multiple processes.

    :param sys_decl: system declaration of timed automaton
    :param process_name: name of synchronized process
    :return: system declaration of synchronized product
    """
    return __call_tck_syntax(sys_decl, "tck_syntax_create_synchronized_product", process_name)

import tempfile
from enum import Enum
from tcheckerpy.utils import call_tchecker

class __SimulationType(Enum):
    INTERACTIVE = 0 # interactive simulation
    ONE_STEP = 1 # one-step simulation (output initial or next states)
    RANDOMIZED = 2 # randomized simulation

def __call_tck_simulate(sys_decl: str, simulation_type: __SimulationType, nsteps: int,
                        starting_state: str | None = None) -> str:
    
    if simulation_type == __SimulationType.RANDOMIZED and nsteps == None:
        raise ValueError("Randomized simulation requires number of steps")
    
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(sys_decl.encode('utf-8'))
        temp_file_path = temp_file.name

    # call TChecker function
    _, result = call_tchecker.call_tchecker_function_in_new_process(
        func_name="tck_simulate",
        argtypes=["ctypes.c_char_p", "ctypes.c_int", "ctypes.c_int", "ctypes.c_char_p", 
                  "ctypes.POINTER(ctypes.c_int)", "ctypes.c_bool"],
        has_result=True,
        args=[temp_file_path, simulation_type.value, 1, starting_state or "",
              nsteps, not simulation_type == __SimulationType.ONE_STEP] 
    )

    return result

def one_step_simulation(sys_decl: str, starting_state: str | None = None) -> str:
    """
    Simulates one step of timed automaton, starting from the given state.

    :param sys_decl: system declaration of timed automaton
    :param starting_state: starting state, specified as a JSON object with keys vloc, intval and zone
                           vloc: comma-separated list of location names (one per process), in-between < and >
                           intval: comma-separated list of assignments (one per integer variable)
                           zone: conjunction of clock-constraints (following TChecker expression syntax)
    :return: initial states if `starting_state` is none, next states otherwise
    """
    return __call_tck_simulate(sys_decl, __SimulationType.ONE_STEP, 0, starting_state)

def randomized_simulation(sys_decl: str, nsteps: int, starting_state: str | None = None) -> str:
    """
    Randomly simulates steps of timed automaton, starting from the given state.

    :param sys_decl: system declaration of timed automaton
    :param starting_state: starting state, specified as a JSON object with keys vloc, intval and zone
                           vloc: comma-separated list of location names (one per process), in-between < and >
                           intval: comma-separated list of assignments (one per integer variable)
                           zone: conjunction of clock-constraints (following TChecker expression syntax)
    :param nsteps: number of steps to simulate
    :return: simulation trace
    """
    return __call_tck_simulate(sys_decl, __SimulationType.RANDOMIZED, nsteps, starting_state)
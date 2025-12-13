from tcheckerpy.tools import tck_compare, tck_liveness, tck_reach, tck_simulate, tck_syntax
import os

# test systems and oracle
test_systems_path = os.path.join(os.path.dirname(__file__), "examples")
with open(os.path.join(test_systems_path, "ad94.tck")) as file:
    system = file.read()
with open(os.path.join(test_systems_path, "ad94_witness.gv")) as file:
    witness = file.read()
with open(os.path.join(test_systems_path, "ad94_first_step.json")) as file:
    first_step = file.read()
with open(os.path.join(test_systems_path, "ad94.gv")) as file:
    dot_format = file.read()
with open(os.path.join(test_systems_path, "ad94.json")) as file:
    json_format = file.read()
with open(os.path.join(test_systems_path, "ad94_product.tck")) as file:
    product = file.read()

def test_tck_compare():
    result = tck_compare.compare(system, system, generate_witness = True)
    assert result[0]
    assert result[2] == witness

def test_tck_liveness():
    result = tck_liveness.liveness(system, tck_liveness.Algorithm.COUVSCC)
    assert not result[0]
    assert result[2] == ""

def test_tck_reach():
    assert not tck_reach.reach(system, tck_reach.Algorithm.REACH)[0]

def test_tck_simulate():
    assert tck_simulate.one_step_simulation(system) == first_step

def test_tck_syntax():
    tck_syntax.check(system)
    assert tck_syntax.to_dot(system) == dot_format
    assert tck_syntax.to_json(system) == json_format
    assert tck_syntax.create_product(system) == product
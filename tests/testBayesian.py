from app.bayesianNetwork import create_bayesian_network
from pgmpy.inference import VariableElimination

def test_engine_issue():
    model = create_bayesian_network()
    inference = VariableElimination(model)
    evidence = {"EngineDoesNotStart": 1, "NoDashboardLights": 1}
    result = inference.map_query(evidence=evidence)
    assert result["BatteryIssue"] == 1

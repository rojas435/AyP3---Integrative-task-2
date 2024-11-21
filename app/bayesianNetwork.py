from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

class CarDiagnosticBN:
    def __init__(self):
        # Initialize the Bayesian Network
        self.model = BayesianNetwork([
            ('EngineProblem', 'EngineSound'),
            ('StarterProblem', 'StartingIssue'),
            ('StarterProblem', 'ClickingSound'),
            ('BrakeProblem', 'BrakeGrinding'),
            ('BrakeProblem', 'Squealing')
        ])

        # Define all CPDs (Conditional Probability Distributions)
        cpd_engine_problem = TabularCPD(
            variable='EngineProblem', variable_card=2,
            values=[[0.8], [0.2]]  # [No, Yes]
        )

        cpd_engine_sound = TabularCPD(
            variable='EngineSound', variable_card=2,
            values=[[0.9, 0.3],
                   [0.1, 0.7]],
            evidence=['EngineProblem'],
            evidence_card=[2]
        )

        cpd_starter_problem = TabularCPD(
            variable='StarterProblem', variable_card=2,
            values=[[0.85], [0.15]]  # [No, Yes]
        )

        cpd_starting_issue = TabularCPD(
            variable='StartingIssue', variable_card=2,
            values=[[0.95, 0.4],
                   [0.05, 0.6]],
            evidence=['StarterProblem'],
            evidence_card=[2]
        )

        cpd_clicking_sound = TabularCPD(
            variable='ClickingSound', variable_card=2,
            values=[[0.9, 0.2],
                   [0.1, 0.8]],
            evidence=['StarterProblem'],
            evidence_card=[2]
        )

        cpd_brake_problem = TabularCPD(
            variable='BrakeProblem', variable_card=2,
            values=[[0.9], [0.1]]  # [No, Yes]
        )

        cpd_brake_grinding = TabularCPD(
            variable='BrakeGrinding', variable_card=2,
            values=[[0.95, 0.3],
                   [0.05, 0.7]],
            evidence=['BrakeProblem'],
            evidence_card=[2]
        )

        cpd_squealing = TabularCPD(
            variable='Squealing', variable_card=2,
            values=[[0.9, 0.4],
                   [0.1, 0.6]],
            evidence=['BrakeProblem'],
            evidence_card=[2]
        )

        # Add CPDs to the model
        self.model.add_cpds(cpd_engine_problem, cpd_engine_sound, cpd_starter_problem, cpd_starting_issue, cpd_clicking_sound, cpd_brake_problem, cpd_brake_grinding, cpd_squealing)

        self.model.check_model()

        # Initialize the inference engine
        self.inference = VariableElimination(self.model)

    def get_probabilities(self, symptoms):
        # Convert symptoms to evidence format
        evidence = {}
        for symptom in symptoms:
            question, answer = symptom.split(':')
            if 'engine' in question.lower():
                evidence['EngineSound'] = 1 if answer == 'Yes' else 0
            elif 'clicking' in question.lower():
                evidence['ClickingSound'] = 1 if answer == 'Yes' else 0
            elif 'starting' in question.lower():
                evidence['StartingIssue'] = 1 if answer == 'Yes' else 0
            elif 'grinding' in question.lower():
                evidence['BrakeGrinding'] = 1 if answer == 'Yes' else 0
            elif 'squealing' in question.lower():
                evidence['Squealing'] = 1 if answer == 'Yes' else 0

        results = {
            'Engine Problem': self.inference.query(
                variables=['EngineProblem'],
                evidence=evidence
            ).values[1] * 100,
            'Starter Problem': self.inference.query(
                variables=['StarterProblem'],
                evidence=evidence
            ).values[1] * 100,
            'Brake Problem': self.inference.query(
                variables=['BrakeProblem'],
                evidence=evidence
            ).values[1] * 100
        }

        return results
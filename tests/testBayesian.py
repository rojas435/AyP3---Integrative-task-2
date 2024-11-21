import pytest
import itertools
import numpy as np
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.bayesianNetwork import CarDiagnosticBN
from pgmpy.inference import VariableElimination

class TestCarDiagnosticBayesianNetwork:

    @pytest.fixture
    def bn_system(self):
        """Fixture to create a fresh CarDiagnosticBN instance for each test"""
        return CarDiagnosticBN()

    def test_single_symptom_inference(self, bn_system):
        """Test inference with single symptoms"""
        test_cases = [

            {'symptoms': ['Is the sound coming from the engine?:Yes'], 
             'expected_keys': ['Engine Problem', 'Starter Problem', 'Brake Problem']},
            {'symptoms': ['Is there a clicking sound when starting?:Yes'], 
             'expected_keys': ['Engine Problem', 'Starter Problem', 'Brake Problem']},
            {'symptoms': ['Do you hear grinding when braking?:Yes'], 
             'expected_keys': ['Engine Problem', 'Starter Problem', 'Brake Problem']},
        ]

        for case in test_cases:
            results = bn_system.get_probabilities(case['symptoms'])
            
            assert set(results.keys()) == set(case['expected_keys'])
            
            for prob in results.values():
                assert 0 <= prob <= 100

    def test_multiple_symptom_scenarios(self, bn_system):
        """Test inference with multiple symptoms"""
        scenarios = [
            # No symptoms
            [],
            # Single symptom
            ['Is the sound coming from the engine?:Yes'],
            # Multiple symptoms
            [
                'Is the sound coming from the engine?:Yes', 
                'Is there a clicking sound when starting?:Yes'
            ],
            [
                'Do you hear grinding when braking?:Yes',
                'Is there a squealing sound while driving?:Yes'
            ]
        ]

        for scenario in scenarios:
            results = bn_system.get_probabilities(scenario)
            
            assert set(results.keys()) == {'Engine Problem', 'Starter Problem', 'Brake Problem'}

            for prob in results.values():
                assert 0 <= prob <= 100

def test_stress_all_symptom_combinations():
    """
    Stress test to run through all possible symptom combinations
    This ensures the Bayesian Network doesn't break under various input scenarios
    """
    bn_system = CarDiagnosticBN()
    
    symptoms = [
        'Is the sound coming from the engine?:Yes',
        'Is the sound coming from the engine?:No',
        'Does the sound occur while braking?:Yes', 
        'Does the sound occur while braking?:No',
        'Does the car have trouble starting?:Yes',
        'Does the car have trouble starting?:No',
        'Is there a clicking sound when starting?:Yes',
        'Is there a clicking sound when starting?:No',
        'Do you hear grinding when braking?:Yes',
        'Do you hear grinding when braking?:No',
        'Is there a squealing sound while driving?:Yes',
        'Is there a squealing sound while driving?:No'
    ]

    for r in range(len(symptoms) + 1):
        for combination in itertools.combinations(symptoms, r):
            try:
                results = bn_system.get_probabilities(list(combination))
                
                assert set(results.keys()) == {'Engine Problem', 'Starter Problem', 'Brake Problem'}
                for prob in results.values():
                    assert 0 <= prob <= 100
            except Exception as e:

                pytest.fail(f"Failed for symptoms {combination}: {str(e)}")

def test_performance_multiple_queries():
    """
    Performance test to ensure the Bayesian Network can handle multiple rapid queries
    """
    bn_system = CarDiagnosticBN()
    
    scenarios = [
        [],
        ['Is the sound coming from the engine?:Yes'],
        ['Is there a clicking sound when starting?:Yes'],
        ['Do you hear grinding when braking?:Yes'],
        ['Is the sound coming from the engine?:Yes', 'Is there a clicking sound when starting?:Yes'],
        ['Do you hear grinding when braking?:Yes', 'Is there a squealing sound while driving?:Yes']
    ]

    for _ in range(100):
        for scenario in scenarios:
            results = bn_system.get_probabilities(scenario)
            
            assert set(results.keys()) == {'Engine Problem', 'Starter Problem', 'Brake Problem'}
            for prob in results.values():
                assert 0 <= prob <= 100

if __name__ == "__main__":
    pytest.main([__file__])
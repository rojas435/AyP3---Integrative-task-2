import unittest
from experta import Fact, KnowledgeEngine, Rule, AND

class CarDiagnosisExpert(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.diagnoses = []

    @Rule(Fact(engine_sound='Yes'))
    def engine_sound_rule(self):
        self.diagnoses.append("Possible engine mechanical issue - recommend mechanic inspection")

    @Rule(Fact(clicking_sound='Yes'))
    def clicking_sound_rule(self):
        self.diagnoses.append("Possible starter or battery issue - check battery voltage")

    @Rule(AND(Fact(brake_grinding='Yes'),
              Fact(squealing='Yes')))
    def severe_brake_issue_rule(self):
        self.diagnoses.append("Urgent: Brake system requires immediate inspection")

class CarExpertSystem:
    def __init__(self):
        self.engine = CarDiagnosisExpert()

    def diagnose(self, symptoms):
        # Reset the engine
        self.engine.reset()
        self.engine.diagnoses = []

        # Convert symptoms to facts
        for symptom in symptoms:
            question, answer = symptom.split(':')
            if 'engine' in question.lower():
                self.engine.declare(Fact(engine_sound=answer))
            elif 'clicking' in question.lower():
                self.engine.declare(Fact(clicking_sound=answer))
            elif 'grinding' in question.lower():
                self.engine.declare(Fact(brake_grinding=answer))
            elif 'squealing' in question.lower():
                self.engine.declare(Fact(squealing=answer))

        # Run the engine
        self.engine.run()

        return self.engine.diagnoses

class TestCarExpertSystem(unittest.TestCase):
    def setUp(self):
        self.expert_system = CarExpertSystem()

    def test_engine_sound_diagnosis(self):
        symptoms = ["engine sound: Yes"]
        diagnoses = self.expert_system.diagnose(symptoms)
        self.assertEqual(len(diagnoses), 1)
        self.assertIn("Possible engine mechanical issue", diagnoses[0])

    def test_clicking_sound_diagnosis(self):
        symptoms = ["clicking sound: Yes"]
        diagnoses = self.expert_system.diagnose(symptoms)
        self.assertEqual(len(diagnoses), 1)
        self.assertIn("Possible starter or battery issue", diagnoses[0])

    def test_brake_system_urgent_issue(self):
        symptoms = [
            "brake grinding: Yes", 
            "squealing: Yes"
        ]
        diagnoses = self.expert_system.diagnose(symptoms)
        self.assertEqual(len(diagnoses), 1)
        self.assertIn("Urgent: Brake system requires immediate inspection", diagnoses[0])

    def test_multiple_symptoms(self):
        symptoms = [
            "engine sound: Yes", 
            "clicking sound: Yes"
        ]
        diagnoses = self.expert_system.diagnose(symptoms)
        self.assertEqual(len(diagnoses), 2)
        
    def test_no_symptoms(self):
        symptoms = []
        diagnoses = self.expert_system.diagnose(symptoms)
        self.assertEqual(len(diagnoses), 0)

    def test_unrelated_symptoms(self):
        symptoms = ["random symptom: Yes"]
        diagnoses = self.expert_system.diagnose(symptoms)
        self.assertEqual(len(diagnoses), 0)

def main():
    # Ejemplo de uso del sistema experto
    expert_system = CarExpertSystem()
    
    print("Escenario 1: Sonido de motor")
    diagnoses1 = expert_system.diagnose(["engine sound: Yes"])
    print("Diagnósticos:", diagnoses1)

    print("\nEscenario 2: Sonido de clic")
    diagnoses2 = expert_system.diagnose(["clicking sound: Yes"])
    print("Diagnósticos:", diagnoses2)

    print("\nEscenario 3: Problema grave de frenos")
    diagnoses3 = expert_system.diagnose(["brake grinding: Yes", "squealing: Yes"])
    print("Diagnósticos:", diagnoses3)

if __name__ == "__main__":
    # Ejecutar pruebas unitarias
    unittest.main(exit=False)
    
    # Ejecutar ejemplo de uso
    main()
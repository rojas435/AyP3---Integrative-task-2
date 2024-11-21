from experta import Fact, KnowledgeEngine, Rule, AND

class CarDiagnosisExpert(KnowledgeEngine):
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
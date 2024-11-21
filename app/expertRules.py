from experta import *

class CarDiagnosisExpert(KnowledgeEngine):
    @DefFacts()
    def initial_facts(self):
        yield Fact(start=True)
        
    @Rule(Fact(start=True))
    def ask_initial_question(self):
        response = input("¿Clunk or single tick? (yes/no): ").lower()
        if response == 'yes':
            self.declare(Fact(clunk_or_single_tick=True))
        else:
            self.declare(Fact(clunk_or_single_tick=False))
            
    @Rule(Fact(clunk_or_single_tick=True))
    def check_noise_on_bumps(self):
        response = input("¿Noise on bumps only? (yes/no): ").lower()
        if response == 'yes':
            self.declare(Fact(noise_on_bumps=True))
            print("Diagnóstico: Check struts, shocks, springs, frame welds.")
        else:
            self.declare(Fact(noise_on_bumps=False))
            print("Diagnóstico: Check ball joints, brakes, rack and tie rod ends, motor mounts.")
            
    @Rule(Fact(clunk_or_single_tick=False))
    def check_moving_ticks(self):
        response = input("¿Only ticks when moving? (yes/no): ").lower()
        if response == 'yes':
            self.declare(Fact(ticks_when_moving=True))
        else:
            self.declare(Fact(check_bomb=True))



    @Rule(Fact(check_bomb=True))
    def check_bomb(self):
        response = input("Time bomb under seat? (yes/no): ").lower()
        if response == 'yes':
            print("Get out of the car and run or tell google to desarm the bomb")
        else:
            print("Idk ur car is ok then")
            
    @Rule(Fact(ticks_when_moving=True))
    def check_neutral_rolling(self):
        response = input("¿Ticks rolling in neutral? (yes/no): ").lower()
        if response == 'yes':
            self.declare(Fact(frecuency_drops=True))
        else:
            self.declare(Fact(check_reverse=True))


    @Rule(Fact(frecuency_drops=True))
    def check_frequency_drops(self):
        response = input("¿Frecuency drops on shifts? (yes/no): ").lower()
        if response == 'yes':
            print("Try to localize tick wit the hearing tube or long screwdriver (Listen at the handle).")
            self.declare(Fact(hearing_tube=True))
        else:
            self.declare(Fact(only_curves=True))


    @Rule(Fact(hearing_tube=True))
    def check_hearing_tube(self):
        response = input("¿Wanna continue? (yes/no): ").lower()
        if response == 'yes':
            response = input("¿Only ticks when cold? (yes/no): ").lower()
            if response == 'yes':
                self.declare(Fact(check_hearing_tube=True))
                print("Check the exhaust pipe foward of catalytic converter for leaks. Listen for lifter rap on valve corner")

            else:
                response = input("Windshield wipers, radio off? (yes/no): ").lower()
                if response == 'yes':
                    print("Look for pulley wouble, inspect bellts. Check for exhaust mani fold leak. Get Somebody withe better hearing to help you localize where its coming from on the engine")
                else:
                    print("Always check the silly stuff, like your passenger tapping on the roof")
        else:
            print("Exit...")
             
    @Rule(Fact(check_reverse=True))
    def check_reverse_ticks(self):
        response = input("¿Ticks only in reverse? (yes/no): ").lower()
        if response == 'yes':
            print("Possible rear brake adjuster, make sure parking brake fully released.")
        else:
            print("Possible transmission tick. Check transmission fluid, filter.")




    @Rule(Fact(only_curves=True))
    def check_ticks_turns(self):
        response = input("¿Only ticks in turns, curves? (yes/no): ").lower()
        if response == 'yes':
            print("CV Joint going or tire too big for wheel well (But not for long).")
        else:
            self.declare(Fact(check_wheel_rotation=True))




    @Rule(Fact(check_wheel_rotation=True))
    def check_wheel_rotation_related(self):
        print("The tick is related to the rotation of the wheel")
        response = input("¿Just changed tires? (yes/no): ").lower()
        if response == 'yes':
            print("Stop driving (and call a tow truck now). Make sure the wheel nuts are tightened properly.")
        else:
            self.declare(Fact(check_hubcaps=True))

    

    
    @Rule(Fact(check_hubcaps=True))
    def check_hubcaps(self):
        response = input("¿Removed hubcaps? (yes/no): ").lower()
        if response == 'yes':
            self.declare(Fact(inspect_tire_treads=True))
        else:
            print("Remove the hubcaps before proceeding. Loose cable retainer, stones can cause ticks.")
            
    @Rule(Fact(inspect_tire_treads=True))
    def check_tire_treads(self):
        response = input("¿Inspect the tire tread? (yes/no): ").lower()
        if response == 'yes':
            self.declare(Fact(check_hearing_tube=True))
        else:
            print("Check for nails or stones embedded in the tread.")




    @Rule(Fact(check_hearing_tube=True))
    def check_slow_speed(self):
        response = input("¿Does it only tick at a low speed? (yes/no): ").lower()
        if response == 'yes':
            print("Check bolted wheel covers and hub caps for pebbles.")
        else:
            print("Probably the brake pads are ticking on the warped rotor, also check the axles for friction.")

class CarExpertSystem:
    def __init__(self):
        self.engine = CarDiagnosisExpert()
    
    def diagnose(self):
        self.engine.reset()
        self.engine.run()

# Ejemplo de uso
if __name__ == "__main__":
    expert_system = CarExpertSystem()
    print("Sistema de diagnóstico de ruidos del auto")
    print("Responde a las preguntas con 'yes' o 'no'")
    expert_system.diagnose()
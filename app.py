import streamlit as st
from app.bayesianNetwork import CarDiagnosticBN
from app.expertRules import CarExpertSystem

def main():
    st.title("Advanced Car Diagnostic System")
    
    # Initialize the diagnostic systems
    bn_system = CarDiagnosticBN()
    expert_system = CarExpertSystem()
    
    # Get diagnostic flows
    diagnostic_flows = bn_system.get_diagnostic_flow()
    
    # Session state to store conversation and symptoms
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
        st.session_state.current_symptoms = {}
        st.session_state.current_flow = list(diagnostic_flows.keys())[0]
        st.session_state.current_question_index = 0
    
    # Display chat history
    for message in st.session_state.chat_history:
        st.write(message)
    
    # Get current flow and questions
    current_flow_questions = diagnostic_flows[st.session_state.current_flow]
    
    # Display current question
    if st.session_state.current_question_index < len(current_flow_questions):
        current_question = current_flow_questions[st.session_state.current_question_index]
        
        col1, col2 = st.columns(2)
        st.write(f"### {current_question}")
        with col1:
            if st.button("Sí"):
                st.session_state.chat_history.append(f"Q: {current_question}")
                st.session_state.chat_history.append("A: Sí")


                symptom_mapping = {
                    'Clunk or single tick?': 'clunk_tick',
                    'Noise on bumps only?': 'noise_bumps',
                    'Only ticks when moving?': 'ticks_moving',
                    'Ticks rolling in neutral?': 'ticks_neutral',
                    'Ticks only in reverse?': 'ticks_reverse',
                    'Frequency drops on shifts?': 'frequency_drops',
                    'Only ticks in turns, curves?': 'ticks_turns',
                    # Agrega todas las demás preguntas aquí, todavia faltan, creo
                }

                mapped_var = symptom_mapping.get(current_question)
                if mapped_var:
                    st.session_state.current_symptoms[mapped_var] = 'si'

                st.session_state.current_question_index += 1
                st.rerun()
                
        with col2:
            if st.button("No"):
                st.session_state.chat_history.append(f"Q: {current_question}")
                st.session_state.chat_history.append("A: No")

                mapped_var = symptom_mapping.get(current_question)
                if mapped_var:
                    st.session_state.current_symptoms[mapped_var] = 'no'
        
                st.session_state.current_question_index += 1
                st.rerun()
    
    # Move to next diagnostic flow or show results
    elif st.session_state.current_flow == list(diagnostic_flows.keys())[-1]:
        st.write("### Diagnostic Results")
        
        # Determine main problem probabilities
        bn_results = bn_system.get_probabilities(st.session_state.current_symptoms)
        st.write("#### Bayesian Network Analysis")
        for problem, prob in bn_results.items():
            st.write(f"{problem}: {prob:.1f}% probability")
        
        # Get expert system results
        expert_results = expert_system.diagnose({
            'engine_problem': 'si' if bn_results['EngineProblem'] > 50 else 'no',
            'starter_problem': 'si' if bn_results['StarterProblem'] > 50 else 'no',
            'brake_problem': 'si' if bn_results['BrakeProblem'] > 50 else 'no'
        })
        
        st.write("#### Expert System Analysis")
        for diagnosis in expert_results:
            st.write(f"- {diagnosis}")
        
        if st.button("Start Over"):
            st.session_state.chat_history = []
            st.session_state.current_symptoms = {}
            st.session_state.current_flow = list(diagnostic_flows.keys())[0]
            st.session_state.current_question_index = 0
            st.rerun()
    
    else:
        # Move to next diagnostic flow
        current_flow_index = list(diagnostic_flows.keys()).index(st.session_state.current_flow)
        st.session_state.current_flow = list(diagnostic_flows.keys())[current_flow_index + 1]
        st.session_state.current_question_index = 0
        st.rerun()

if __name__ == "__main__":
    main()
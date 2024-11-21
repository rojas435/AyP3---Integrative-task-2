import streamlit as st
import json
from app.bayesianNetwork import CarDiagnosticBN
from app.expertRules import CarExpertSystem
from datetime import datetime
import os

def load_previous_results():
    # Load previous results from the JSON file
    try:
        with open('diagnostic_results_history.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_results_to_json(results):
    # Load previous results
    previous_results = load_previous_results()
    
    # Add timestamp to the current results
    results['timestamp'] = datetime.now().isoformat()
    
    # Append new results
    previous_results.append(results)
    
    # Save updated results
    with open('diagnostic_results_history.json', 'w') as f:
        json.dump(previous_results, f, indent=4)

def reset_session_state():
    # Explicitly reset all session state variables
    st.session_state.chat_history = []
    st.session_state.current_symptoms = set()
    st.session_state.current_question_index = 0
    st.session_state.diagnostic_completed = False

def main():
    st.title("Car Diagnostic System")

    # Initialize the diagnostic systems
    bn_system = CarDiagnosticBN()
    expert_system = CarExpertSystem()

    # Initialize session state if not already set
    if 'chat_history' not in st.session_state:
        reset_session_state()

    # Display chat history
    for message in st.session_state.chat_history:
        st.write(message)

    # Display the option to view previous results
    st.sidebar.title("Options")
    view_history_button = st.sidebar.button("View Diagnostic History")

    if view_history_button:
        previous_results = load_previous_results()
        if previous_results:
            st.sidebar.write("### Diagnostic History")
            for idx, result in enumerate(previous_results, 1):
                st.sidebar.write(f"#### Diagnostic Session {idx} - {result.get('timestamp', 'Unknown Time')}")
                st.sidebar.write("**Bayesian Network**:")
                st.sidebar.json(result["Bayesian Network"])
                st.sidebar.write("**Expert System**:")
                st.sidebar.write(result["Expert System"])
                st.sidebar.write("---")
        else:
            st.sidebar.write("No previous diagnostic results found.")

    # Questions to ask
    questions = [
        "Is the sound coming from the engine?",
        "Does the sound occur while braking?",
        "Does the car have trouble starting?",
        "Is there a clicking sound when starting?",
        "Do you hear grinding when braking?",
        "Is there a squealing sound while driving?"
    ]

    # Display current question
    if st.session_state.current_question_index < len(questions):
        current_question = questions[st.session_state.current_question_index]

        col1, col2 = st.columns(2)
        st.write(f"### {current_question}")
        with col1:
            if st.button("Yes"):
                st.session_state.chat_history.append(f"Q: {current_question}")
                st.session_state.chat_history.append("A: Yes")
                st.session_state.current_symptoms.add(f"{current_question}:Yes")
                st.session_state.current_question_index += 1
                st.rerun()

        with col2:
            if st.button("No"):
                st.session_state.chat_history.append(f"Q: {current_question}")
                st.session_state.chat_history.append("A: No")
                st.session_state.current_symptoms.add(f"{current_question}:No")
                st.session_state.current_question_index += 1
                st.rerun()

    # Show results when all questions are answered
    elif st.session_state.current_question_index == len(questions):
        # Only save results if not already saved
        if not getattr(st.session_state, 'diagnostic_completed', False):
            st.write("### Diagnostic Results")

            # Get probabilistic results from Bayesian Network
            bn_results = bn_system.get_probabilities(st.session_state.current_symptoms)
            st.write("#### Bayesian Network Analysis")
            for problem, prob in bn_results.items():
                st.write(f"{problem}: {prob:.1f}% probability")

            # Get expert system results
            expert_results = expert_system.diagnose(st.session_state.current_symptoms)
            st.write("#### Expert System Analysis")
            for diagnosis in expert_results:
                st.write(f"- {diagnosis}")

            # Combine results
            results = {
                "Bayesian Network": bn_results,
                "Expert System": expert_results
            }

            # Save the results to a JSON file
            save_results_to_json(results)

            # Mark diagnostic as completed to prevent multiple saves
            st.session_state.diagnostic_completed = True

        if st.button("Start Over"):
            reset_session_state()
            st.rerun()

if __name__ == "__main__":
    main()
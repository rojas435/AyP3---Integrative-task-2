# Advanced Car Diagnostic System

This repository contains the **Advanced Car Diagnostic System** project, an expert system that combines inference rules and Bayesian networks to diagnose common vehicle problems using **Python**, **Streamlit**, **Experta**, and **pgmpy**.

## Project Description

The goal of this project is to assist users in diagnosing mechanical issues in vehicles through an interactive chatbot. Users input symptoms such as unusual noises, starting difficulties, or warning lights on the dashboard, and the system suggests possible causes and solutions.

## Team

- Felipe Rojas Prado A00393918
- Juan Sebastian Gonzalez A00371810

### Academic Context

- **Course:** Algorithms and Programming III  
- **Professor:** Andrés Aristizábal  
- **Study Unit:** Reasoning Under Uncertainty and Expert System Design  
- **Final Submission Date:** November 20, 2024  

This project applies principles of **artificial intelligence** in a practical setting, showcasing the implementation of expert systems for real-world problems while making technical knowledge accessible to a broader audience.

## Key Features

1. **Rule-based diagnostics:** Utilizes the **Experta** library to model inference rules, such as symptoms associated with various mechanical issues.
2. **Bayesian networks:** Implements **pgmpy** to assess probabilities and improve diagnostic accuracy.
3. **Interactive web interface:** Uses **Streamlit** to provide users with a seamless and intuitive experience.
4. **Explainability:** The system offers clear explanations for diagnoses and recommendations.

## Project Structure

```plaintext
📂 Advanced-Car-Diagnostic-System
├── 📂 app
│   ├── bayesianNetwork.py        # Bayesian network implementation
│   ├── expertRules.py            # Expert system rules
│   └── __init__.py
├── 📂 docs
│   ├── system_design.md          # System design documentation
│   └── user_guide.md             # User guide
├── 📂 data                       # Test data and diagnostic flows
├── 📂 tests                      # Validation and testing scripts
├── app.py                        # Main Streamlit application file
├── requirements.txt              # Project dependencies
└── README.md                     # This file
````

Required libraries:
- streamlit
- experta
- pgmpy


Technical Implementation
The project follows a structured workflow divided into key phases:

1. Knowledge Acquisition: Collecting information from technical manuals and consulting automotive experts.
2. System Design: Creating models for rule-based and probabilistic reasoning.
3. Implementation: Integrating logic into a user-friendly environment.
4. Testing: Validating responses and performance under different scenarios.
5. Deployment: The application is designed to be accessible in web browsers using Streamlit.


## Example Usage
Startup: The application presents initial questions based on basic symptoms.
Diagnosis: Based on the responses, the system uses rules and Bayesian networks to identify probable issues.

## Recommendation: The system suggests possible solutions or next steps.
Expected Outcomes
Functional expert system: Effective diagnostics with clear explanations of reasoning.
User-friendly interface: Accessible and easy-to-use application, even for non-technical users.



[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/suWkZtY3)



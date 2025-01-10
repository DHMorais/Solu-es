import streamlit as st

def calculate_solution_preparation():
    st.title("Preparador de Soluções Químicas")

    # Sidebar for variable selection
    st.sidebar.header("Quais variáveis você possui?")
    available_variables = {
        "Massa (m) em g": st.sidebar.checkbox("Massa (m) em g"),
        "Número de mols (n) em mol": st.sidebar.checkbox("Número de mols (n) em mol"),
        "Volume (V) em L": st.sidebar.checkbox("Volume (V) em L"),
        "Concentração (C) em mol/L": st.sidebar.checkbox("Concentração (C) em mol/L"),
        "Massa molar (M) em g/mol": st.sidebar.checkbox("Massa molar (M) em g/mol")
    }

    # Radio buttons for calculation choice
    st.sidebar.header("Escolha a variável que deseja calcular:")
    calculation_choice = st.sidebar.radio(
        "Escolha a variável:",
        ("Número de mols (n)", "Massa (m)", "Volume (V)", "Concentração (C)", "Massa molar (M)")
    )

    input_fields = {}
    if calculation_choice == "Número de mols (n)":
        st.subheader("Calcular Número de Mols (n)")
        if available_variables["Massa (m) em g"] and available_variables["Massa molar (M) em g/mol"]:
            m = st.number_input("Massa (m) em g:", min_value=0.0)
            M = st.number_input("Massa molar (M) em g/mol:", min_value=0.0)
            if st.button("Calcular n"):
                n = m / M
                st.success(f"O número de mols (n) é: {n:.3f} mol")
        elif available_variables["Volume (V) em L"] and available_variables["Concentração (C) em mol/L"]:
            V = st.number_input("Volume (V) em L:", min_value=0.0)
            C = st.number_input("Concentração (C) em mol/L:", min_value=0.0)
            if st.button("Calcular n"):
                n = C * V
                st.success(f"O número de mols (n) é: {n:.3f} mol")

    elif calculation_choice == "Massa (m)":
        st.subheader("Calcular Massa (m)")
        if available_variables["Número de mols (n) em mol"] and available_variables["Massa molar (M) em g/mol"]:
            n = st.number_input("Número de mols (n) em mol:", min_value=0.0)
            M = st.number_input("Massa molar (M) em g/mol:", min_value=0.0)
            if st.button("Calcular m"):
                m = n * M
                st.success(f"A massa do soluto (m) é: {m:.3f} g")
        elif available_variables["Concentração (C) em mol/L"] and available_variables["Volume (V) em L"] and available_variables["Massa molar (M) em g/mol"]:
            C = st.number_input("Concentração (C) em mol/L:", min_value=0.0)
            V = st.number_input("Volume (V) em L:", min_value=0.0)
            M = st.number_input("Massa molar (M) em g/mol:", min_value=0.0)
            if st.button("Calcular m"):
                m = C * V * M
                st.success(f"A massa do soluto (m) é: {m:.3f} g")

    elif calculation_choice == "Volume (V)":
        st.subheader("Calcular Volume (V)")
        n = st.number_input("Número de mols (n) em mol:", min_value=0.0)
        C = st.number_input("Concentração (C) em mol/L:", min_value=0.0)
        if st.button("Calcular V"):
            V = n / C
            st.success(f"O volume da solução (V) é: {V:.3f} L")

    elif calculation_choice == "Concentração (C)":
        st.subheader("Calcular Concentração (C)")
        m = st.number_input("Massa (m) em g:", min_value=0.0)
        V = st.number_input("Volume (V) em L:", min_value=0.0)
        M = st.number_input("Massa molar (M) em g/mol:", min_value=0.0)
        if st.button("Calcular C"):
            n = m / M
            C = n / V
            st.success(f"A concentração da solução (C) é: {C:.3f} mol/L")

    elif calculation_choice == "Massa molar (M)":
        st.subheader("Calcular Massa Molar (M)")
        formula = st.text_input("Insira a fórmula molecular (exemplo: 2:H,1:O):")
        if st.button("Calcular M"):
            try:
                elements = formula.split(',')
                total_molar_mass = 0
                for element in elements:
                    qty, atomic_mass = map(float, element.split(':'))
                    total_molar_mass += qty * atomic_mass
                st.success(f"A massa molar calculada é: {total_molar_mass:.3f} g/mol")
            except ValueError:
                st.error("Formato inválido. Por favor, use o formato '2:H,1:O'.")

# Run the app
if __name__ == "__main__":
    calculate_solution_preparation()

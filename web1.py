import streamlit as st
import pandas as pd
import re  # Para expressões regulares ao lidar com a fórmula digitada

# Dicionário de massas atômicas dos elementos mais comuns
ELEMENTOS_QUIMICOS = {
    'H': 1.008, 'He': 4.003, 'Li': 6.941, 'Be': 9.012, 'B': 10.811,
    'C': 12.011, 'N': 14.007, 'O': 15.999, 'F': 18.998, 'Ne': 20.180,
    'Na': 22.990, 'Mg': 24.305, 'Al': 26.982, 'Si': 28.086, 'P': 30.974,
    'S': 32.065, 'Cl': 35.453, 'K': 39.098, 'Ca': 40.078, 'Fe': 55.845,
    'Cu': 63.546, 'Zn': 65.380, 'Ag': 107.868, 'Au': 196.967,
}


def initialize_session_state():
    """Inicializa variáveis de estado da sessão"""
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'selected_elements' not in st.session_state:
        st.session_state.selected_elements = []


def validate_inputs(*args):
    """Valida se todos os inputs são maiores que zero"""
    return all(arg > 0 for arg in args)


def format_result(value, unit):
    """Formata o resultado com 3 casas decimais e unidade"""
    return f"{value:.3f} {unit}"


def add_to_history(calculation_type, inputs, result):
    """Adiciona o cálculo ao histórico"""
    st.session_state.history.append({
        'Tipo de Cálculo': calculation_type,
        'Valores de Entrada': inputs,
        'Resultado': result,
    })


def parse_formula(formula):
    """Parse a fórmula química para extrair os elementos e suas quantidades"""
    # Expressão regular para encontrar elementos e suas quantidades
    element_pattern = r'([A-Z][a-z]?)(\d*)'
    elements = re.findall(element_pattern, formula)

    parsed_elements = []
    for element, quantity in elements:
        quantity = int(quantity) if quantity else 1
        if element in ELEMENTOS_QUIMICOS:
            parsed_elements.append((element, quantity))
        else:
            st.error(f"Elemento não encontrado: {element}")

    return parsed_elements


def calcular_massa_molar():
    """Interface para cálculo de massa molar"""
    st.subheader("Calculadora de Massa Molar")

    # Campo para o usuário digitar a fórmula química
    formula_input = st.text_input(
        "Digite a fórmula química (ex: H2O, NaCl, C6H12O6):",
        help="Digite a fórmula sem espaços. Exemplo: H2O, NaCl, C6H12O6"
    )

    # Adicionar os elementos selecionados manualmente
    with st.expander("Adicionar elementos manualmente"):
        col1, col2 = st.columns(2)
        with col1:
            elemento = st.selectbox("Selecione o elemento", list(ELEMENTOS_QUIMICOS.keys()))
            quantidade = st.number_input("Quantidade de átomos", min_value=1, value=1)

            if st.button("Adicionar Elemento"):
                st.session_state.selected_elements.append((elemento, quantidade))

        # Mostrar elementos selecionados
        with col2:
            st.write("Elementos selecionados:")
            for elem, qtd in st.session_state.selected_elements:
                st.write(f"{elem}: {qtd} átomo(s)")

            if st.button("Limpar Elementos"):
                st.session_state.selected_elements = []

    # Calcular a massa molar com base na fórmula
    if formula_input:
        # Se o usuário digitou uma fórmula
        parsed_elements = parse_formula(formula_input)
        st.session_state.selected_elements = parsed_elements

    if st.session_state.selected_elements:
        massa_molar_total = sum(ELEMENTOS_QUIMICOS[elem] * qtd
                                for elem, qtd in st.session_state.selected_elements)

        formula_display = "".join([f"{elem}{qtd if qtd > 1 else ''}"
                                   for elem, qtd in st.session_state.selected_elements])

        st.write(f"Fórmula: {formula_display}")
        st.write(f"Massa Molar Total: {massa_molar_total:.3f} g/mol")

        if st.button("Salvar no Histórico"):
            add_to_history(
                "Massa Molar",
                f"Fórmula: {formula_display}",
                f"{massa_molar_total:.3f} g/mol"
            )


def calculate_solution_preparation():
    st.set_page_config(
        page_title="Calculadora de Soluções Químicas",
        page_icon="🧪",
        layout="wide"
    )

    initialize_session_state()

    st.title("🧪 Calculadora de Soluções Químicas 🧪")

    # Criar abas para separar as funcionalidades
    tab1, tab2 = st.tabs(["Cálculos de Solução", "Massa Molar"])

    with tab1:
        # Criar duas colunas principais
        col1, col2 = st.columns([2, 1])

        with col1:
            # Variáveis disponíveis com descrições
            st.header("Variáveis Disponíveis")
            available_variables = {
                "Massa (m)": {
                    "selected": st.checkbox("Massa (m)", help="Massa do soluto em gramas"),
                    "unit": "g"
                },
                "Volume (V)": {
                    "selected": st.checkbox("Volume (V)", help="Volume da solução em litros"),
                    "unit": "L"
                },
                "Concentração (C)": {
                    "selected": st.checkbox("Concentração (C)", help="Concentração em mols por litro"),
                    "unit": "mol/L"
                },
                "Massa molar (M)": {
                    "selected": st.checkbox("Massa molar (M)", help="Massa molar em gramas por mol"),
                    "unit": "g/mol"
                }
            }

            st.header("Selecione o Cálculo Desejado")
            calculation_options = {
                "Massa (m)": "Calcular massa do soluto",
                "Volume (V)": "Calcular volume da solução",
                "Concentração (C)": "Calcular concentração molar",
                "Massa molar (M)": "Calcular massa molar"
            }

            calculation_choice = st.radio(
                "Escolha a variável a calcular:",
                calculation_options.keys(),
                format_func=lambda x: calculation_options[x]
            )

            st.header("Valores de Entrada")
            if calculation_choice == "Massa (m)":
                if all([available_variables["Volume (V)"]["selected"],
                        available_variables["Concentração (C)"]["selected"],
                        available_variables["Massa molar (M)"]["selected"]]):

                    with st.form("mass_calculation"):
                        C = st.number_input("Concentração (mol/L):", min_value=0.0, step=0.1)
                        V = st.number_input("Volume (L):", min_value=0.0, step=0.1)
                        M = st.number_input("Massa molar (g/mol):", min_value=0.0, step=0.1)
                        submitted = st.form_submit_button("Calcular Massa")

                        if submitted and validate_inputs(C, V, M):
                            m = C * V * M
                            result = format_result(m, "g")
                            st.success(f"A massa do soluto é: {result}")
                            add_to_history("Massa", f"C={C}, V={V}, M={M}", result)
                        elif submitted:
                            st.error("Todos os valores devem ser maiores que zero!")

            elif calculation_choice == "Volume (V)":
                if all([available_variables["Massa (m)"]["selected"],
                        available_variables["Concentração (C)"]["selected"],
                        available_variables["Massa molar (M)"]["selected"]]):

                    with st.form("volume_calculation"):
                        m = st.number_input("Massa (g):", min_value=0.0, step=0.1)
                        C = st.number_input("Concentração (mol/L):", min_value=0.0, step=0.1)
                        M = st.number_input("Massa molar (g/mol):", min_value=0.0, step=0.1)
                        submitted = st.form_submit_button("Calcular Volume")

                        if submitted and validate_inputs(m, C, M):
                            V = (m / M) / C
                            result = format_result(V, "L")
                            st.success(f"O volume da solução é: {result}")
                            add_to_history("Volume", f"m={m}, C={C}, M={M}", result)
                        elif submitted:
                            st.error("Todos os valores devem ser maiores que zero!")

        with col2:
            # Histórico de cálculos
            st.header("Histórico de Cálculos")
            if st.session_state.history:
                df = pd.DataFrame(st.session_state.history)
                st.dataframe(df, use_container_width=True)
                if st.button("Limpar Histórico"):
                    st.session_state.history = []
                    st.experimental_rerun()
            else:
                st.info("Nenhum cálculo realizado ainda.")

            # Área de ajuda e informações
            st.header("Informações Úteis")
            with st.expander("Como usar"):
                st.markdown("""
                1. Marque as variáveis que você possui
                2. Escolha qual variável deseja calcular
                3. Preencha os valores necessários
                4. Clique em calcular
                """)

            with st.expander("Fórmulas"):
                st.markdown("""
                - Massa (m) = C × V × M
                - Volume (V) = (m/M) ÷ C
                - Concentração (C) = (m/M) ÷ V
                Onde:
                - m = massa (g)
                - V = volume (L)
                - C = concentração (mol/L)
                - M = massa molar (g/mol)
                """)

    with tab2:
        calcular_massa_molar()


if __name__ == "__main__":
    calculate_solution_preparation()

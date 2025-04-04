import streamlit as st
import random

def init_session_state():
    if 'equation_generated' not in st.session_state:
        st.session_state.equation_generated = False
        st.session_state.feedback_message = None
        st.session_state.feedback_type = None
        st.session_state.score = 0
        st.session_state.user_input = ""

def generate_equation():
    coefficient = random.choice([i for i in range(-10, 11) if i not in [0, -1]]) 
    constant_term = random.choice([i for i in range(-10, 11) if i != 0])
    solution = random.randint(-10, 10)
    right_side = coefficient * solution + constant_term

    return {
        'coefficient': coefficient,
        'constant_term': constant_term,
        'right_side': right_side,
        'solution': solution
    }

def format_equation(equation_data):
    coefficient = equation_data['coefficient']
    constant_term = equation_data['constant_term']
    right_side = equation_data['right_side']

    if coefficient == 1:
        coefficient_display = "x"
    elif coefficient == -1:
        coefficient_display = "-x"
    else:
        coefficient_display = f"{coefficient}x"

    if constant_term > 0:
        constant_display = f" + {constant_term}"
    elif constant_term < 0:
        constant_display = f" - {abs(constant_term)}"
    else:
        constant_display = ""

    return f"{coefficient_display}{constant_display} = {right_side}"

def check_answer(user_answer, correct_solution):
    return user_answer == correct_solution

def update_score(is_correct):
    if is_correct:
        st.session_state.score += 1
        return f"Correct! 🎉 Well done! Your score increased to {st.session_state.score}!", "success"
    else:
        if st.session_state.score > 0:
            st.session_state.score -= 1
            return f"Incorrect! Try again! Score: {st.session_state.score}", "error"
        return "Incorrect! Your score is already at 0. Try again!", "error"

def render_header():
    st.title("🧮 Linear Equation Practice")
    score_col1, score_col2 = st.columns([1, 3])
    with score_col1:
        st.markdown(f"### Score: {st.session_state.score}")
    st.write("Solve for `x` in the equation below:")

def render_equation(equation_string):
    st.markdown(f"## {equation_string}")

def render_input_section():
    user_input_str = st.text_input("Enter your answer (integer):", value=st.session_state.user_input)
    try:
        user_answer = int(user_input_str) if user_input_str else 0
        input_valid = True
    except ValueError:
        user_answer = 0
        input_valid = False
    return user_input_str, user_answer, input_valid

def render_buttons():
    col1, col2 = st.columns([1, 3])
    with col1:
        check_button = st.button("✅ Check Answer")
    with col2:
        new_equation_button = st.button("🔄 New Equation")
    return check_button, new_equation_button

def main():
    init_session_state()

    if not st.session_state.equation_generated:
        st.session_state.equation_data = generate_equation()
        st.session_state.equation_generated = True
        st.session_state.attempts = 0

    render_header()
    equation_string = format_equation(st.session_state.equation_data)
    render_equation(equation_string)

    user_input_str, user_answer, input_valid = render_input_section()
    check_button, new_equation_button = render_buttons()

    if not input_valid and user_input_str:
        st.error("Please enter a valid integer (e.g., 5, -3, 0)")
    elif st.session_state.feedback_message and input_valid:
        if st.session_state.feedback_type == "success":
            st.success(st.session_state.feedback_message)
        else:
            st.error(st.session_state.feedback_message)

    if check_button and input_valid and user_input_str.strip():
        st.session_state.attempts += 1
        is_correct = check_answer(user_answer, st.session_state.equation_data['solution'])
        st.session_state.feedback_message, st.session_state.feedback_type = update_score(is_correct)

        if is_correct:
            st.session_state.equation_data = generate_equation()
            st.session_state.attempts = 0
            st.session_state.user_input = ""
        else:
            st.session_state.user_input = user_input_str

        st.experimental_rerun()

    if new_equation_button:
        st.session_state.equation_data = generate_equation()
        st.session_state.attempts = 0
        st.session_state.feedback_message = None
        st.session_state.feedback_type = None
        st.session_state.user_input = ""
        st.experimental_rerun()

    with st.expander("💡 Need help? Click here for solving steps"):
        st.write("To solve an equation in the form `ax + b = c`:")
        st.markdown("""
        1. Subtract `b` from both sides → `ax = c - b`  
        2. Divide both sides by `a` → `x = (c - b) / a`  
        3. Simplify to get your answer
        """)

    if st.button("🔁 Reset Score"):
        st.session_state.score = 0
        st.experimental_rerun()

if __name__ == "__main__":
    main()

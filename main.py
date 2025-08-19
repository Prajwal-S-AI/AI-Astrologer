!pip install gradio -q
import gradio as gr
import random

# --- Astrology Logic ---
def generate_prediction(name, dob, tob, place):
    zodiacs = [
        "🌟 You will find success in your career soon.",
        "💖 A new opportunity in relationships may arise.",
        "🧘 Focus on your health and inner peace.",
        "💰 Financial growth is on the horizon.",
        "⚡ You may face challenges, but you will overcome them."
    ]
    return f"Hello {name}, based on your details (DOB: {dob}, TOB: {tob}, Place: {place}),\n\n" \
           f"✨ Your stars suggest: {random.choice(zodiacs)}"

def answer_question(question):
    q = question.lower()
    if "career" in q:
        return "🌟 Your career path looks promising; stay focused."
    elif "love" in q or "relationship" in q:
        return "💖 A positive shift in relationships may occur soon."
    elif "health" in q:
        return "🧘 Take care of your health by balancing work and rest."
    elif "money" in q or "finance" in q:
        return "💰 Financial improvements may be coming your way."
    else:
        return "🔮 The stars are unclear, but stay positive and hopeful."

# --- Gradio UI ---
def get_prediction(name, dob, tob, place):
    return generate_prediction(name, dob, tob, place)

def ask_question(question):
    return answer_question(question)

with gr.Blocks() as demo:
    gr.Markdown("# AI Astrologer App")

    with gr.Tab("🔮 Horoscope Prediction"):
        name = gr.Textbox(label="Name", placeholder="Enter your full name")
        dob = gr.Textbox(label="Date of Birth", placeholder="DD/MM/YYYY")
        tob = gr.Textbox(label="Time of Birth", placeholder="HH:MM")
        place = gr.Textbox(label="Place of Birth", placeholder="City, Country")
        predict_btn = gr.Button("Generate Prediction")
        prediction_output = gr.Textbox(label="Prediction", lines=4)
        predict_btn.click(get_prediction, [name, dob, tob, place], prediction_output)

    with gr.Tab("✨ Ask a Question"):
        question = gr.Textbox(label="Your Question", placeholder="e.g., How is my career going?")
        ask_btn = gr.Button("Ask the Stars")
        answer_output = gr.Textbox(label="Astrology Answer", lines=3)
        ask_btn.click(ask_question, question, answer_output)

demo.launch()

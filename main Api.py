# ai_astrologer_app_gradio.py

import gradio as gr
from openai import OpenAI
import datetime
import plotly.graph_objects as go
from geopy.geocoders import Nominatim
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.const import SUN, MOON, MERCURY, VENUS, MARS, JUPITER, SATURN, ASC

# ---------------- OpenAI Client ---------------- #
client = OpenAI(api_key="Enter api key")

# ---------------- Utility Functions ---------------- #
def decimal_to_dms(decimal_deg):
    is_negative = decimal_deg < 0
    decimal_deg = abs(decimal_deg)
    degrees = int(decimal_deg)
    minutes_full = (decimal_deg - degrees) * 60
    minutes = int(minutes_full)
    seconds = int((minutes_full - minutes) * 60)
    return f"{'-' if is_negative else ''}{degrees}:{minutes}:{seconds}"

def generate_zodiac_positions(dob, tob, place_name):
    geolocator = Nominatim(user_agent="astro_app")
    location = geolocator.geocode(place_name)
    if not location:
        return {"error": "Location not found. Please enter a valid city/town."}

    lat_dms = decimal_to_dms(location.latitude)
    lon_dms = decimal_to_dms(location.longitude)

    date_str = dob.strftime('%Y/%m/%d')
    time_str = tob if tob else "12:00"

    dt = Datetime(date_str, time_str, '+05:30')
    pos = GeoPos(lat_dms, lon_dms)

    chart = Chart(dt, pos)
    planets = [SUN, MOON, MERCURY, VENUS, MARS, JUPITER, SATURN, ASC]
    positions = {body: chart.get(body).sign for body in planets}

    return positions

# ---------------- Astrology Reading ---------------- #
def get_astrology_reading(name, dob, time, place, favorite_number):
    try:
        # Convert DOB (string) -> datetime.date
        if isinstance(dob, str):
            dob = datetime.datetime.strptime(dob, "%Y-%m-%d").date()

        prompt = (
            f"I want you to act as a professional astrologer and give a detailed astrology and numerology reading "
            f"for someone named {name} born on {dob} at {time} in {place}. "
            f"Their favorite number is {favorite_number}. Also, rate their Love, Career, Health, and Spirituality from 1 to 10."
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        result = response.choices[0].message.content

        # Radar chart (placeholder values for now)
        categories = ['Love', 'Career', 'Health', 'Spirituality']
        values = [8, 7, 6, 9]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Life Aspects',
            line=dict(color='gold')
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 10])
            ),
            showlegend=False
        )

        zodiac_data = generate_zodiac_positions(dob, time, place)
        if "error" in zodiac_data:
            zodiac_result = zodiac_data["error"]
        else:
            zodiac_result = "\n".join([f"{planet}: {sign}" for planet, sign in zodiac_data.items()])

        return result, fig, zodiac_result

    except Exception as e:
        return f"Error: {e}", None, None

# ---------------- Chatbot ---------------- #
messages = [{"role": "system", "content": "You are an expert astrologer. Answer with deep astrology & numerology knowledge."}]

def astro_chat(user_input):
    messages.append({"role": "user", "content": user_input})
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        return reply
    except Exception as e:
        return f"Error: {e}"

# ---------------- Gradio UI ---------------- #
with gr.Blocks(theme=gr.themes.Soft(primary_hue="purple")) as demo:
    gr.Markdown("## 🔮 AI Astrologer")
    gr.Markdown("Get your personalized astrology and numerology reading")

    with gr.Row():
        name = gr.Textbox(label="Name")
        dob = gr.Textbox(label="Date of Birth (YYYY-MM-DD)")
    with gr.Row():
        time = gr.Textbox(label="Time of Birth (HH:MM format)")
        place = gr.Textbox(label="Place of Birth")
    favorite_number = gr.Textbox(label="Favorite Number")

    btn = gr.Button("🔍 Get My Reading")
    output_text = gr.Markdown()
    output_chart = gr.Plot()
    output_zodiac = gr.Textbox(label="Planetary Positions", lines=8)

    btn.click(get_astrology_reading, inputs=[name, dob, time, place, favorite_number],
              outputs=[output_text, output_chart, output_zodiac])

    gr.Markdown("---")
    gr.Markdown("### 💬 Ask the AI Astrologer")
    chat_in = gr.Textbox(label="Your Question")
    chat_out = gr.Textbox(label="Astrologer's Reply")

    chat_in.submit(astro_chat, inputs=chat_in, outputs=chat_out)

demo.launch()

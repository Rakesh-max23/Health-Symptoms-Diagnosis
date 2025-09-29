from flask import Flask, render_template, request, jsonify, url_for
import pickle
import pandas as pd
import mysql.connector
import google.generativeai as genai

app = Flask(__name__)

model = pickle.load(open("model/model.pkl", "rb"))

genai.configure(api_key="AIzaSyBKD8e0VmjjNYdl7GZAcZbU3pQ1-TV_kSw") 

db = mysql.connector.connect(
    host="localhost",
    user="root",         
    password="9819572170", 
    database="health_checker"
)
cursor = db.cursor()

SYMPTOMS = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain', 
'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition', 'spotting_ urination',
'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness', 'lethargy', 
'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes', 'breathlessness', 'sweating', 
'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 
'pain_behind_the_eyes', 'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine', 
'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 
'blurred_and_distorted_vision', 'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 
'congestion', 'chest_pain', 'weakness_in_limbs', 'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 
'bloody_stool', 'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs', 
'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties', 
'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech', 'knee_pain', 'hip_joint_pain', 
'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness', 'spinning_movements', 'loss_of_balance', 
'unsteadiness', 'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine', 
'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)', 'depression', 'irritability', 
'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain', 'abnormal_menstruation', 'dischromic _patches', 
'watering_from_eyes', 'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum', 'rusty_sputum', 
'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 
'stomach_bleeding', 'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload.1', 'blood_in_sputum', 
'prominent_veins_on_calf', 'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 
'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose', 
'yellow_crust_ooze']

@app.route("/")
def index():
    return render_template("index.html", symptoms=SYMPTOMS)

@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        selected_symptoms = request.form.getlist("symptoms")

        input_data = [1 if symptom in selected_symptoms else 0 for symptom in SYMPTOMS]
        input_df = pd.DataFrame([input_data], columns=SYMPTOMS)

        prediction = model.predict(input_df)[0]

        symptoms_str = ", ".join(selected_symptoms)
        query = "INSERT INTO history (symptoms, predicted_disease) VALUES (%s, %s)"
        values = (symptoms_str, prediction)
        cursor.execute(query, values)
        db.commit()

        return render_template("results.html", disease=prediction, symptoms=selected_symptoms)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    model_ai = genai.GenerativeModel("gemini-1.5-flash")

    response = model_ai.generate_content(
        f"You are a helpful medical  assistant. The user said: {user_message}. "
        f"Give a safe health suggestion in simple words."
    )

    return jsonify({"reply": response.text})

@app.route("/history")
def history():
    cursor.execute("SELECT id, symptoms, predicted_disease, created_at FROM history ORDER BY created_at DESC LIMIT 20")
    records = cursor.fetchall()
    return render_template("history.html", records=records)

@app.route("/delete_history/<int:record_id>")
def delete_history(record_id):
    cursor.execute("DELETE FROM history WHERE id = %s", (record_id,))
    db.commit()
    return history()


if __name__ == "__main__":
    app.run(debug=True)

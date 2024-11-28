import tkinter as tk
from tkinter import ttk, messagebox
import joblib
import math

# Load the machine learning model
joblib_filename = "model.joblib"
model = joblib.load(joblib_filename)

# Dictionaries
city_names = {
    '0': 'Ahmedabad', '1': 'Bengaluru', '2': 'Chennai', '3': 'Coimbatore', '4': 'Delhi',
    '5': 'Ghaziabad', '6': 'Hyderabad', '7': 'Indore', '8': 'Jaipur', '9': 'Kanpur',
    '10': 'Kochi', '11': 'Kolkata', '12': 'Kozhikode', '13': 'Lucknow', '14': 'Mumbai',
    '15': 'Nagpur', '16': 'Patna', '17': 'Pune', '18': 'Surat'
}
crimes_names = {
    '0': 'Crime Committed by Juveniles', '1': 'Crime against SC', '2': 'Crime against ST',
    '3': 'Crime against Senior Citizen', '4': 'Crime against children', '5': 'Crime against women',
    '6': 'Cyber Crimes', '7': 'Economic Offences', '8': 'Kidnapping', '9': 'Murder'
}
population = {
    '0': '63.50', '1': '85.00', '2': '87.00', '3': '21.50', '4': '163.10', '5': '23.60', '6': '77.50',
    '7': '21.70', '8': '30.70', '9': '29.20', '10': '21.20', '11': '141.10', '12': '20.30', '13': '29.00',
    '14': '184.10', '15': '25.00', '16': '20.50', '17': '50.50', '18': '45.80'
}

# Reverse dictionaries for dropdown lookup
city_codes = {v: k for k, v in city_names.items()}
crime_codes = {v: k for k, v in crimes_names.items()}

# Prediction logic
def predict():
    selected_city = city_dropdown.get()
    selected_crime = crime_dropdown.get()
    year = year_dropdown.get()

    if not selected_city or not selected_crime or not year:
        messagebox.showerror("Input Error", "Please select all inputs!")
        return

    city_code = city_codes[selected_city]
    crime_code = crime_codes[selected_crime]
    pop = float(population[city_code])
    year_diff = int(year) - 2011
    pop += 0.01 * year_diff * pop

    # Predict crime rate
    crime_rate = model.predict([[int(year), int(city_code), pop, int(crime_code)]])[0]

    # Determine crime status
    if crime_rate <= 1:
        crime_status = "Very Low Crime Area"
    elif crime_rate <= 5:
        crime_status = "Low Crime Area"
    elif crime_rate <= 15:
        crime_status = "High Crime Area"
    else:
        crime_status = "Very High Crime Area"

    # Calculate estimated number of cases
    cases = math.ceil(crime_rate * pop)

    # Display results
    result_text.set(
        f"City: {selected_city}\n"
        f"Crime Type: {selected_crime}\n"
        f"Year: {year}\n"
        f"Crime Status: {crime_status}\n"
        f"Crime Rate: {crime_rate:.2f}\n"
        f"Estimated Cases: {cases}\n"
        f"Population: {pop:.2f} Lakhs"
    )

# Tkinter GUI
root = tk.Tk()
root.title("Crime Rate Predictor")
root.geometry("800x900")
root.configure(bg="#fff2df")

# Title
title = tk.Label(root, text="Crime Rate Predictor", font=("Lora", 24, "italic"), bg="#002244", fg="#fff2df")
title.pack(fill=tk.X, pady=10)

# Tagline
tagline = tk.Label(root, text="Unlock Safety: Reduce Crime Rate Together", font=("Lora", 14), bg="#002244", fg="#fff2df")
tagline.pack(fill=tk.X)

# Input Section
frame = tk.Frame(root, bg="#fff2df")
frame.pack(pady=20)

# Dropdowns
tk.Label(frame, text="Select City:", font=("Lora", 14), bg="#fff2df").grid(row=0, column=0, pady=5, sticky=tk.W)
city_dropdown = ttk.Combobox(frame, values=list(city_names.values()), state="readonly", width=30)
city_dropdown.grid(row=0, column=1, pady=5)

tk.Label(frame, text="Select Crime Type:", font=("Lora", 14), bg="#fff2df").grid(row=1, column=0, pady=5, sticky=tk.W)
crime_dropdown = ttk.Combobox(frame, values=list(crimes_names.values()), state="readonly", width=30)
crime_dropdown.grid(row=1, column=1, pady=5)

tk.Label(frame, text="Select Year:", font=("Lora", 14), bg="#fff2df").grid(row=2, column=0, pady=5, sticky=tk.W)
year_dropdown = ttk.Combobox(frame, values=[str(y) for y in range(2000, 2051)], state="readonly", width=20)
year_dropdown.grid(row=2, column=1, pady=5)

# Predict Button
predict_button = tk.Button(root, text="Predict", font=("Lora", 14, "bold"), bg="#002244", fg="#fff2df", command=predict)
predict_button.pack(pady=20)

# Results Section
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, font=("Lora", 14), bg="#fff2df", justify=tk.LEFT)
result_label.pack(pady=20)

# Footer
footer = tk.Label(root, text="About Crime Forecasting", font=("Lora", 12), bg="#002244", fg="#fff2df")
footer.pack(fill=tk.X, pady=10)

# Introduction Section
introduction = tk.Text(root, font=("Lora", 12), bg="#fff2df", wrap=tk.WORD, height=20, padx=20, pady=20)
introduction.insert(
    tk.END,
    """Crime rate prediction has become an important tool for law enforcement agencies to help them better understand patterns of crime and anticipate where crime is likely to occur. By predicting future crime trends, law enforcement agencies can better allocate resources to areas that are likely to experience increases in criminal activity. This could lead to a decrease in crime overall, as well as an increase in public safety. Additionally, crime rate prediction can help police departments develop better strategies for responding to crime as it happens.

    The dataset is prepared manually based on the publication available on the Indian National Crime Rate Bureau (NCRB) official website. This data provides statistics on crimes committed in 19 metropolitan cities during the year 2014 to 2021. With the help of this application, we can predict the crime rates for 10 different categories of crime that are likely to occur in 19 Indian metropolitan cities over the next few years. It includes statistics on 10 different categories of crime, including murder, kidnapping, crime against women, crime against children, crime committed by juveniles, crime against senior citizens, crime against SC, crime against ST, economic offences and cyber crimes.

    The system uses scikit-learn's Random Forest Regression model, which takes year, city name, and crime type data as inputs. Random Forest Regression is a type of ensemble learning technique that can be used to predict continuous values from a collection of data. It works by creating a large number of "decision trees" which each make a prediction about the target variable. Then it averages all the predictions to come up with a final prediction. This makes it more accurate than a single decision tree. The model predicts the crime rate with an accuracy of 93.20 percent on the testing dataset."""
)
introduction.config(state=tk.DISABLED)
introduction.pack(fill=tk.BOTH, pady=10)

root.mainloop()

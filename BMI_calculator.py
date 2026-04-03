import tkinter as tk
import tkinter.messagebox
import csv
from datetime import datetime
import os
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import initialize_database, save_record, load_records, load_all_records


initialize_database()

def analyze_user_trends():
    user_name = analyze_name_entry.get().strip()
    if not user_name:
        tk.messagebox.showerror("Input Error", "Please enter a name to analyze.")
        return
    
    records = load_records(user_name)
    
    if not records:
        tk.messagebox.showinfo("No Data", f"No records found for '{user_name}'.")
        return
        
    analysis_window = tk.Toplevel(root)
    analysis_window.title(f"Analysis for {user_name}")
    analysis_window.geometry("800x600")
    analysis_window.config(bg="#f0f0f0")

    df = pd.DataFrame(records, columns=['Timestamp', 'BMI'])
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    stats_frame = tk.Frame(analysis_window, bg="#f0f0f0")
    stats_frame.pack(pady=10, padx=10, fill=tk.X)
    
    avg_bmi = df['BMI'].mean()
    max_bmi = df['BMI'].max()
    min_bmi = df['BMI'].min()

    stats_label = tk.Label(stats_frame, 
                           text=f"Statistics for {user_name}:\n"
                                f"Average BMI: {avg_bmi:.2f}\n"
                                f"Highest BMI: {max_bmi:.2f}\n"
                                f"Lowest BMI: {min_bmi:.2f}",
                           font=("Helvetica", 12), bg="#f0f0f0", justify=tk.LEFT)
    stats_label.pack()

    fig = Figure(figsize=(7, 4), dpi=100)
    plot = fig.add_subplot(1, 1, 1)
    
    plot.plot(df['Timestamp'], df['BMI'], marker='o', linestyle='-', color='b')
    plot.set_title(f"BMI Trend for {user_name}")
    plot.set_xlabel("Date")
    plot.set_ylabel("BMI")
    plot.grid(True)
    fig.autofmt_xdate()

    canvas = FigureCanvasTkAgg(fig, master=analysis_window)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10, padx=10)

def bmi_calculator(weight, height):
    if height == 0:
        return 0
    bmi = weight / (height ** 2)
    return round(bmi, 2)
    
def open_history_window():
    history_window = tk.Toplevel(root)
    history_window.title("Full BMI History")
    history_window.geometry("800x600")
    history_window.config(bg="#f0f0f0")
    history_window.grab_set()

    history_text = tk.Text(history_window, font=("Courier", 12), wrap=tk.NONE, state="disabled")
    history_text.pack(expand=True, fill="both", padx=10, pady=10)
    
    all_records = load_all_records()
    
    history_text.config(state="normal")
    if not all_records:
        history_text.insert(tk.END, "No history found. Calculate a BMI to create a record.")
    else:
        header = f"{'Timestamp':<20} | {'Name':<15} | {'BMI':<8} | {'Category'}\n"
        history_text.insert(tk.END, header)
        history_text.insert(tk.END, "="*80 + "\n")
        
        for record in all_records:
            timestamp, name, bmi, category = record
            formatted_time = datetime.fromisoformat(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            display_row = f"{formatted_time:<20} | {name:<15} | {bmi:<8.2f} | {category}\n"
            history_text.insert(tk.END, display_row)
    
    history_text.config(state="disabled")

def on_click():
    try:
        name = user_entry.get().strip()
        if not name:
            result_label.config(text="Please enter your name.", fg="white", bg="#c03b2b")
            return

        weight = float(weight_entry.get())
        height = float(height_entry.get())
        
        result_label.config(bg="#3498db")

        if height <= 0 or weight <= 0:
            result_label.config(text="Please enter positive values.", fg="white", bg="#c03b2b")
            return
        
        bmi = bmi_calculator(weight, height)
        category, message, text_color, bg_color = "", "", "white", "#3498db"

        if bmi < 18.5:
            category, message, text_color, bg_color = "Underweight", "You are in the underweight range.", "white", "#000080"
        elif 18.5 <= bmi < 25:
            category, message, text_color, bg_color = "Normal weight", "Excellent! You are in a healthy range.", "white", "#27ae60"
        elif 25 <= bmi < 30:
            category, message, text_color, bg_color = "Overweight", "You are in the overweight range.", "black", "#f39c12"
        else:
            category, message, text_color, bg_color = "Obesity", "You are in the obesity range.", "white", "#c03b2b"

        save_record(name, weight, height, bmi, category)

        result_label.config(text=f"BMI: {bmi}\nCategory: {category}\n\n{message}", fg=text_color, bg=bg_color)
    except ValueError:
        result_label.config(text="Please enter valid numbers.", fg="white", bg="#c03b2b")

root = tk.Tk()
root.title("BMI Calculator")
root.geometry("500x700")
root.config(bg="#3498db")

input_frame = tk.Frame(root, bg="#3498db")
input_frame.pack(pady=10)

user_label = tk.Label(input_frame, text="Your Name:", bg="#3498db", fg="white", font=("Helvetica", 14,"bold"))
user_label.pack()
user_entry = tk.Entry(input_frame, font=("Helvetica", 14), width=20)
user_entry.pack(pady=5)

weight_label = tk.Label(input_frame, text="Weight (kg):", bg="#3498db", fg="white", font=("Helvetica", 14,"bold"))
weight_label.pack()
weight_entry = tk.Entry(input_frame, font=("Helvetica", 14), width=20)
weight_entry.pack(pady=5)

height_label = tk.Label(input_frame, text="Height (m):", bg="#3498db", fg="white", font=("Helvetica", 14, "bold"))
height_label.pack()
height_entry = tk.Entry(input_frame, font=("Helvetica", 14), width=20)
height_entry.pack(pady=5)

calculate_but = tk.Button(root, text="Calculate BMI", fg= "white", font=("Helvetica", 16, "bold"), bg="#FF8400", command=on_click)
calculate_but.pack(pady=10)

history_button = tk.Button(root, text="View History", fg="white", font=("Helvetica", 14, "bold"), bg="#5D6D7E", command=open_history_window)
history_button.pack(pady=5)

result_label = tk.Label(root, text="", bg="#3498db", fg="white", font=("Helvetica", 16, "bold"), justify=tk.CENTER)
result_label.pack(pady=10)

separator = tk.Frame(root, height=2, bg="white", bd=0)
separator.pack(fill=tk.X, padx=20, pady=10)

analysis_frame = tk.Frame(root, bg="#3498db")
analysis_frame.pack(pady=10)

analyze_name_label = tk.Label(analysis_frame, text="Enter Name to Analyze:", bg="#3498db", fg="white", font=("Helvetica", 14, "bold"))
analyze_name_label.pack()
analyze_name_entry = tk.Entry(analysis_frame, font=("Helvetica", 14), width=20)
analyze_name_entry.pack(pady=5)

analyze_button = tk.Button(analysis_frame, text="Analyze Trends", fg="white", font=("Helvetica", 16, "bold"), bg="#9B59B6", command=analyze_user_trends)
analyze_button.pack(pady=10)

root.mainloop()

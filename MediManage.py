import tkinter as tk
from tkinter import messagebox

import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'mypassword',
    'database': 'hospital',
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    age INT,
    gender VARCHAR(10),
    address TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    date DATE,
    time TIME
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS billing (
    bill_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    amount DECIMAL(10, 2),
    paid BOOLEAN
)
""")
conn.commit()
def add_billing():
    patient_id = entry_billing_patient_id.get()
    amount = entry_billing_amount.get()
    paid = entry_billing_paid.get()

    cursor.execute("INSERT INTO billing (patient_id, amount, paid) VALUES (%s, %s, %s)",
                   (patient_id, amount, paid))
    conn.commit()

    entry_billing_patient_id.delete(0, tk.END)
    entry_billing_amount.delete(0, tk.END)
    entry_billing_paid.delete(0, tk.END)

    messagebox.showinfo("Success", "Billing record added successfully.")

def edit_billing():
    bill_id = entry_billing_patient_id.get()
    amount = entry_billing_amount.get()
    paid = entry_billing_paid.get()

    cursor.execute("UPDATE billing SET amount = ?, paid = ? WHERE bill_id = ?",
                   (amount, paid, bill_id))
    conn.commit()

    entry_billing_patient_id.delete(0, tk.END)
    entry_billing_amount.delete(0, tk.END)
    entry_billing_paid.delete(0, tk.END)

    messagebox.showinfo("Success", "Billing record updated successfully.")

def delete_billing():
    bill_id = entry_billing_patient_id.get()

    confirm = messagebox.askyesno("Delete Billing Record", "Are you sure you want to delete this billing record?")
    if confirm:
        cursor.execute("DELETE FROM billing WHERE bill_id = ?", (bill_id,))
        conn.commit()
        entry_billing_patient_id.delete(0, tk.END)
        messagebox.showinfo("Success", "Billing record deleted successfully.")
root = tk.Tk()
root.title("Hospital Management System")
tk.Label(root, text="Billing Patient ID").grid(row=9, column=0)
entry_billing_patient_id = tk.Entry(root)
entry_billing_patient_id.grid(row=9, column=1)

tk.Label(root, text="Billing Amount").grid(row=10, column=0)
entry_billing_amount = tk.Entry(root)
entry_billing_amount.grid(row=10, column=1)

tk.Label(root, text="Billing Paid (True/False)").grid(row=11, column=0)
entry_billing_paid = tk.Entry(root)
entry_billing_paid.grid(row=11, column=1)

# Buttons for billing
add_billing_button = tk.Button(root, text="Add Billing Record", command=add_billing)
add_billing_button.grid(row=12, column=0, columnspan=2)

edit_billing_button = tk.Button(root, text="Edit Billing Record", command=edit_billing)
edit_billing_button.grid(row=13, column=0, columnspan=2)

delete_billing_button = tk.Button(root, text="Delete Billing Record", command=delete_billing)
delete_billing_button.grid(row=14, column=0, columnspan=2)
def add_patient():
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    age = entry_age.get()
    gender = entry_gender.get()
    address = entry_address.get()

    cursor.execute("INSERT INTO patients (first_name, last_name, age, gender, address) VALUES (%s, %s, %s, %s, %s)",
                   (first_name, last_name, age, gender, address))
    conn.commit()

    entry_first_name.delete(0, tk.END)
    entry_last_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_gender.delete(0, tk.END)
    entry_address.delete(0, tk.END)

    messagebox.showinfo("Success", "Patient information added successfully.")

def edit_patient():
    patient_id = entry_edit_patient_id.get()
    first_name = entry_edit_first_name.get()
    last_name = entry_edit_last_name.get()
    age = entry_edit_age.get()
    gender = entry_edit_gender.get()
    address = entry_edit_address.get()

    cursor.execute("UPDATE patients SET first_name = %s, last_name = %s, age = %s, gender = %s, address = %s WHERE patient_id = %s",
                   (first_name, last_name, age, gender, address, patient_id))
    conn.commit()

    entry_edit_patient_id.delete(0, tk.END)
    entry_edit_first_name.delete(0, tk.END)
    entry_edit_last_name.delete(0, tk.END)
    entry_edit_age.delete(0, tk.END)
    entry_edit_gender.delete(0, tk.END)
    entry_edit_address.delete(0, tk.END)

    messagebox.showinfo("Success", "Patient details updated successfully.")

def delete_patient():
    patient_id = entry_delete_patient_id.get()

    confirm = messagebox.askyesno("Delete Patient", "Are you sure you want to delete this patient record?")
    if confirm:
        cursor.execute("DELETE FROM patients WHERE patient_id = %s", (patient_id,))
        conn.commit()
        entry_delete_patient_id.delete(0, tk.END)
        messagebox.showinfo("Success", "Patient record deleted successfully.")
def view_patients():
    # Create a new window for displaying patient records
    view_patients_window = tk.Toplevel(root)
    view_patients_window.title("View Patients")

    # Create a text widget to display patient records
    patient_records_text = tk.Text(view_patients_window)
    patient_records_text.pack()

    # Query the database to fetch patient records
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()

    # Display the patient records in the text widget
    for patient in patients:
        patient_records_text.insert(tk.END, f"Patient ID: {patient[0]}\n")
        patient_records_text.insert(tk.END, f"First Name: {patient[1]}\n")
        patient_records_text.insert(tk.END, f"Last Name: {patient[2]}\n")
        patient_records_text.insert(tk.END, f"Age: {patient[3]}\n")
        patient_records_text.insert(tk.END, f"Gender: {patient[4]}\n")
        patient_records_text.insert(tk.END, f"Address: {patient[5]}\n")
        patient_records_text.insert(tk.END, "\n")

# Create a button to trigger the view_patients function
view_patients_button = tk.Button(root, text="View Patients", command=view_patients)
view_patients_button.grid(row=24, column=0, columnspan=2)
root = tk.Tk()
root.title("Hospital Management System")

# Create and place labels and entry fields
tk.Label(root, text="First Name").grid(row=0, column=0)
entry_first_name = tk.Entry(root)
entry_first_name.grid(row=0, column=1)

tk.Label(root, text="Last Name").grid(row=1, column=0)
entry_last_name = tk.Entry(root)
entry_last_name.grid(row=1, column=1)

tk.Label(root, text="Age").grid(row=2, column=0)
entry_age = tk.Entry(root)
entry_age.grid(row=2, column=1)

tk.Label(root, text="Gender").grid(row=3, column=0)
entry_gender = tk.Entry(root)
entry_gender.grid(row=3, column=1)

tk.Label(root, text="Address").grid(row=4, column=0)
entry_address = tk.Entry(root)
entry_address.grid(row=4, column=1)

# Create and place buttons
add_button = tk.Button(root, text="Add Patient", command=add_patient)
add_button.grid(row=5, column=0, columnspan=2)

view_button = tk.Button(root, text="View Patients", command=view_patients)
view_button.grid(row=6, column=0, columnspan=2)
def add_appointment():
    patient_id = entry_appointment_patient_id.get()
    date = entry_appointment_date.get()
    time = entry_appointment_time.get()

    cursor.execute("INSERT INTO appointments (patient_id, date, time) VALUES (%s, %s, %s)",
                   (patient_id, date, time))
    conn.commit()

    entry_appointment_patient_id.delete(0, tk.END)
    entry_appointment_date.delete(0, tk.END)
    entry_appointment_time.delete(0, tk.END)

    messagebox.showinfo("Success", "Appointment added successfully.")

def edit_appointment():
    appointment_id = entry_appointment_patient_id.get()
    date = entry_appointment_date.get()
    time = entry_appointment_time.get()

    cursor.execute("UPDATE appointments SET date = %s, time = %s WHERE appointment_id = %s",
                   (date, time, appointment_id))
    conn.commit()

    entry_appointment_patient_id.delete(0, tk.END)
    entry_appointment_date.delete(0, tk.END)
    entry_appointment_time.delete(0, tk.END)

    messagebox.showinfo("Success", "Appointment updated successfully.")

def delete_appointment():
    appointment_id = entry_appointment_patient_id.get()

    confirm = messagebox.askyesno("Delete Appointment", "Are you sure you want to delete this appointment?")
    if confirm:
        cursor.execute("DELETE FROM appointments WHERE appointment_id = %s", (appointment_id,))
        conn.commit()
        entry_appointment_patient_id.delete(0, tk.END)
        messagebox.showinfo("Success", "Appointment deleted successfully.")

# Create the main application window
root = tk.Tk()
root.title("Hospital Management System")

# Create and place labels and entry fields for appointments
tk.Label(root, text="Appointment Patient ID").grid(row=7, column=0)
entry_appointment_patient_id = tk.Entry(root)
entry_appointment_patient_id.grid(row=7, column=1)

tk.Label(root, text="Appointment Date").grid(row=8, column=0)
entry_appointment_date = tk.Entry(root)
entry_appointment_date.grid(row=8, column=1)

tk.Label(root, text="Appointment Time").grid(row=9, column=0)
entry_appointment_time = tk.Entry(root)
entry_appointment_time.grid(row=9, column=1)

# Buttons for appointments
add_appointment_button = tk.Button(root, text="Add Appointment", command=add_appointment)
add_appointment_button.grid(row=10, column=0, columnspan=2)

edit_appointment_button = tk.Button(root, text="Edit Appointment", command=edit_appointment)
edit_appointment_button.grid(row=11, column=0, columnspan=2)

delete_appointment_button = tk.Button(root, text="Delete Appointment", command=delete_appointment)
delete_appointment_button.grid(row=12, column=0, columnspan=2)



root = tk.Tk()
root.title("Hospital Management System")

tk.Label(root, text="Edit Patient ID").grid(row=15, column=0)
entry_edit_patient_id = tk.Entry(root)
entry_edit_patient_id.grid(row=15, column=1)

tk.Label(root, text="Edit First Name").grid(row=16, column=0)
entry_edit_first_name = tk.Entry(root)
entry_edit_first_name.grid(row=16, column=1)

tk.Label(root, text="Edit Last Name").grid(row=17, column=0)
entry_edit_last_name = tk.Entry(root)
entry_edit_last_name.grid(row=17, column=1)

tk.Label(root, text="Edit Age").grid(row=18, column=0)
entry_edit_age = tk.Entry(root)
entry_edit_age.grid(row=18, column=1)

tk.Label(root, text="Edit Gender").grid(row=19, column=0)
entry_edit_gender = tk.Entry(root)
entry_edit_gender.grid(row=19, column=1)

tk.Label(root, text="Edit Address").grid(row=20, column=0)
entry_edit_address = tk.Entry(root)
entry_edit_address.grid(row=20, column=1)

tk.Label(root, text="Delete Patient ID").grid(row=21, column=0)
entry_delete_patient_id = tk.Entry(root)
entry_delete_patient_id.grid(row=21, column=1)

edit_patient_button = tk.Button(root, text="Edit Patient Details", command=edit_patient)
edit_patient_button.grid(row=22, column=0, columnspan=2)

delete_patient_button = tk.Button(root, text="Delete Patient Record", command=delete_patient)
delete_patient_button.grid(row=23, column=0, columnspan=2)



root.mainloop()

conn.close()
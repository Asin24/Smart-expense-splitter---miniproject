import tkinter as tk
from tkinter import messagebox, ttk

# Function to toggle password visibility
def toggle_password():
    if password_entry["show"] == "*":
        password_entry["show"] = ""
        confirm_password_entry["show"] = ""
        toggle_btn.config(text="🙈 Hide")
    else:
        password_entry["show"] = "*"
        confirm_password_entry["show"] = "*"
        toggle_btn.config(text="👀 Show")

# Function to handle form submission
def submit_form():
    full_name = name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    institution = institution_entry.get()
    user_role = role_var.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    # Input Validations
    if len(full_name) < 3:
        messagebox.showerror("Error", "Full Name must be at least 3 characters long.")
        return
    if "@" not in email or "." not in email:
        messagebox.showerror("Error", "Invalid email format.")
        return
    if not phone.isdigit() or len(phone) != 10:
        messagebox.showerror("Error", "Enter a valid 10-digit phone number.")
        return
    if institution.strip() == "":
        messagebox.showerror("Error", "Institution Name is required.")
        return
    if user_role not in ["Issuer", "Verifier", "Recipient"]:
        messagebox.showerror("Error", "Please select a valid user role.")
        return
    if len(password) < 8:
        messagebox.showerror("Error", "Password must be at least 8 characters long.")
        return
    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match.")
        return

    # If all inputs are valid
    messagebox.showinfo("Success", f"🎉 Registration Successful!\n\nWelcome, {full_name} ({user_role})!")

# Create the main window
root = tk.Tk()
root.title("Blockchain-Based Certificate Verification")
root.geometry("500x550")
root.configure(bg="black")

# Title Label
tk.Label(root, text="🔗 Blockchain-Based Certificate Verification", font=("Arial", 16, "bold"), fg="purple", bg="black").pack(pady=10)

# Function to create labels and entry fields
def create_label_entry(text, is_password=False):
    tk.Label(root, text=text, font=("Arial", 11, "bold"), fg="purple", bg="black").pack(pady=2)
    entry = tk.Entry(root, width=40, font=("Arial", 11), bg="gray20", fg="white", insertbackground="white", relief="ridge", bd=5)
    if is_password:
        entry.config(show="*")
    entry.pack()
    return entry

# Creating Input Fields
name_entry = create_label_entry("Full Name:")
email_entry = create_label_entry("Email:")
phone_entry = create_label_entry("Phone Number:")
institution_entry = create_label_entry("Institution Name:")

# Role Selection Dropdown
tk.Label(root, text="Select Role:", font=("Arial", 11, "bold"), fg="purple", bg="black").pack(pady=2)
role_var = tk.StringVar()
role_dropdown = ttk.Combobox(root, textvariable=role_var, values=["Issuer", "Verifier", "Recipient"], state="readonly", width=37)
role_dropdown.pack(pady=5)

password_entry = create_label_entry("Password:", is_password=True)
confirm_password_entry = create_label_entry("Confirm Password:", is_password=True)

# Password Toggle Button
toggle_btn = tk.Button(root, text="👀 Show", command=toggle_password, font=("Arial", 10), bg="purple", fg="white", relief="ridge", bd=5)
toggle_btn.pack(pady=5)

# Submit Button with 3D Effect and Hover Effect
def on_enter(e):
    submit_button.config(bg="gold", fg="black")

def on_leave(e):
    submit_button.config(bg="purple", fg="white")

submit_button = tk.Button(root, text="🚀 Register Now", command=submit_form, 
                          font=("Arial", 12, "bold"), bg="purple", fg="white", 
                          relief="raised", bd=7, padx=15, pady=7)
submit_button.pack(pady=20)

submit_button.bind("<Enter>", on_enter)
submit_button.bind("<Leave>", on_leave)

# Run the application
root.mainloop()

import socket
import tkinter as tk
from tkinter import messagebox

# Create the main Tkinter window
root = tk.Tk()
root.title("Login")

# Function to handle login
def login():
    username = username_entry.get()
    password = password_entry.get()
    if username == "kamillo" and password == "password":  # Example check
        messagebox.showinfo("Login", "Login successful!")
        show_timer_screen()
    else:
        messagebox.showerror("Login", "Invalid username or password")

# Function to handle sending timer details
def send_timer():
    time_to_explosion = time_entry.get()
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_ip = "10.207.1.146"  # Replace with the server's IP address
        server_port = 8000  # Replace with the server's port number
        client.connect((server_ip, server_port))
        client.send(time_to_explosion.encode("utf-8"))
        
        while True:
            response = client.recv(1024)
            response = response.decode("utf-8")
            messagebox.showinfo("Server Response", f"Received: {response}")
            
            if response.lower() == "self destruct finished":
                client.close()
                messagebox.showinfo("Server", "Connection to server closed")
            else:
                print(f"Received: {response}")
            
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to show the timer screen
def show_timer_screen():
    for widget in root.winfo_children():
        widget.destroy()
    
    tk.Label(root, text="Time to explosion (seconds)").grid(row=0, column=0)
    global time_entry
    time_entry = tk.Entry(root)
    time_entry.grid(row=0, column=1)
    
    tk.Button(root, text="Send Timer", command=send_timer).grid(row=1, columnspan=2)

# Username label and text entry box
tk.Label(root, text="Username").grid(row=0, column=0)
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1)

# Password label and password entry box
tk.Label(root, text="Password").grid(row=1, column=0)
password_entry = tk.Entry(root, show='*')
password_entry.grid(row=1, column=1)

# Login button
tk.Button(root, text="Login", command=login).grid(row=2, columnspan=2)

# Run the main event loop
root.mainloop()

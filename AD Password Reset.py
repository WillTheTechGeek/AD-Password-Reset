import subprocess
import tkinter as tk
from tkinter import messagebox

def reset_password():
    username = username_entry.get()
    new_password = new_password_entry.get()
    change_password_at_next_logon = change_password_var.get()
    
    powershell_command = f'Get-ADUser -Identity "{username}" | Set-ADAccountPassword -NewPassword (ConvertTo-SecureString "{new_password}" -AsPlainText -Force) -PassThru | Set-AdUser -ChangePasswordAtLogon {"$true" if change_password_at_next_logon else "$false"} > $null'
    
    try:
        result = subprocess.run(["powershell", "-Command", powershell_command], capture_output=True, text=True, check=True)

        if result.returncode == 0:
            display_name = subprocess.run(["powershell", "-Command", f'Get-ADUser -Identity "{username}" | Select-Object -ExpandProperty DisplayName'], capture_output=True, text=True, check=True)
            message = f"Display Name: {display_name.stdout.strip()}\nUsername: {username}\nChange Password at Next Logon: {'Yes' if change_password_at_next_logon else 'No'}"

            if change_password_at_next_logon:
                message += f"\nNew Password: {new_password}"
            
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", "PowerShell command failed. Check the username and password.")
    
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error running PowerShell command: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

window = tk.Tk()
window.title("Reset AD Password")
window.geometry("275x225")

title_label = tk.Label(window, text="Reset AD Password\n")
title_label.pack()

username_label = tk.Label(window, text="Username:")
username_label.pack()
username_entry = tk.Entry(window)
username_entry.pack()

new_password_label = tk.Label(window, text="New Password:")
new_password_label.pack()
new_password_entry = tk.Entry(window, show="*") 
new_password_entry.pack()

change_password_var = tk.BooleanVar()
change_password_checkbox = tk.Checkbutton(window, text="Change Password at Next Logon", variable=change_password_var)
change_password_checkbox.pack()

reset_button = tk.Button(window, text="Reset Password", command=reset_password)
reset_button.pack()

wttgCOPYRIGHT = tk.Label(window, text="\nWill the Tech Geek\nwww.willthetechgeek.co.uk")
wttgCOPYRIGHT.pack()

window.mainloop()

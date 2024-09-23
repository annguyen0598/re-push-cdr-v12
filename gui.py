import tkinter as tk
from tkinter import messagebox
from processor import process_cdr  # Import hàm xử lý từ file processor

def on_submit():
    global ACCESS_TOKEN
    ACCESS_TOKEN = access_token_entry.get()
    tenant_id = tenant_id_entry.get()
    tenant_name = tenant_name_entry.get()
    start_time = start_time_entry.get()
    end_time = end_time_entry.get()
    webhook_url = webhook_url_entry.get()  # Lấy URL webhook từ trường nhập
    
    if not all([ACCESS_TOKEN, tenant_id, tenant_name, start_time, end_time, webhook_url]):
        messagebox.showerror("Input Error", "Please fill out all fields.")
        return
    
    # Gọi hàm xử lý từ file processor
    process_cdr(start_time, end_time, ACCESS_TOKEN, tenant_id, tenant_name, webhook_url)
    messagebox.showinfo("Success", "CDR processing completed.")

# Tạo giao diện người dùng với Tkinter
def create_gui():
    root = tk.Tk()
    root.title("CDR Processor")

    tk.Label(root, text="ACCESS_TOKEN").grid(row=0, column=0, padx=10, pady=5)
    global access_token_entry
    access_token_entry = tk.Entry(root, width=50)
    access_token_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Tenant ID").grid(row=1, column=0, padx=10, pady=5)
    global tenant_id_entry
    tenant_id_entry = tk.Entry(root, width=50)
    tenant_id_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="Tenant Name").grid(row=2, column=0, padx=10, pady=5)
    global tenant_name_entry
    tenant_name_entry = tk.Entry(root, width=50)
    tenant_name_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(root, text="Start Time (e.g., 2024-09-16 00:00:39 GMT+07:00)").grid(row=3, column=0, padx=10, pady=5)
    global start_time_entry
    start_time_entry = tk.Entry(root, width=50)
    start_time_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(root, text="End Time (e.g., 2024-09-16 23:59:59 GMT+07:00)").grid(row=4, column=0, padx=10, pady=5)
    global end_time_entry
    end_time_entry = tk.Entry(root, width=50)
    end_time_entry.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(root, text="Webhook URL").grid(row=5, column=0, padx=10, pady=5)
    global webhook_url_entry
    webhook_url_entry = tk.Entry(root, width=50)
    webhook_url_entry.grid(row=5, column=1, padx=10, pady=5)

    submit_button = tk.Button(root, text="Submit", command=on_submit)
    submit_button.grid(row=6, column=1, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()

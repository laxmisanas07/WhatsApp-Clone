import tkinter as tk
from tkinter import messagebox, simpledialog
import socket
import threading

# --- Config ---
# Theme Colors (WhatsApp Style)
TEAL_GREEN = "#075E54"
LIGHT_GREEN = "#25D366"
WHITE = "#ffffff"
BG_GRAY = "#ECE5DD"
MY_MSG_COLOR = "#DCF8C6"
OTHER_MSG_COLOR = "#FFFFFF"

class WhatsUpChat:
    def __init__(self, root):
        self.root = root
        self.root.title("W - What's-Up (LAN Chat)")
        self.root.geometry("400x600")
        self.root.config(bg=BG_GRAY)

        self.client_socket = None
        self.running = True

        # --- UI Layout ---
        # Header
        header = tk.Frame(root, bg=TEAL_GREEN, height=60)
        header.pack(fill=tk.X)
        tk.Label(header, text="What's-Up", font=("Helvetica", 18, "bold"), bg=TEAL_GREEN, fg=WHITE).pack(pady=15)

        # Chat Area
        self.chat_frame = tk.Frame(root, bg=BG_GRAY)
        self.chat_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        self.msg_list = tk.Listbox(self.chat_frame, height=20, width=50, bg=BG_GRAY, font=("Arial", 12), borderwidth=0, highlightthickness=0)
        self.msg_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(self.chat_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.msg_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.msg_list.yview)

        # Input Area
        input_frame = tk.Frame(root, bg=BG_GRAY)
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        self.entry_msg = tk.Entry(input_frame, font=("Arial", 14), width=25)
        self.entry_msg.pack(side=tk.LEFT, padx=5, ipady=5)
        self.entry_msg.bind("<Return>", self.send_msg)

        send_btn = tk.Button(input_frame, text="➤", font=("Arial", 14, "bold"), bg=TEAL_GREEN, fg=WHITE, command=self.send_msg)
        send_btn.pack(side=tk.LEFT, padx=5)

        # --- Connection Setup ---
        self.setup_connection()

    def setup_connection(self):
        mode = simpledialog.askstring("Mode", "Type 'host' to Start Server or 'join' to Connect:")
        
        if mode and mode.lower() == 'host':
            self.mode = "Server"
            threading.Thread(target=self.start_server).start()
            self.root.title("What's-Up (HOST) 🟢")
        else:
            self.mode = "Client"
            host_ip = simpledialog.askstring("Connect", "Enter Host IP (Use '127.0.0.1' for same PC):")
            if host_ip:
                threading.Thread(target=self.connect_to_server, args=(host_ip,)).start()
                self.root.title("What's-Up (CLIENT) 🔵")

    def start_server(self):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(('0.0.0.0', 9999))
            server.listen(1)
            self.update_chat(f"[System]: Waiting for connection...", "center")
            
            client, addr = server.accept()
            self.client_socket = client
            self.update_chat(f"[System]: Connected to {addr}", "center")
            
            threading.Thread(target=self.receive_msg).start()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def connect_to_server(self, ip):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((ip, 9999))
            self.update_chat(f"[System]: Connected to Host!", "center")
            
            threading.Thread(target=self.receive_msg).start()
        except Exception as e:
            messagebox.showerror("Connection Error", "Is the Host running?")

    def send_msg(self, event=None):
        msg = self.entry_msg.get()
        if msg and self.client_socket:
            try:
                self.client_socket.send(msg.encode('utf-8'))
                self.update_chat(f"You: {msg}", "right")
                self.entry_msg.delete(0, tk.END)
            except:
                messagebox.showerror("Error", "Message send failed.")

    def receive_msg(self):
        while self.running:
            try:
                msg = self.client_socket.recv(1024).decode('utf-8')
                if msg:
                    self.update_chat(f"Partner: {msg}", "left")
            except:
                break

    def update_chat(self, msg, align):
        self.msg_list.insert(tk.END, msg)
        # Just simple visual distinction (Color formatting in Listbox is tricky in basic Tkinter, keeping it simple)
        if align == "right":
            self.msg_list.itemconfig(tk.END, {'fg': TEAL_GREEN})
        elif align == "left":
            self.msg_list.itemconfig(tk.END, {'fg': 'black'})
        else:
            self.msg_list.itemconfig(tk.END, {'fg': 'gray'})
        
        self.msg_list.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = WhatsUpChat(root)
    root.mainloop()
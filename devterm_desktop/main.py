"""DevTerm Desktop - Desktop GUI application with CustomTkinter."""

import customtkinter as ctk
import json
import base64
import urllib.parse
import hashlib
import uuid
import re
import secrets
import time
import io
import qrcode
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class DevTermDesktop(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DevTerm Desktop")
        self.geometry("900x600")
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create sidebar
        self.create_sidebar()
        
        # Create main content
        self.create_main_content()
        
        # Default tool
        self.show_tool("json")
    
    def create_sidebar(self):
        """Create the sidebar with tool buttons."""
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Title
        title = ctk.CTkLabel(
            self.sidebar, 
            text="DevTerm", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=20)
        
        # Tool buttons
        tools = [
            ("JSON", "json"),
            ("Base64", "base64"),
            ("URL", "url"),
            ("Hash", "hash"),
            ("UUID", "uuid"),
            ("Password", "password"),
            ("QR Code", "qr"),
            ("Case", "case"),
        ]
        
        for text, tool_id in tools:
            btn = ctk.CTkButton(
                self.sidebar, 
                text=text, 
                command=lambda t=tool_id: self.show_tool(t),
                fg_color="transparent",
                border_width=1,
            )
            btn.pack(pady=5, padx=20, fill="x")
    
    def create_main_content(self):
        """Create the main content area."""
        self.content = ctk.CTkFrame(self)
        self.content.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Input area
        self.input_label = ctk.CTkLabel(self.content, text="Input", font=ctk.CTkFont(size=14, weight="bold"))
        self.input_label.pack(pady=(10, 5))
        
        self.input_text = ctk.CTkTextbox(self.content, height=150)
        self.input_text.pack(fill="x", padx=10)
        
        # Action buttons
        self.btn_frame = ctk.CTkFrame(self.content)
        self.btn_frame.pack(fill="x", padx=10, pady=10)
        
        self.action_btn = ctk.CTkButton(self.btn_frame, text="Execute", command=self.execute_tool)
        self.action_btn.pack(side="left", padx=5)
        
        self.clear_btn = ctk.CTkButton(
            self.btn_frame, 
            text="Clear", 
            command=self.clear_all,
            fg_color="gray"
        )
        self.clear_btn.pack(side="left", padx=5)
        
        # Output area
        self.output_label = ctk.CTkLabel(
            self.content, 
            text="Output", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.output_label.pack(pady=(10, 5))
        
        self.output_text = ctk.CTkTextbox(self.content, height=200)
        self.output_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.current_tool = "json"
    
    def show_tool(self, tool_id):
        """Show the selected tool."""
        self.current_tool = tool_id
        self.clear_all()
        
        tool_names = {
            "json": "JSON Formatter",
            "base64": "Base64 Encoder/Decoder",
            "url": "URL Encoder/Decoder",
            "hash": "Hash Generator",
            "uuid": "UUID Generator",
            "password": "Password Generator",
            "qr": "QR Code Generator",
            "case": "Case Converter",
        }
        
        self.title(f"DevTerm Desktop - {tool_names.get(tool_id, 'Tool')}")
        
        # Update placeholder
        placeholders = {
            "json": '{"key": "value"}',
            "base64": "Enter text...",
            "url": "Enter URL...",
            "hash": "Enter text to hash...",
            "uuid": "Click Generate",
            "password": "Click Generate",
            "qr": "Enter text for QR code...",
            "case": "Enter text...",
        }
        
        self.input_text.delete("1.0", "end")
        self.input_text.insert("1.0", placeholders.get(tool_id, ""))
    
    def execute_tool(self):
        """Execute the current tool."""
        input_val = self.input_text.get("1.0", "end").strip()
        output = ""
        
        try:
            if self.current_tool == "json":
                data = json.loads(input_val)
                output = json.dumps(data, indent=2)
            
            elif self.current_tool == "base64":
                if input_val:
                    output = base64.b64encode(input_val.encode()).decode()
            
            elif self.current_tool == "url":
                if input_val:
                    output = urllib.parse.quote(input_val, safe='')
            
            elif self.current_tool == "hash":
                if input_val:
                    output = f"MD5: {hashlib.md5(input_val.encode()).hexdigest()}\n"
                    output += f"SHA-256: {hashlib.sha256(input_val.encode()).hexdigest()}\n"
                    output += f"SHA-512: {hashlib.sha512(input_val.encode()).hexdigest()}"
            
            elif self.current_tool == "uuid":
                output = str(uuid.uuid4())
            
            elif self.current_tool == "password":
                chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*'
                output = ''.join(secrets.choice(chars) for _ in range(16))
            
            elif self.current_tool == "qr":
                if input_val:
                    qr = qrcode.QRCode(version=1, box_size=10, border=4)
                    qr.add_data(input_val)
                    qr.make(fit=True)
                    img = qr.make_image(fill_color="black", back_color="white")
                    img.save("qrcode.png")
                    output = "QR code saved to qrcode.png"
            
            elif self.current_tool == "case":
                if input_val:
                    output = input_val.lower()
            
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", output)
            
        except Exception as e:
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", f"Error: {str(e)}")
    
    def clear_all(self):
        """Clear input and output."""
        self.input_text.delete("1.0", "end")
        self.output_text.delete("1.0", "end")


def main():
    app = DevTermDesktop()
    app.mainloop()


if __name__ == "__main__":
    main()

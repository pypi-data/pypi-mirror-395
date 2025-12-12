"""
Tkinter-based interactive GUI for AURA data Q&A
Pure Black & White Design - Fixed Layout & Typography
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import threading
from PIL import Image, ImageTk
from io import BytesIO


class AuraGUI:
    """Tkinter GUI for interactive data Q&A - Pure Black & White Edition"""
    
    def __init__(self, aura_instance):
        self.aura = aura_instance
        self.window = None
        self.chat_display = None
        self.input_field = None
        self.send_button = None
        self.graphs_button = None
        
    def launch(self):
        """Launch the Tkinter GUI"""
        self.window = tk.Tk()
        self.window.title("AURA - Data Insights Q&A")
        self.window.geometry("950x750")
        self.window.configure(bg="#000000")
        
        # Main container to prevent overlapping
        main_container = tk.Frame(self.window, bg="#000000")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # ===== HEADER SECTION =====
        header_frame = tk.Frame(main_container, bg="#000000")
        header_frame.pack(fill=tk.X, padx=0, pady=(15, 5))
        
        # Diamond icon
        icon_label = tk.Label(
            header_frame,
            text="◆",
            font=("Arial", 28),
            bg="#000000",
            fg="#FFFFFF"
        )
        icon_label.pack()
        
        # Main title - AURA
        title = tk.Label(
            header_frame,
            text="AURA",
            font=("Arial", 32, "bold"),
            bg="#000000",
            fg="#FFFFFF"
        )
        title.pack()
        
        # Subtitle
        subtitle = tk.Label(
            header_frame,
            text="Autonomous Understanding & Response Architecture",
            font=("Arial", 9),
            bg="#000000",
            fg="#888888"
        )
        subtitle.pack(pady=(2, 0))
        
        # ===== DATASET INFO BAR =====
        info_bar = tk.Frame(main_container, bg="#0d0d0d")
        info_bar.pack(fill=tk.X, padx=0, pady=(10, 0))
        
        info_text = tk.Label(
            info_bar,
            text=f"DATASET: {self.aura.data.shape[0]} rows × {self.aura.data.shape[1]} columns   •   MODEL: EfficientNetB7   •   GRAPHS: {len(self.aura.graphs)}",
            font=("Consolas", 9),
            bg="#0d0d0d",
            fg="#999999"
        )
        info_text.pack(pady=10)
        
        # ===== SYSTEM STATUS =====
        status_frame = tk.Frame(main_container, bg="#000000")
        status_frame.pack(fill=tk.X, padx=0, pady=(12, 8))
        
        status_label = tk.Label(
            status_frame,
            text="SYSTEM",
            font=("Consolas", 8),
            bg="#000000",
            fg="#666666"
        )
        status_label.pack()
        
        status_indicator = tk.Label(
            status_frame,
            text="◆  AURA INITIALIZED  ◆",
            font=("Consolas", 9, "bold"),
            bg="#000000",
            fg="#FFFFFF"
        )
        status_indicator.pack(pady=(3, 0))
        
        # ===== CHAT DISPLAY AREA =====
        chat_container = tk.Frame(main_container, bg="#000000")
        chat_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(12, 0))
        
        # Outer border frame
        chat_border = tk.Frame(chat_container, bg="#2a2a2a", bd=0)
        chat_border.pack(fill=tk.BOTH, expand=True)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_border,
            wrap=tk.WORD,
            font=("Consolas", 11),
            bg="#000000",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
            selectbackground="#333333",
            selectforeground="#FFFFFF",
            bd=1,
            relief=tk.SOLID,
            highlightthickness=0,
            padx=10,
            pady=10
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)
        
        # Initial welcome message
        welcome_msg = """Neural interface active. Ready to analyze your dataset.

▸ QUERY EXAMPLES:
  • Identify correlations and patterns
  • Detect data quality anomalies
  • Feature importance analysis
  • Outlier detection

Awaiting input..."""
        self._append_message("AURA", welcome_msg, is_assistant=True)
        
        # ===== INPUT SECTION =====
        input_section = tk.Frame(main_container, bg="#000000")
        input_section.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        # Input field with border
        input_border = tk.Frame(input_section, bg="#2a2a2a", bd=1, relief=tk.SOLID)
        input_border.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 12))
        
        self.input_field = tk.Entry(
            input_border,
            font=("Consolas", 11),
            bg="#000000",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
            selectbackground="#333333",
            selectforeground="#FFFFFF",
            bd=0
        )
        self.input_field.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self.input_field.bind("<Return>", lambda e: self._send_message())
        
        # Buttons
        button_container = tk.Frame(input_section, bg="#000000")
        button_container.pack(side=tk.RIGHT)
        
        # Send button - white with black text
        self.send_button = tk.Button(
            button_container,
            text="⚡  SEND",
            command=self._send_message,
            bg="#FFFFFF",
            fg="#000000",
            font=("Consolas", 10, "bold"),
            padx=22,
            pady=8,
            bd=0,
            relief=tk.FLAT,
            cursor="hand2",
            activebackground="#DDDDDD",
            activeforeground="#000000"
        )
        self.send_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Graphs button - outlined
        self.graphs_button = tk.Button(
            button_container,
            text="◆  GRAPHS",
            command=self._view_graphs,
            bg="#000000",
            fg="#FFFFFF",
            font=("Consolas", 10, "bold"),
            padx=20,
            pady=7,
            bd=1,
            relief=tk.SOLID,
            cursor="hand2",
            highlightbackground="#FFFFFF",
            activebackground="#1a1a1a",
            activeforeground="#FFFFFF"
        )
        self.graphs_button.pack(side=tk.LEFT)
        
        # ===== FOOTER STATUS =====
        footer = tk.Frame(main_container, bg="#000000")
        footer.pack(fill=tk.X, padx=15, pady=(8, 12))
        
        footer_text = tk.Label(
            footer,
            text="●  ACTIVE",
            font=("Consolas", 8),
            bg="#000000",
            fg="#666666"
        )
        footer_text.pack()
        
        # Run GUI
        self.window.mainloop()
    
    def _send_message(self):
        """Send user message and get AI response"""
        user_input = self.input_field.get().strip()
        if not user_input:
            return
        
        # Display user message
        self._append_message("USER", user_input, is_assistant=False)
        self.input_field.delete(0, tk.END)
        
        # Process in background thread to avoid freezing UI
        thread = threading.Thread(target=self._get_response, args=(user_input,))
        thread.daemon = True
        thread.start()
    
    def _get_response(self, question):
        """Get AI response (runs in separate thread)"""
        try:
            response = self.aura.ask(question)
            self.window.after(0, lambda: self._append_message("AURA", response, is_assistant=True))
        except Exception as e:
            self.window.after(0, lambda: self._append_message("AURA", f"ERROR: {str(e)}", is_assistant=True))
    
    def _append_message(self, sender, message, is_assistant=False):
        """Append message to chat display with proper formatting"""
        self.chat_display.config(state=tk.NORMAL)
        
        # Add spacing between messages
        if self.chat_display.get("1.0", tk.END).strip():
            self.chat_display.insert(tk.END, "\n\n")
        
        # Sender header
        if is_assistant:
            self.chat_display.insert(tk.END, f"{sender}:\n", "assistant_header")
            self.chat_display.tag_config("assistant_header", 
                                        foreground="#FFFFFF", 
                                        font=("Consolas", 11, "bold"))
        else:
            self.chat_display.insert(tk.END, f"{sender}:\n", "user_header")
            self.chat_display.tag_config("user_header", 
                                        foreground="#CCCCCC", 
                                        font=("Consolas", 11, "bold"))
        
        # Message content
        if is_assistant:
            self.chat_display.insert(tk.END, f"{message}", "assistant_msg")
            self.chat_display.tag_config("assistant_msg", 
                                        foreground="#FFFFFF", 
                                        font=("Consolas", 10))
        else:
            self.chat_display.insert(tk.END, f"{message}", "user_msg")
            self.chat_display.tag_config("user_msg", 
                                        foreground="#BBBBBB", 
                                        font=("Consolas", 10))
        
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def _view_graphs(self):
        """Display generated graphs in a new window"""
        if not self.aura.graphs:
            # Custom messagebox with black theme
            msg_window = tk.Toplevel(self.window)
            msg_window.title("No Graphs")
            msg_window.geometry("450x180")
            msg_window.configure(bg="#000000")
            msg_window.resizable(False, False)
            
            # Center the window
            msg_window.transient(self.window)
            msg_window.grab_set()
            
            msg_label = tk.Label(
                msg_window,
                text="No graphs generated yet.\n\nRun generate_insights() first.",
                font=("Consolas", 11),
                bg="#000000",
                fg="#FFFFFF",
                justify=tk.CENTER
            )
            msg_label.pack(expand=True, pady=30)
            
            ok_button = tk.Button(
                msg_window,
                text="OK",
                command=msg_window.destroy,
                bg="#FFFFFF",
                fg="#000000",
                font=("Consolas", 10, "bold"),
                padx=30,
                pady=8,
                bd=0,
                cursor="hand2",
                activebackground="#DDDDDD"
            )
            ok_button.pack(pady=(0, 25))
            return
        
        # Graph viewer window
        graph_window = tk.Toplevel(self.window)
        graph_window.title("AURA - Graph Viewer")
        graph_window.geometry("1050x850")
        graph_window.configure(bg="#000000")
        
        # Header
        header = tk.Frame(graph_window, bg="#000000")
        header.pack(fill=tk.X, padx=0, pady=(18, 12))
        
        icon = tk.Label(
            header,
            text="◆",
            font=("Arial", 20),
            bg="#000000",
            fg="#FFFFFF"
        )
        icon.pack()
        
        title = tk.Label(
            header,
            text="Graph Viewer",
            font=("Arial", 16, "bold"),
            bg="#000000",
            fg="#FFFFFF"
        )
        title.pack(pady=(3, 0))
        
        # Canvas container
        canvas_container = tk.Frame(graph_window, bg="#000000")
        canvas_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(canvas_container, bg="#000000", highlightthickness=0, bd=0)
        scrollbar = tk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview, 
                                bg="#1a1a1a", troughcolor="#000000", bd=0, width=12)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Scrollable frame
        scrollable_frame = tk.Frame(canvas, bg="#000000")
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # Add all graphs
        for idx, (graph_bytes, metadata) in enumerate(zip(self.aura.graphs, self.aura.graph_metadata)):
            try:
                # Convert bytes to PIL Image
                img = Image.open(BytesIO(graph_bytes))
                img.thumbnail((950, 450))
                photo = ImageTk.PhotoImage(img)
                
                # Graph container with border
                graph_border = tk.Frame(scrollable_frame, bg="#2a2a2a", bd=1, relief=tk.SOLID)
                graph_border.pack(fill=tk.X, padx=0, pady=12)
                
                graph_frame = tk.Frame(graph_border, bg="#000000")
                graph_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
                
                # Title
                title_label = tk.Label(
                    graph_frame,
                    text=f"Graph {idx + 1}: {metadata.get('name', 'Unknown')}",
                    font=("Consolas", 11, "bold"),
                    bg="#000000",
                    fg="#FFFFFF"
                )
                title_label.pack(pady=12)
                
                # Image
                img_label = tk.Label(graph_frame, image=photo, bg="#000000", bd=0)
                img_label.image = photo
                img_label.pack(pady=(0, 12))
                
            except Exception as e:
                error_label = tk.Label(
                    scrollable_frame,
                    text=f"ERROR: Graph {idx + 1} - {str(e)}",
                    font=("Consolas", 10),
                    bg="#000000",
                    fg="#FF4444"
                )
                error_label.pack(pady=12)
        
        # Update scroll region
        def _configure_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        scrollable_frame.bind("<Configure>", _configure_scroll)
        
        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
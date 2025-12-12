# -*- coding: utf-8 -*-
import tkinter as tk
from thonny import get_workbench, get_shell
import thonny.shell # Import the shell module
from tkinter import ttk, scrolledtext, messagebox, Menu
import threading
import queue
import requests
import json
import logging
import platform
import re
import locale # <-- Import locale module
import tkinter.font as tk_font
from thonny import get_workbench, get_shell # <-- Import get_shell

# --- Constants ---
PLUGIN_TITLE = "AI Chat Interface"
VIEW_ID = "AIChatView"
CONFIG_PREFIX = "plugin.ai_chat."
CONFIG_API_URL = CONFIG_PREFIX + "api_url"
CONFIG_API_KEY = CONFIG_PREFIX + "api_key"
CONFIG_MODEL = CONFIG_PREFIX + "model"
# CONFIG_HISTORY = CONFIG_PREFIX + "history" # History persistence not implemented

# Configure basic logging
logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG) # Uncomment for more detailed logs

# --- Global state for view visibility (needed for older Thonny) ---
_ai_chat_view_visible = False

# --- Helper Functions ---
def is_macos():
    return platform.system() == "Darwin"

def get_system_language():
    """Attempts to get the system's language name."""
    try:
        # Get default locale (e.g., ('en_US', 'cp1252'), ('zh_TW', 'UTF-8'))
        lang_code, encoding = locale.getdefaultlocale()

        if not lang_code:
            return "English" # Default if detection fails

        # Simple mapping for common languages (extend as needed)
        lang_map = {
            'en': 'English',
            'de': 'German',
            'fr': 'French',
            'es': 'Spanish',
            'it': 'Italian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'zh': 'Chinese', # Generic Chinese
            'zh_CN': 'Simplified Chinese',
            'zh_TW': 'Traditional Chinese',
            'zh_HK': 'Traditional Chinese (Hong Kong)',
            # Add more mappings here
        }

        # Check full code first (e.g., 'zh_TW')
        if lang_code in lang_map:
            return lang_map[lang_code]

        # Check base language code (e.g., 'zh' from 'zh_TW')
        base_lang = lang_code.split('_')[0]
        if base_lang in lang_map:
            return lang_map[base_lang]

        # Fallback to language code if no mapping found
        return lang_code

    except Exception as e:
        logger.warning(f"Could not detect system language, defaulting to English: {e}")
        return "English"

import tkinter as tk
from tkinter import ttk, messagebox
# ... (其他 import)

# --- Settings Dialog Class ---
class SettingsDialog(tk.Toplevel):
    def __init__(self, master, ai_view_instance):
        """
        Initializes the Settings Dialog.

        Args:
            master: The parent window (usually Thonny's main window).
            ai_view_instance: The instance of the main AIChatView.
        """
        super().__init__(master)
        self.transient(master) # Keep dialog on top of master
        self.title(f"{PLUGIN_TITLE} - Settings")
        self.ai_view = ai_view_instance # Store reference to the main view instance

        # Make dialog modal (optional but recommended for settings)
        self.grab_set()
        # self.focus_set() # Set focus to the dialog

        # --- Build the dialog UI ---
        # We'll move the settings frame creation logic here
        self._build_settings_ui()

        # Center the dialog (optional)
        self.update_idletasks() # Ensure window size is calculated
        x = master.winfo_rootx() + (master.winfo_width() // 2) - (self.winfo_width() // 2)
        y = master.winfo_rooty() + (master.winfo_height() // 3) - (self.winfo_height() // 2) # Place slightly higher
        self.geometry(f"+{x}+{y}")

        # Handle closing the dialog via 'X' button
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)

        # Wait for the dialog to close before returning control
        self.wait_window(self)

    def _build_settings_ui(self):
        """Builds the UI elements inside the dialog."""
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(expand=True, fill="both")

        # --- Settings Frame ---
        # Use the LabelFrame directly in the dialog
        settings_frame = ttk.LabelFrame(main_frame, text="API Configuration", padding=(10, 5))
        settings_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        settings_frame.columnconfigure(1, weight=1)

        ttk.Label(settings_frame, text="API URL:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        # Use the StringVar FROM THE MAIN VIEW INSTANCE
        url_entry = ttk.Entry(settings_frame, textvariable=self.ai_view.api_url, width=40)
        url_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(settings_frame, text="API Key:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        # Use the StringVar FROM THE MAIN VIEW INSTANCE
        key_entry = ttk.Entry(settings_frame, textvariable=self.ai_view.api_key, show="*", width=40)
        key_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(settings_frame, text="Model:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        # Use the Combobox FROM THE MAIN VIEW INSTANCE (or recreate and sync)
        # Easiest is to use the existing one if possible, but might cause issues
        # Let's recreate it here and keep it synced.
        # We need access to the model list and selected model variable.
        self.model_combo_dialog = ttk.Combobox(
            settings_frame,
            textvariable=self.ai_view.selected_model, # Share the variable
            state="readonly", # Initial state
            width=38
        )
        self.model_combo_dialog.grid(row=2, column=1, sticky="ew", padx=5, pady=2)
        # Update the values from the main view's list
        self._update_dialog_model_list()

        # --- Buttons Frame ---
        # Recreate buttons here, commands will call methods on ai_view_instance
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=1, column=0, pady=(10, 5), sticky="e") # Align to right

        refresh_btn = ttk.Button(
            btn_frame,
            text="Refresh Models",
            command=self._on_refresh_models, # Call dialog's method
            width=15
        )
        refresh_btn.pack(side="left", padx=5)

        # "Save" now means "Apply and Close"
        save_btn = ttk.Button(
            btn_frame,
            text="Save & Close",
            command=self._on_save, # Call dialog's method
            width=15
        )
        save_btn.pack(side="left", padx=5)

        cancel_btn = ttk.Button(
            btn_frame,
            text="Cancel",
            command=self._on_cancel, # Call dialog's method
            width=15
        )
        cancel_btn.pack(side="left", padx=5)

        # Clear Chat button - does it belong here? Maybe better in main view.
        # If kept, it needs to call the main view's method.
        # clear_hist_btn = ttk.Button(
        #     main_frame, # Maybe put it separately below settings?
        #     text="Clear Chat History",
        #     command=self.ai_view._clear_chat_history, # Directly call main view method
        #     width=20
        # )
        # clear_hist_btn.grid(row=2, column=0, pady=10)

    def _update_dialog_model_list(self):
        """Updates the model list in the dialog's combobox."""
        # Get models and current selection from the main view instance
        available_models = self.ai_view.models
        current_selection = self.ai_view.selected_model.get()

        self.model_combo_dialog['values'] = available_models
        if current_selection in available_models:
             self.model_combo_dialog.set(current_selection)
        elif available_models:
             self.model_combo_dialog.set(available_models[0]) # Default to first if invalid
             self.ai_view.selected_model.set(available_models[0]) # Update shared var
        else:
            self.model_combo_dialog.set("No models found")

        # Set state based on model list
        self.model_combo_dialog.config(state="readonly" if available_models else "disabled")


    def _on_refresh_models(self):
        """Handles the Refresh Models button click."""
        logger.debug("SettingsDialog: Refresh models requested.")
        # --- ADD UI UPDATE FOR DIALOG'S COMBOBOX ---
        try:
            # Update the dialog's combobox to show fetching state
            self.model_combo_dialog.set("Fetching...")
            self.model_combo_dialog.config(state="disabled")
        except tk.TclError as e:
             logger.warning(f"Could not update dialog combobox state: {e}") # Handle if dialog closed unexpectedly
        # ---------------------------------------------

        # Call the main view's method to fetch models
        # Add error handling in case ai_view is somehow invalid
        try:
            if self.ai_view and hasattr(self.ai_view, '_fetch_models_async'):
                 self.ai_view._fetch_models_async()
                 # Start polling to check when the main view updates the list
                 self.after(100, self._check_model_refresh_status)
            else:
                 logger.error("SettingsDialog: ai_view instance is invalid or missing _fetch_models_async.")
                 messagebox.showerror("Error", "Cannot communicate with the main AI Chat view.")
                 # Restore combobox state on error
                 self._update_dialog_model_list()
        except Exception as e:
             logger.error(f"Error calling _fetch_models_async from dialog: {e}", exc_info=True)
             messagebox.showerror("Error", f"Failed to start model refresh:\n{e}")
             # Restore combobox state on error
             self._update_dialog_model_list()
             
    def _check_model_refresh_status(self):
        """Checks if the main view has updated the model list."""
        # This is a simple polling mechanism. A callback would be better.
        current_combo_text = self.model_combo_dialog.get()
        if current_combo_text == "Fetching...":
             # Check if the main view's variable has changed from an error/empty state
             main_view_model = self.ai_view.selected_model.get()
             if main_view_model and main_view_model not in ["Error fetching", "No models found", ""]:
                  logger.debug("SettingsDialog: Detected model list update, refreshing dialog combobox.")
                  self._update_dialog_model_list()
             else:
                  # Still fetching or failed, check again later
                  self.after(500, self._check_model_refresh_status)
        else:
             # Refresh seems complete or was already done
             self._update_dialog_model_list() # Ensure sync


    def _on_save(self):
        """Handles the Save & Close button click."""
        logger.debug("SettingsDialog: Save requested.")
        # Call the main view's save method to persist changes
        self.ai_view._save_settings()
        self.destroy() # Close the dialog

    def _on_cancel(self):
        """Handles the Cancel button or window close click."""
        logger.debug("SettingsDialog: Cancelled.")
        # Reload original settings in case user changed StringVars but didn't save
        self.ai_view._load_settings()
        self.destroy() # Close the dialog

# --- The AI Chat View class ---
class AIChatView(ttk.Frame):
    """The main frame for the AI Chat interface."""

    def __init__(self, master):
        super().__init__(master)
        self.workbench = get_workbench()
        self.api_url = tk.StringVar()
        self.api_key = tk.StringVar()
        self.selected_model = tk.StringVar()
        self.models = []
        self.chat_history = [] # List of {"role": "user/assistant", "content": "..."}
        self.stream_queue = queue.Queue()
        self.streaming_thread = None
        self.current_assistant_message_id = None # To append stream chunks
        self.system_language = get_system_language() # Store detected language

        self._load_settings()
        self._build_ui()
        self._configure_tags() # Use robust version

        # Fetch models shortly after startup (non-blocking)
        self.after(500, self._fetch_models_async)

        # Start checking the queue for streaming updates
        self._check_stream_queue()

        logger.info(f"{VIEW_ID} initialized. Detected system language: {self.system_language}")

    def _load_settings(self):
        """Load settings from Thonny's configuration."""
        self.api_url.set(self.workbench.get_option(CONFIG_API_URL, "https://api.openai.com/v1"))
        self.api_key.set(self.workbench.get_option(CONFIG_API_KEY, ""))
        self.selected_model.set(self.workbench.get_option(CONFIG_MODEL, ""))
        logger.debug(f"Settings loaded. Last selected model: '{self.selected_model.get()}'")

    def _save_settings(self):
        """Save settings to Thonny's configuration."""
        try:
            self.workbench.set_option(CONFIG_API_URL, self.api_url.get().strip())
            self.workbench.set_option(CONFIG_API_KEY, self.api_key.get().strip())
            self.workbench.set_option(CONFIG_MODEL, self.selected_model.get())
            logger.debug(f"Settings saved. API URL: '{self.api_url.get()}', Model: '{self.selected_model.get()}'")
        except Exception as e:
            logger.error(f"Failed to save settings: {e}", exc_info=True)
            messagebox.showerror("Error", f"Could not save settings:\n{e}")

    def _build_ui(self):
        """Construct the UI elements (REMOVING settings frame)."""
        self.columnconfigure(0, weight=1)
        # --- REMOVE Settings Frame ---
        # settings_frame = ttk.LabelFrame(...)
        # settings_frame.grid(...)
        # ... (Remove all code related to url_entry, key_entry, model_combo, refresh_btn, save_btn, clear_hist_btn IN THIS METHOD)

        # Adjust row configuration if needed (row 0 is now chat history)
        self.rowconfigure(0, weight=1) # Chat history frame is now row 0 and expands

        # --- Chat History Frame ---
        chat_frame = ttk.Frame(self)
        # Grid chat frame into row 0
        chat_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5) # Added top padding
        chat_frame.columnconfigure(0, weight=1)
        chat_frame.rowconfigure(0, weight=1)

        self.chat_display = scrolledtext.ScrolledText(
            chat_frame, wrap=tk.WORD, state="disabled", bd=0, relief=tk.FLAT, padx=5, pady=5, font="TkDefaultFont"
        )
        self.chat_display.grid(row=0, column=0, sticky="nsew")

        # --- Input Frame ---
        input_frame = ttk.Frame(self, padding=(5, 5))
        input_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=(0, 5)) # Input is row 1
        # Configure columns for input area and buttons
        input_frame.columnconfigure(0, weight=1) # Text area expands
        # Add columns for buttons if needed, or use pack
        # Let's put buttons in their own frame to the right

        self.user_input = tk.Text(input_frame, height=4, wrap=tk.WORD, relief=tk.SOLID, bd=1)
        self.user_input.grid(row=0, column=0, sticky="nsew", pady=(0, 5)) # Add bottom padding to separate from buttons if they are below
        # ... (Bindings for user_input) ...
        if is_macos():
            self.user_input.bind("<Command-Return>", self._on_send_message)
        else:
            self.user_input.bind("<Control-Return>", self._on_send_message)
        self.user_input.bind("<Shift-Return>", self._on_send_message)

        # --- Button Frame within Input Frame ---
        button_subframe = ttk.Frame(input_frame)
        # Place it next to the text input (column 1) or below (row 1)?
        # Let's try next to it.
        button_subframe.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        # --- ADD CLEAR CHAT BUTTON ---
        # Make buttons slightly smaller? Or use icons later?
        clear_button = ttk.Button(
            button_subframe,
            text="Clear", # Shorter label?
            command=self._clear_chat_history, # Ensure this method exists
            width=8 # Adjust width as needed
        )
        # Pack buttons vertically within the subframe
        clear_button.pack(side="top", pady=(0, 5), fill="x") # Add padding between buttons
        # ---------------------------
        
        send_button = ttk.Button(
            button_subframe,
            text="Send", # Shorter label?
            command=self._on_send_message,
            width=8 # Adjust width as needed
            # Consider making Send button the default? (Requires different handling)
        )
        send_button.pack(side="top", fill="x")
        
        # --- ADD THIS SECTION BACK ---
        # --- Context Menu for Chat Display ---
        try: # Add try-except for robustness
            self.context_menu = Menu(self.chat_display, tearoff=0) # Create Menu for chat_display
            self.context_menu.add_command(label="Copy Selection", command=self._copy_selection)
            self.context_menu.add_command(label="Copy Code Block", command=self._copy_code_block)
            self.context_menu.add_command(label="Copy Message (Markdown)", command=lambda: self._copy_message(format="markdown"))
            self.context_menu.add_command(label="Copy Message (Text)", command=lambda: self._copy_message(format="text"))

            # Bind right-click events directly to chat_display
            if is_macos():
                 self.chat_display.bind("<Button-2>", self._show_context_menu, add='+') # Add '+' to be safe
                 self.chat_display.bind("<Control-Button-1>", self._show_context_menu, add='+')
            else:
                 self.chat_display.bind("<Button-3>", self._show_context_menu, add='+')
            logger.info("Successfully created and bound context menu for chat display.")
        except Exception as e:
            logger.error(f"Failed to create or bind chat display context menu: {e}", exc_info=True)
        # --- END OF SECTION TO ADD BACK ---

    def _configure_tags(self):
        """Configure Text widget tags for formatting (robust version)."""
        logger.debug("Configuring text tags (robust)...")
        base_font_name = "TkDefaultFont" # Start with a safe default
        try:
            # Use the font set during ScrolledText creation
            retrieved_font = self.chat_display.cget("font")
            if isinstance(retrieved_font, str) and retrieved_font:
                base_font_name = retrieved_font
            elif isinstance(retrieved_font, tk_font.Font): # If it returns a Font object
                 base_font_name = retrieved_font.actual("family") # Try to get family name
            logger.debug(f"Base font name determined: {repr(base_font_name)}")
        except Exception as e_get_font:
            logger.warning(f"Could not get base font, using default '{base_font_name}': {e_get_font}")

        # --- Manually create bold and italic fonts ---
        bold_font = None
        italic_font = None

        try:
            temp_bold_font = tk_font.Font(font=base_font_name)
            temp_bold_font.configure(weight=tk_font.BOLD)
            bold_font = temp_bold_font
            logger.info("Successfully created bold font object.")
        except Exception as e_bold:
            logger.error(f"Failed to create bold font object: {e_bold}", exc_info=True)

        try:
            temp_italic_font = tk_font.Font(font=base_font_name)
            temp_italic_font.configure(slant=tk_font.ITALIC)
            italic_font = temp_italic_font
            logger.info("Successfully created italic font object.")
        except Exception as e_italic:
            logger.error(f"Failed to create italic font object: {e_italic}", exc_info=True)

        # --- Configure tags using the created fonts (or base font name if creation failed) ---
        try:
            effective_bold_font = bold_font if bold_font else base_font_name
            effective_italic_font = italic_font if italic_font else base_font_name
            logger.debug(f"Using effective bold font: {effective_bold_font}")
            logger.debug(f"Using effective italic font: {effective_italic_font}")

            # Basic styles
            self.chat_display.tag_configure("bold", font=effective_bold_font)
            self.chat_display.tag_configure("italic", font=effective_italic_font)

            # Role indicators
            self.chat_display.tag_configure("user_role", font=effective_bold_font, foreground="blue")
            self.chat_display.tag_configure("assistant_role", font=effective_bold_font, foreground="green")
            self.chat_display.tag_configure("error_role", font=effective_bold_font, foreground="red")

            # Code blocks
            code_font_family = "Courier New" if not is_macos() else "Monaco"
            code_font_size = 10 if not is_macos() else 11
            code_font_config = base_font_name

            try:
                code_tk_font = tk_font.Font(family=code_font_family, size=code_font_size)
                code_font_config = code_tk_font
                logger.info("Using tk_font.Font object for code block.")
            except Exception as e_code_font:
                logger.error(f"Failed to create tk_font.Font for code block: {e_code_font}. Using base font.", exc_info=True)

            self.chat_display.tag_configure(
                "code_block",
                font=code_font_config,
                background="#f0f0f0",
                borderwidth=1,
                relief=tk.SOLID,
                lmargin1=15, lmargin2=15, rmargin=15,
            )

            # --- New Tags for Enhanced Markdown ---
            # Inline Code
            self.chat_display.tag_configure("inline_code", font=code_font_config, background="#e6e6e6")

            # Lists
            self.chat_display.tag_configure("list_item", lmargin1=20, lmargin2=35)

            # Headings
            try:
                # Helper to create larger fonts based on base font
                def create_heading_font(scale, weight="bold"):
                    f = tk_font.Font(font=base_font_name)
                    current_size = f.cget("size")
                    # Handle negative size (pixels) vs positive (points)
                    new_size = int(current_size * scale) if current_size > 0 else int(current_size * scale)
                    f.configure(size=new_size, weight=weight)
                    return f

                self.chat_display.tag_configure("heading_1", font=create_heading_font(1.5), spacing3=10, foreground="#2c3e50")
                self.chat_display.tag_configure("heading_2", font=create_heading_font(1.3), spacing3=8, foreground="#34495e")
                self.chat_display.tag_configure("heading_3", font=create_heading_font(1.15), spacing3=5, foreground="#7f8c8d")
            except Exception as e_headings:
                 logger.error(f"Failed to configure heading fonts: {e_headings}", exc_info=True)
                 # Fallback for headings
                 self.chat_display.tag_configure("heading_1", font=effective_bold_font)
                 self.chat_display.tag_configure("heading_2", font=effective_bold_font)
                 self.chat_display.tag_configure("heading_3", font=effective_bold_font)


            # Tag to store the raw code content for easy copying
            self.chat_display.tag_configure("code_content")
            self.chat_display.tag_raise("sel")
            logger.info("Text tags configured successfully.")

        except Exception as e_config:
             logger.error(f"Unexpected error during tag configuration: {e_config}", exc_info=True)

    def _apply_markdown_tags(self, text_content, start_index):
        """Apply markdown formatting tags to the text widget. Operates from start_index."""
        logger.debug(f"Applying markdown tags starting from index {start_index}")

        # List of (pattern, tag_name) tuples. Order matters for precedence if matches start at same index.
        # But our loop finds the *earliest* match regardless of list order.
        patterns = [
            (r"(?s)```(?:[a-zA-Z]*)?\n(.*?)\n```", "code_block"),
            (r"(?<!`)`([^`]+)`(?!`)", "inline_code"),
            (r"(?m)^(#{1,3})\s+(.*)$", "heading"), # Groups: 1=hashes, 2=content
            (r"(?m)^(\s*[-*+])\s+(.*)$", "list_item"), # Groups: 1=bullet, 2=content
            (r"\*\*(.*?)\*\*", "bold"),
            (r"(?<!\*)\*(?!\*|_)(.*?)(?<!\*)\*(?!\*|_)", "italic"),
            (r"(?<!_)_(?!_|\*)(.*?)(?<!_)_(?!_|\*)", "italic"),
        ]

        # Operate only on the newly added text range
        try:
            end_index = self.chat_display.index("end-1c")
            if self.chat_display.compare(start_index, ">=", end_index):
                 return

            current_pos = start_index
            while self.chat_display.compare(current_pos, "<", end_index):
                first_match_info = None # (tag, start_idx, end_idx, match_object)

                search_start_index = self.chat_display.index(current_pos)
                text_to_search = self.chat_display.get(search_start_index, end_index)

                if not text_to_search: break

                for pattern, tag in patterns:
                    match = re.search(pattern, text_to_search)
                    if match:
                        match_start_abs = self.chat_display.index(f"{search_start_index}+{match.start()}c")
                        
                        # Optimization: If we already have a match that starts earlier, keep it.
                        if first_match_info and self.chat_display.compare(match_start_abs, ">=", first_match_info[1]):
                            continue
                            
                        match_end_abs = self.chat_display.index(f"{search_start_index}+{match.end()}c")
                        
                        if first_match_info is None or self.chat_display.compare(match_start_abs, "<", first_match_info[1]):
                            first_match_info = (tag, match_start_abs, match_end_abs, match)

                if first_match_info is None:
                    break # No matches found

                tag_to_apply, start_idx, end_idx, match = first_match_info
                
                self.chat_display.config(state="normal")
                self.chat_display.delete(start_idx, end_idx)

                # Logic for each tag type
                if tag_to_apply == "code_block":
                    content = match.group(1)
                    self.chat_display.insert(start_idx, "\n")
                    code_start_idx = self.chat_display.index(f"{start_idx}+1c")
                    self.chat_display.insert(code_start_idx, content)
                    code_end_idx = self.chat_display.index(f"{code_start_idx}+{len(content)}c")
                    self.chat_display.insert(code_end_idx, "\n")
                    
                    block_end_idx = self.chat_display.index(f"{code_end_idx}+1c")
                    self.chat_display.tag_add(tag_to_apply, code_start_idx, block_end_idx)
                    self.chat_display.tag_add("code_content", code_start_idx, code_end_idx)
                    current_pos_update_idx = block_end_idx

                elif tag_to_apply == "heading":
                    # Groups: 1=hashes, 2=content
                    hashes = match.group(1)
                    content = match.group(2)
                    level = len(hashes)
                    heading_tag = f"heading_{level}"
                    
                    self.chat_display.insert(start_idx, content + "\n") # Restore newline
                    tag_end_idx = self.chat_display.index(f"{start_idx}+{len(content)}c")
                    self.chat_display.tag_add(heading_tag, start_idx, tag_end_idx)
                    current_pos_update_idx = self.chat_display.index(f"{tag_end_idx}+1c")

                elif tag_to_apply == "list_item":
                    # Groups: 1=bullet_char_with_space, 2=content
                    # We'll replace bullet with a standard dot
                    content = match.group(2)
                    display_text = f" • {content}\n"
                    self.chat_display.insert(start_idx, display_text)
                    
                    item_end_idx = self.chat_display.index(f"{start_idx}+{len(display_text)-1}c") # Exclude newline from some tags? No, include it.
                    self.chat_display.tag_add("list_item", start_idx, item_end_idx)
                    current_pos_update_idx = self.chat_display.index(f"{start_idx}+{len(display_text)}c")

                elif tag_to_apply == "inline_code":
                    content = match.group(1)
                    self.chat_display.insert(start_idx, content)
                    code_end = self.chat_display.index(f"{start_idx}+{len(content)}c")
                    self.chat_display.tag_add("inline_code", start_idx, code_end)
                    self.chat_display.tag_add("code_content", start_idx, code_end) # Also allow copy
                    current_pos_update_idx = code_end

                elif tag_to_apply in ["bold", "italic"]:
                    content = match.group(1)
                    self.chat_display.insert(start_idx, content)
                    tag_end_idx = self.chat_display.index(f"{start_idx}+{len(content)}c")
                    self.chat_display.tag_add(tag_to_apply, start_idx, tag_end_idx)
                    current_pos_update_idx = tag_end_idx

                self.chat_display.config(state="disabled")
                current_pos = current_pos_update_idx
                end_index = self.chat_display.index("end-1c") # Re-evaluate end
            
            logger.debug("Finished applying markdown tags.")

        except Exception as e:
            logger.error(f"Error applying markdown tags: {e}", exc_info=True)
            # Ensure state is disabled even if error occurs
            if self.chat_display.cget('state') == tk.NORMAL:
                 self.chat_display.config(state="disabled")


    def _add_message_to_display(self, role, content, message_id=None):
        """Adds a formatted message to the chat display."""
        self.chat_display.config(state="normal")
        start_index_msg = self.chat_display.index("end-1c")

        if start_index_msg != "1.0":
            self.chat_display.insert("end", "\n\n")
            start_index_msg = self.chat_display.index("end-1c") # Recalculate after newlines

        role_text = f"{role.capitalize()}: "
        role_tag_id = f"msg_{message_id}_role" if message_id else ""
        self.chat_display.insert("end", role_text, (f"{role}_role", "role_label", role_tag_id))
        content_start_index = self.chat_display.index("end")

        self.chat_display.insert("end", content)
        content_end_index = self.chat_display.index("end-1c") # Before potential final newline

        # Apply markdown only to the newly added content
        self._apply_markdown_tags(content, content_start_index)

        # Adjust end index in case markdown changed content length
        final_end_index = self.chat_display.index("end-1c")

        if message_id:
             msg_tag = f"msg_{message_id}"
             self.chat_display.tag_add(msg_tag, start_index_msg, final_end_index)
             self.chat_display.tag_add("message_block", start_index_msg, final_end_index)

        self.chat_display.config(state="disabled")
        self.chat_display.see("end")
        return start_index_msg

    def _append_stream_chunk(self, chunk):
        """Appends a chunk of text from the stream to the current assistant message."""
        if not self.current_assistant_message_id:
            logger.warning("Received stream chunk but no current assistant message ID.")
            return

        msg_tag = f"msg_{self.current_assistant_message_id}"
        ranges = self.chat_display.tag_ranges(msg_tag)
        if not ranges:
            # Possible if placeholder was cleared aggressively. Try adding the message again.
            logger.warning(f"Cannot find message range for tag {msg_tag}. Re-adding assistant placeholder.")
            # Find last known history message to get content? Or just use chunk?
            # Let's assume the placeholder logic handles this - if it fails, something else is wrong.
            # For now, log and return might be safer than adding partial content.
            return

        insert_pos = ranges[1] # Append at the current end of the message block

        self.chat_display.config(state="normal")
        self.chat_display.insert(insert_pos, chunk)
        new_end_pos = self.chat_display.index(f"{insert_pos}+{len(chunk)}c")

        # Extend tags to cover the new content
        self.chat_display.tag_remove(msg_tag, ranges[0], ranges[1])
        self.chat_display.tag_add(msg_tag, ranges[0], new_end_pos)
        self.chat_display.tag_remove("message_block", ranges[0], ranges[1])
        self.chat_display.tag_add("message_block", ranges[0], new_end_pos)

        # Skip dynamic markdown during streaming for performance/simplicity
        self.chat_display.config(state="disabled")
        self.chat_display.see("end")

    def _finalize_assistant_message(self):
        """Called after streaming is complete to apply final formatting."""
        if not self.current_assistant_message_id: return
        logger.debug(f"Finalizing assistant message: {self.current_assistant_message_id}")

        msg_tag = f"msg_{self.current_assistant_message_id}"
        ranges = self.chat_display.tag_ranges(msg_tag)
        if not ranges:
            logger.warning(f"Cannot find ranges for {msg_tag} during finalization.")
            self.current_assistant_message_id = None
            return

        # Find content start index (after role label)
        role_tag = f"msg_{self.current_assistant_message_id}_role"
        role_ranges = self.chat_display.tag_ranges(role_tag)
        content_start_index = role_ranges[1] if role_ranges else ranges[0]

        # Get the complete content for this message
        full_content = self.chat_display.get(content_start_index, ranges[1])

        # Apply markdown to the entire completed message content
        self._apply_markdown_tags(full_content, content_start_index)

        # Find the *new* end index after markdown might have changed things
        final_end_index = self.chat_display.index("end-1c")
        # Re-apply the message tags to the potentially adjusted final range
        # This seems problematic if other messages were added after. Let's trust initial range end.
        # self.chat_display.tag_remove(msg_tag, ranges[0], ranges[1])
        # self.chat_display.tag_add(msg_tag, ranges[0], final_end_index)
        # self.chat_display.tag_remove("message_block", ranges[0], ranges[1])
        # self.chat_display.tag_add("message_block", ranges[0], final_end_index)


        self.current_assistant_message_id = None # Reset for next message
        logger.debug("Assistant message finalized.")

    def _add_error_message(self, error_text):
         """Displays an error message in the chat history."""
         self._add_message_to_display("error", str(error_text), message_id=f"error_{len(self.chat_history)}")

    def _clear_chat_history(self):
         """Clears the chat display and the internal history."""
         if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear the entire chat history?"):
             self.chat_history.clear()
             self.chat_display.config(state="normal")
             self.chat_display.delete("1.0", "end")
             self.chat_display.config(state="disabled")
             logger.info("Chat history cleared.")

    def _fetch_models_async(self):
        """
        Starts the background thread to fetch models from the API.
        Does NOT interact with UI elements directly.
        """
        # Get necessary info directly from the instance variables (StringVars)
        api_url = self.api_url.get().strip()
        api_key = self.api_key.get().strip()

        # Basic checks before starting the thread
        if not api_url:
            # Log the warning, but don't show messagebox from here.
            # The dialog should handle user feedback if called from dialog.
            logger.warning("API URL not set. Model fetch initiated but likely to fail.")
            # We might still start the worker to report the error via the queue.
        if not api_key:
            logger.warning("API Key not set. Model fetch initiated but likely to fail.")
            # We might still start the worker to report the error via the queue.

        # --- No UI Interaction Here ---
        # The responsibility of updating UI state (like "Fetching...")
        # now belongs to the caller (e.g., the SettingsDialog).
        # logger.debug("AIChatView: Starting model fetch worker thread.") # Optional log

        # Start the background worker thread
        thread = threading.Thread(
            target=self._fetch_models_worker,
            args=(api_url, api_key), # Pass URL and key to the worker
            daemon=True
        )
        thread.start()

    def _fetch_models_worker(self, api_url, api_key):
        """Worker thread for fetching models."""
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        models_endpoint = api_url.rstrip('/') + "/models"
        try:
            response = requests.get(models_endpoint, headers=headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            model_list = []
            if isinstance(data, dict) and 'data' in data and isinstance(data['data'], list):
                 model_list = sorted([m.get('id') for m in data['data'] if m.get('id')])
            elif isinstance(data, dict) and 'models' in data and isinstance(data['models'], list):
                 model_list = sorted(data['models'])
            elif isinstance(data, list):
                 model_list = sorted([m.get('id') for m in data if isinstance(m, dict) and m.get('id')])
            else:
                 raise ValueError(f"Unexpected API response format for models: {str(data)[:100]}")

            self.stream_queue.put({"type": "models_result", "models": model_list})
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch models: {e}", exc_info=True)
            self.stream_queue.put({"type": "models_error", "error": f"Network or API Error: {e}"})
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            logger.error(f"Failed to parse models response: {e}", exc_info=True)
            self.stream_queue.put({"type": "models_error", "error": f"API Response Error: {e}"})
        except Exception as e:
            logger.error(f"Unexpected error fetching models: {e}", exc_info=True)
            self.stream_queue.put({"type": "models_error", "error": f"Unexpected Error: {e}"})

    def _update_models_dropdown(self, models, error=None):
        """Updates the main view's model list and notifies open settings dialog."""
        # --- Keep the existing logic for updating self.models and self.selected_model ---
        restored_selection = False
        current_selection = self.selected_model.get()

        if error:
            # ... (handle error - set self.models, self.selected_model) ...
            self.models = []
            self.selected_model.set("") # Clear on error
            logger.error(f"Error updating models dropdown: {error}")
        elif models:
            self.models = models
            logger.debug(f"Main view updating models. Loaded selection: '{current_selection}'. Available models: {models}")
            if current_selection and current_selection in self.models:
                # Variable already holds the value, no change needed here
                restored_selection = True
                logger.info(f"Model selection '{current_selection}' remains valid.")
            elif not restored_selection and self.models:
                default_model = self.models[0]
                # Update the shared variable - this will affect comboboxes using it
                self.selected_model.set(default_model)
                logger.info(f"Defaulting main view model to '{default_model}'.")
                # Optionally save immediately? Or wait for user action? Let's wait.
                # self._save_settings()
            else:
                 self.selected_model.set("") # Clear if no models
                 logger.info("No models available.")
        else: # No models returned
            self.models = []
            self.selected_model.set("")
            logger.info("Received empty list of models.")

        # --- Notify the Settings Dialog if it's open ---
        # Check if a dialog window exists and is an instance of our class
        # This requires the dialog to store a reference or check window properties.
        # Simpler: Check if a window with the specific title exists? Risky.
        # Best: Store a reference to the open dialog in the workbench or AIChatView?
        # Let's try finding the window by title (less robust).
        try:
            # Iterate through top-level windows managed by the root
            root = get_workbench().winfo_toplevel()
            for win in root.winfo_children():
                 if isinstance(win, tk.Toplevel) and win.title() == f"{PLUGIN_TITLE} - Settings":
                     # Found the dialog, call its update method
                     if hasattr(win, '_update_dialog_model_list'):
                          logger.debug("Notifying open settings dialog to update model list.")
                          win._update_dialog_model_list()
                     break # Assume only one settings dialog open
        except Exception as e:
            logger.warning(f"Could not check/notify settings dialog: {e}")
        # ---------------------------------------------

        # Note: The main view doesn't have its own combobox anymore.
        # self.model_combo.config(...) is removed.

    def _on_send_message(self, event=None):
        """Handles sending the user's message."""
        user_text = self.user_input.get("1.0", "end-1c").strip()
        if not user_text:
            return "break" # Prevent sending empty and break default newline

        if self.streaming_thread and self.streaming_thread.is_alive():
             messagebox.showwarning("Busy", "Please wait for the current response to complete.")
             return "break"

        api_url = self.api_url.get().strip()
        api_key = self.api_key.get().strip()
        model = self.selected_model.get()

        if not api_url or not api_key or not model or model == "Configure API first" or model == "Error fetching" or model == "No models found":
             messagebox.showerror("Missing Info", "Please configure API URL, Key, and select a valid Model.")
             return "break"

        # Add user message to history and display
        msg_id = f"user_{len(self.chat_history)}"
        self.chat_history.append({"role": "user", "content": user_text})
        self._add_message_to_display("user", user_text, message_id=msg_id)
        self.user_input.delete("1.0", "end") # Clear input field

        # Prepare for assistant's response (placeholder)
        self.current_assistant_message_id = f"asst_{len(self.chat_history)}"
        self._add_message_to_display("assistant", "...", message_id=self.current_assistant_message_id)

        # Start streaming request in background thread
        self.streaming_thread = threading.Thread(
            target=self._stream_chat_worker,
            args=(api_url, api_key, model, list(self.chat_history)), # Send a copy
            daemon=True
        )
        self.streaming_thread.start()

        return "break" # Prevents default handling of the Enter key

    def _stream_chat_worker(self, api_url, api_key, model, history_copy):
        """Worker thread for streaming chat completions, adding system prompt."""
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

        # --- Add System Prompt with Language ---
        system_prompt = f"You are a helpful coding assistant. Please respond in {self.system_language}. Reply in short."
        messages_to_send = [{"role": "system", "content": system_prompt}] + history_copy
        # --------------------------------------

        payload = {
            "model": model,
            "messages": messages_to_send, # Use the list with system prompt
            "stream": True,
        }
        chat_endpoint = api_url.rstrip('/') + "/chat/completions"
        full_response_content = ""
        first_chunk = True

        try:
            with requests.post(chat_endpoint, headers=headers, json=payload, stream=True, timeout=60) as response:
                response.raise_for_status()
                logger.debug(f"Streaming response status: {response.status_code}")

                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8')
                        if decoded_line.startswith("data: "):
                            data_str = decoded_line[len("data: "):].strip()
                            if data_str == "[DONE]":
                                logger.debug("Stream [DONE] received.")
                                break
                            try:
                                data = json.loads(data_str)
                                if data.get("choices"):
                                     delta = data["choices"][0].get("delta", {})
                                     content_chunk = delta.get("content")
                                     if content_chunk:
                                         if first_chunk:
                                             self.stream_queue.put({"type": "stream_clear_placeholder"})
                                             first_chunk = False
                                         self.stream_queue.put({"type": "stream_chunk", "chunk": content_chunk})
                                         full_response_content += content_chunk
                            except json.JSONDecodeError:
                                logger.warning(f"Failed to decode stream JSON chunk: {data_str}")
                                continue
                        elif decoded_line.strip():
                             logger.warning(f"Received unexpected non-SSE line: {decoded_line}")

                self.stream_queue.put({"type": "stream_end", "full_content": full_response_content})
                logger.debug("Stream processing finished.")

        except requests.exceptions.Timeout:
             logger.error("API request timed out.")
             self.stream_queue.put({"type": "stream_error", "error": "Request timed out."})
        except requests.exceptions.RequestException as e:
            error_detail = str(e)
            try:
                if e.response is not None:
                     error_content = e.response.text
                     logger.error(f"API request failed: {e} - Response: {error_content[:500]}")
                     try:
                         error_json = json.loads(error_content)
                         if isinstance(error_json, dict) and 'error' in error_json:
                             error_detail = error_json['error'].get('message', str(error_json['error']))
                         else: error_detail = error_content[:200]
                     except json.JSONDecodeError: error_detail = error_content[:200]
                else:
                     logger.error(f"API request failed: {e} (No response object)", exc_info=True)
            except Exception: pass
            self.stream_queue.put({"type": "stream_error", "error": f"API Error: {error_detail}"})
        except Exception as e:
            logger.error(f"Unexpected error during streaming: {e}", exc_info=True)
            self.stream_queue.put({"type": "stream_error", "error": f"Unexpected Error: {e}"})

    def _check_stream_queue(self):
        """Periodically check the queue for updates from worker threads."""
        try:
            processed_count = 0
            while True:
                message = self.stream_queue.get_nowait()
                msg_type = message.get("type")

                if msg_type == "models_result":
                    self._update_models_dropdown(message["models"])
                elif msg_type == "models_error":
                    self._update_models_dropdown(None, error=message["error"])
                elif msg_type == "stream_clear_placeholder":
                     if self.current_assistant_message_id:
                          msg_tag = f"msg_{self.current_assistant_message_id}"
                          ranges = self.chat_display.tag_ranges(msg_tag)
                          if ranges:
                              role_tag = f"msg_{self.current_assistant_message_id}_role"
                              role_ranges = self.chat_display.tag_ranges(role_tag)
                              content_start_index = role_ranges[1] if role_ranges else ranges[0]
                              if self.chat_display.get(content_start_index, ranges[1]).strip() == "...":
                                 self.chat_display.config(state="normal")
                                 self.chat_display.delete(content_start_index, ranges[1])
                                 # Adjust ranges AFTER deletion
                                 new_end_pos = content_start_index # Placeholder content is gone
                                 self.chat_display.tag_remove(msg_tag, ranges[0], ranges[1])
                                 self.chat_display.tag_add(msg_tag, ranges[0], new_end_pos)
                                 self.chat_display.tag_remove("message_block", ranges[0], ranges[1])
                                 self.chat_display.tag_add("message_block", ranges[0], new_end_pos)
                                 self.chat_display.config(state="disabled")
                                 logger.debug("Cleared placeholder '...'")

                elif msg_type == "stream_chunk":
                    self._append_stream_chunk(message["chunk"])
                    # Force UI update every few chunks to ensure smooth streaming visual
                    processed_count += 1
                    if processed_count % 2 == 0:
                        self.update_idletasks()

                elif msg_type == "stream_end":
                     # Important: Add to history *before* finalizing display
                     if self.current_assistant_message_id: # Check if still relevant
                        self.chat_history.append({"role": "assistant", "content": message["full_content"]})
                        self._finalize_assistant_message()
                        logger.debug("Stream ended successfully.")
                     else:
                        logger.warning("Stream ended but no current assistant message ID. Response lost?")

                elif msg_type == "stream_error":
                     error_msg = message["error"]
                     # Add error message to display, but NOT to persistent history
                     self._add_error_message(f"Assistant Error: {error_msg}")
                     if self.current_assistant_message_id:
                         # Remove the "..." placeholder line entirely on error
                         msg_tag = f"msg_{self.current_assistant_message_id}"
                         ranges = self.chat_display.tag_ranges(msg_tag)
                         if ranges:
                             # Check if it's still just the placeholder
                             role_tag = f"msg_{self.current_assistant_message_id}_role"
                             role_ranges = self.chat_display.tag_ranges(role_tag)
                             content_start_index = role_ranges[1] if role_ranges else ranges[0]
                             if self.chat_display.get(content_start_index, ranges[1]).strip() == "...":
                                 self.chat_display.config(state="normal")
                                 self.chat_display.delete(ranges[0], ranges[1]) # Delete whole line
                                 self.chat_display.config(state="disabled")
                                 logger.debug("Removed placeholder '...' on stream error.")

                     self.current_assistant_message_id = None # Reset on error
                     logger.error(f"Stream error processed: {error_msg}")

                self.stream_queue.task_done()
        except queue.Empty:
            pass
        finally:
            self.after(50, self._check_stream_queue) # Check more frequently (50ms)

    # --- Context Menu Actions for Chat Display ---
    def _show_context_menu(self, event):
        """Display the context menu at the clicked position."""
        try:
            current_index = self.chat_display.index(f"@{event.x},{event.y}")
            tags_here = self.chat_display.tag_names(current_index)

            is_in_code_block = "code_block" in tags_here or "code_content" in tags_here
            self.context_menu.entryconfig("Copy Code Block", state="normal" if is_in_code_block else "disabled")

            has_selection = bool(self.chat_display.tag_ranges("sel"))
            self.context_menu.entryconfig("Copy Selection", state="normal" if has_selection else "disabled")

            is_in_message = any(tag.startswith("msg_") for tag in tags_here) or "message_block" in tags_here
            self.context_menu.entryconfig("Copy Message (Markdown)", state="normal" if is_in_message else "disabled")
            self.context_menu.entryconfig("Copy Message (Text)", state="normal" if is_in_message else "disabled")

            self.context_menu.tk_popup(event.x_root, event.y_root)
        except Exception as e:
             logger.error(f"Error showing context menu: {e}", exc_info=True)
        finally:
            # Ensure grab release even if error occurred
            try:
                 self.context_menu.grab_release()
            except:
                 pass


    def _copy_selection(self):
        try:
            selected_text = self.chat_display.get(tk.SEL_FIRST, tk.SEL_LAST)
            if selected_text:
                self.clipboard_clear()
                self.clipboard_append(selected_text)
                logger.debug("Copied selection to clipboard.")
        except tk.TclError:
            logger.debug("Copy Selection: No text selected.")
        except Exception as e:
            logger.error(f"Failed to copy selection: {e}", exc_info=True)

    def _copy_code_block(self):
        try:
            current_index = self.chat_display.index(tk.CURRENT)
            ranges = self.chat_display.tag_ranges("code_content")
            target_range = None
            for i in range(0, len(ranges), 2):
                 start, end = ranges[i], ranges[i+1]
                 if self.chat_display.compare(current_index, ">=", start) and \
                    self.chat_display.compare(current_index, "<=", end): # Use <= for end
                     target_range = (start, end)
                     break
            if target_range:
                code_text = self.chat_display.get(target_range[0], target_range[1])
                self.clipboard_clear()
                self.clipboard_append(code_text)
                logger.debug("Copied code block to clipboard.")
            else:
                 logger.warning("Copy Code Block: Cursor not inside a detected code block content.")
        except Exception as e:
            logger.error(f"Failed to copy code block: {e}", exc_info=True)

    def _get_message_range_and_content(self, index):
        """Finds the message tag, its range, and original content."""
        tags = self.chat_display.tag_names(index)
        msg_tag = next((tag for tag in tags if tag.startswith("msg_") and "_role" not in tag), None)

        if msg_tag:
            ranges = self.chat_display.tag_ranges(msg_tag)
            if ranges:
                role = msg_tag.split('_')[1]
                msg_index_str = msg_tag.split('_')[-1]
                original_content = f"[Could not find original message for {msg_tag}]"
                display_text = "[Error getting display text]"
                try:
                    role_tag = f"{msg_tag}_role"
                    role_ranges = self.chat_display.tag_ranges(role_tag)
                    content_start_index = role_ranges[1] if role_ranges else ranges[0]
                    display_text = self.chat_display.get(content_start_index, ranges[1]).strip()

                    try:
                         msg_num = int(msg_index_str)
                         history_idx = -1
                         count = -1
                         target_role = 'user' if role == 'user' else ('assistant' if role == 'asst' else None)

                         if target_role:
                             for i, msg in enumerate(self.chat_history):
                                 if msg['role'] == target_role:
                                     count += 1
                                     if count == msg_num:
                                         history_idx = i
                                         break
                         if history_idx != -1:
                            original_content = self.chat_history[history_idx]['content']
                         elif role == 'error': # Errors aren't in history
                             original_content = display_text

                    except (ValueError, IndexError) as e_hist:
                         logger.warning(f"Could not parse index or find message in history for {msg_tag}: {e_hist}")
                         original_content = display_text # Fallback

                    return ranges, original_content, display_text
                except Exception as e_disp:
                    logger.error(f"Error finding message details for {msg_tag}: {e_disp}", exc_info=True)
        return None, None, None

    def _copy_message(self, format="markdown"):
        try:
            current_index = self.chat_display.index(tk.CURRENT)
            ranges, original_content, display_text = self._get_message_range_and_content(current_index)
            if ranges:
                content_to_copy = original_content if format == "markdown" else display_text
                self.clipboard_clear()
                self.clipboard_append(content_to_copy)
                logger.debug(f"Copied message ({format}) to clipboard.")
            else:
                 logger.warning("Copy Message: Cursor not inside a detected message block.")
        except Exception as e:
            logger.error(f"Failed to copy message: {e}", exc_info=True)

    # --- Method called by Explain context menu ---
    def explain_this(self, text_to_explain, source):
        """Receives text from editor/shell and initiates explanation."""
        logger.info(f"Received text from {source} for explanation.")

        if self.streaming_thread and self.streaming_thread.is_alive():
             messagebox.showwarning("Busy", "AI Chat is busy. Please wait.")
             return

        api_url = self.api_url.get().strip()
        api_key = self.api_key.get().strip()
        model = self.selected_model.get()

        if not api_url or not api_key or not model or model == "Configure API first" or model == "Error fetching" or model == "No models found":
             messagebox.showerror("Missing Info", "Please configure AI Chat API URL, Key, and select a valid Model.")
             return

        # Construct the prompt (Instruction in English, mentioning target language)
        prompt = (f"Explain the following {source} selection "
                  f"(please respond in {self.system_language}):\n\n"
                  f"```\n{text_to_explain}\n```")

        # Add explanation request to history (as user role for context)
        user_msg_id = f"user_{len(self.chat_history)}"
        self.chat_history.append({"role": "user", "content": prompt})
        self._add_message_to_display("user", prompt, message_id=user_msg_id)

        # Prepare placeholder for assistant response
        self.current_assistant_message_id = f"asst_{len(self.chat_history)}"
        self._add_message_to_display("assistant", "...", message_id=self.current_assistant_message_id)

        # Start streaming request
        logger.debug("Starting stream worker for explanation request.")
        self.streaming_thread = threading.Thread(
            target=self._stream_chat_worker,
            args=(api_url, api_key, model, list(self.chat_history)), # Send copy
            daemon=True
        )
        self.streaming_thread.start()

    def destroy(self):
        """Called when the view is closed."""
        global _ai_chat_view_visible
        _ai_chat_view_visible = False # Update state when closed
        logger.info(f"{VIEW_ID} destroy method called, setting _ai_chat_view_visible to False.")
        self._save_settings() # Save settings on close
        super().destroy()

# --- Toggle Function (Robust Version) ---
def toggle_ai_chat_view():
    """Handles the click from the View menu, using manual state tracking."""
    global _ai_chat_view_visible
    workbench = get_workbench()
    if workbench is None:
         logger.error("Failed to get workbench in toggle function")
         messagebox.showerror("Error", "Could not get Thonny workbench.")
         return

    logger.debug(f"Toggle requested. Current manual state: {_ai_chat_view_visible}")
    try:
        if not _ai_chat_view_visible:
            logger.debug(f"Manual toggle: State is hidden, attempting show_view({VIEW_ID}).")
            workbench.show_view(VIEW_ID)
            _ai_chat_view_visible = True
            logger.info(f"Manual toggle: View {VIEW_ID} shown.")
        else:
            logger.debug(f"Manual toggle: State is visible, attempting hide_view({VIEW_ID}).")
            workbench.hide_view(VIEW_ID)
            _ai_chat_view_visible = False
            logger.info(f"Manual toggle: View {VIEW_ID} hidden.")
    except AttributeError as e:
         logger.error(f"Manual show/hide failed - method missing?: {e}", exc_info=True)
         messagebox.showerror("Error", f"Could not toggle AI Chat View (show/hide method missing):\n{e}")
         _ai_chat_view_visible = False # Reset state if methods missing
    except Exception as e:
         logger.error(f"Manual show/hide failed for {VIEW_ID}: {e}", exc_info=True)
         messagebox.showerror("Error", f"Could not toggle AI Chat View:\n{e}")
         _ai_chat_view_visible = False # Reset state defensively

# --- Context Menu Helpers and Handlers ---
def _has_selection(widget):
    """Checks if a Text widget has selected text."""
    if not isinstance(widget, tk.Text): return False
    try: return bool(widget.tag_ranges("sel"))
    except: return False

def _trigger_explain(source_hint="unknown"):
    """Core logic to get selection from focused/relevant widget and call AI Chat view."""
    workbench = get_workbench()
    widget = None
    # ... (代码与上次相同：获取 widget, 检查 Text, 获取 selection, 判断 source, 调用 AI View) ...
    # (请确保这部分逻辑是完整的)
    try:
        # Get widget based on hint or focus
        if source_hint == "editor":
             editor = workbench.get_editor_notebook().get_current_editor()
             if editor: widget = editor.get_text_widget()
        elif source_hint == "shell":
             shell_view = get_shell()
             if shell_view: widget = shell_view.text
        else: # Fallback or from generic handler
             widget = workbench.focus_get()

        if not widget or not isinstance(widget, tk.Text):
             logger.warning(f"Explain trigger: Could not get valid Text widget for hint '{source_hint}'.")
             return

    except Exception as e:
        logger.error(f"Explain trigger: Error getting widget for hint '{source_hint}': {e}", exc_info=True)
        return

    # Check selection
    if not _has_selection(widget):
         logger.debug(f"Explain trigger from {source_hint}: No text selected.")
         # Show message only if triggered explicitly by user (not just menu check)
         # messagebox.showinfo("Explain Text", "Please select the text you want to explain first.")
         return # Simply don't proceed if no selection

    selected_text = ""
    try:
        selected_text = widget.get(tk.SEL_FIRST, tk.SEL_LAST).strip()
        if not selected_text: # Check if empty after strip
            logger.debug(f"Explain trigger from {source_hint}: Selected text is empty.")
            return
    except tk.TclError:
        logger.debug(f"Explain trigger from {source_hint}: TclError getting selection.")
        return
    except Exception as e:
         logger.error(f"Explain trigger: Error getting selected text: {e}", exc_info=True)
         messagebox.showerror("Error", f"Could not get selected text:\n{e}")
         return

    # Determine Source (Best Effort if hint was 'unknown' or 'focused_widget')
    if source_hint in ["unknown", "focused_widget"]:
         source_type = "unknown_text"
         try:
             editor = workbench.get_editor_notebook().get_current_editor()
             if editor and widget == editor.get_text_widget():
                 source_type = "editor"
             else:
                 shell_view = get_shell()
                 if shell_view and widget == shell_view.text:
                     source_type = "shell"
         except Exception: pass
    else:
         source_type = source_hint


    # Trigger the AI Chat View
    try:
        workbench.show_view(VIEW_ID)
        workbench.update_idletasks()
        ai_view = workbench.get_view(VIEW_ID)
        if ai_view and hasattr(ai_view, "explain_this"):
            logger.info(f"Sending text from {source_type} (widget: {widget}) to AI Chat for explanation.")
            ai_view.explain_this(selected_text, source_type)
        elif not ai_view:
             logger.error("Explain trigger: Could not get AI Chat View instance.")
             messagebox.showerror("Error", "Could not find the AI Chat View.")
        else:
             logger.error("Explain request: AI Chat View missing 'explain_this' method.")
             messagebox.showerror("Error", "AI Chat View is not configured correctly.")
    except Exception as e:
        logger.error(f"Explain trigger: Error interacting with AI view: {e}", exc_info=True)
        messagebox.showerror("Error", f"Could not send text to AI Chat:\n{e}")




# --- Monkey Patching for Shell Menu ---

# Store the original ShellMenu class (assuming it's accessible via thonny.shell)
try:
    OriginalShellMenu = thonny.shell.ShellMenu
except AttributeError:
    logger.error("Could not find thonny.shell.ShellMenu for monkey patching!")
    OriginalShellMenu = None

# Define your custom class inheriting from the original
if OriginalShellMenu: # Only define if we found the original
    class CustomShellMenu(OriginalShellMenu):
        def __init__(self, target, view):
            # Call original __init__ is crucial
            super().__init__(target, view)
            # Maybe add items here? Or rely on add_extra_items? Let's stick to add_extra_items

        def add_extra_items(self):
            # Call the original method first to get default items
            super().add_extra_items()

            # Now add our custom item, potentially checking selection
            self.add_separator()
            # We need access to the text widget (target) to check selection
#             if hasattr(self, 'text') and _has_selection(self.text): # Use self.target which should be the ShellText
#                  self.add_command(label="Explain Selection (AI Chat)",
#                                   command=lambda: _trigger_explain("shell")) # Pass shell hint
#                  logger.debug("Added enabled 'Explain Selection' to CustomShellMenu.")
#             else:
#                  # Add disabled command if no selection
#                  self.add_command(label="Explain Selection (AI Chat)", state="disabled")
#                  logger.debug("Added disabled 'Explain Selection' to CustomShellMenu.")
            self.add_command(label="🤖Explain Selection (AI Chat)",
                             command=lambda: _trigger_explain("shell"), # Pass shell hint
                             state="normal") # Always enabled
            logger.debug("Added 'Explain Selection' command (always enabled) to CustomShellMenu.")

# --- Plugin Load Function ---
# --- Function to Open Settings Dialog ---
def open_settings_dialog():
    """Handler function to open the settings dialog."""
    workbench = get_workbench()
    ai_view = workbench.get_view(VIEW_ID) # Get the main view instance

    if not ai_view:
        # If view isn't open yet, maybe open it first? Or show error?
        # Let's try showing the view first.
        try:
            logger.info("AI Chat View not open, showing it before opening settings.")
            toggle_ai_chat_view() # Use the existing toggle function
            workbench.update_idletasks() # Allow view to appear
            ai_view = workbench.get_view(VIEW_ID) # Try getting it again
            if not ai_view:
                 messagebox.showerror("Error", "Could not open AI Chat View to access settings.")
                 return
        except Exception as e:
             logger.error(f"Error trying to show AI view for settings: {e}", exc_info=True)
             messagebox.showerror("Error", f"Could not open AI Chat View to access settings:\n{e}")
             return

    # Now open the dialog, passing the main view instance
    try:
        # Pass Thonny's main window as master
        SettingsDialog(workbench, ai_view)
    except Exception as e:
         logger.error(f"Failed to open Settings Dialog: {e}", exc_info=True)
         messagebox.showerror("Error", f"Could not open settings dialog:\n{e}")


# --- Plugin Load Function ---
def load_plugin():
    """Registers the view, commands, menus, and applies patches."""
    # ... (Logging, workbench check, requests check) ...
    global logger
    logger = logging.getLogger(__name__)
    # ... (Rest of setup) ...

    workbench = get_workbench()
    if workbench is None: return
    try: import requests
    except ImportError: # ... (handle missing requests) ...
        return

    # 1. Register the View itself
    # ... (add_view code for location 'e') ...
    try:
        workbench.add_view(AIChatView, PLUGIN_TITLE, "w", view_id=VIEW_ID) # Use 'e'
        logger.info(f"Registered view '{PLUGIN_TITLE}' at location 'w'.")
    except TypeError:
        workbench.add_view(AIChatView, PLUGIN_TITLE, "w") # Fallback 'e'
        logger.info(f"Registered view '{PLUGIN_TITLE}' (fallback) at location 'w'.")
    except Exception as e: # ... (handle add_view error) ...
        return

    # 2. Add command to the "View" menu for toggling the view
    # ... (add_command for toggle_ai_chat_view) ...
#     try:
#         workbench.add_command(command_id="toggle_ai_chat_view", menu_name="view",
#                                 command_label=PLUGIN_TITLE, handler=toggle_ai_chat_view, group=10)
#         logger.info("Added 'toggle_ai_chat_view' command to 'View' menu.")
#     except Exception as e: # ... (handle add_command error) ...
#         pass # Continue loading other parts

    # --- 3. Create "AI" Main Menu and "Settings" item ---
    ai_menu_name = "ai_plugin_menu" # Internal name for the AI menu
    settings_command_id = "ai_plugin_settings"
    try:
        # Add the Settings command under the new AI menu
        # Thonny should automatically create the top-level "AI" menu
        # when a command is added to a non-existent menu_name.
        # The label for the top-level menu is often derived from the first added command's context
        # or might need a separate registration (less common). Let's try adding command first.
        workbench.add_command(
            command_id=settings_command_id,
            menu_name=ai_menu_name, # Target our new menu
            command_label="Settings...", # Label shown in the AI menu
            handler=open_settings_dialog, # Function to call
            group=10 # Position within the AI menu
        )
        logger.info(f"Added 'Settings...' command under menu '{ai_menu_name}'.")

        # Optional: Add a dummy command to potentially control the top-level menu label directly?
        # Might not be needed if Thonny names it "AI" automatically.
        # try:
        #     workbench.add_command(command_id="ai_top_menu_label", menu_name=MENUBAR_ITEM, # Special constant?
        #                           command_label="AI", group=55) # Position relative to File, Edit etc.
        # except NameError: # If MENUBAR_ITEM not known
        #     logger.debug("Could not add explicit top-level menu label.")
        # except Exception as e_label:
        #     logger.warning(f"Could not add explicit top-level menu label: {e_label}")


    except Exception as e:
        logger.error(f"Failed to add 'Settings...' command or 'AI' menu: {e}", exc_info=True)
    # -----------------------------------------------------

    # --- 4. Add command to Editor Context Menu ---
    # ... (add_command for editor context menu, using menu_name='edit') ...
    editor_menu_name = "edit"
    try:
        editor_explain_handler = lambda: _trigger_explain("editor")
        workbench.add_command(command_id="explain_editor_selection", menu_name=editor_menu_name,
                                command_label="🤖Explain Selection (AI Chat)", handler=editor_explain_handler, group=80)
        workbench.add_command(command_id="explain_editor_separator", menu_name=editor_menu_name,
                                command_label="---", group=79)
        logger.info(f"Added 'Explain Selection' to editor menu '{editor_menu_name}'.")
    except Exception as e: # ... (handle add_command error) ...
        logger.error(f"Failed to add command to editor menu '{editor_menu_name}': {e}", exc_info=True)


    # --- 5. Apply Monkey Patch for Shell Menu ---
    # ... (Monkey patching code for ShellMenu remains the same) ...
    if OriginalShellMenu and CustomShellMenu:
        try:
            logger.info("Attempting to monkey-patch thonny.shell.ShellMenu...")
            thonny.shell.ShellMenu = CustomShellMenu
            logger.info("Successfully monkey-patched thonny.shell.ShellMenu.")
            def restore_original_shell_menu(event=None): # ... (restore function) ...
                 try:
                     if hasattr(thonny.shell, 'ShellMenu') and thonny.shell.ShellMenu == CustomShellMenu:
                         logger.info("Restoring original thonny.shell.ShellMenu...")
                         thonny.shell.ShellMenu = OriginalShellMenu
                 except Exception as e: logger.error(f"Error restoring ShellMenu: {e}", exc_info=True)
            workbench.bind("WorkbenchClose", restore_original_shell_menu, True)
            logger.info("Bound WorkbenchClose event to restore original ShellMenu.")
        except Exception as e: # ... (handle patch error) ...
            logger.error(f"Failed to monkey-patch ShellMenu: {e}", exc_info=True)
    else:
        logger.warning("Could not apply ShellMenu monkey patch.")
    # ------------------------------------------

    logger.info(f"{PLUGIN_TITLE} plugin loaded successfully.")

# --- Optional unload_plugin function for immediate cleanup ---
def unload_plugin():
   logger.info(f"Unloading plugin: {PLUGIN_TITLE}")
   try:
       # Attempt to restore original ShellMenu if patch was applied
       if OriginalShellMenu and hasattr(thonny.shell, 'ShellMenu') and thonny.shell.ShellMenu == CustomShellMenu:
            logger.info("Unloading: Restoring original thonny.shell.ShellMenu...")
            thonny.shell.ShellMenu = OriginalShellMenu
   except Exception as e:
       logger.error(f"Error restoring ShellMenu during unload: {e}")
   # Unbind event? Workbench might handle this, but explicit unbind is safer if possible.
   # try:
   #    workbench = get_workbench()
   #    if workbench:
   #         workbench.unbind("WorkbenchClose", ...) # Need the handler instance or ID
   # except Exception as e:
   #    logger.warning(f"Could not unbind WorkbenchClose handler: {e}")

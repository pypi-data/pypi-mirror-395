import os
import sys
import subprocess
from pathlib import Path
import re
from datetime import datetime
from shiny import App, ui, render, reactive, req
import toml as toml  # pip: toml

# --- Configuration Management ---
CONFIG_FILE = Path("config.toml")

DEFAULT_CONFIG = {
    "models": [
    "GPT-4o", "GPT-4o mini", "GPT-5.1", "GPT-5",  # OpenAI
    "Gemini 3 Pro",  # Google
    "Claude Sonnet 4.5", "Claude Haiku 4.5", "Claude Opus 4.5",  # Anthropic
    ],
    "author": "Karl Dafoe",
    "port": 5555
}

def load_config():
    """Loads config from file or returns default if not exists."""
    if CONFIG_FILE.exists():
        try:
            return toml.load(CONFIG_FILE)
        except Exception as e:
            print(f"Error loading config: {e}")
            return DEFAULT_CONFIG
    return DEFAULT_CONFIG

def save_config(models_list, human_author):
    """Saves the updated models list and human author to config.toml."""
    try:
        data = {
            "models": models_list,
            "author": human_author
        }
        with open(CONFIG_FILE, "w") as f:
            toml.dump(data, f)
    except Exception as e:
        print(f"Error saving config: {e}")

def preprocess_markdown(text):
    """
    Cleans up the markdown text based on specific rules:
    1. Gemini Wrapper Cleanup: Collapses the block from '## Gemini' to 'Update location'
       keeping only the Activity Status and Location.
    2. Add empty line between horizontal rule '---' and bold text '**' if they are adjacent.
    3. Remove lines starting with '![profile picture]'
    4. Remove lines containing '{{@CAPTURE_ARTIFACT_CONTENT:undefined}}'
    5. Clean 'Exported on...' lines to remove SaveYourChat branding.
    """
    
    # Rule 1: Gemini Wrapper Block Cleanup
    # Matches a block starting with "## Gemini" and ending with "Update location"
    # Extract only the relevant metadata lines from inside this block.
    def gemini_block_cleaner(match):
        content = match.group(0)
        
        # Extract "Gemini Apps Activity is ..."
        activity_match = re.search(r"(Gemini Apps Activity is (?:on|off))", content, re.IGNORECASE)
        activity_line = activity_match.group(1) if activity_match else ""
        
        # Extract location line (ends with "Update location")
        # We look for the specific line in the content that ends with the marker
        location_match = re.search(r"(^.*Update location$)", content, re.MULTILINE)
        location_line = location_match.group(1) if location_match else ""
        
        # Return cleaned block (only the two extracted lines)
        return f"{activity_line}  \n{location_line}"

    # Apply regex on the full text
    # flags=re.DOTALL allows .*? to match across newlines
    # flags=re.MULTILINE allows ^ and $ to match start/end of lines
    text = re.sub(
        r"^## Gemini.*?Update location$", 
        gemini_block_cleaner, 
        text, 
        flags=re.DOTALL | re.MULTILINE
    )

    # Rule 2: Fix spacing between horizontal rule and bold text
    # If "---" is immediately followed by "**" on the next line, insert an empty line.
    text = re.sub(r'^---\n\*\*', r'---\n\n**', text, flags=re.MULTILINE)

    lines = text.splitlines()
    cleaned_lines = []
    
    for line in lines:
        stripped = line.strip()
        
        # Rule 3: Remove profile picture lines
        if stripped.startswith("![profile picture]"):
            continue

        # Rule 4: Remove capture artifact undefined lines
        if "{{@CAPTURE_ARTIFACT_CONTENT:undefined}}" in line:
            continue

        # Rule 5: Remove '[Turn it on here...]' lines (Redundant if caught by Rule 1, but safe to keep)
        if stripped.startswith("[Turn it on here Opens in a new window]"):
            continue
            
        # Rule 6: Clean Exported on... lines
        if " - with [SaveYourChat" in line:
            line = re.sub(r'\s+-\s+with\s+\[SaveYourChat\].*?$', '', line)
            line = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', line)
            
        cleaned_lines.append(line)
        
    return "\n".join(cleaned_lines)

# --- UI Definition ---
app_ui = ui.page_fluid(
    # Link the favicon located in the mounted static directory
    ui.tags.head(
        ui.tags.link(rel="icon", type="image/svg+xml", href="/static/favicon.svg")
    ),
    ui.tags.style(
        """
        .form-control { margin-bottom: 10px; }
        .btn-primary { margin-top: 10px; }
        """
    ),
    ui.panel_title("Markdown to PDF Converter (Quarto)"),
    
    ui.layout_sidebar(
        ui.sidebar(
            ui.h4("Settings"),
            
            # Directory Selection
            ui.input_action_button("choose_dir_btn", "Choose Folder", icon="folder-open"),
            ui.output_text_verbatim("selected_path_display", placeholder=True),
            
            ui.hr(),
            
            # File Name
            ui.input_text("filename", "File Name (no extension)", placeholder="my_document"),
            
            # Model Selection
            ui.input_selectize(
                "author_model", 
                "Select Model:", 
                choices=[], 
                multiple=False,
                options={"create": True, "placeholder": "Select or type new..."}
            ),

            # Human Author Selection
            ui.input_text("human_author", "Human Author:", placeholder="Name"),
            
            ui.hr(),
            
            # Save Button
            ui.input_action_button("save_btn", "Save & Convert", class_="btn-primary"),
            
            # Status Output
            ui.output_ui("status_message"),
            width=350
        ),
        
        # Main Content Area
        ui.card(
            ui.card_header("Content"),
            ui.input_text_area(
                "markdown_content", 
                "", 
                placeholder="Paste your Markdown text here...", 
                height="600px"
            ),
            full_screen=True
        )
    )
)

# --- Server Logic ---
def server(input, output, session):
    # Reactive value to store the selected directory path
    selected_dir = reactive.Value(str(Path.home()))
    
    # Reactive value to manage the list of available models
    available_models = reactive.Value([])

    # Initialize: Load config on startup
    @reactive.Effect
    def startup():
        conf = load_config()
        # Clean list to ensure unique values
        models = sorted(list(set(conf.get("models", DEFAULT_CONFIG["models"]))))
        available_models.set(models)
        
        # Load human author
        human_author = conf.get("author", DEFAULT_CONFIG["author"])
        ui.update_text("human_author", value=human_author)
        
        # Update the UI dropdown
        ui.update_selectize(
            "author_model",
            choices=models,
            selected=models[0] if models else None,
            options={"create": True, "maxItems": 1}
        )

    # Directory Picker Logic (Separate Subprocess)
    @reactive.Effect
    @reactive.event(input.choose_dir_btn)
    def handle_dir_selection():
        current_dir = selected_dir.get()
        
        # We run a small independent script to open the dialog.
        # This ensures the Tkinter event loop runs in a completely separate process (PID),
        # isolating it from the Shiny async loop and preventing macOS hangs.
        dialog_script = """
import tkinter as tk
from tkinter import filedialog
import sys

# Get initial dir from args or default to None
initial_dir = sys.argv[1] if len(sys.argv) > 1 else None

root = tk.Tk()
root.withdraw()  # Hide the main window
# root.attributes('-topmost', True)  # Ensure dialog is on top

try:
    root.update()
    path = filedialog.askdirectory(initialdir=initial_dir)
    # Print path to stdout so parent process can read it
    if path:
        print(path, end='')
finally:
    # Destroying root here ends the Tcl interpreter.
    # Since this is a subprocess, the OS will clean up the PID immediately after this script exits.
    root.destroy()
"""
        try:
            # Run the script in a separate process
            result = subprocess.run(
                [sys.executable, "-c", dialog_script, current_dir],
                capture_output=True,
                text=True,
                check=False 
            )
            
            new_path = result.stdout.strip()
            if new_path:
                selected_dir.set(new_path)
                
        except Exception as e:
            print(f"Subprocess Error: {e}")

    # Display selected path
    @render.text
    def selected_path_display():
        return f"Save in:\n{selected_dir.get()}"

    # Main Save Logic
    @output
    @render.ui
    @reactive.event(input.save_btn)
    def status_message():
        # 1. Validation
        raw_md_text = input.markdown_content()
        fname = input.filename()
        save_path = selected_dir.get()
        model_name = input.author_model()
        human_name = input.human_author()

        if not fname:
            return ui.notification_show("Error: Please enter a file name.", type="error")
        if not raw_md_text:
            return ui.notification_show("Error: Text content is empty.", type="error")
        
        # Preprocessing: Clean the markdown text
        md_text = preprocess_markdown(raw_md_text)
        
        # 2. Update Configuration (if new model added OR author changed)
        current_models = available_models.get()
        
        # Update models list if new one added
        if model_name and model_name not in current_models:
            current_models = sorted(list(set(current_models + [model_name])))
            available_models.set(current_models)
            ui.update_selectize("author_model", choices=current_models, selected=model_name)
        
        # Save to config (both models list and the current human author)
        save_config(current_models, human_name)

        # 3. Prepare Author String
        final_author = f"{model_name} & {human_name}" if human_name else model_name

        # 4. Prepare Paths
        try:
            base_path = Path(save_path) / fname
            md_file = base_path.with_suffix(".md")
            
            # Generate Timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 5. Construct Content with Front Matter
            front_matter = f"""---
title: "{fname}"
author: "{final_author}"
date: "{timestamp}"
format: pdf
---

"""
            full_content = front_matter + md_text

            # 6. Save Markdown
            with open(md_file, "w", encoding="utf-8") as f:
                f.write(full_content)
            
            # 7. Convert to PDF using Quarto
            cmd = ["quarto", "render", str(md_file.name), "--to", "pdf"]
            
            process = subprocess.run(
                cmd, 
                cwd=str(base_path.parent),
                capture_output=True, 
                text=True
            )

            if process.returncode == 0:
                # Clear the text area after successful save
                ui.update_text_area("markdown_content", value="")

                msg = ui.div(
                    ui.h5("Success!", style="color: green"),
                    ui.p(f"Markdown saved: {md_file}"),
                    ui.p(f"PDF generated: {base_path.with_suffix('.pdf')}")
                )
                ui.notification_show("Files saved and converted successfully!", type="message")
                return msg
            else:
                err_msg = f"Quarto Error: {process.stderr}"
                ui.notification_show("PDF Conversion Failed", type="error")
                return ui.div(
                    ui.h5("Saved Markdown, but PDF failed.", style="color: orange"),
                    ui.pre(err_msg)
                )

        except Exception as e:
            return ui.div(f"System Error: {str(e)}", style="color: red")

# --- App Definition ---
# Mount the 'static' directory to serve the favicon
static_dir = Path(__file__).parent / "static"
app = App(app_ui, server, static_assets={"/static": static_dir})

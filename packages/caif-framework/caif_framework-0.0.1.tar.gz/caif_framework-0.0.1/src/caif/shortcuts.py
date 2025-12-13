# We assume the core logic components are available (imported in a real setup)
# from .model_core import CAIF_MODEL_CORE
# from .data_handler import _DataHandler
# from .output_processor import CAIF_OUTPUT_PROCESSOR

class _Shortcuts:
    """
    Internal class managing high-level, multi-step shortcut commands 
    like WEB_CHATBOT and ANALYZE for the CAIF framework.
    """

    @staticmethod
    def run_analyze_shortcut(data_source, target_column, focus):
        """
        Implements the CAIF.ANALYZE() command logic.
        Loads data, trains a model, and generates a report or visualization.
        """
        print("\n[ANALYZE SHORTCUT] Step 1: Data Preparation...")
        # 1. DATA: Load the data and get the embeddings
        # We assume the data source type is derived from the extension or detected automatically
        source_type = data_source.split('.')[-1]
        X, Y = _DataHandler.load_and_embed(data_source, source_type, target_column)

        print("[ANALYZE SHORTCUT] Step 2: Model Training...")
        # 2. MODEL: Train the best model for this data (target column)
        CAIF_MODEL_CORE.train_model(X, Y, type_tag="data_analyzer", complexity=7, time_limit="30m")
        
        # 3. ANALYZE/PREDICT: Generate a rich report based on the focus
        markdown_report = ""
        if focus == "report":
            # Generate a rich report using model evaluation metrics
            print("[ANALYZE SHORTCUT] Step 3: Generating Performance Report...")
            score = CAIF_MODEL_CORE.trained_model.score(X, Y) # Example evaluation
            markdown_report = (
                f"## CAIF Data Analysis Report\n\n"
                f"**Target:** `{target_column}`\n"
                f"**Model Type:** `{CAIF_MODEL_CORE.model_target_type}`\n"
                f"**Performance Score:** **{score:.4f}** (Closer to 1 is better for classification)\n\n"
                f"The analysis is complete. Use `CAIF.OUTPUT()` to save this report as HTML or Python code."
            )
        elif focus == "web_viz":
            # Generate a code block that represents an interactive HTML dashboard
            print("[ANALYZE SHORTCUT] Step 3: Generating Web Visualization Code...")
            markdown_report = (
                f"## CAIF Web Visualization Code\n\n"
                f"Below is the generated **HTML and JavaScript** code for a live prediction dashboard:\n\n"
                "```html\n"
                "<div class='caif-dashboard'>... Interactive Form Code Here ...</div>\n"
                "```\n\n"
                "Save this output as HTML using `CAIF.OUTPUT(target='HTML', save_as='viz.html')`."
            )

        # Update the output processor with the generated report
        CAIF_OUTPUT_PROCESSOR.last_markdown_result = markdown_report
        
        print(f"[ANALYZE SHORTCUT] **Success:** Analysis complete. Markdown report ready.")
        return True
    

    @staticmethod
    def run_web_chatbot_shortcut(personality, data_source, interface, look_spec, parameters):
        """
        Implements the CAIF.WEB_CHATBOT() command logic.
        Trains a model and generates a full HTML/CSS/JS interface.
        """
        print("\n[CHATBOT SHORTCUT] Step 1: Data Preparation...")
        # 1. DATA: Load the dialogue data and get the embeddings (Assuming text/dialogue type)
        X, Y = _DataHandler.load_and_embed(data_source, "text/dialogue", target_column="response")
        
        print("[CHATBOT SHORTCUT] Step 2: Model Training...")
        # 2. MODEL: Train the model for text generation
        CAIF_MODEL_CORE.train_model(X, Y, type_tag="chatbot_generator", complexity=5, time_limit="10m")
        
        print("[CHATBOT SHORTCUT] Step 3: Interface Generation (MDP/HTML/CSS/JS)...")
        # 3. MDP: Generate the necessary HTML/CSS/JS code
        
        # Simple CSS generation based on look_spec (Abstraction)
        css_styles = f"body {{ background: {look_spec.get('window', 'white')}; font: {look_spec.get('font', 'Arial')}; }}"

        # Simple HTML structure
        html_code = (
            f"<div id='caif-chat-box' style='{css_styles}'>\n"
            f"  <h1>{personality.title()} CAIF Chatbot</h1>\n"
            f"  <div id='chat-history'></div>\n"
            f"  <input type='text' id='user-input' placeholder='Type a message...'>\n"
            f"  <button onclick='sendMessage()'>Send</button>\n"
            f"</div>"
        )
        
        # Simple JavaScript to handle interaction
        js_code = (
            f"function sendMessage() {{\n"
            f"  const userInput = document.getElementById('user-input').value;\n"
            f"  // In a real CAIF deployment, this sends 'userInput' to the masked AI route\n"
            f"  const aiResponse = `I am a {personality} chatbot trained on your data!`;\n" # Placeholder response
            f"  document.getElementById('chat-history').innerHTML += `<p>You: ${{userInput}}</p><p>AI: ${{aiResponse}}</p>`;\n"
            f"}}\n"
        )

        # 4. Final Markdown combining all the rich text output
        markdown_output = (
            f"## CAIF Web Chatbot Builder Output\n\n"
            f"The chatbot model is trained and the interface code is generated.\n\n"
            f"**Interface Technologies:** `{interface}`\n"
            f"**Personality:** `{personality}`\n\n"
            f"### HTML Structure\n```html\n{html_code}\n```\n\n"
            f"### CSS Styles\n```css\n{css_styles}\n```\n\n"
            f"### JavaScript Logic\n```javascript\n{js_code}\n```"
        )
        
        # Update the output processor with the generated code
        CAIF_OUTPUT_PROCESSOR.last_markdown_result = markdown_output
        
        print(f"[CHATBOT SHORTCUT] **Success:** Web interface code generated. Use CAIF.OUTPUT() to save as HTML.")
        return True


# We create a single instance of the Shortcuts manager for clean internal use.
CAIF_SHORTCUTS = _Shortcuts()

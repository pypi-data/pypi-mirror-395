# src/caif/__init__.py

# --- 1. Import Internal CAIF Components ---
# This is how the simple user command connects to the powerful logic.
try:
    from .data_handler import _DataHandler
    from .model_core import CAIF_MODEL_CORE
    from .output_processor import CAIF_OUTPUT_PROCESSOR
    from .shortcuts import CAIF_SHORTCUTS
except ImportError:
    # This handles the case where the user runs the package without installing it locally first
    print("[CAIF] Warning: Running in development mode. Ensure package is installed for full functionality.")
    
# --- 2. Define the CAIF Class ---
class CAIF:
    """
    The Code AI Fast (CAIF) Framework. 
    A unified interface for fast, code-simplified AI development.
    """
    
    # --- CORE COMMANDS ---
    
    @staticmethod
    def DATA(source, type, target_column=None):
        """
        Loads and prepares training data from any source (URL or file) 
        and any native type (CSV, MP4, JPG, etc.). Stores embeddings internally.
        """
        print(f"[CAIF.DATA] Initializing data load...")
        # Calls the actual data handling logic
        X, Y = _DataHandler.load_and_embed(source, type, target_column)
        
        # Store the prepared data (X and Y) in the model core for the next command to use
        CAIF_MODEL_CORE.set_data(X, Y)
        
        print(f"[CAIF.DATA] Data preparation complete. Embeddings ready for model training.")
        return True 

    @staticmethod
    def MODEL(type, complexity, time_limit="1h"):
        """
        Builds, sketches, and trains the Neural Network model.
        """
        print(f"[CAIF.MODEL] Starting model sketch and training...")
        # Calls the actual model training logic using the stored data
        CAIF_MODEL_CORE.train_model(
            CAIF_MODEL_CORE.X_data, 
            CAIF_MODEL_CORE.Y_data, 
            type_tag=type, 
            complexity=complexity, 
            time_limit=time_limit
        )
        print(f"[CAIF.MODEL] Training complete. Model tagged as '{type}'.")
        return True 

    @staticmethod
    def PREDICT(input):
        """
        Runs the trained model on new input and returns the AI's raw Markdown response.
        """
        print(f"[CAIF.PREDICT] Running prediction...")
        # Calls the output processor to generate the prediction and format it as Markdown (AILP)
        markdown_result = CAIF_OUTPUT_PROCESSOR.generate_prediction(CAIF_MODEL_CORE, input)
        print(f"[CAIF.PREDICT] Prediction complete. Markdown stored in output processor.")
        return markdown_result

    @staticmethod
    def OUTPUT(target, save_as):
        """
        Processes the last AI Markdown response and converts it into 
        the target format (HTML or PYTHON code) using the MDP.
        """
        print(f"[CAIF.OUTPUT] Generating final output...")
        # Calls the output processor to convert and save the file (MDP)
        success = CAIF_OUTPUT_PROCESSOR.process_output(target, save_as)
        if success:
            print(f"[CAIF.OUTPUT] Successfully saved converted content to {save_as}")
        return success
        
    # --- SHORTCUT COMMANDS ---

    @classmethod
    def WEB_CHATBOT(cls, personality, data_source, interface, look_spec, parameters):
        """
        Shortcut: Builds a complete, styled, web-based chatbot (HTML/CSS/JS).
        """
        print(f"[CAIF.WEB_CHATBOT] Running specialized Web Chatbot shortcut...")
        # Calls the shortcut logic from the shortcuts file
        return CAIF_SHORTCUTS.run_web_chatbot_shortcut(personality, data_source, interface, look_spec, parameters)

    @classmethod
    def ANALYZE(cls, data_source, target_column, focus="report"):
        """
        Shortcut: Loads tabular data and trains a model for prediction/analysis.
        """
        print(f"[CAIF.ANALYZE] Running specialized Data Analysis shortcut...")
        # Calls the shortcut logic from the shortcuts file
        return CAIF_SHORTCUTS.run_analyze_shortcut(data_source, target_column, focus)

# To make the framework simple, we expose only the main class.
__all__ = ['CAIF']

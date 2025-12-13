# src/caif/__init__.py

# --- 1. Import Internal CAIF Components ---
try:
    from .data_handler import _DataHandler
    from .model_core import _ModelCore
    from .output_processor import _OutputProcessor
    from .shortcuts import _Shortcuts
except ImportError:
    print("[CAIF] Warning: Running in development mode. Ensure package is installed for full functionality.")

# --- 2. Create Global Instances for State Management ---
# These single instances manage which data is loaded and which model is trained.
CAIF_MODEL_CORE = _ModelCore()
CAIF_OUTPUT_PROCESSOR = _OutputProcessor()
CAIF_SHORTCUTS = _Shortcuts()

# --- 3. Define the CAIF Class (The User Interface) ---
class CAIF:
    """
    The Code AI Fast (CAIF) Framework. 
    A unified interface for fast, code-simplified AI development.
    """
    
    # --- CORE COMMANDS ---
    
    @staticmethod
    def DATA(source, type, target_column=None):
        """
        Loads and prepares training data. Stores embeddings internally in the model core.
        """
        print(f"[CAIF.DATA] Initializing data load...")
        # Get the processed data
        X, Y = _DataHandler.load_and_embed(source, type, target_column)
        
        # Pass the data to the model core for the next command to use
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
        # Calls the output processor (AILP)
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
        # Calls the output processor (MDP)
        success = CAIF_OUTPUT_PROCESSOR.process_output(target, save_as)
        return success
        
    # --- SHORTCUT COMMANDS ---

    @classmethod
    def WEB_CHATBOT(cls, personality, data_source, interface, look_spec, parameters):
        return CAIF_SHORTCUTS.run_web_chatbot_shortcut(personality, data_source, interface, look_spec, parameters)

    @classmethod
    def ANALYZE(cls, data_source, target_column, focus="report"):
        return CAIF_SHORTCUTS.run_analyze_shortcut(data_source, target_column, focus)

__all__ = ['CAIF']

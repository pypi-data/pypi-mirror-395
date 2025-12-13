# src/caif/error_handler.py

class CAIFError(Exception):
    """
    Custom exception class for all errors within the CAIF framework. 
    This allows CAIF to catch its own specific errors.
    """
    def __init__(self, message, advice=None):
        self.message = message
        self.advice = advice
        super().__init__(self.message)

class _ErrorHandler:
    """
    Internal class managing all error reporting and handling for CAIF.
    Provides clear messages and actionable advice to the user.
    """
    
    @staticmethod
    def handle_data_error(error: Exception, source: str, file_type: str):
        """Handles errors specifically during the CAIF.DATA() command."""
        
        if isinstance(error, FileNotFoundError):
            raise CAIFError(
                f"Data Source Error: File or URL not found.",
                advice=f"Check the path/URL for '{source}'. Make sure the file exists and the URL is correct."
            )
        elif "Unsupported tabular type" in str(error):
            raise CAIFError(
                f"Data Type Error: The type '{file_type}' is not supported for tabular processing.",
                advice="Ensure the file type matches the content (e.g., don't use 'csv' for a '.zip' file)."
            )
        elif "target value" in str(error):
             raise CAIFError(
                f"Data Target Error: The target column was missing or empty.",
                advice="Check your data file to ensure the column you want to predict ('target_column') has values in it."
            )
        else:
            # Catch-all for other unexpected data issues
            raise CAIFError(
                f"General Data Error: Could not process data source. Details: {error}",
                advice="Review the full error details and check if your file is corrupted or incorrectly formatted."
            )

    @staticmethod
    def handle_model_error(error: Exception):
        """Handles errors specifically during the CAIF.MODEL() command."""
        
        if "cannot convert string to float" in str(error):
            raise CAIFError(
                "Model Data Mismatch: Text found where numbers were expected.",
                advice="Make sure your data is clean. Non-numerical data (like text) cannot be used in numerical columns for training."
            )
        elif "Input X contains NaN" in str(error):
            raise CAIFError(
                "Model Input Error: Missing values (NaN) found in features.",
                advice="Your input data has missing values. Try cleaning your data or using a data pre-processing step before CAIF.DATA()."
            )
        else:
            raise CAIFError(
                f"General Model Error: Training failed. Details: {error}",
                advice="Try reducing the complexity level or increasing the 'time_limit'."
            )
            
    @staticmethod
    def check_model_performance(score, target_type, threshold=0.6):
        """Checks if the AI learned correctly and warns the user if accuracy is too low."""
        if target_type == 'classification':
            if score < threshold:
                print(f"\n[CAIF WARNING] 🚨 Low Accuracy Alert! The model's test accuracy ({score:.2f}) is very low.")
                print("  [CAIF WARNING] Advice: This AI may not be very good! Get more training data or increase the complexity.")
                return False
        # (Similar logic would be added for checking regression error thresholds)
        return True

# Create a single instance for easy access
CAIF_ERROR_HANDLER = _ErrorHandler()

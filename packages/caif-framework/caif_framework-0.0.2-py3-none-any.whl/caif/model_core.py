import numpy as np
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error

# IMPORTANT: Import the Error Handler to be used in training and evaluation
from .error_handler import CAIFError, _ErrorHandler

# --- Internal Utility Functions for Neural Network Sketching ---

def _sketch_neural_network(X_shape, complexity):
    """
    CAIF's intelligent function to design the network architecture.
    It determines the number of neurons and layers based on the data size
    and the user's requested complexity (1-10).
    """
    if X_shape[0] == 0 or X_shape[1] == 0:
        raise ValueError("Cannot sketch network; input data X is empty.")
        
    num_features = X_shape[1]
    
    # 1. Base Layer Size: The first hidden layer is typically related to the number of features.
    base_neurons = num_features * 2
    
    # 2. Complexity Adjustment: Scale the network size based on the 1-10 complexity rating.
    scale_factor = complexity / 10.0
    
    # Determine the number of hidden layers (1-3 layers based on complexity)
    num_layers = 1
    if complexity >= 4:
        num_layers = 2
    if complexity >= 8:
        num_layers = 3
        
    # Determine the size of each hidden layer
    hidden_layer_sizes = []
    for i in range(num_layers):
        size = int(base_neurons * (1.5 * scale_factor) * (1 - 0.2 * i))
        hidden_layer_sizes.append(max(8, size))
        
    print(f"  [MC] Network Sketch: {num_layers} hidden layers.")
    print(f"  [MC] Neuron count per layer: {hidden_layer_sizes}")
    
    return tuple(hidden_layer_sizes)

# --- The Main Internal ModelCore Class ---

class _ModelCore:
    """
    Internal class managing model creation, training, and intelligent 
    Neural Network sketching for the CAIF framework.
    """
    
    def __init__(self):
        # Attributes to store the data passed from CAIF.DATA()
        self.X_data = None
        self.Y_data = None
        
        self.trained_model = None
        self.model_type_tag = None
        self.model_target_type = None # 'regression' or 'classification'

    def set_data(self, X, Y):
        """Stores the processed embeddings (X) and targets (Y) for later use by CAIF.MODEL()."""
        self.X_data = X
        self.Y_data = Y
        print("  [MC] Data successfully stored for training.")

    def train_model(self, X, Y, type_tag: str, complexity: int, time_limit: str):
        """
        The core logic for CAIF.MODEL(). Sets up and trains the AI.
        """
        if X is None or Y is None:
            raise CAIFError(
                "Training Data Missing: Cannot run CAIF.MODEL().",
                advice="Run CAIF.DATA(...) first to load and process your training data."
            )
            
        print(f"  [MC] Starting CAIF Model Training...")
        
        # 1. Determine Model Type (Target Type)
        # Check if the target (Y) is primarily continuous (regression) or discrete (classification)
        if np.issubdtype(Y.dtype, np.number) and len(np.unique(Y)) > max(20, len(Y) * 0.1):
            self.model_target_type = 'regression'
            print("  [MC] Target is numerical prediction (Regression).")
        else:
            self.model_target_type = 'classification'
            print("  [MC] Target is category prediction (Classification).")

        # 2. Sketch the Neural Network Architecture
        hidden_layer_sizes = _sketch_neural_network(X.shape, complexity)
        
        # 3. Split Data for Testing (80% Train, 20% Test)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

        # 4. Create the Model based on target type
        if self.model_target_type == 'regression':
            model = MLPRegressor(hidden_layer_sizes=hidden_layer_sizes, max_iter=500, verbose=False)
        else:
            model = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes, max_iter=500, verbose=False)

        # 5. Train the Model! (The AI learning process)
        print(f"  [MC] Training model for up to {time_limit}...")
        try:
            model.fit(X_train, Y_train)
        except Exception as e:
            # Use the Error Handler for graceful failure during training
            _ErrorHandler.handle_model_error(e) 

        # 6. Evaluate Performance
        Y_pred = model.predict(X_test)
        
        if self.model_target_type == 'classification':
            score = accuracy_score(Y_test, Y_pred)
            print(f"  [MC] Training complete! Test Accuracy: {score:.2f}")
        else:
            score = mean_squared_error(Y_test, Y_pred)
            print(f"  [MC] Training complete! Test Error (MSE): {score:.2f}")

        # NEW: Check if the score is bad and issue a user-friendly warning
        _ErrorHandler.check_model_performance(score, self.model_target_type) 

        # Save the results
        self.trained_model = model
        self.model_type_tag = type_tag
        
        return self.trained_model, score

# Note: The global instance creation (CAIF_MODEL_CORE = _ModelCore()) is now handled in __init__.py.

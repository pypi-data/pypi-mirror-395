import numpy as np
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error

# --- Internal Utility Functions for Neural Network Sketching ---

def _sketch_neural_network(X_shape, complexity):
    """
    CAIF's intelligent function to design the network architecture.
    It determines the number of neurons and layers based on the data size
    and the user's requested complexity (1-10).
    """
    num_features = X_shape[1]
    
    # 1. Base Layer Size: The first hidden layer is typically related to the number of features.
    base_neurons = num_features * 2
    
    # 2. Complexity Adjustment: Scale the network size based on the 1-10 complexity rating.
    # Higher complexity = more neurons and more layers.
    scale_factor = complexity / 10.0
    
    # Determine the number of hidden layers (Complexity 1-3: 1 layer; 4-7: 2 layers; 8-10: 3 layers)
    num_layers = 1
    if complexity >= 4:
        num_layers = 2
    if complexity >= 8:
        num_layers = 3
        
    # Determine the size of each hidden layer
    # The layers decrease in size to funnel information towards the output
    hidden_layer_sizes = []
    for i in range(num_layers):
        # The size is the base size, scaled by complexity and layer depth
        size = int(base_neurons * (1.5 * scale_factor) * (1 - 0.2 * i))
        # Ensure the size is at least a minimum value (e.g., 8 neurons)
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
        # A dictionary to store the currently trained model and its tag
        self.trained_model = None
        self.model_type_tag = None
        self.model_target_type = None # 'regression' (number) or 'classification' (category)

    def train_model(self, X, Y, type_tag: str, complexity: int, time_limit: str):
        """
        The core logic for CAIF.MODEL(). Sets up and trains the AI.
        X: The features (input numbers/embeddings); Y: The targets (output numbers/categories).
        """
        if X is None or Y is None:
            raise ValueError("Training data (X and Y) must be provided by CAIF.DATA() before training.")
            
        print(f"  [MC] Starting CAIF Model Training...")
        
        # 1. Determine Model Type (Target Type)
        # If the target (Y) is a list of numbers (floats/many unique integers), it's Regression.
        # If the target (Y) is categories (strings/few unique integers), it's Classification.
        if np.issubdtype(Y.dtype, np.number) and len(np.unique(Y)) > 20:
            self.model_target_type = 'regression'
            print("  [MC] Target is numerical prediction (Regression).")
        else:
            self.model_target_type = 'classification'
            print("  [MC] Target is category prediction (Classification).")

        # 2. Sketch the Neural Network Architecture
        hidden_layer_sizes = _sketch_neural_network(X.shape, complexity)
        
        # 3. Split Data for Testing (A key step for checking performance)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

        # 4. Create the Model based on target type
        if self.model_target_type == 'regression':
            # Uses a Multi-Layer Perceptron (Neural Network) for number prediction
            model = MLPRegressor(
                hidden_layer_sizes=hidden_layer_sizes,
                max_iter=500, # A standard number of training runs
                verbose=False
            )
        else: # Classification
            # Uses a Multi-Layer Perceptron (Neural Network) for category prediction
            model = MLPClassifier(
                hidden_layer_sizes=hidden_layer_sizes,
                max_iter=500,
                verbose=False
            )

        # 5. Train the Model! (The AI learning process)
        print(f"  [MC] Training model for up to {time_limit}...")
        model.fit(X_train, Y_train)
        
        # 6. Evaluate Performance (Checking if the AI learned correctly)
        Y_pred = model.predict(X_test)
        
        if self.model_target_type == 'classification':
            score = accuracy_score(Y_test, Y_pred)
            print(f"  [MC] Training complete! Test Accuracy: {score:.2f}")
        else:
            score = mean_squared_error(Y_test, Y_pred)
            print(f"  [MC] Training complete! Test Error (MSE): {score:.2f}")

        # Save the results to the internal class state
        self.trained_model = model
        self.model_type_tag = type_tag
        
        # In a real framework, we would also enforce the time_limit here by stopping the training early!

        return self.trained_model, score

# We also need to create a single instance of the Model Core to manage the state
# (which model is currently trained).
CAIF_MODEL_CORE = _ModelCore()

import pandas as pd
import numpy as np
from PIL import Image
import os
import zipfile
import io
import json
import yaml
import requests # For handling URL sources

# --- Internal Utility Functions (The 'magic' CAIF does behind the scenes) ---

def _load_data_from_source(source, is_url):
    """Handles loading data from either a local path or a URL."""
    if is_url:
        print(f"  [DH] Fetching data from URL: {source}...")
        try:
            response = requests.get(source)
            response.raise_for_status() # Raise an error for bad status codes
            return io.BytesIO(response.content)
        except requests.exceptions.RequestException as e:
            raise FileNotFoundError(f"Error fetching data from URL: {e}")
    else:
        print(f"  [DH] Reading local file: {source}...")
        return source

def _process_tabular_data(data_source, file_type, target_column):
    """Processes CSV, EXCEL, JSON, JSONL, YAML data into a DataFrame."""
    try:
        if file_type == 'csv':
            data = pd.read_csv(data_source)
        elif file_type == 'excel':
            data = pd.read_excel(data_source)
        elif file_type in ['json', 'jsonl']:
            # For JSON/JSONL, we read line by line or use pandas read_json
            if isinstance(data_source, io.BytesIO):
                data = pd.read_json(data_source, lines=(file_type == 'jsonl'))
            else:
                data = pd.read_json(data_source, lines=(file_type == 'jsonl'))
        elif file_type == 'yaml':
            if isinstance(data_source, io.BytesIO):
                yaml_content = data_source.read().decode('utf-8')
            else:
                with open(data_source, 'r') as f:
                    yaml_content = f.read()
            # YAML is complex; we assume a list of dictionaries for pandas conversion
            data_list = yaml.safe_load(yaml_content)
            data = pd.DataFrame(data_list)
        else:
            raise ValueError(f"Unsupported tabular type: {file_type}")

        # Basic data cleaning: handling missing values (A necessary part of CAIF)
        print("  [DH] Cleaning data: Dropping rows with missing target value...")
        data = data.dropna(subset=[target_column])
        
        # We don't convert to numbers here yet; we just return the clean table
        return data

    except Exception as e:
        raise RuntimeError(f"Data processing failed for {file_type}: {e}")

# --- The Main Internal DataHandler Class ---

class _DataHandler:
    """
    Internal class managing all data loading, cleaning, and preparation 
    for the CAIF framework.
    """
    
    @staticmethod
    def load_and_embed(source: str, type_str: str, target_column: str = None):
        """
        The core function for CAIF.DATA(). Handles all file types and outputs 
        the final "special numbers" for training.
        """
        is_url = source.lower().startswith('http')
        # Split type string for containers (zip) and content (images)
        file_types = [t.strip().lower() for t in type_str.split(',')]
        main_type = file_types[-1] # The content type is usually the last one

        # Step 1: Load the source content
        loaded_content = _load_data_from_source(source, is_url)

        # Step 2: Handle ZIP/Container Files
        if 'zip' in file_types:
            print("  [DH] Container detected: ZIP. Extracting contents...")
            with zipfile.ZipFile(loaded_content) as zf:
                # Assuming the content is images if not specified otherwise
                content_type = main_type if main_type != 'zip' else 'images' 
                
                all_embeddings = []
                all_targets = []
                
                # Iterate through all files in the ZIP
                for file_name in zf.namelist():
                    if file_name.lower().endswith(('.jpg', '.png', '.webp')):
                        with zf.open(file_name) as f:
                            # This is where the image processing (e.g., resizing, converting to numpy array) happens
                            img = Image.open(f).resize((32, 32)) # Standard size for fast AI
                            embedding = np.array(img).flatten() / 255.0 # Normalize to numbers 0-1
                            all_embeddings.append(embedding)
                            
                            # Simple target assumption: use the directory name or file start as a label
                            label = file_name.split(os.sep)[-2] 
                            all_targets.append(label)
                            
                print(f"  [DH] Extracted and embedded {len(all_embeddings)} {content_type}.")
                # In a real project, this is where audio (MP3/WAV/MP4) processing would also occur

            # We return a placeholder for the embeddings (X) and targets (Y)
            return np.array(all_embeddings), np.array(all_targets)

        # Step 3: Handle Tabular Data (CSV, EXCEL, JSON, YAML)
        elif main_type in ['csv', 'excel', 'json', 'jsonl', 'yaml']:
            data_table = _process_tabular_data(loaded_content, main_type, target_column)
            
            # Feature columns (X) are all columns except the target
            X = data_table.drop(columns=[target_column]).values
            # Target column (Y) is what we want to predict
            Y = data_table[target_column].values

            # Scale/Normalize numerical features (a key part of 'Special Numbers')
            from sklearn.preprocessing import StandardScaler
            X_scaled = StandardScaler().fit_transform(X)
            
            print(f"  [DH] Tabular data processed. Features (X) shape: {X_scaled.shape}")
            return X_scaled, Y

        # Step 4: Handle Single Image/Text Files
        elif main_type in ['jpg', 'png', 'webp', 'svg']:
            # For a single file, CAIF would convert it and assume a prediction request 
            # or add it to a batch if the context suggests training.
            print("  [DH] Single file processing initiated...")
            # (Detailed single-file processing code omitted for brevity)
            pass

        else:
            raise NotImplementedError(f"CAIF Error: Native support for '{type_str}' is defined but the processor is not yet written.")


# --- Linking back to the main CAIF class (Example of what is needed) ---
# Note: In a real project, the CAIF.DATA function in __init__.py would be updated 
# to call this specific function:
#
#    @staticmethod
#    def DATA(source, type, target_column=None):
#        X, Y = _DataHandler.load_and_embed(source, type, target_column)
#        # CAIF would store X and Y internally for the MODEL command
#        return True

#TODO: let us find a name that does not conflict with the json module of python
import json 
import numpy as np

#%% packing of input parameters
def pack(model,name):

    def convert_np_arrays(obj):
        if isinstance(obj, dict):
            return {k: convert_np_arrays(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_np_arrays(i) for i in obj]
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.integer) or isinstance(obj, np.unsignedinteger):
            return int(obj)        
        elif isinstance(obj, np.floating):
            return float(obj)                
        else:
            return obj

    # Convert np.array objects to lists
    model_serialized = convert_np_arrays(model)

    # Save the cantilever_beam_model to a JSON file
    with open(name + '.json', 'w') as fid:
        json.dump(model_serialized, fid)

#%% unpacking of input parameters
def unpack(json_file):

    # Load the cantilever_beam_model from the JSON file
    with open(json_file + '.json', 'r') as fid:
        model = json.load(fid)

    # Convert lists to numpy arrays in the nested dictionaries
    for pars in model.keys():
        if isinstance(model[pars], list) and len(model[pars]) > 0 and isinstance(model[pars][0], dict):
            # Handle list of dictionaries
            for item in model[pars]:
                for key, value in item.items():
                    if isinstance(value, list):
                        item[key] = np.array(value)
        else: # isinstance(model[pars], dict):
            # Handle dictionary
            for key, value in model[pars].items():
                if isinstance(value, list):
                    model[pars][key] = np.array(value)
    
    return model
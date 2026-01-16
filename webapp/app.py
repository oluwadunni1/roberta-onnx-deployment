from flask import Flask, request, jsonify
import numpy as np
from transformers import RobertaTokenizer
import onnxruntime

app = Flask(__name__)
tokenizer = RobertaTokenizer.from_pretrained("roberta-base")
session = onnxruntime.InferenceSession("roberta-sequence-classification-9.onnx")

@app.route("/predict", methods=["POST"])
def predict():
    # 1. Tokenize the input text (Returns a list of integers)
    input_text = request.json[0]
    encoded_input = tokenizer.encode(input_text, add_special_tokens=True)
    
    # 2. Convert to NumPy Array
    # We create a list containing the encoded input to add the batch dimension (Batch Size = 1)
    # Equivalent to torch.unsqueeze(0)
    input_ids = np.array([encoded_input], dtype=np.int64)
        
    # 3. Run Inference
    inputs = {session.get_inputs()[0].name: input_ids}
    out = session.run(None, inputs)
    
    # 4. Process Output
    result = np.argmax(out)
    return jsonify({"positive": bool(result)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
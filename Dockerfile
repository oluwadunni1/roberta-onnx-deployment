# Use the lightweight Python image
FROM python:3.9-slim

# Copy requirements
COPY ./requirements.txt /webapp/requirements.txt
WORKDIR /webapp

# Install dependencies (No special Torch handling needed!)
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY webapp/* /webapp

# Copy the model file
COPY roberta-sequence-classification-9.onnx /webapp/

# Start the app
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
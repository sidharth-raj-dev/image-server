from flask import Flask, send_file, request, abort
from flask_cors import CORS
from PIL import Image
import io
import os

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# Create images directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/images/<path:filename>')
def serve_image(filename):
    """
    Serve an image file from the images directory with its original dimensions.
    This endpoint maintains the original quality and size of the image.
    """
    try:
        # Construct the full file path
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        # Verify the file exists and is actually an image
        if not os.path.exists(file_path):
            abort(404, description="Image not found")
        
        if not allowed_file(filename):
            abort(400, description="Invalid file type")
            
        # Serve the file with appropriate mimetype
        return send_file(
            file_path,
            # Let Flask determine the correct mimetype based on the file extension
            as_attachment=False
        )

    except Exception as e:
        app.logger.error(f"Error serving image {filename}: {str(e)}")
        abort(500, description=f"Error serving image: {str(e)}")

@app.route('/api/upload', methods=['POST'])
def upload_image():
    """
    Handle image uploads. This is useful for testing the server
    with new images.
    """
    if 'file' not in request.files:
        abort(400, description="No file part")
        
    file = request.files['file']
    if file.filename == '':
        abort(400, description="No selected file")
        
    if file and allowed_file(file.filename):
        # Securely save the file
        filename = os.path.basename(file.filename)  # Get just the filename part
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        return {"message": "File uploaded successfully", "path": f"/api/images/{filename}"}, 200
    
    return {"error": "Invalid file type"}, 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
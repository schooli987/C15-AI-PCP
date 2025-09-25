from flask import Flask, request, render_template
from PIL import Image
import pytesseract

app = Flask(__name__)

# Configure Tesseract path (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Global variable for cumulative total
cumulative_total = 0.0

@app.route("/", methods=["GET", "POST"])
def index():
    global cumulative_total
    extracted_text = ""
    current_total = 0.0

    if request.method == "POST":
        file = request.files.get("image")
        if file:
            filepath = file.filename
            file.save(filepath)

            # OCR
            image = Image.open(filepath)
            extracted_text = pytesseract.image_to_string(image)

            
            lines = extracted_text.lower().splitlines()
            current_total = 0.0

            for line in lines:
                if "total" in line and "subtotal" not in line:
                
                    number_str = ""
                    for ch in line:
                        if ch.isnumeric() or ch == '.':
                            number_str += ch
                        elif number_str:
                            break
                    if number_str:
                        current_total = float(number_str)
                        cumulative_total += current_total
                        break  

    return render_template(
        "index.html",
        extracted_text=extracted_text,
        current_total=current_total,
        cumulative_total=cumulative_total
    )


if __name__ == "__main__":
    app.run(debug=True)

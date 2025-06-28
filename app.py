from flask import Flask, render_template, request
import random
import string

app = Flask(__name__)

def generate_password(length, use_lower, use_upper, use_digits, use_special):
    characters = ""
    if use_lower:
        characters += string.ascii_lowercase
    if use_upper:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation

    if not characters:
        return "Select at least one character type."
    
    return ''.join(random.choice(characters) for _ in range(length))
def check_strength(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1

    labels = ["Very Weak", "Weak", "Medium", "Strong", "Very Strong"]
    colors = ["#dc3545", "#fd7e14", "#ffc107", "#0d6efd", "#28a745"]

    if score == 0:
        return "", ""
    return labels[score - 1], colors[score - 1]


@app.route('/', methods=['GET', 'POST'])
def index():
    password = ""
    strength_label = ""
    strength_color = ""
    checkbox_states = {
        "use_lower": False,
        "use_upper": False,
        "use_digits": False,
        "use_special": False
    }

    if request.method == 'POST':
        length = int(request.form.get('length'))
        checkbox_states["use_lower"] = 'lowercase' in request.form
        checkbox_states["use_upper"] = 'uppercase' in request.form
        checkbox_states["use_digits"] = 'digits' in request.form
        checkbox_states["use_special"] = 'special' in request.form

        password = generate_password(
            length,
            checkbox_states["use_lower"],
            checkbox_states["use_upper"],
            checkbox_states["use_digits"],
            checkbox_states["use_special"]
        )
        if "Select at least one" not in password:
            strength_label, strength_color = check_strength(password)
        else:
            strength_label, strength_color = "", ""
            strength_label, strength_color = check_strength(password)

    return render_template('index.html', password=password, strength_label=strength_label, strength_color=strength_color, **checkbox_states)


if __name__ == '__main__':
    app.run(debug=True)
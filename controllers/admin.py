from flask import render_template
from flask_login import current_user, login_required
from controllers import app

@app.route("/admin")
@login_required
def admin():
    if current_user.is_admin:
        return render_template("admin.html")
    else:
        return {"message":"unauthorized"}, 401
from app import app
from app.routes import routes

@app.route('/')
@app.route('/health')
def hello():
    return "Life is Good, Health is Good !"

@app.route("/liveness_probe")
def liveness_probe():
    # Do readiness and hardness dependency
    # checks here.
    return "Liveness probe"


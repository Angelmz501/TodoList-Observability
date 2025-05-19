from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_sqlalchemy import SQLAlchemy
import os
import time

# Prometheus client
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# OpenTelemetry
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.wsgi import OpenTelemetryMiddleware
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# Recursos OTEL
resource = Resource(attributes={"service.name": "todo-list-app"})

# Configurar trazas
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)
otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4318/v1/traces")
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))

# Flask App
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "dev"

# Instrumentación OTEL y middleware
app.wsgi_app = OpenTelemetryMiddleware(app.wsgi_app)
FlaskInstrumentor().instrument_app(app)

# Instrumentación Prometheus
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Número total de peticiones HTTP",
    ["method", "endpoint", "http_status"]
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "Duración de las peticiones HTTP",
    ["method", "endpoint"]
)

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def record_metrics(response):
    if hasattr(request, "start_time"):
        latency = time.time() - request.start_time
        REQUEST_LATENCY.labels(request.method, request.path).observe(latency)
        REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()
    return response

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

# Base de datos
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(1000), nullable=False)
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)

# Rutas
@app.route('/')
def index():
    todoList = Todo.query.all()
    return render_template('base.html', todo_list=todoList)

@app.route('/add', methods=["POST"])
def add():
    title = request.form.get("title")
    if title == "":
        flash("La tarea no puede estar vacía.")
        return redirect(url_for("index"))

    newTask = Todo(task=title, complete=False)
    try:
        db.session.add(newTask)
        db.session.commit()
        return redirect(url_for("index"))
    except:
        return "There was an issue adding your task."

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    task = Todo.query.filter_by(id=todo_id).first()
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for("index"))
    except:
        return "There was an issue deleting your task."

@app.route('/update/<int:todo_id>')
def update(todo_id):
    task = Todo.query.filter_by(id=todo_id).first()
    task.complete = not task.complete
    try:
        db.session.commit()
        return redirect(url_for("index"))
    except:
        return "There was an issue updating your task."

# Main
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

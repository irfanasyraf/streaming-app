cat > app.py <<'EOF'
import json
import random
import time
from datetime import datetime, timezone
from flask import Flask, Response, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/health")
def health():
    return {"status": "ok"}, 200

@app.route("/stream")
def stream():
    def generate():
        while True:
            data = {
                "timestamp": datetime.now(
                    timezone.utc
                ).isoformat(),
                "temperature": round(
                    random.uniform(22, 35), 2
                ),
                "cpu": round(
                    random.uniform(10, 90), 2
                ),
                "memory": round(
                    random.uniform(30, 80), 2
                )
            }

            yield f"data: {json.dumps(data)}\n\n"
            time.sleep(1)

    return Response(
        generate(),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        }
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
EOF

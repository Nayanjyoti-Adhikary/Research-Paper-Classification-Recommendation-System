const express = require("express");
const cors = require("cors");
const { spawn } = require("child_process");
const path = require("path");

const app = express();

app.use(cors());
app.use(express.json());

app.post("/predict", (req, res) => {
    const text = req.body.text;

    if (!text) {
        return res.status(400).json({ error: "No input text provided" });
    }

    // Absolute path to Python script
    const scriptPath = path.join(__dirname, "../ml/predict.py");

    console.log("Running script:", scriptPath);
    console.log("Input text:", text);

    // ⚠️ IMPORTANT: Use your full Python path
    const py = spawn(
        "C:\\Users\\nayan\\AppData\\Local\\Programs\\Python\\Python313\\python.exe",
        [scriptPath]
    );

    let result = "";

    // Send input to Python via stdin
    py.stdin.write(JSON.stringify({ text }));
    py.stdin.end();

    // Capture output
    py.stdout.on("data", (data) => {
        console.log("Python output:", data.toString());
        result += data.toString();
    });

    // Capture errors
    py.stderr.on("data", (data) => {
        console.error("Python error:", data.toString());
    });

    py.on("error", (err) => {
        console.error("Failed to start Python process:", err);
        res.status(500).json({ error: "Python process failed to start" });
    });

    py.on("close", () => {
        try {
            // Extract JSON from output (safe parsing)
            const jsonStart = result.indexOf("{");
            const jsonString = result.slice(jsonStart);

            const parsed = JSON.parse(jsonString);

            res.json(parsed);
        } catch (err) {
            console.error("Parsing error:", result);
            res.json({ error: "Parsing error", raw: result });
        }
    });
});

app.listen(5000, () => {
    console.log("Server running on port 5000");
});
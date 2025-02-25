const express = require("express");
const multer = require("multer");
const axios = require("axios");
const cors = require("cors");
const { spawn } = require("child_process");
const path = require("path");
const fs = require("fs");

const app = express();
const PORT = 5000;

// Enable CORS
app.use(cors());
app.use(express.json());

// Set up file upload using Multer
const upload = multer({ dest: "uploads/" });

// Upload endpoint
app.post("/upload", upload.single("file"), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: "No file uploaded" });
    }

    const filePath = path.join(__dirname, req.file.path);

    // Call Python script
    const pythonProcess = spawn("python", ["index.py", filePath]);

    let output = "";
    pythonProcess.stdout.on("data", (data) => {
        output += data.toString();
    });

    pythonProcess.stderr.on("data", (data) => {
        console.error(Python Error: ${data});
    });

    pythonProcess.on("close", (code) => {
        fs.unlinkSync(filePath); // Delete file after processing
        try {
            const result = JSON.parse(output);
            res.json(result);
        } catch (error) {
            res.status(500).json({ error: "Error processing file" });
        }
    });
});

// Start the server
app.listen(PORT, () => {
    console.log(Server running on http://localhost:${PORT});
});
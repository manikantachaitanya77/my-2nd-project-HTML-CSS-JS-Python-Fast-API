from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from typing import Dict
import os
import yt_dlp

app = FastAPI()

# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Serve HTML Form
@app.get("/", response_class=HTMLResponse)
def get_form():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Chaitanya's Page</title>
      <style>
        body {
          font-family: Arial, sans-serif;
          margin: 0;
          padding: 0;
          height: 100vh;
          display: flex;
          flex-direction: column;
          justify-content: center;
          background: linear-gradient(to bottom, #87CEEB, #FFB6C1); /* Sky Blue and Baby Pink */
        }

        h1 {
          text-align: center;
          color: #ffffff;
          margin-bottom: 20px;
          font-size: 36px;
        }

        .content-container {
          width: 50%; /* Half the screen width */
          margin: 0 auto;
          padding: 20px;
          background-color: #ffffff;
          border-radius: 8px;
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
          text-align: center;
        }

        .content-container form {
          background: #ffffff;
          padding: 20px;
          margin: 15px 0;
          border-radius: 8px;
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .content-container label {
          display: block;
          margin-bottom: 8px;
          font-weight: bold;
        }

        .content-container input {
          width: 100%;
          padding: 10px;
          margin-bottom: 15px;
          border: 1px solid #ccc;
          border-radius: 4px;
        }

        .content-container button {
          width: 100%;
          background-color: #FF0000; /* Red button */
          color: white;
          padding: 10px;
          border: none;
          border-radius: 4px;
          cursor: pointer;
          font-size: 16px;
        }

        .content-container button:hover {
          background-color: #D10000; /* Darker red when hovered */
        }

        hr {
          border: 0;
          border-top: 1px solid #ccc;
          margin: 30px 0;
        }

        @media (max-width: 768px) {
          .content-container {
            width: 90%;
          }
        }
      </style>
    </head>
    <body>
      <h1>Chaitanya's Page</h1>
      <div class="content-container">
        <form id="downloadForm">
          <label for="link">YouTube Link:</label>
          <input type="text" id="link" name="link" required>
          <br>
          <label for="id">Filename:</label>
          <input type="text" id="id" name="id" required>
          <br>
          <button type="submit">Download Video</button>
        </form>
        <hr>
      </div>

      <script>
        document.getElementById("downloadForm").addEventListener("submit", async function(event) {
          event.preventDefault(); // Prevent the default form submission
          const formData = new FormData(event.target);
          const response = await fetch('/download', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                link: formData.get("link"),
                id: formData.get("id")
              })
          });
          const result = await response.json();
          alert(result.message);
        });
      </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


# API to download video
@app.post("/download")
def download_video(request: Dict[str, str]):
    link = request.get("link")
    video_id = request.get("id")
    current_dir = os.getcwd()
    video_path = os.path.join(current_dir, f"{video_id}.mp4")

    youtube_dl_options = {
        "format": "best",
        "outtmpl": video_path
    }
    try:
        with yt_dlp.YoutubeDL(youtube_dl_options) as ydl:
            ydl.download([link])
        return {"message": f"Video downloaded successfully as {video_id}.mp4"}
    except Exception as e:
        return {"message": f"Error downloading video: {str(e)}"}

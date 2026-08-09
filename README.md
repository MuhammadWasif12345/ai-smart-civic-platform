# AI Smart Civic Services

## Problem Statement
Citizens often struggle to report local issues (like broken streetlights or overflowing garbage) effectively, and city administrations struggle to triage and assign the influx of raw, unstructured complaints. This leads to slow resolution times and frustrated citizens. 

This project solves this by using AI to automatically read, categorize, prioritize, and summarize citizen complaints the moment they are submitted, routing them to the correct department while providing the administration with a powerful statistical dashboard to track resolution performance.

## Features
* **AI-Powered Triage:** Automatic classification (Road, Water, Electricity, etc.) and urgency prediction (Low, Medium, High, Critical).
* **Citizen Portal:** A public-facing web app to submit complaints and track their progress via a unique ID.
* **Admin Dashboard:** A secure, JWT-authenticated portal for city staff to view, filter, assign, and resolve complaints.
* **Batch 4 Statistics Engine:** Advanced analytics calculating mean, median, mode, standard deviation, and IQR for complaint resolution times, complete with plain-English interpretations.
* **Fully Responsive UI:** Built from scratch using modern design tokens (no heavy frameworks).

## AI Technology Used — which AI, why it was chosen, and its limitations
This project supports two AI pathways (toggleable via `.env`):
1. **Google Gemini API (Default/Production):** Uses `gemini-1.5-flash`. Chosen for its generous free tier, speed, and native ability to return strict, parsable JSON. 
2. **Local Hugging Face Models (Fallback):** Uses `valhalla/distilbart-mnli-12-3` for zero-shot classification, rule-based urgency heuristics, and `sumy` (LexRank) for summarization. Chosen to fulfill offline/explainability requirements.

**Limitations:** The AI is not 100% accurate. Ambiguous slang, extremely short descriptions, or complaints covering multiple issues (e.g., "A truck hit a pole and water is leaking") can lead to incorrect categorization or priority. It serves to augment, not replace, human review.

## Architecture Diagram
Please view the full diagram and explanation here: [ARCHITECTURE.md](ARCHITECTURE.md)

## Tech Stack
* **Backend:** Python, FastAPI
* **Database:** SQLite (local dev), PostgreSQL (Render production), SQLAlchemy (ORM)
* **AI:** Google Generative AI SDK, Hugging Face `transformers`, `sumy`
* **Analytics:** `pandas`, `numpy`, `statistics`
* **Frontend:** Vanilla HTML5, CSS3, JavaScript
* **Charts:** Chart.js

## Folder Structure
```
ai-smart-civic-services/
├── backend/
│   ├── main.py
│   ├── database.py, models.py, schemas.py
│   ├── services/ (ai, complaint, stats, auth, notifications)
│   ├── routers/ (complaints, admin, analytics, auth)
│   └── tests/
├── frontend/
│   ├── css/ (variables, base, components, dashboard)
│   ├── js/ (api, track, submit, dashboard)
│   └── *.html (views)
├── render.yaml
└── README.md
```

## Setup & Installation
Follow these steps to run the project locally.

1. **Clone the repository:**
   `git clone <repository-url>`
   *(Downloads the code to your computer)*
2. **Navigate into the project folder:**
   `cd ai-smart-civic-services`
3. **Create a Python virtual environment:**
   `python -m venv venv`
   *(Creates an isolated environment for dependencies)*
4. **Activate the virtual environment:**
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
5. **Install the required packages:**
   `pip install -r backend/requirements.txt`
   *(Installs FastAPI, Pandas, SQLAlchemy, etc.)*

## Environment Variables
1. Copy the example file to create a real one:
   `cp backend/.env.example backend/.env`
2. Open `backend/.env` and add your Google Gemini API key:
   `LLM_API_KEY=your_key_here`
   *(Get your free key at aistudio.google.com)*

## Running Locally
1. **Start the FastAPI server:**
   `uvicorn backend.main:app --reload`
   *(Starts the server on http://127.0.0.1:8000)*
2. **Access the frontend:**
   Open a browser and go to `http://127.0.0.1:8000/`.
3. **Admin Login:**
   Navigate to the Admin Login page and use username: `admin`, password: `admin123`.

## API Documentation
Once the server is running, you can view the auto-generated interactive API documentation (Swagger UI) at:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Deployment
This project is configured for one-click deployment on Render.com using the free tier.

1. Push your code to GitHub.
2. In the Render Dashboard, click **New > Blueprint**.
3. Connect your repository. Render will read `render.yaml` and automatically provision both a free Web Service and a free PostgreSQL Database, linking them together automatically.
4. Once created, go to the Web Service settings in Render and add your `LLM_API_KEY` to the environment variables.

**Cold-start note:** On Render's free tier, the server spins down after 15 minutes of inactivity. The very first request after this idle period may take 30-60 seconds to wake up. The frontend UI accounts for this by displaying a friendly loading overlay.

## AI Testing Evidence
Below is a sample of our AI's performance against test complaints:

| Complaint Text | Expected Category & Priority | Actual AI Result |
|---|---|---|
| "There is a large water leak near the main road and traffic is becoming difficult." | Water/Drainage (High/Critical) | Water/Drainage, High |
| "Streetlight on Block C has been off for two weeks, it's very dark at night and feels unsafe." | Electricity (Medium/High) | Electricity, Medium |
| "Garbage bin outside the mosque has been overflowing for 3 days, smell is unbearable." | Waste/Garbage (Medium) | Waste/Garbage, Medium |
| "Pothole on the main road near the school is getting bigger, a bike almost fell yesterday." | Road (High) | Road, High |
| "Electricity pole near the park is leaning after the storm, looks like it could fall." | Electricity (Critical) | Electricity, Critical |
| "General feedback: the new park benches are a nice addition, thank you." | Other (Low) | Other, Low |

*Note: The AI successfully filters non-complaints (like the park bench feedback) into the "Other" category with "Low" priority.*

## Screenshots
*(To be added after deployment: Place screenshots of the Citizen Submission flow and the Admin Statistics Dashboard here)*

## Statistics/Analytics Explanation
This project fulfills the Batch 4 requirements by utilizing `pandas` and `numpy` to calculate:
- **Central Tendency:** Identifies the Mean, Median, and Mode of complaint resolution times (in hours).
- **Spread:** Calculates Variance and Standard Deviation to understand how consistently the team performs.
- **Quartiles/IQR:** Determines the 25th (Q1) and 75th (Q3) percentiles to find the middle 50% of resolution times, effectively identifying outliers.
- **Interpretation:** The AI provides a plain-English explanation of these metrics directly on the dashboard, making complex stats understandable to city officials.

## Known Limitations
- The Render Free Postgres database expires after ~30-90 days. For long-term production, a paid database plan is required.
- Image uploads are currently supported structurally in the database (`image_path`), but local storage is wiped on Render redeployments. Cloud storage (like AWS S3) would be needed for persistent images.

## Future Improvements
- Add email/SMS notifications for citizens when their complaint status changes.
- Implement a drag-and-drop Kanban board for the Admin Complaints view.
- Add map integration (Google Maps/Mapbox) to pinpoint complaint locations geographically.

## Team / Credits
- **Muhammad Wasif** - Solo Developer (Batch 4 - Statistics)

# Stonebranch UAC – Task Viewer (Technical Exercise)

This project is my completed solution for the Stonebranch Solution Engineer Technical Assessment.

The requirement was to connect to the **Stonebranch Universal Automation Center (UAC)**, retrieve tasks using the UAC REST API, extract specific information, and present the output in a simple UI. My implementation follows a clean backend–frontend separation, uses secure practices, and applies object-oriented design principles.

---

# 📌 1. Assessment Requirements

The exercise asked me to:

### ✔ Call the UAC API using Python  
### ✔ Retrieve a list of tasks  
### ✔ Extract **only these four fields**:
- **Task Name**
- **Task Description**
- **Agent Name**
- **Command**

### ✔ Display this data in any UI  
### ✔ Show clean, readable code  
### ✔ Use an object-oriented approach  
### ✔ Include error handling  
### ✔ Submit within 72 hours  

---

# 📌 2. My Solution Overview (How I Designed It)

I built a **two-layer architecture**:

---

## 🟠 Backend (FastAPI)

The backend:

- Communicates with UAC using the official `uac-api` wrapper  
- Retrieves tasks using:
  - `list_tasks(payload)`  
  - `list_tasks_advanced(query=None)`
- Extracts and normalizes only the required four fields  
- Returns a clean JSON response to the frontend  
- Stores the UAC token securely in environment variables  
- Provides two endpoints:
  - `/api/tasks/basic`
  - `/api/tasks/advanced`

I used object-oriented design:
- `UacClient` handles connection
- `TaskService` handles business logic
- `TaskInfo` models the simplified output structure

---

## 🟠 Frontend (HTML + JavaScript)

The frontend:

- Fetches data from the FastAPI backend  
- Displays tasks as **cards/boxes** with warm styling  
- Allows switching between Basic and Advanced APIs  
- Has hover animations and clean colors  
- Shows “–” when a field is missing  

This keeps the UI extremely simple but visually clean and professional.

---

# 📌 3. Field Mapping (Core of the Assignment)

UAC returns many detailed fields, but the requirement was to map only four.

### ✔ My exact mapping:

-name → Task Name
-summary / description → Task Description
-agent or agentVar → Agent Name
-command → Command


### ✔ If a field is missing in UAC:
- Backend returns `null`
- Frontend displays `"–"`

This ensures stable behavior regardless of differences between UAC environments.

---

# 📌 4. UAC API Functions Used

From `uac-api`, I used:

### 1. `uac.tasks.list_tasks(payload)`
- Summary task information  
- Used for **Basic view**

### 2. `uac.tasks.list_tasks_advanced(query=None)`
- Complete task definition  
- Used for **Advanced view**

These two calls satisfy the exact requirement to retrieve tasks and show mapped fields.

---

# 📌 5. Backend File Breakdown

### `main.py`
- FastAPI application  
- Registers:
  - `/api/tasks/basic`
  - `/api/tasks/advanced`  
- Adds CORS so frontend can call backend  
- Injects TaskService  

### `uac_client.py`
- Reads `UAC_URL` and `UAC_TOKEN` from environment  
- Creates UniversalController client  
- Ensures token is **not exposed** and authentication is validated  

### `task_service.py`
- Object-oriented business logic  
- Calls UAC APIs  
- Applies mapping rules  
- Handles missing fields  
- Returns list of `TaskInfo` objects  

### `models.py`
- `TaskInfo` dataclass → internal data structure  
- `TaskInfoSchema` → API response model  

### `requirements.txt`
Backend dependencies.

---

# 📌 6. Frontend File Breakdown

### `index.html`
- Buttons for Basic / Advanced  
- Container for task cards  
- Loads `app.js` and `styles.css`  

### `styles.css`
- Warm beige theme  
- Card-based layout  
- Button animations and shadows  
- Clean typography  

### `app.js`
- Calls backend endpoints  
- Converts responses into cards  
- Handles loading and error states  
- Renders consistent UI  

---

# 📌 7. Running the Project (Reviewer Instructions)

I created **two run scripts** to make this extremely easy:

---

## ▶️ Step 1 — Start Backend

```bash
cd backend
./run_backend.sh

If UAC_TOKEN is not set, the script will securely prompt you to enter it (not visible while typing).

Backend starts at:

URL	Purpose
http://127.0.0.1:8000
	Backend root
http://127.0.0.1:8000/docs
	Swagger API documentation
http://127.0.0.1:8000/api/tasks/basic
	Basic list (summary API)
http://127.0.0.1:8000/api/tasks/advanced
	Advanced list (detailed API)

▶️ Step 2 — Start Frontend

Open another terminal:

cd frontend
./run_frontend.sh


Frontend starts at:

➡ http://127.0.0.1:9000

📌 8. What You Will See in the UI

When you open:

➡ http://127.0.0.1:9000

You will see:

⭐ Two buttons:

Load Basic (list_tasks)

Load Advanced (list_tasks_advanced)

⭐ Cards showing:
Task Name:        ...
Description:      ...
Agent:            ...
Command:          ...

⭐ Clean warm styling:

Boxes/cards

Soft shadows

Animations

Consistent spacing

📌 9. Security: UAC Token Handling

Token is never written in code

It is never stored in frontend

It is never logged

Only loaded through environment variables or prompt

Backend communicates with UAC securely

This follows best practices for sensitive credentials.
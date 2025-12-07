// -----------------------------------------------
// Base URL of the backend FastAPI service.
// Frontend always calls these endpoints to fetch
// task data from UAC via the Python backend.
// -----------------------------------------------
const API_BASE = "http://127.0.0.1:8000";


// -------------------------------------------------------------
// loadTasks(mode)
// This function loads either:
//   - Basic tasks     → using list_tasks()
//   - Advanced tasks  → using list_tasks_advanced()
// based on the button the user clicks.
//
// Steps:
//   1. Choose the correct API endpoint
//   2. Fetch JSON from backend
//   3. Clear previous table rows
//   4. Insert new rows dynamically
// -------------------------------------------------------------
async function loadTasks(mode) {
    
    // Get references to elements in the HTML page
    const tableBody = document.querySelector("#taskTable tbody");
    const errorDiv = document.getElementById("error");
    const infoDiv = document.getElementById("info");

    // Reset any previous error/info messages
    errorDiv.textContent = "";
    infoDiv.textContent = "";

    // ------------------------------
    // Select backend API endpoint
    // ------------------------------
    let url;
    if (mode === "basic") {
        // Basic → summary data from list_tasks()
        url = `${API_BASE}/api/tasks/basic`;
        infoDiv.textContent = 
            "Using list_tasks (basic summary). Agent and Command may not appear if not included in API.";
    } else {
        // Advanced → full definition from list_tasks_advanced()
        url = `${API_BASE}/api/tasks/advanced`;
        infoDiv.textContent = 
            "Using list_tasks_advanced (detailed). Mapping: name, description/summary, agent, command.";
    }

    // Show loading message before API returns
    errorDiv.textContent = "Loading tasks...";

    // Clear the table so old rows do not stay visible
    tableBody.innerHTML = "";

    try {
        // ----------------------------------------------------------
        // Fetch data from backend
        // ----------------------------------------------------------
        const response = await fetch(url);

        // If backend returns a non-200 status → throw error
        if (!response.ok) {
            throw new Error(`Backend returned status ${response.status}`);
        }

        // Convert backend JSON into a JavaScript array
        const tasks = await response.json();

        // Remove loading message
        errorDiv.textContent = "";

        // Handle case where no task data is returned
        if (!tasks || tasks.length === 0) {
            errorDiv.textContent = "No tasks found.";
            return;
        }

        // ----------------------------------------------------------
        // Insert each task as a new row in the HTML table
        // ----------------------------------------------------------
        tasks.forEach(task => {
            const tr = document.createElement("tr");

            // Build row content using our 4 required fields
            tr.innerHTML = `
                <td>${task.name || ""}</td>
                <td>${task.description || ""}</td>
                <td>${task.agent || ""}</td>
                <td><pre>${task.command || ""}</pre></td>
            `;

            // Add row to table
            tableBody.appendChild(tr);
        });

    } catch (err) {
        // Display error messages (connection issue, backend error, etc.)
        errorDiv.textContent = `Failed to load tasks: ${err.message}`;
    }
}


// -------------------------------------------------------------
// Wire the two buttons to the loadTasks() function.
// Clicking a button loads basic or advanced data.
// -------------------------------------------------------------
document.getElementById("loadBasicBtn")
        .addEventListener("click", () => loadTasks("basic"));

document.getElementById("loadAdvancedBtn")
        .addEventListener("click", () => loadTasks("advanced"));


// -------------------------------------------------------------
// Automatically load advanced tasks when the page first opens.
// This gives the user immediate data without clicking anything.
// -------------------------------------------------------------
loadTasks("advanced");

// --------------------------------------------------------------------------------
// ADMIN COMPLAINT DETAIL JAVASCRIPT
// Fetches a single complaint, populates the UI, and handles status/dept updates.
// --------------------------------------------------------------------------------

// Grab the complaint ID from the URL (e.g., admin-complaint-detail.html?id=123)
const urlParams = new URLSearchParams(window.location.search);
const currentId = urlParams.get('id');

async function loadComplaintDetails() {
  if (!currentId) {
    alert("No complaint ID provided in the URL.");
    window.location.href = "admin-complaints.html";
    return;
  }

  try {
    // We use the public citizen tracking endpoint to grab the complaint data,
    // which gives us everything we need including history.
    const response = await fetch(`/api/complaints/${currentId}`);
    if (!response.ok) {
      alert("Complaint not found.");
      window.location.href = "admin-complaints.html";
      return;
    }

    const data = await response.json();

    // 1. Header Info
    document.getElementById("displayId").innerText = `ID: ${data.complaint_id}`;
    let statusClass = data.status.replace(" ", "").toLowerCase();
    document.getElementById("displayStatusBadge").innerHTML = `<span class="badge status-${statusClass}" style="font-size: 1rem; border: 1px solid currentColor; padding: 6px 16px;">${data.status}</span>`;

    // 2. AI Panel
    document.getElementById("aiCategory").innerText = data.category;
    document.getElementById("aiPriority").innerHTML = `<span class="badge badge-${data.priority.toLowerCase()}">${data.priority}</span>`;
    document.getElementById("aiSummary").innerText = data.ai_summary || "No summary available.";
    
    const conf = data.ai_confidence ? Math.round(data.ai_confidence * 100) : 0;
    document.getElementById("aiConfidence").innerText = conf;

    // 3. Original Data
    document.getElementById("originalDesc").innerText = data.description;
    document.getElementById("originalLocation").innerText = data.location;
    document.getElementById("originalContact").innerText = data.citizen_contact || "None provided";

    // 4. Action Dropdowns (set their current values)
    if (data.assigned_department) {
      document.getElementById("actionAssign").value = data.assigned_department;
    }
    document.getElementById("actionStatus").value = data.status;

    // 5. Timeline
    const timelineContainer = document.getElementById("timelineContainer");
    timelineContainer.innerHTML = "";
    
    if (data.history && data.history.length > 0) {
      // Sort history oldest first
      const sortedHistory = data.history.sort((a, b) => new Date(a.changed_at) - new Date(b.changed_at));
      
      sortedHistory.forEach(item => {
        const dateObj = new Date(item.changed_at);
        const dateStr = dateObj.toLocaleDateString() + ' ' + dateObj.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        
        const div = document.createElement("div");
        div.style.position = "relative";
        div.style.marginBottom = "1.5rem";
        div.innerHTML = `
          <div style="position: absolute; left: -1.35rem; top: 0.25rem; width: 12px; height: 12px; border-radius: 50%; background-color: var(--primary-color); border: 2px solid white;"></div>
          <div style="font-weight: 600; color: var(--text-primary); font-size: 0.9rem;">${item.new_status}</div>
          <div style="font-size: 0.8rem; color: var(--text-secondary);">${dateStr} &bull; by ${item.changed_by}</div>
        `;
        timelineContainer.appendChild(div);
      });
    }

  } catch (error) {
    console.error("Error loading complaint details:", error);
  }
}

// Function called when admin clicks "Save" on department assignment
async function assignDepartment() {
  const dept = document.getElementById("actionAssign").value;
  if (!dept) return;

  try {
    const res = await ApiClient.fetchSecure(`/api/admin/complaints/${currentId}/assign`, {
      method: "PATCH",
      body: JSON.stringify({ department: dept })
    });
    
    if (res && res.ok) {
      // Reload the page to reflect the new assignment and history
      loadComplaintDetails();
    } else {
      alert("Failed to assign department.");
    }
  } catch(e) {
    console.error(e);
  }
}

// Function called when admin clicks "Update" on status
async function updateStatus() {
  const newStatus = document.getElementById("actionStatus").value;
  if (!newStatus) return;

  try {
    const res = await ApiClient.fetchSecure(`/api/admin/complaints/${currentId}/status`, {
      method: "PATCH",
      body: JSON.stringify({ new_status: newStatus, changed_by: "admin" }) // normally username comes from token implicitly, but API expects body anyway
    });
    
    if (res && res.ok) {
      // Reload the page to show the new status badge and history item
      loadComplaintDetails();
    } else {
      alert("Failed to update status.");
    }
  } catch(e) {
    console.error(e);
  }
}

// Load on page ready
document.addEventListener("DOMContentLoaded", loadComplaintDetails);

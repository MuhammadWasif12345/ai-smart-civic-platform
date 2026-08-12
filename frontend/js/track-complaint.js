// --------------------------------------------------------------------------------
// TRACK COMPLAINT JAVASCRIPT
// Handles fetching a specific complaint by ID and rendering its status and timeline.
// --------------------------------------------------------------------------------

const trackForm = document.getElementById("trackForm");
const resultCard = document.getElementById("resultCard");
const searchError = document.getElementById("searchError");
const submitBtn = trackForm.querySelector("button[type='submit']");

trackForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  
  // Hide previous errors or results
  searchError.style.display = "none";
  resultCard.style.display = "none";
  
  const complaintId = document.getElementById("complaint_id").value.trim();
  if (!complaintId) return;

  // Change button text to show activity
  const originalBtnText = submitBtn.innerHTML;
  submitBtn.innerHTML = "Tracking... <i data-lucide='loader' class='loading-spinner' style='display:inline-block; border-color:transparent; animation: spin 1s linear infinite;'></i>";
  submitBtn.disabled = true;

  try {
    // Fetch data from the public tracking endpoint
    const response = await fetch(`/api/complaints/${complaintId}`);
    let data;
    
    if (response.status === 404) {
      // Fallback to local storage for Vercel demo where DB resets
      let saved = [];
      try {
        saved = JSON.parse(localStorage.getItem('my_complaints') || '[]');
      } catch (e) {}
      
      let localData = saved.find(c => String(c.complaint_id) === String(complaintId));
      if (localData) {
        data = localData;
      } else {
        throw new Error("We couldn't find a complaint with that ID — double-check and try again.");
      }
    } else if (!response.ok) {
      throw new Error("Couldn't reach the server. Please try again later.");
    } else {
      data = await response.json();
    }
    
    // --- POPULATE THE UI ---
    
    // ID and Department
    document.getElementById("displayId").innerText = `ID: ${data.complaint_id}`;
    document.getElementById("displayDepartment").innerText = data.assigned_department || "Not assigned yet";
    document.getElementById("displayCategory").innerText = data.category;
    
    // Status Badge
    let statusClass = data.status.replace(" ", "").toLowerCase(); // "In Progress" -> "inprogress"
    document.getElementById("displayStatusBadge").innerHTML = 
      `<span class="badge" style="font-size: 1rem; border: 1px solid currentColor;" class="status-${statusClass}">${data.status}</span>`;
      
    // Priority Badge
    document.getElementById("displayPriority").innerHTML = 
      `<span class="badge badge-${data.priority.toLowerCase()}">${data.priority}</span>`;

    // Timeline Construction
    const timelineContainer = document.getElementById("timelineContainer");
    timelineContainer.innerHTML = ""; // Clear old timeline
    
    // The backend returns a list of StatusHistory objects. We loop through them.
    if (data.history && data.history.length > 0) {
      // Sort history oldest to newest (just in case)
      const sortedHistory = data.history.sort((a, b) => new Date(a.changed_at) - new Date(b.changed_at));
      
      sortedHistory.forEach(item => {
        const dateObj = new Date(item.changed_at);
        const dateStr = dateObj.toLocaleDateString() + ' ' + dateObj.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        
        const div = document.createElement("div");
        div.className = "timeline-item";
        div.innerHTML = `
          <div class="timeline-status">${item.new_status}</div>
          <div class="timeline-date">${dateStr}</div>
        `;
        timelineContainer.appendChild(div);
      });
    } else {
      timelineContainer.innerHTML = "<p>No history available.</p>";
    }

    // Show the result card
    resultCard.style.display = "block";
    lucide.createIcons(); // Re-initialize icons if needed

  } catch (error) {
    searchError.innerText = error.message;
    searchError.style.display = "block";
  } finally {
    // Restore button state
    submitBtn.innerHTML = originalBtnText;
    submitBtn.disabled = false;
  }
});

// Auto-track if ID is in the URL (e.g. from submission page)
document.addEventListener("DOMContentLoaded", () => {
  const urlParams = new URLSearchParams(window.location.search);
  const idParam = urlParams.get('id');
  if (idParam) {
    document.getElementById("complaint_id").value = idParam;
    // trigger form submit
    trackForm.dispatchEvent(new Event("submit", { cancelable: true, bubbles: true }));
  }
});

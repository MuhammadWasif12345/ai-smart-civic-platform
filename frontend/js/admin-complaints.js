// --------------------------------------------------------------------------------
// ADMIN COMPLAINTS LIST JAVASCRIPT
// Handles fetching the paginated/filtered list of complaints and drawing the table.
// --------------------------------------------------------------------------------

const filterForm = document.getElementById("filterForm");
const tableBody = document.getElementById("tableBody");
const totalCount = document.getElementById("totalCount");

async function loadComplaints() {
  // Read the current values of our filter dropdowns
  const status = document.getElementById("filterStatus").value;
  const priority = document.getElementById("filterPriority").value;
  const category = document.getElementById("filterCategory").value;

  // Build the query string manually
  const params = new URLSearchParams();
  if (status) params.append("status", status);
  if (priority) params.append("priority", priority);
  if (category) params.append("category", category);

  // Show a loading message in the table
  tableBody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding:2rem;"><i data-lucide="loader" class="loading-spinner" style="display:inline-block; animation: spin 1s linear infinite;"></i> Loading...</td></tr>`;
  lucide.createIcons();

  try {
    const response = await ApiClient.fetchSecure(`/api/admin/complaints?${params.toString()}`);
    if (!response) return; // API client handles 401 redirects automatically
    
    const data = await response.json();
    totalCount.innerText = data.total;

    // Clear the table
    tableBody.innerHTML = "";

    // Empty state handling
    if (data.complaints.length === 0) {
      tableBody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding:3rem; color:var(--text-secondary);">No complaints match these filters yet.</td></tr>`;
      return;
    }

    // Loop through each complaint and build a table row (tr)
    data.complaints.forEach(c => {
      const row = document.createElement("tr");
      
      // Format the date nicely
      const dateObj = new Date(c.created_at);
      const dateStr = dateObj.toLocaleDateString() + '<br><span style="font-size:0.75rem;color:gray;">' + dateObj.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) + '</span>';
      
      // Use the AI summary if available, otherwise truncate the description safely
      const descStr = c.description || "";
      const summaryText = c.ai_summary ? c.ai_summary : (descStr.length > 50 ? descStr.substring(0, 50) + "..." : descStr);
      
      // Build the status and priority badges using our CSS classes
      const safeStatus = c.status || "Open";
      const statusClass = safeStatus.replace(" ", "").toLowerCase();
      const statusHtml = `<span style="font-size: 0.85rem;" class="status-${statusClass}">${safeStatus}</span>`;
      
      const safePriority = c.priority || "Medium";
      const priorityHtml = `<span class="badge badge-${safePriority.toLowerCase()}">${safePriority}</span>`;
      
      const safeCategory = c.category || "Uncategorized";
      
      const deptHtml = c.assigned_department ? `<span style="font-size:0.85rem;">${c.assigned_department}</span>` : `<span style="font-size:0.85rem;color:gray;">Unassigned</span>`;

      row.innerHTML = `
        <td>${dateStr}</td>
        <td style="max-width: 300px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="${summaryText}">${summaryText}</td>
        <td><span style="font-size:0.85rem;">${safeCategory}</span></td>
        <td>${priorityHtml}</td>
        <td>${statusHtml}</td>
        <td>${deptHtml}</td>
        <td>
          <a href="admin-complaint-detail.html?id=${c.complaint_id}" class="btn btn-outline" style="padding: 0.25rem 0.75rem; font-size: 0.85rem;">
            View <i data-lucide="arrow-right" style="width:14px; height:14px;"></i>
          </a>
        </td>
      `;
      tableBody.appendChild(row);
    });
    
    // Initialize the lucide icons we just injected into the DOM
    lucide.createIcons();

  } catch (error) {
    console.error("Failed to load complaints table", error);
    tableBody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding:2rem; color:red;">Error loading data. Please refresh.</td></tr>`;
  }
}

// Listen for the filter form submission
filterForm.addEventListener("submit", (e) => {
  e.preventDefault();
  loadComplaints();
});

// Listen for the clear filters button
document.getElementById("resetFilters").addEventListener("click", () => {
  document.getElementById("filterStatus").value = "";
  document.getElementById("filterPriority").value = "";
  document.getElementById("filterCategory").value = "";
  loadComplaints(); // Reload everything
});

// Load immediately on page load
document.addEventListener("DOMContentLoaded", () => {
  loadComplaints();
});

// js/submit-complaint.js

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('complaintForm');
  const submitBtn = document.getElementById('submitBtn');
  const loadingOverlayTitle = document.getElementById('loadingOverlayTitle');
  const loadingOverlayDesc = document.getElementById('loadingOverlayDesc');
  const loadingProgressBar = document.getElementById('loadingProgressBar');
  const formCard = document.getElementById('formCard');
  const aiExplanation = document.getElementById('aiExplanation');
  const successCard = document.getElementById('successCard');
  
  // File Upload Elements
  const dropArea = document.getElementById('dropArea');
  const fileInput = document.getElementById('image_upload');
  const imagePreviewContainer = document.getElementById('imagePreviewContainer');
  const imagePreview = document.getElementById('imagePreview');
  const imageName = document.getElementById('imageName');
  const removeImageBtn = document.getElementById('removeImageBtn');
  const fileError = document.getElementById('fileError');
  
  // Success Elements
  const copyIdBtn = document.getElementById('copyIdBtn');
  const copyFeedback = document.getElementById('copyFeedback');
  const trackLinkBtn = document.getElementById('trackLinkBtn');

  let currentBase64Image = null;

  // --- DRAG AND DROP LOGIC ---
  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
  });
  function preventDefaults(e) { e.preventDefault(); e.stopPropagation(); }

  ['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, () => dropArea.classList.add('dragover'), false);
  });
  ['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, () => dropArea.classList.remove('dragover'), false);
  });

  dropArea.addEventListener('drop', (e) => {
    const dt = e.dataTransfer;
    const files = dt.files;
    if (files.length > 0) handleFile(files[0]);
  });

  fileInput.addEventListener('change', function() {
    if (this.files.length > 0) handleFile(this.files[0]);
  });

  function handleFile(file) {
    fileError.style.display = 'none';
    
    if (!file.type.startsWith('image/')) {
      fileError.textContent = 'Invalid file type. Please upload an image.';
      fileError.style.display = 'block';
      return;
    }
    
    if (file.size > 10 * 1024 * 1024) {
      fileError.textContent = 'File is too large. Max size is 10 MB.';
      fileError.style.display = 'block';
      return;
    }

    const reader = new FileReader();
    reader.onload = function(e) {
      currentBase64Image = e.target.result.split(',')[1];
      imagePreview.src = e.target.result;
      imageName.textContent = file.name;
      
      dropArea.style.display = 'none';
      imagePreviewContainer.style.display = 'flex';
    };
    reader.readAsDataURL(file);
  }

  removeImageBtn.addEventListener('click', () => {
    currentBase64Image = null;
    fileInput.value = '';
    imagePreviewContainer.style.display = 'none';
    dropArea.style.display = 'block';
  });

  // --- COPY ID LOGIC ---
  copyIdBtn.addEventListener('click', () => {
    const idText = document.getElementById('successId').textContent;
    navigator.clipboard.writeText(idText).then(() => {
      copyFeedback.style.opacity = '1';
      setTimeout(() => { copyFeedback.style.opacity = '0'; }, 2000);
    });
  });

  // --- FORM SUBMISSION ---
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Reset errors
    document.getElementById('descriptionError').style.display = 'none';
    document.getElementById('locationError').style.display = 'none';
    document.getElementById('contactError').style.display = 'none';
    document.getElementById('serverError').style.display = 'none';
    
    // Get values
    const description = document.getElementById('description').value.trim();
    const locationStr = document.getElementById('location').value.trim();
    const citizenContact = document.getElementById('citizen_contact').value.trim();

    let hasError = false;
    if (!description) {
      document.getElementById('descriptionError').style.display = 'block';
      hasError = true;
    }
    if (!locationStr) {
      document.getElementById('locationError').style.display = 'block';
      hasError = true;
    }

    // Validate Contact Info (Email or Phone Number)
    if (citizenContact) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      // Basic phone regex (allows optional +, numbers, spaces, dashes, parens)
      const phoneRegex = /^\+?[0-9\s\-()]{7,15}$/;
      
      if (!emailRegex.test(citizenContact) && !phoneRegex.test(citizenContact)) {
        document.getElementById('contactError').style.display = 'block';
        hasError = true;
      }
    }

    if (hasError) return;

    const payload = {
      description: description,
      location: locationStr,
      citizen_contact: citizenContact
    };
    
    if (currentBase64Image) {
      payload.image_base64 = currentBase64Image;
    }

    // UI Loading state
    submitBtn.disabled = true;
    submitBtn.innerHTML = 'Processing...';
    loadingOverlay.style.display = 'flex';
    
    // Reset progress
    loadingProgressBar.style.width = '10%';
    loadingOverlayTitle.textContent = 'Analyzing description...';
    loadingOverlayDesc.textContent = 'Our AI is reading your submission.';

    try {
      // Simulate stepped progress
      const steps = [
        { wait: 600, p: '30%', t: 'Classifying category...', d: 'Determining the correct department.' },
        { wait: 600, p: '60%', t: 'Assessing priority...', d: 'Checking for critical keywords and hazards.' },
        { wait: 600, p: '85%', t: 'Routing complaint...', d: 'Assigning to the appropriate municipal team.' }
      ];
      
      const simulateSteps = async () => {
        for (const s of steps) {
            await new Promise(r => setTimeout(r, s.wait));
            loadingProgressBar.style.width = s.p;
            loadingOverlayTitle.textContent = s.t;
            loadingOverlayDesc.textContent = s.d;
        }
      };
      
      // Run the fetch and the simulation concurrently
      const [response] = await Promise.all([
        fetch('/api/complaints', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        }),
        simulateSteps()
      ]);
      
      loadingProgressBar.style.width = '100%';
      loadingOverlayTitle.textContent = 'Done!';
      loadingOverlayDesc.textContent = 'Redirecting...';
      await new Promise(r => setTimeout(r, 400)); // Brief pause at 100%

      if (!response.ok) {
        throw new Error('Server returned an error');
      }

      const data = await response.json();

      // Save to localStorage for demo persistence (Vercel ephemeral DB workaround)
      try {
        let saved = JSON.parse(localStorage.getItem('my_complaints') || '[]');
        // We ensure data has the fields needed by track-complaint.js
        if (!data.status) data.status = "SUBMITTED";
        if (!data.history) data.history = [{ old_status: "None", new_status: "SUBMITTED", changed_at: new Date().toISOString() }];
        saved.push(data);
        localStorage.setItem('my_complaints', JSON.stringify(saved));
      } catch (err) {
        console.error("Local storage error:", err);
      }

      // Show success screen
      formCard.style.display = 'none';
      aiExplanation.style.display = 'none';
      loadingOverlay.style.display = 'none';
      successCard.style.display = 'block';

      // Populate Success Data
      document.getElementById('successId').textContent = data.complaint_id;
      document.getElementById('successCategory').textContent = data.category || 'N/A';
      document.getElementById('successDepartment').textContent = data.department || 'General';
      document.getElementById('successSummary').textContent = data.ai_summary || 'No summary generated.';
      
      trackLinkBtn.href = 'track-complaint.html?id=' + data.complaint_id;

      // Priority Badge
      const priorityEl = document.getElementById('successPriority');
      const priorityLower = (data.priority || '').toLowerCase();
      let badgeClass = 'badge-low';
      if (priorityLower === 'critical') badgeClass = 'badge-critical';
      else if (priorityLower === 'high') badgeClass = 'badge-high';
      else if (priorityLower === 'medium') badgeClass = 'badge-medium';
      
      priorityEl.innerHTML = `<span class="badge ${badgeClass}">${data.priority}</span>`;

      // Timeline Logic
      const tlAssigned = document.getElementById('tlAssigned');
      const tlInProgress = document.getElementById('tlInProgress');
      const tlResolved = document.getElementById('tlResolved');
      
      // By default, just submitted and analyzed are completed.
      // If status is somehow already further along:
      const statusLower = (data.status || '').toLowerCase();
      if (statusLower === 'assigned' || statusLower === 'in_progress' || statusLower === 'resolved') {
        tlAssigned.classList.add('completed');
        tlAssigned.classList.remove('active');
        tlInProgress.classList.add('active');
        tlInProgress.querySelector('strong').style.color = 'inherit';
      }
      if (statusLower === 'in_progress' || statusLower === 'resolved') {
        tlInProgress.classList.add('completed');
        tlInProgress.classList.remove('active');
        tlResolved.classList.add('active');
        tlResolved.querySelector('strong').style.color = 'inherit';
      }
      if (statusLower === 'resolved') {
        tlResolved.classList.add('completed');
        tlResolved.classList.remove('active');
      }

    } catch (error) {
      console.error(error);
      document.getElementById('serverError').textContent = 'An error occurred while submitting. Please try again.';
      document.getElementById('serverError').style.display = 'block';
    } finally {
      submitBtn.disabled = false;
      submitBtn.innerHTML = 'Analyze & Submit Complaint &rarr;';
      loadingOverlay.style.display = 'none';
    }
  });
});

// Global function for Quick Samples
window.fillSample = function(desc, loc) {
    document.getElementById('description').value = desc;
    document.getElementById('location').value = loc;
};

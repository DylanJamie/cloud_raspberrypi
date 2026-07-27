// dashboard.js

// this file will have 3 jobs
// on the page load fetch the file list and render it
// handel the upload form
// handel the delete and download clicks and the log out button

// Every fetch call here includes credentials include
// this is what tells the browser "attach my session_id cookie to this request"
// without this, the server has no way to know who it is asking.

// --------------
// "DOMContentLoaded" fires once the HTML is fully parsed and avaliable to the JS
// We wrap the start up code in this so whe dont try to grab an incorrect element like 'fileList'
// before the browser actually created it yet
// --------------
document.addEventListener("DOMContentLoaded", () => {
    loadFiles();

    document.getElementById("uploadForm").addEventListener("submit", handleUpload);
    document.getElementById("logoutBtn").addEventListener("click", handleLogout);

    // Event delegation: instead of attaching a click listener to every
    // individual delete button (which don't exist yet at this point —
    // they get created later by renderFiles), we attach ONE listener to
    // the parent container and check what was actually clicked. This
    // means it keeps working even for rows added after the page loads.
    document.getElementById("fileList").addEventListener("click", handleFileListClick);
});

// ---------------------------------------------------------
// Fetch the current user's files and render them
// ---------------------------------------------------------
async function loadFiles() {
    // Actually use the Python endpoint
    const listEl = document.getElementById("fileList");

    const response = await fetch("/files", {
	credentials: "include",
    });

    // if the response is ok continue
    if (!response.ok) {
	// Most likely a 401 — the session cookie is missing or expired
	listEl.innerHTML = `<p class="empty-state">You're not logged in. <a href="/">Go to login</a></p>`;
	return;
    }

    // if we dont get an error we send the json
    const files = await response.json();
    renderFiles(files);
}

// ---------------------------------------------------------
// Turn the array of file objects from the API into actual HTML
// ---------------------------------------------------------
function renderFiles(files) {
    const listEl = document.getElementById("fileList");

    if (files.length === 0) {
	listEl.innerHTML = `<p class="empty-state">No files yet — upload your first one above.</p>`;
	return;
    }

    // .map() turns each file object into a chunk of HTML (a string),
    // and .join("") glues all those chunks together into one big string.
    // Template literals (the backticks `...`) let us drop JS variables
    // directly into the HTML using ${...}.
    listEl.innerHTML = files
        .map(
	    (file) => `
        <div class="file-row" data-file-id="${file.file_id}">
          <div class="file-row__info">
            <span class="file-row__name">${file.original_filename}</span>
            <span class="file-row__meta">${formatSize(file.size_bytes)}</span>
          </div>
          <div class="file-row__actions">
            <a class="btn btn--small" href="/files/${file.file_id}/download">Download</a>
            <button class="btn btn--small btn--danger" data-action="delete">Delete</button>
          </div>
        </div>
      `
	)
	.join("");
}

// ---------------------------------------------------------
// Small helper — turns raw bytes into something readable (e.g. "42.3 KB")
// ---------------------------------------------------------
function formatSize(bytes) {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

// ---------------------------------------------------------
// Handle clicks inside the file list (delete buttons)
// ---------------------------------------------------------
async function handleFileListClick(event) {
    // event.target is the exact element that was clicked. Since our
    // buttons live inside .file-row divs, we use .closest() to walk up
    // and find the nearest ancestor (or itself) matching a selector —
    // this is how we figure out WHICH row's delete button was pressed.
    const deleteBtn = event.target.closest('[data-action="delete"]');
    // the click wasn't on a delete button — ignore it
    if (!deleteBtn)
	return;

    const row = deleteBtn.closest(".file-row");
    const fileId = row.dataset.fileId; // reads the data-file-id="..." attribute we set in renderFiles

    const confirmed = confirm("Delete this file? This can't be undone.");
    if (!confirmed)
	return;

    const response = await fetch(`/files/delete?file_id=${fileId}`, {
	method: "DELETE",
	credentials: "include",
    });

    if (response.ok) {
	row.remove(); // no need to re-fetch the whole list — just remove this one row
    } else {
	alert("Couldn't delete that file.");
    }

}

// ---------------------------------------------------------
// Handle the upload form
// ---------------------------------------------------------
async function handleUpload(event) {
    // stop the browser's default full-page form submit
    event.preventDefault();

    const fileInput = document.getElementById("fileInput");
    const statusEl = document.getElementById("uploadStatus");
    
    if (fileInput.files.length === 0)
	return;

    // File uploads can't be sent as plain JSON — they need to be packaged
    // as "multipart/form-data", which is exactly what FormData builds for us.
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    statusEl.textContent = "Uploading…";
    statusEl.className = "status-text";

    const response = await fetch("/files/upload", {
	method: "POST",
	credentials: "include",
	body: formData,
	// NOTE: do NOT set a "Content-Type" header manually here — the
	// browser sets it automatically for FormData, including a required
	// "boundary" value. Setting it yourself will actually break the upload.
    });

    if (response.ok) {
	statusEl.textContent = "Upload complete.";
	statusEl.className = "status-text status-text--success";
	fileInput.value = ""; // clear the file picker
	loadFiles(); // refresh the list so the new file shows up
    } else {
	statusEl.textContent = "Upload failed.";
	statusEl.className = "status-text status-text--error";
    }
}

// ---------------------------------------------------------
// Handle logout
// ---------------------------------------------------------
async function handleLogout() {
    await fetch("/logout", {
	method: "POST",
	credentials: "include",
    });

    // send the user back to the log in page
    window.location.href = "/"
}

// login.js

// file will control all of the log in page functions

// querySelector function to verify a log in is successful
document.querySelector(".cloud__form").addEventListener("submit", async (event) => {
    // Stop the form from doing a normal page reload and submit
    event.preventDefault();

    // Connect the HTML class names to this function
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    // wait for the response and fetch the log in username and password from the data base, encrypt/decrypt it and validate the post method
    const response = await fetch(`/login?username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`, {
        method: "POST",
        credentials: "include", // required so the session cookie actually gets stored
    });

    // if the response worked and is true show the user dashboard other wise show log in failed pop up
    if (response.ok) {
	// file list page
	window.location.href = "/dashboard";
    } else {
	alert("Login failed - check your username and password.");
    }
});


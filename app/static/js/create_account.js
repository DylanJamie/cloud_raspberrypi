// create_account.js

// this file will create new users for the site

// newUser function to create a new user
document.querySelector("#createAccountForm").addEventListener("submit", async (event) => {
    // stop the form from doing a normal page reload and submit
    event.preventDefault();

    // Connect the HTML class names and make the variables
    const newUsername = document.getElementById("newUsername").value;    const newPassword = document.getElementById("newPassword").value;
    const confirm_password = document.getElementById("confirm_password").value;

    // ensure that the password matches the confirm password
    if (newPassword !== confirm_password) {
	alert("Passwords don't match");
	return;
    }

    // wait for the response and create a new username and account into the SQL database with the python endpoint
    const response = await fetch(`/register?username=${encodeURIComponent(newUsername)}&password=${encodeURIComponent(newPassword)}`, {
	method: "POST",
	credentials: "include",
    });

    // check to make sure the response went through
    // Account has been created
    if (response.ok) {
	// go back to Login window
	window.location.href = "/login";
    } else {
	alert("Could not create that account the username maybe already taken.");
    }
});
	   

				     

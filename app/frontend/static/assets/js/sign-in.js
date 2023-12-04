// On Page load:
 $(function() {
    // Bind keypress event listener to input fields
    $('input[name="username"], input[name="password"]').keypress(function(e) {
      if (e.which === 13) { // Check if Enter key (key code 13) is pressed
        e.preventDefault(); // Prevent the default form submission
        $('#btn-sign-in').click(); // Trigger a click event on the Sign In button
      }
    });

    // Attach a click event listener to the button
    $('#btn-sign-in').click(function(event) {
      event.preventDefault(); // Prevent the default form submission
      signIn(); // Call the AJAX request function
    });
  });


 // Function to Sign In:
function signIn() {

    // Get the values of username, password, and otp fields
    var username = $('#username').val();
    var password = $('input[name="password"]').val();

    var button = $('#btn-sign-in');

    // Check if any of the fields is empty:
    if (!username || !password) {
      // Display an error message or perform any other necessary action
      $('#error-message').text('All fields are mandatory. Contact Admin.');
      $('#error-message').show();
      return; // Exit the function to prevent the form submission
    }

    // Create FormData object with form input values
    var formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    $.ajax({
      url: '/sign-in',
      type: 'POST',
      data: formData, // Use the FormData object here
      processData: false, // Important: prevent jQuery from processing the data
      contentType: false, // Important: prevent jQuery from setting the content type
      beforeSend: function() {
        // Show progress indicator or disable the button if needed
        // Disable the button and change its text
        button.prop('disabled', true); // Disable the button
        button.text('Signing... Please wait.'); // Change the button text

      },
      success: function(data) {
        // Handle the success response
        console.log('Success Response:', data);

        // Redirect to data.path on successful login
        window.location.href = data.path;

      },
      error: function(xhr, status, error) {
        // Handle the error response
        console.log('Error Response:', xhr, status, error);
        var errorMessage;

        // set the error message:
        if (xhr.status === 429) {
            errorMessage = error;
        } else {
            errorMessage = JSON.parse(xhr.responseText).error;
        }

        // Display the error message on the web page
        var errorMessageDiv = $('#error-message');
        errorMessageDiv.text(errorMessage);
        errorMessageDiv.show();

      },
      complete: function() {
        // Perform any necessary cleanup or UI updates
        // Enable the button and restore its original text
        button.prop('disabled', false); // Enable the button
        button.text('Sign In'); // Restore the original button text
      }
    });
  }


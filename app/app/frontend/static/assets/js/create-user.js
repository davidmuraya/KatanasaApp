// On Page load:
 $(function() {

    // Attach a click event listener to the button
    $('#btn-submit').click(function(event) {
      event.preventDefault(); // Prevent the default form submission
      createUser(); // Call the AJAX request function
    });
  });


 // Function to Create a User:
function createUser() {

    // Get the values of username, password fields
    var username = $('#username').val();
    var password = $('#password').val();
    var read_only = $('#read-only').prop('checked');
    var are_you_sure = $('#are-you-sure').prop('checked');

    var button = $('#btn-submit');

    // Check if any of the fields is empty:
    if (!username || !password) {
      // Display an error message or perform any other necessary action
      $('#error-message').text('Username and password fields are mandatory.');
      $('#error-message').show();
      return; // Exit the function to prevent the form submission
    }

    // Create FormData object with form input values
    var formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    formData.append('read_only', read_only);
    formData.append('are_you_sure', are_you_sure);


    $.ajax({
      url: '/create-user',
      type: 'POST',
      data: formData, // Use the FormData object here
      processData: false, // Important: prevent jQuery from processing the data
      contentType: false, // Important: prevent jQuery from setting the content type
      beforeSend: function() {
        // Show progress indicator or disable the button if needed
        // Disable the button and change its text
        button.prop('disabled', true); // Disable the button
        button.text('Saving... Please wait.'); // Change the button text


      },
      success: function(data) {
        // Handle the success response
        console.log('Success Response:', data);

        // Redirect to data.path on successful login
        //window.location.href = data.path;
        var message = $('#success-message');
        message.text(data.message + " User reference "+ data.doc_id);
        message.show();
        $('#error-message').hide();

      },
      error: function(xhr, status, error) {
        // Handle the error response
        console.log('Error Response:', xhr, status, error);
        var errorMessage;

        // set the error message:
        if (xhr.status === 422) {
            errorMessage = error;
        } else {
            errorMessage = JSON.parse(xhr.responseText).error;
        }

        // Display the error message on the web page
        var errorMessageDiv = $('#error-message');
        errorMessageDiv.text(errorMessage);
        errorMessageDiv.show();

        // hide success message
        $('#success-message').hide();

      },
      complete: function() {
        // Perform any necessary cleanup or UI updates
        // Enable the button and restore its original text
        button.prop('disabled', false); // Enable the button
        button.text('Save'); // Restore the original button text

      }
    });
  }



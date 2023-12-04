// On Page load:
 $(function() {

    // Attach a click event listener to the button
    $('#btn-submit').click(function(event) {
      event.preventDefault(); // Prevent the default form submission
      createCustomer(); // Call the AJAX request function
    });
  });


 // Function to Create a Customer:
function createCustomer() {

    // Get the values of username, password, and otp fields
    var first_name = $('#first_name').val();
    var last_name = $('#last_name').val();
    var gender = $('#gender').val();
    var source = $('#business-source').val();
    var city = $('#city').val();
    var phone = $('#phone').val();
    var email = $('#email').val();


    var button = $('#btn-submit');

    // Check if any of the fields is empty:
    if (!first_name || !last_name || !city || !gender || !phone) {
      // Display an error message or perform any other necessary action
      $('#error-message').text('Names, Email, Phone, Gender and City are mandatory.');
      $('#error-message').show();
      return; // Exit the function to prevent the form submission
    }

    // Check if field is empty:
    if (gender === 'Gender') {
      // Display an error message or perform any other necessary action
      $('#error-message').text('Select a valid Gender.');
      $('#error-message').show();
      return; // Exit the function to prevent the form submission
    }

    // Create FormData object with form input values
    var formData = new FormData();
    formData.append('first_name', first_name);
    formData.append('last_name', last_name);
    formData.append('gender', gender);
    formData.append('source', source);
    formData.append('city', city);
    formData.append('phone', phone);
    formData.append('email', email);

    $.ajax({
      url: '/create-customer',
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
        message.text(data.message + " Customer reference "+ data.doc_id);
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


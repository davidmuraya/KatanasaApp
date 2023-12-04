// On Page load:
 $(function() {
    // get list of customers:
    getListOfCustomers();

    // Attach a click event listener to the button
    $('#btn-submit').click(function(event) {
      event.preventDefault(); // Prevent the default form submission
      createCustomerAttendance(); // Call the AJAX request function
    });

    // Attach a click event listener to the dropdown
    $('#customer').change(function() {
        // Get the selected value
        var customerId = $('#customer').val();

        // Fetch data based on the selected text
        getListOfCustomerAttendanceEntries(customerId);
    });

  });



 // Function to Create a Customer Attendance:
function createCustomerAttendance() {

    // Get the values of the form fields
    var customer_id = $('#customer').val();
    var customer_name = $('#customer option:selected').text();
    var attendance = $('#attendance').val();
    var are_you_sure = $('#are-you-sure').prop('checked');


    var button = $('#btn-submit');

    // Check if any of the fields is empty:
    if (!customer || !attendance) {
      // Display an error message or perform any other necessary action
      $('#error-message').text('All fields are mandatory.');
      $('#error-message').show();
      return; // Exit the function to prevent the form submission
    }

    // Create FormData object with form input values
    var formData = new FormData();
    formData.append('customer_id', customer_id);
    formData.append('attendance_date', attendance);
    formData.append('are_you_sure', are_you_sure);
    formData.append('customer_name', customer_name);

    $.ajax({
      url: '/create-customer-attendance',
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
        //console.log('Success Response:', data);

        // Redirect to data.path on successful login
        //window.location.href = data.path;
        var message = $('#success-message');
        message.text(data.message + ". Attendance reference "+ data.doc_id);
        message.show();
        $('#error-message').hide();

        // update the table grid:
        // Get the selected value
        var customerId = $('#customer').val();

        // Fetch data based on the selected value:
        getListOfCustomerAttendanceEntries(customerId);

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



 // Function to get list of attendance entries:
function getListOfCustomerAttendanceEntries(customerId) {

    $.ajax({
      url: '/customers/attendance/json?customer_id=' + customerId,
      type: 'GET',
      beforeSend: function() {
        // Show progress indicator or disable the button if needed



      },
      success: function(data) {
        // Handle the success response
        //console.log('Success Response:', data);

        // set the number of records values:
        $('#no-of-records').text(data.number_of_records);
        $('#total-no-of-records').text(data.number_of_records);

        // Clear existing rows in the tbody
        $('#tbl-attendance tbody').empty();

        // Iterate over the received data and append rows to the tbody
        $.each(data.entries, function(index, entry) {
            // Accessing data within each log
            var entryData = entry.entry_data;
            var entryId = entry.entry_id

            // Append a new row to the tbody
            $('#tbl-attendance tbody').append(`
                <tr>
                    <td>${index + 1}</td>
                    <td>${entryData.attendance_date}</td>
                    <td>${entryData.customer_name}</td>
                    <td>${entryData.added_by}</td>
                    <td>${entryData.entry_date}</td>

                </tr>
            `);
        });


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


      }
    });
  }



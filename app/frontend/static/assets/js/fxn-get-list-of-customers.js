
 // Function to Get List of Customers:
function getListOfCustomers() {

    $.ajax({
      url: '/customers/json',
      type: 'GET',
      beforeSend: function() {
        // Show progress indicator or disable the button if needed

      },
      success: function(data) {
        // Handle the success response
        //console.log('Success Response:', data);

        var customer_dropdown_list = $('#customer');
        customer_dropdown_list.empty();


        // Iterate over the received data and append rows to the dropdown list
        $.each(data.customers, function(index, customer) {
            // Accessing customer_data within each customer
            var customerData = customer.customer_data;
            var customerId = customer.customer_id

            customer_dropdown_list.append('<option value="' + customerId + '">' + customerData.first_name + ' ' + customerData.last_name + '</option>');
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


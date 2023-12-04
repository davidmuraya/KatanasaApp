// On Page load:
 $(function() {
    // get list of all sales:
    getMpesaTransactions();

    // Attach a click event listener to the refresh button:
    $('#btn-refresh').click(function(event) {
      event.preventDefault(); // Prevent the default form submission
      getMpesaTransactions(); // Call the AJAX request function
    });

  });

// Function to get list of all mpesa transactions:
function getMpesaTransactions() {

    $.ajax({
      url: '/m-pesa-transactions/json',
      type: 'GET',
      beforeSend: function() {
        // Show progress indicator or disable the button if needed
        // Clear existing rows in the tbody:
        $('#tbl-mpesa-transactions tbody').empty();

        // Append a new row to the tbody and the add the loading message:
        $('#tbl-mpesa-transactions tbody').append(`
            <tr>
                <td class="text-center align-middle" colspan="8">
                    <span class="text-danger">Loading M-Pesa Transactions. Please wait....</span>
                </td>
            </tr>
        `);


      },
      success: function(data) {
        // Handle the success response
        console.log('Success Response:', data);

        // set the number of records values:
        $('#no-of-records').text(data.number_of_records);
        $('#total-no-of-records').text(data.number_of_records);

        // Clear existing rows in the tbody
        $('#tbl-mpesa-transactions tbody').empty();

        // Iterate over the received data and append rows to the tbody
        $.each(data.transactions, function(index, transaction) {
            // Accessing data within each item
            var TransactionData = transaction.transaction_data.request;
            var TransactionId = transaction.transaction_id


            // Append a new row to the tbody:
            $('#tbl-mpesa-transactions tbody').append(`
                <tr>
                    <td>${index + 1}</td>
                    <td>${TransactionData.TransID}</td>
                    <td>${TransactionData.TransTime}</td>
                    <td>${TransactionData.TransAmount}</td>
                    <td>${TransactionData.MSISDN}</td>
                    <td>${TransactionData.FirstName}</td>
                    <td>${TransactionData.MiddleName}</td>
                    <td>${TransactionData.LastName}</td>

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



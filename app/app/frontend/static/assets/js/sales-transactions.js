// On Page load:
 $(function() {
    // get list of all sales:
    getSalesTransactions();

  });

// Function to get list of all sales:
function getSalesTransactions() {

    $.ajax({
      url: '/transactions/customers/json',
      type: 'GET',
      beforeSend: function() {
        // Show progress indicator or disable the button if needed


      },
      success: function(data) {
        // Handle the success response
        console.log('Success Response:', data);

        // set the number of records values:
        $('#no-of-records').text(data.number_of_records);
        $('#total-no-of-records').text(data.number_of_records);

        // Clear existing rows in the tbody
        $('#tbl-sales tbody').empty();

        // Iterate over the received data and append rows to the tbody
        $.each(data.transactions, function(index, transaction) {
            // Accessing data within each item
            var TransactionData = transaction.transaction_data;
            var TransactionId = transaction.transaction_id
            /*
            customer_id: str
            customer_name: Optional[str] = None
            sales_date: str
            payment_method: Optional[str] = None
            discount: Optional[str] = None
            amount_received: float = 0.00
            added_by: Optional[str] = None
            entry_date: Optional[str] = None*/

            // Append a new row to the tbody:
            $('#tbl-sales tbody').append(`
                <tr>
                    <td>${index + 1}</td>
                    <td>${TransactionData.customer_name}</td>
                    <td>${TransactionData.amount_received}</td>
                    <td>${TransactionData.plan}</td>
                    <td>${TransactionData.discount}</td>
                    <td>${TransactionData.payment_method}</td>
                    <td>${TransactionData.added_by}</td>
                    <td>${TransactionData.sales_date}</td>

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



// On Page load:
 $(function() {
    // get list of customers:
    getListOfCustomers();

    // Attach a click event listener to the button:
    $('#btn-submit').click(function(event) {
      event.preventDefault(); // Prevent the default form submission
      createSaleTransaction(); // Call the AJAX request function
    });

    // Attach a click event listener to the customer dropdown:
    $('#customer').change(function() {
        // Get the selected value
        var customerId = $('#customer').val();

        // Fetch data based on the selected customer:
        getListOfCustomerTransactions(customerId);
    });

    // Attach a click event listener to the payment-method dropdown:
    $('#payment-method').change(function() {
        // Get the selected value
        var paymentMethod = $('#payment-method').val();
        var transactionDate = $('#sale-date').val();

        if (paymentMethod ==='M-Pesa'){
            $('#amount-received').prop('disabled', true);
            // set the value back to 0.00
            $('#amount-received').val(0.00);

            $('#m-pesa').show();

            // get list of all m-pesa transactions for the sales date selected:
            getMpesaTransactionsByDate(transactionDate);

        }else{
            $('#amount-received').prop('disabled', false);
            $('#m-pesa').hide();

        }

    });

    // Attach a click event listener to the transaction date selector:
    $('#sale-date').change(function() {
        // Get the selected value
        var transactionDate = $('#sale-date').val();
        var payment_method = $('#payment-method').val();

        //reset amount received to 0
        $('#amount-received').val(0.00);

        // get list of all m-pesa transactions for the sales date selected, if the payment method is m-pesa:
        if (payment_method === 'M-Pesa'){

            getMpesaTransactionsByDate(transactionDate);

        }

    });

    // Attach a click event listener to the m-pesa transaction dropdown:
    $('#transaction-ref').change(function() {
        // Get the selected value
        var paymentMethod = $('#payment-method').val();
        var transactionAmount = $('#transaction-ref').val();

        if (paymentMethod ==='M-Pesa'){

            // set the value to show the transaction amount selected:
            $('#amount-received').val(transactionAmount);

            }

    });


  });


 // Function to Create a Sale:
function createSaleTransaction() {

    // Get the values of the form fields
    var sale_date = $('#sale-date').val();
    var payment_method = $('#payment-method').val();
    var customer_id = $('#customer').val();
    var discount_applied = $('#discount').val();
    var plan = $('#plan').val();
    var customer_name = $('#customer option:selected').text();
    var amount_received = $('#amount-received').val();
    var transaction_ref = $('#transaction-ref :selected').text();
    var are_you_sure = $('#are-you-sure').prop('checked');
    var create_attendance_record = $('#create-attendance-record-for-today').prop('checked');


    var button = $('#btn-submit');

    // Check if any of the fields below are empty:
    if (!sale_date || !customer_name) {
      // Display an error message or perform any other necessary action
      $('#error-message').text('Sales date, and customer fields are mandatory.');
      $('#error-message').show();
      return; // Exit the function to prevent the form submission
    }

    // Validate the drop-downs:
    if (plan === 'no-plan-selected' || payment_method === 'no-payment-method-selected') {
      // Display an error message or perform any other necessary action
      $('#error-message').text('Please select a valid plan, and/or select a valid payment method.');
      $('#error-message').show();
      return; // Exit the function to prevent the form submission
    }

    // Validate the payment method drop-down
    if (payment_method === 'M-Pesa' &&  (transaction_ref === 'no-transaction-selected' || !transaction_ref)) {
      // Display an error message or perform any other necessary action
      $('#error-message').text('Please select a M-Pesa Transaction.');
      $('#error-message').show();
      return; // Exit the function to prevent the form submission
    }

    // Validate the amount-received fields:
    if (!amount_received || amount_received <= 0) {
      // Display an error message or perform any other necessary action
      $('#error-message').text('Amount must be greater than 0.00');
      $('#error-message').show();
      return; // Exit the function to prevent the form submission
    }

    // console.log(amount_received);

    // Create FormData object with form input values
    var formData = new FormData();
    formData.append('sale_date', sale_date);
    formData.append('payment_method', payment_method);
    formData.append('customer_id', customer_id);
    formData.append('customer_name', customer_name);
    formData.append('amount_received', amount_received);
    formData.append('transaction_ref', transaction_ref);
    formData.append('discount_applied', discount_applied);
    formData.append('plan', plan);
    formData.append('are_you_sure', are_you_sure);
    formData.append('create_attendance_record', create_attendance_record)

    $.ajax({
      url: '/transactions/transaction',
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

        var message = $('#success-message');
        message.text(data.message + ". Sale reference "+ data.doc_id);
        message.show();
        $('#error-message').hide();

        // update the table grid:
        var customerId = $('#customer').val();

        // Fetch data based on the selected value:
        getListOfCustomerTransactions(customerId);

      },
      error: function(xhr, status, error) {
        // Handle the error response
        // console.log('Error Response:', xhr, status, error);
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


 // Function to get list of sales by customer:
function getListOfCustomerTransactions(customerId) {

    $.ajax({
      url: '/transactions/customer/json?customer_id=' + customerId,
      type: 'GET',
      beforeSend: function() {
        // Show progress indicator or disable the button if needed

      },
      success: function(data) {
        // Handle the success response
        // console.log('Success Response:', data);

        // set the number of records values:
        $('#no-of-records').text(data.number_of_records);
        $('#total-no-of-records').text(data.number_of_records);

        // Clear existing rows in the tbody
        $('#tbl-sales-by-customer tbody').empty();

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
            $('#tbl-sales-by-customer tbody').append(`
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
        // console.log('Error Response:', xhr, status, error);
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


// Function to get transactions by date:
function getMpesaTransactionsByDate(transactionDate) {

    $.ajax({
      url: '/m-pesa-transactions/' + transactionDate + '/json',
      type: 'GET',
      beforeSend: function() {
        // Show progress indicator or disable the button if needed

      },
      success: function(data) {
        // Handle the success response
        // console.log('Success Response:', data);

        var transactionRef = $('#transaction-ref');
        transactionRef.empty();
        transactionRef.append(`<option value="0.00" selected="">Select an M-Pesa Transaction</option>`);

        // Iterate over the received data and append rows to the tbody
        $.each(data.transactions, function(index, transaction) {
            // Accessing data within each item
            var TransactionData = transaction.transaction_data.request;
            var TransactionId = transaction.transaction_id

            transactionRef.append('<option value="'
            + TransactionData.TransAmount + '">(' + TransactionData.TransAmount + ') '
            + TransactionData.FirstName
            + ' (' + TransactionData.MSISDN + ') ' + TransactionData.TransID
            + '</option>');

        });

      },
      error: function(xhr, status, error) {
        // Handle the error response
        // console.log('Error Response:', xhr, status, error);
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

// On Page load:
 $(function() {

    // get all customers
    getCustomers();

    // Use event delegation to handle "Edit" and "Cancel" and "Update" button clicks:
    $('#customers').on('click', '.edit-row', function () {
        var row = $(this).closest('tr');

        // Iterate over the fields and replace text with input elements
        row.find('.edit-field').each(function () {
            var originalValue = $(this).text();

            // Store the original value in the data attribute:
            $(this).data('original-value', originalValue);

            // Replace text with input element
            $(this).html(`<input type="text" class="form-control edit-input" value="${originalValue}">`);

        });

        row.find('.edit-row').hide();
        row.find('.update-row, .cancel-edit').show();
    });

    // Cancel button click event:
    $('#customers').on('click', '.cancel-edit', function () {
        var row = $(this).closest('tr');

        // Restore original values from data attributes or initial values
        row.find('.edit-field').each(function () {
            //
            var originalValue = $(this).data('original-value');

            if (originalValue !== undefined) {
                // Restore original text content
                $(this).text(originalValue);
            } else {
                // If original value is not present, use input value
                $(this).text($(this).find('.edit-input').val());
            }
        });

        row.find('.update-row, .cancel-edit').hide();
        row.find('.edit-row').show();
    });


  });


 // Function to Create a Customer:
function getCustomers() {

    $.ajax({
      url: '/customers-overview/json',
      type: 'GET',
      beforeSend: function() {
        // Show progress indicator or disable the button if needed


      },
      success: function(data) {
        // Handle the success response
        console.log('Success Response:', data);

        // Clear existing rows in the tbody
        $('#customers tbody').empty();

        // set the number of records values:
        $('#no-of-records').text(data.number_of_customers);
        $('#total-no-of-records').text(data.number_of_customers);

        // Iterate over the received data and append rows to the tbody
        $.each(data.customers, function(index, customer) {
            let balanceHtml;

            // Set the styling based on the balance
            if (customer.total_unearned_amount == 0) {
                balanceHtml = `<td><span class="fw-bold text-warning">${customer.total_unearned_amount}</span></td>`;
            } else if (customer.total_unearned_amount > 0) {
                balanceHtml = `<td><span class="fw-bold text-success">${customer.total_unearned_amount}</span></td>`;
            } else {
                balanceHtml = `<td><span class="fw-bold text-danger">${customer.total_unearned_amount}</span></td>`;
            }

            // Append a new row to the tbody
            $('#customers tbody').append(`
                <tr data-doc-id=${customer.customer_id}>
                    <td>${index + 1}</td>
                    <td class="edit-field">${customer.first_name} ${customer.last_name}</td>
                    <td class="edit-field">${customer.gender}</td>
                    <td class="edit-field">${customer.phone}</td>
                    <td class="edit-field">${customer.email}</td>
                    <td>${customer.total_amount_received}</td>
                    ${balanceHtml} <!-- Append the balance HTML here -->
                    <td class="edit-field">${customer.city}</td>
                    <td class="edit-field">${customer.source}</td>
                    <td>
                        <button class="btn btn-link text-dark dropdown-toggle dropdown-toggle-split m-0 p-0 edit-row">Edit</button>
                        <button class="btn btn-success btn-sm m-0 update-row">Update</button>
                        <button class="btn btn-danger btn-sm m-0 cancel-edit">Cancel</button>
                    </td>
                </tr>
            `);

            // Hide update and cancel buttons initially
            $('.update-row, .cancel-edit').hide();
        });


      },
      error: function(xhr, status, error) {
        // Handle the error response
        console.log('Error Response:', xhr, status, error);
        var errorMessage;

        // set the error message:
        errorMessage = error + JSON.parse(xhr.responseText).error;

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


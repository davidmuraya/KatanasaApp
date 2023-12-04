// On Page load:
 $(function() {

    // get all customers
    getUsers();

    // Use event delegation to handle "Edit" and "Cancel" and "Update" button clicks:
    $('#tbl-users').on('click', '.edit-row', function () {
        var row = $(this).closest('tr');

        // Iterate over the fields and replace text with input elements
        row.find('.edit-field').each(function () {
            var originalValue = $(this).text();

            // Store the original value in the data attribute:
            $(this).data('original-value', originalValue);

            // Replace text with input element
            $(this).html(`<input type="text" class="form-control edit-input" value="${originalValue}">
            `);
        });

        // Iterate over the fields and replace text with checkbox elements
        row.find('.edit-checkbox').each(function () {
            var originalValue = $(this).text();

            // Store the original value in the data attribute:
            $(this).data('original-value', originalValue);

            if (originalValue.toLowerCase() === "true"){
                $(this).html(`<input type="checkbox" class="form-check-input" checked>`);
            }else {
                $(this).html(`<input type="checkbox" class="form-check-input">`);
            }

        });

        row.find('.edit-row').hide();
        row.find('.update-row, .cancel-edit').show();
    });

    // Cancel button click event:
    $('#tbl-users').on('click', '.cancel-edit', function () {
        var row = $(this).closest('tr');

        // Restore original values from data attributes or initial values
        row.find('.edit-field').each(function () {
            var originalValue = $(this).data('original-value');

            if (originalValue !== undefined) {
                // Restore original text content
                $(this).text(originalValue);
            } else {
                // If original value is not present, use input value
                $(this).text($(this).find('.edit-input').val());
            }
        });

        // Restore original values from data attributes
        row.find('.edit-checkbox').each(function () {

            var originalValue = $(this).data('original-value');
            var checkbox = $(this).find('.form-check-input');

            if (originalValue !== undefined) {
                // Restore original text content
                $(this).text(originalValue);
            } else {
                // If original value is not present, use checkbox value
                $(this).text(checkbox.prop('checked'));
            }

        });

        row.find('.update-row, .cancel-edit').hide();
        row.find('.edit-row').show();
    });

  });


 // Function to get all Users:
function getUsers() {

    $.ajax({
      url: '/users/json',
      type: 'GET',
      beforeSend: function() {
        // Show progress indicator or disable the button if needed


      },
      success: function(data) {
        // Handle the success response
        //console.log('Success Response:', data);

        // Clear existing rows in the tbody
        $('#tbl-users tbody').empty();

        // set the number of records values:
        $('#no-of-records').text(data.number_of_users);
        $('#total-no-of-records').text(data.number_of_users);

        // Iterate over the received data and append rows to the tbody
        $.each(data.users, function(index, user) {
            // Accessing data within each item
            var userData = user.user_data;
            var userId = user.user_id

            // Append a new row to the tbody
            $('#tbl-users tbody').append(`
                <tr>
                    <td>${index + 1}</td>
                    <td>${userData.username}</td>
                    <td class="edit-field">${userData.password}</td>
                    <td class="edit-checkbox">${userData.read_only}</td>
                    <td>${userId}</td>
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
        errorMessage = error +": "+ JSON.parse(xhr.responseText).error;

        // Clear existing rows in the tbody
        $('#tbl-users tbody').empty();

        // Append a new row to the tbody and the add the error:
        $('#tbl-users tbody').append(`
            <tr>
                <td class="text-center align-middle" colspan="6">
                    <span class="text-danger">${errorMessage}</span>
                </td>
            </tr>
        `);

      },
      complete: function() {
        // Perform any necessary cleanup or UI updates


      }
    });
  }


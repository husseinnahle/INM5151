$(document).ready(function () {
    $('.editbtn').click(function () {
        var currentTD = $(this).parents('tr').find('td');
        if ($(this).html() == 'Edit') {                  
            $.each(currentTD, function () {
                $(this).prop('contenteditable', true)
            });
        } else {
           $.each(currentTD, function () {
                $(this).prop('contenteditable', false)
            });
        }

        $(this).html($(this).html() == 'Edit' ? 'Save' : 'Edit')

    });

});
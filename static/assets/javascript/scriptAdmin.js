$(document).ready(function(){
    $(".add-row").click(function(){
        var Username = $("#Username").val();
        var Email = $("#Emaill").val();
        var Type = $("#Type").val();
        var Status = $("#Status").val();
        var markup = "<tr><td><input type='checkbox' Username ='record'></td><td>" + Username + "</td><td>" 
                                + Email + Type  + "</td><td>" + Status + "</td></tr>";
        $("table tbody").append(markup);
    });
    
    // Find and remove selected table rows
    $(".delete-row").click(function(){
        $("table tbody").find('input[name="record"]').each(function(){
            if($(this).is(":checked")){
                $(this).parents("tr").remove();
            }
        });
    });
});
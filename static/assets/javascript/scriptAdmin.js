$(document).ready(function(){
    $(".add-row").click(function(){
        var Username = $("#Username").val();
        var Email = $("#Email").val();
        var Type = $("#Type").val();
        var Status = $("#Status").val();
        var markup = "<tr><td><input type='checkbox' name ='record'></td><td>" + Username + "</td><td>" 
                                + Email +"</td><td>" + Type  + "</td><td>" + Status + "</td>" +
                                "<td> <button type=\"button\" id=\"editBtn\">Edit</button></td></tr>" +
                                "<td> <button type=\"button\" class=\"delete-row\" id=\"editBtn\">Delete</button></td>";
        $("table tbody").append(markup);
    });
    
    // Find and remove selected table rows
    $(".delete-rows").click(function(){
        $("table tbody").find('input[name="record"]').each(function(){
            if($(this).is(":checked")){
                $(this).parents("tr").remove();
            }
        });
    });

     // Find and remove selected table rows
     $(".delete-row").click(function(){

        var id =$(this).parents("tr").attr("id");
        fetch('/api/compteA/supprimer?id=' + id)
        .then(function (response) {
          return response.text();
        })
      
        $(this).parents("tr").remove();
            
    });
});
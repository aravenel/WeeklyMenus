//Date picker
$(document).ready(function(){

    //Helper functions for CSRF annoyances
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


    //Functions to add new recipes to modal
    function get_recipe_data(input_data, callback){
        console.log("Getting recipe data for menu item " + input_data.menuitem_id);
        $.ajax({
            url:'/recipes/get_recipe_data',
            dataType:'json',
            type:'GET',
            data: {'menuitem_id': input_data.menuitem_id},
            success: function(data, ret_code, jqHXR){
                var base_id = "#" + input_data.menu_id + "_" + input_data.menu_date + "_" + input_data.menu_type;
                callback(base_id, data);
            },
            error: function(jqHXR, textStatus, errorThrown){
                var msg = '<div class="alert alert-error">'+ errorThrown + '</div>';
                $('.ajax_errors').append(msg);
                return null;
            },
        });
    };
    function add_recipe(data) {
        get_recipe_data(data, function(base_id, recipe_data) {

            //Update the modal
            var recipe_html_modal = '<li class="span4"><div class="thumbnail">' +
                '<img src="' + recipe_data.thumbnail_large + '" width="300" height="200" float="top"\\>'+
                '<div class="caption"><p>' + recipe_data.title + '</p>'+
                '<a class="btn btn-danger recipe_delete" data-dismiss="alert" recipe_id="'+
                recipe_data.id + '">Delete from menu</a></div></div></li>';
            if ($('.reciperow:last ul .span4').length >= 3){
                console.log('Already three recipes in last row--adding new.');
                var newrow = '<div class="row-fluid reciperow"><ul class="thumbnails"></ul></div>';
                $('#recipes').append(newrow);
            }
            $('.reciperow:last .thumbnails').append(recipe_html_modal);

            //Update the base page
            var recipe_html_base = '<div style="margin-top:5px;">' +
                '<div class="media clearfix"><div class="pull-left">'+
                '<img src="'+recipe_data.thumbnail_small+'" width="50" height="50" \\>'+
                '</div><div class="media-body">'+recipe_data.title+'</div></div></div>';
            $(base_id).append(recipe_html_base);

        });
    };


    //Datepicker code
    $('.datepicker').datepicker({
        format: 'mm/dd/yyyy'
    }).on('changeDate', function(ev){
        $(this).datepicker('hide');
    });

    //Modal config
    $('[data-toggle="modal"]').click(function(e) {
        e.preventDefault();
        var url = $(this).attr('href');
        if (url.indexOf('#') == 0) {
            $(url).modal('open');
        } else {
            $.get(url, function(data) {
                $('<div class="modal hide fade">' + data + '</div>').modal({
                    width: 940,
                });
            });
        }
    });

    //Recipe delete ajax
    $(document).on("click", ".recipe_delete", function(event){
        event.preventDefault();
        recipe_id = $(this).attr('recipe_id');
        li_item = $(this).closest('li .span4');
        $.ajax({
            url:'/menus/ajax_delete/',
            dataType: 'json',
            type: 'POST',
            data: {'menuitem_id': recipe_id},
            success: function(data, ret_code, jqHXR){
                li_item.remove();
            },
            error: function(jqHXR, textStatus, errorThrown){
                var msg = '<div class="alert alert-error">'+ errorThrown + '</div>';
                $('.ajax_errors').append(msg);
            },
        });
    });

    //Autocomplete
    $(document).on("focus", ".autocomplete", function(event){
        if (!$(this).data("autocomplete")) {
            $(this).autocomplete({
                autoFocus: true,
                minLength: 2,
                source: function(request, response) { //Fetch matches via AJAX
                    $.ajax({
                        url: '/recipes/ajax_search',
                        dataType: 'json',
                        data: {'term': request.term},
                        success: function(data, ret_code, jqXHR) {
                            response(data);
                        },
                    });
                },
                response: function(event, ui){  //If no matches, give option to create new recipe
                    if (ui.content.length === 0){
                        ui.content.push({
                            'value': $('.autocomplete').val(),
                            'label': 'Add new recipe: '+$('.autocomplete').val(),
                        });
                    }
                },
                select: function(event, ui) { //When option selected, add to menu via AJAX
                    event.preventDefault();
                    var menu_id = $('#menu_id').val();
                    var menu_date = $('#menu_date').val();
                    var menu_type = $('#menu_type').val();
                    $.ajax({
                        url: '/menus/ajax_add_to_menu/',
                        type: 'POST',
                        dataType: 'json',
                        data: {
                            'recipe_id': ui.item.value,
                            'menu_id': menu_id,
                            'menu_date': menu_date,
                            'menu_type': menu_type,
                        },
                        success: function(data, ret_code, jqHXR){
                            add_recipe(data);
                            $('#no_recipe_warning').remove();
                            $('.autocomplete').val(null);
                        },
                        error: function(jqXHR, textStatus, errorThrown) {
                            var msg = '<div class="alert alert-error">'+ errorThrown + '</div>';
                            $('.ajax_errors').append(msg);
                        },
                    });
                },
            });
        }
    });

});

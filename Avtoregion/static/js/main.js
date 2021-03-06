// This function gets cookie with a given name
function getCookie(name)
{
    var cookieValue = null;
    if (document.cookie && document.cookie != '')
    {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++)
        {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '='))
            {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/*
The functions below will create a header with csrftoken
*/
function csrfSafeMethod(method)
{
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url)
{
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

function reserv()
{
    localStorage.setItem('id_race_date', $('#id_race_date').val());
    localStorage.setItem('id_arrival_time', $('#id_arrival_time').val());
    localStorage.setItem('id_ttn_number', $('#id_ttn_number').val());
    localStorage.setItem('id_car', $('#id_car').val());
    localStorage.setItem('id_driver', $('#id_driver').val());
    localStorage.setItem('id_type_ship', $('#id_type_ship').val());
    localStorage.setItem('id_supplier', $('#id_supplier').val());
    localStorage.setItem('id_place_load', $('#id_place_load').val());
    localStorage.setItem('id_customer', $('#id_customer').val());
    localStorage.setItem('id_order_type_race', $('#id_order_type_race').val());
    localStorage.setItem('id_shipment', $('#id_shipment').val());
    localStorage.setItem('id_product', $('#id_product').val());
    localStorage.setItem('id_s_milage', $('#id_s_milage').val());
    localStorage.setItem('id_e_milage', $('#id_e_milage').val());
    localStorage.setItem('id_weight_load', $('#id_weight_load').val());
    localStorage.setItem('id_unit_load', $('#id_unit_load').val());
    localStorage.setItem('id_weight_unload', $('#id_weight_unload').val());
    localStorage.setItem('id_unit_unload', $('#id_unit_unload').val());
    localStorage.setItem('id_comm', $('#id_comm').val());
    localStorage.setItem('id_state', $('#id_state').val());
    localStorage.setItem('id_gas_start', $('#id_gas_start').val());
    localStorage.setItem('id_gas_end', $('#id_gas_end').val());
    localStorage.setItem('id_gas_given', $('#id_gas_given').val());
    localStorage.setItem('id_shoulder', $('#id_shoulder').val());
    localStorage.setItem('id_count', $('#id_count').val());
    localStorage.setItem('id_price', $('#id_price').val());
}

function reestablish()
{
    for(var i=0, len=localStorage.length; i<len; i++){
        var key = localStorage.key(i);
        var value = localStorage[key];
        $('#'+key).val(value)
    }

}

function getfile()
{
    var csrftoken = getCookie('csrftoken');
    var url = $('#excel').attr('data-url');

    // Data to post
    function html2json()
    {
        var json = '{';
        var otArr = [];
        var tbl2 = $('#tab_body tr').each(function (i)
        {
            x = $(this).children();
            var itArr = [];
            x.each(function ()
            {
                itArr.push('"' + $(this).text() + '"');
            });
            otArr.push('"' + i + '": [' + itArr.join(',') + ']');
        });
        otArr.push('"org": "' + $('#organization').text().replace(/"/g, "\\\"") + '"');
        otArr.push('"start_date": "' + $('#start_date').text() + '"');
        otArr.push('"end_date": "' + $('#end_date').text() + '"');
        json += otArr.join(",") + '}';

        return json;
    }

    var $data = html2json();

    // Use XMLHttpRequest instead of Jquery $ajax
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function ()
    {
        var a;
        if (xhttp.readyState === 4 && xhttp.status === 200)
        {
            // Trick for making downloadable link
            a = document.createElement('a');
            a.href = window.URL.createObjectURL(xhttp.response);
            // Give filename you wish to download
            a.download = "file.xlsx";
            a.style.display = 'none';
            document.body.appendChild(a);
            a.click();
        }
    };
    // Post data to URL which handles post request
    xhttp.open("POST", url);
    xhttp.setRequestHeader("Content-Type", "application/json");
    if (!csrfSafeMethod("POST") && sameOrigin(url))
    {
        xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    }
    // You should set responseType as blob for binary responses
    xhttp.responseType = 'blob';
    xhttp.send(JSON.stringify($data));
}

$(function ()
{
    var csrftoken = getCookie('csrftoken');


    $.ajaxSetup({
        beforeSend: function (xhr, settings)
        {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url))
            {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

        $('#account-form').on('submit', function (event)
        {
            event.preventDefault();
            var $form = $("#account-form");
            var $daterange = $form.find("#account_daterange").val();
            var $type = $form.find("#account_type option:selected").val();
            var $service = $form.find("#account_service option:selected").val();
            var $supplier = $form.find("#account_supplier option:selected").val();
            var $mediator = $form.find("#account_mediator option:selected").val();
            var $customer = $form.find("#account_customer option:selected").val();
            var $load_place = $form.find("#account_load_place option:selected").val();
            var $unload_place = $form.find("#account_unload_place option:selected").val();
            var $product = $form.find("#account_product").val();
            var $state = $form.find("#account_state option:selected").val();

            if (typeof(Storage) !== "undefined")
            {
                sessionStorage.setItem('daterange', $daterange);
                sessionStorage.setItem('type', $type);
                sessionStorage.setItem('service', $service);
                sessionStorage.setItem('supplier', $supplier);
                sessionStorage.setItem('mediator', $mediator);
                sessionStorage.setItem('customer', $customer);
                sessionStorage.setItem('load_place', $load_place);
                sessionStorage.setItem('unload_place', $unload_place);
                sessionStorage.setItem('product', $product);
                sessionStorage.setItem('state', $state);
            }

            var data = {
                daterange: $daterange,
                type: $type,
                service: $service,
                supplier: $supplier,
                mediator: $mediator,
                customer: $customer,
                load_place: $load_place,
                unload_place: $unload_place,
                product: $product,
                state: $state
            };


            $.post({
                url: $form.attr('action'),
                traditional: true,
                data: JSON.stringify(data),
                success: function (resp)
                {
                    $('#tab_res').html(resp['data']);
                    $('.toggle-toolbar').collapse('toggle');
                }


            });
        });

    $(document).on("click", '#delete_race_ok', function (event)
    {
        $('#delete_race_ok')[0].disabled = true;
        event.preventDefault();

        var rows = document.getElementsByClassName('selected'),
            list = [],
            url = $('#delete_race').attr('data-url');
        for (var i = 0; i < rows.length; ++i)
        {
            list.push(rows[i].id);
        }
        $.ajax(
            {
                url: url,
                method: 'POST',
                traditional: true,
                data: JSON.stringify({"id_list": list}),
                dataType: 'json',
                success: function (resp)
                {
                    if (resp['data'] === 'success')
                    {
                        $('#id_modal_message').html('<p>Успешно удалено!</p>');
                    }
                    else
                    {
                        $('#id_modal_message').html('<p>У вас нет прав!</p>')
                    }
                }
            })
    });


    $(document).on('click', '#change_race', function (event)
    {
        event.preventDefault();
        var rows = document.getElementsByClassName('selected');
        if (rows.length > 1)
        {
            $('#id_modal_update').html('Выбрано слишком много рейсов, выбирать для редактирования можно только один!');
            $race_table.bootstrapTable('uncheckAll');
            $('#ModalUpdateRace').modal('show');
        }
        else if (rows.length === 1)
        {
            window.location.href = '/Race/update/' + rows[0].id + '/';
        }
    });

    $(document).on("click", '#update_state_ok', function (event)
    {
        $('#update_state_ok')[0].disabled = true;
        event.preventDefault();
        var url = $('#update_state').attr('data-url'),
            rows = document.getElementsByClassName('selected'),
            list = [];
        for (var i = 0; i < rows.length; ++i)
        {
            list.push(rows[i].id);
        }
        var state = $('#status_select option:selected').text();
        $.ajax(
            {
                url: url,
                method: 'POST',
                traditional: true,
                data: JSON.stringify({"id_list": list, "state": state}),
                dataType: 'json',
                success: function ()
                {
                    $('#modal-body-state').html('<p>Всё обновлено!</p>');
                }
            })
    });
    $(document).on("click", '#packing_list', function (event)
    {
        event.preventDefault();
        var url = $('#ModalPackingList').attr('data-url');
        var rows = document.getElementsByClassName('selected'),
            list = [];
        for (var i = 0; i < rows.length; ++i)
        {
            list.push(rows[i].id);
        }
        $.ajax(
            {
                url: url,
                method: 'POST',
                traditional: true,
                data: JSON.stringify({"id_list": list}),
                dataType: 'json',
                success: function (data)
                {
                    $('#result_pack').html(data['data']);
                    $('#ModalPackingList').modal('show');
                }
            })
    });
    $(document).on("click", '#way_list', function (event)
    {
        event.preventDefault();
        var url = $('#ModalWayList').attr('data-url');
        var rows = document.getElementsByClassName('selected'),
            list = [];
        for (var i = 0; i < rows.length; ++i)
        {
            list.push(rows[i].id);
        }
        $.ajax(
            {
                url: url,
                method: 'POST',
                traditional: true,
                data: JSON.stringify({"id_list": list}),
                dataType: 'json',
                success: function (data)
                {
                    $('#result_way').html(data['data']);
                    $('#ModalWayList').modal('show');
                }
            })
    });
    $('#id_supplier').change(function ()
    {
        var url = $('#id_race_form').attr('data-form-supplier-url');
        var supplierId = $(this).val();
        var place_load = $('#id_place_load');

        $.ajax(
            {
                type: "GET",
                url: url,
                data: {
                    'id': supplierId
                },
                dataType: 'json',
                success: function (resp)
                {
                    place_load.empty();
                    for (i = 0; i < resp.length; i++)
                    {
                        var option = '<option value="' + resp[i].id_load_place + '">' + resp[i].address + '</option>';
                        place_load.append(option);
                    }
                }


            });
    });

    $("#id_customer").change(function ()
    {
        var url = $('#id_race_form').attr('data-form-customer-url');
        var customerId = $(this).val();
        var place_unload = $('#id_shipment');
        $.ajax(
            {
                type: "GET",
                url: url,
                data: {
                    'id': customerId
                },
                dataType: 'json',
                success: function (resp)
                {
                    place_unload.empty();
                    for (var i = 0; i < resp.length; i++)
                    {
                        var option = '<option value="' + resp[i].id_shipment + '">' + resp[i].name + '</option>';
                        place_unload.append(option)
                    }
                }
            })
    });
// Same behavior of enter like tab
    $(document).keydown(function (e)
    {

        // Set self as the current item in focus
        var self = $(':focus'),
            // Set the form by the current item in focus
            form = self.parents('form:eq(0)'),
            focusable;

        // Array of Indexable/Tab-able items
        focusable = form.find('input,select,button,a,textarea,div[contenteditable=true]').filter(':visible');

        function enterKey()
        {
            if (e.which === 13 && !self.is('div[contenteditable=true]'))
            { // [Enter] key

                // If not a regular hyperlink/button
                if ($.inArray(self, focusable) && (!self.is('a,button')))
                {
                    // Then prevent the default [Enter] key behaviour from submitting the form
                    e.preventDefault();
                } // Otherwise follow the link/button as by design

                // Focus on the next item (either previous or next depending on shift)
                focusable.eq(focusable.index(self) + (e.shiftKey ? -1 : 1)).focus().select();

                return false;
            }
        }

        // We need to capture the [Shift] key and check the [Enter] key either way.
        if (e.shiftKey)
        {
            enterKey()
        } else
        {
            enterKey()
        }
    });

    $(document).on('click', '.delete-confirmation', function ()
    {
        return confirm('Вы уверены, что хотите удалить?');
    });

    $('.dropdown-toggle').dropdown();
});


/*"responsive":    {
    breakpoints: [
        {name: 'bigdesktop', width: Infinity},
        {name: 'meddesktop', width: 1480},
        {name: 'smalldesktop', width: 1280},
        {name: 'medium', width: 1188},
        {name: 'tabletl', width: 1024},
        {name: 'btwtabllandp', width: 848},
        {name: 'tabletp', width: 768},
        {name: 'mobilel', width: 480},
        {name: 'mobilep', width: 320}
    ]
},*/

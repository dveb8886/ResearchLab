
function create_toggle_func(checkbox){
    checkbox.change(function(){
        checkbox.toggleClass('changed');
//        console.log(checkbox.prop('checked'));    // test if a checkbox is checked
    });
}

function search_users(){
    var query = $('.search input').val();
    var resource = $('.search').attr('resource');
    if (query.length == 0){
        query = "*"
    }
    $.ajax({
        url: "/account/search_users/"+query+"/"+resource,
        type: "GET",
        contentType: 'application/json',
        success: function(response){
            console.log(response);
            var table = $('#user-list tbody');
            table.html('');
            table.append($('#user-header-sample tbody').html());

            var h_role = $('.h-role', table);
            var role_tr = $('tr', table)[0];
            var role_sequence = [];
            for (role in response.roles) {
                role = response.roles[role];
                new_h_role = h_role.clone();
                new_h_role.html(role.name);
                role_tr.append(new_h_role[0]);
                role_sequence.push(role.id);
            }
            h_role.remove();

            var user_html_sample = $('#user-row-sample tbody').html();
            for (user in response.users) {
                user = response.users[user]
                table.append(user_html_sample);
                var user_row = $('.table-row', table).last();
                $('.user-name', user_row).html(user.name);
                user_row.attr('user', user.id)

                var user_role_th = $('.user-role', user_row);

                for (idx in response.roles){
                    role = response.roles[idx];
                    role_id = role_sequence[idx];
                    new_user_role_th = user_role_th.clone();
                    checkbox = $('input', new_user_role_th);
                    checkbox.attr('role', role_id);
                    if (user.roles[role_id] == true){
                        checkbox.attr('checked', true);
                    }
                    user_row.append(new_user_role_th[0]);

                    create_toggle_func(checkbox);
                }
                user_role_th.remove();
            }
        }
    });
}

function save_roles(){
    body = {users: []};
    user_list = $('#user-list .table-row');

    user_list.each(function(idx, user_row){
        user = {roles: []};
        roles = $('.user-role input', user_row);
        changed = false;
        console.log('roles: ')
        console.log(roles);

        roles.each(function(idx, checkbox){
            checkbox = $(checkbox)
            console.log('checkbox: ')
            console.log(checkbox);
            is_role_changed = checkbox.hasClass('changed');
            if (is_role_changed){
                changed = true;
                user.roles.push({
                    id: parseInt(checkbox.attr('role')),
                    state: checkbox.prop('checked')
                });
            }
        });

        if (changed){
            user.id = $(user_row).attr('user');
            body.users.push(user);
        }
    });

    console.log(body);

    $.ajax({
        url: "/account/save_roles",
        type: "POST",
        data: JSON.stringify(body),
        contentType: 'application/json',
        success: function(response){

        }
    });


}

// Runs when the page is fully loaded
window.addEventListener('load', function(){

    search_users();

    $('.search button').click(function(){
        search_users();
    });

    $('.btn-save-roles').click(function(){
        save_roles();
    })

})

$(document).ready(function() {

    $('#bugs-table').DataTable({
        'iDisplayLength': 50,
        'order': [
            [0, 'desc'],
        ],
    });
});

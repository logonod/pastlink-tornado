function hide_all() {
    $('#hot-topics').hide();
    $('#hot-links').hide();
    $('#new-topics').hide();
    $('#new-links').hide();
}


function display(id) {
    hide_all();
    $('#'+id).show();
}
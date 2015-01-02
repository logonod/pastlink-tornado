function trim(str) {
  return str.replace(/(^\s+)|(\s+$)/g, "");
}


$(document)
.ready(function() {

    function add_topic() {
        var title = trim($("#new-topic-title").val());
        var abstract = trim($("#new-topic-abstract").val());
        var _xsrf = $( "input[name='_xsrf']").val();
        var top_status = 0;
        if ($("#top_status").is(':checked')) {
            top_status = 1;
        }
        var msg = $("#error-message");
//        alert(title);
//        alert(abstract);
        if (title.length == 0) {
            msg.text("标题不能为空").show();
            return;
        }
        msg.text("添加中...").show();
        var new_topic = {"title": title,
            "abstract": abstract,
            "top_status": top_status,
            "_xsrf": _xsrf};
        var post = $.post( "/new/topic", new_topic, "json");
        post.success(function(data) {
                if (data.success === true) {
                    window.location.href=data.redirect;
                    return;
                }
                if (data.success === false) {
                    msg.text(data.info).show();
                }
            });
        post.error(function(){
                msg.text("请求错误，请稍后再试.").show();
            });

    }
    $('#add-topic').click(add_topic);

    $('.ui.checkbox').checkbox();
});
function trim(str) {
  return str.replace(/(^\s+)|(\s+$)/g, "");
}


$(document)
.ready(function() {

    function modify_password() {
        var old_password = trim($("#old-password").val());
        var new_password_1 = trim($("#new-password-1").val());
        var new_password_2 = trim($("#new-password-2").val());
        var _xsrf = $( "input[name='_xsrf']").val();
        var msg = $("#error-message");
//        alert(title);
//        alert(abstract);
        if (old_password.length == 0 || new_password_1.length==0 || new_password_2.length==0) {
            msg.text("输入内容不能为空，请检查").show();
            return;
        }

        if (new_password_1 != new_password_2) {
            msg.text("新密码两次输入不相同，请检查").show();
            return;
        }

        if (new_password_1.length < 6) {
            msg.text("密码太短，至少6个字符！").show();
            return;
        }
        msg.text("修改中...").show();
        var new_password = {
            "old": old_password,
            "new": new_password_1,
            "_xsrf": _xsrf};
        var post = $.post( "/profile", new_password, "json");
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
    $('#modify-password').click(modify_password);
});
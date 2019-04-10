
//自定义js

//公共配置


$(document).ready(function () {

    // MetsiMenu
    $('#side-menu').metisMenu();

    // 打开右侧边栏
    $('.right-sidebar-toggle').click(function () {
        $('#right-sidebar').toggleClass('sidebar-open');
    });

    //固定菜单栏
    $(function () {
        $('.sidebar-collapse').slimScroll({
            height: '100%',
            railOpacity: 0.9,
            alwaysVisible: false
        });
    });


    // 菜单切换
    $('.navbar-minimalize').click(function () {
        $("body").toggleClass("mini-navbar");
        SmoothlyMenu();
    });


    // 侧边栏高度
    function fix_height() {
        var heightWithoutNavbar = $("body > #wrapper").height() - 61;
        $(".sidebard-panel").css("min-height", heightWithoutNavbar + "px");
    }
    fix_height();

    $(window).bind("load resize click scroll", function () {
        if (!$("body").hasClass('body-small')) {
            fix_height();
        }
    });

    //侧边栏滚动
    $(window).scroll(function () {
        if ($(window).scrollTop() > 0 && !$('body').hasClass('fixed-nav')) {
            $('#right-sidebar').addClass('sidebar-top');
        } else {
            $('#right-sidebar').removeClass('sidebar-top');
        }
    });

    $('.full-height-scroll').slimScroll({
        height: '100%'
    });

    $('#side-menu>li').click(function () {
        if ($('body').hasClass('mini-navbar')) {
            NavToggle();
        }
    });
    $('#side-menu>li li a').click(function () {
        if ($(window).width() < 769) {
            NavToggle();
        }
    });

    $('.nav-close').click(NavToggle);

    //ios浏览器兼容性处理
    if (/(iPhone|iPad|iPod|iOS)/i.test(navigator.userAgent)) {
        $('#content-main').css('overflow-y', 'auto');
    }

});

$(window).bind("load resize", function () {
    if ($(this).width() < 769) {
        $('body').addClass('mini-navbar');
        $('.navbar-static-side').fadeIn();
    }
});

function NavToggle() {
    $('.navbar-minimalize').trigger('click');
}

function SmoothlyMenu() {
    if (!$('body').hasClass('mini-navbar')) {
        $('#side-menu').hide();
        setTimeout(
            function () {
                $('#side-menu').fadeIn(500);
            }, 100);
    } else if ($('body').hasClass('fixed-sidebar')) {
        $('#side-menu').hide();
        setTimeout(
            function () {
                $('#side-menu').fadeIn(500);
            }, 300);
    } else {
        $('#side-menu').removeAttr('style');
    }
}

//刷新bootstrapTable
function refresh_table(table_id){
    $("#" + table_id).bootstrapTable('refresh');
}

//检查session
function check_session(){
    var url = '/check_session?' + new Date().getTime();
    $.ajax({
        url: url,
        type: 'POST',
        data: '',
        dataType: 'text',
        success:function(text){
            if(isNaN(text)){
                swal("操作失败", "会话超时，请重新登陆！", "error");
                $(window.location).attr('href', '/login');
            }else{
                if(parseInt(text) != 0){
                    swal("操作失败", "会话超时，请重新登陆！", "error");
                    $(window.location).attr('href', '/login');
                }
            }
        }
    });
}

//事件通知
$(function() {
    //设置显示配置
    var messageOpts = {
        //"closeButton" : true,//是否显示关闭按钮
        "debug" : false,//是否使用debug模式
        "positionClass" : "toast-bottom-right",//弹出窗的位置
        "onclick" : null,
        "showDuration" : "300",//显示的动画时间
        "hideDuration" : "1000",//消失的动画时间
        "timeOut" : "10000",//展现时间
        "extendedTimeOut" : "1000",//加长展示时间
        "showEasing" : "swing",//显示时的动画缓冲方式
        "hideEasing" : "linear",//消失时的动画缓冲方式
        "showMethod" : "fadeIn",//显示时的动画方式
        "hideMethod" : "fadeOut" //消失时的动画方式
    };
    toastr.options = messageOpts;
})

//循环检查是否有新的信息，邮件
function check_message(){
    var url = '/check_message?' + new Date().getTime();
    $.ajax({
        url: url,
        type: 'POST',
        data: '',
        dataType: 'json',
        success:function(text){
            $('#new_message').html(text);
            $('#total_message').html(text);
            if($('#chat_user_name').html()){
                receive_message();
            }
            //toastr.info('<samll class="text-muted">当前有 '+ text[0]['message_count'] +' 条来自 '+ text[0]['message_from'] +' 的未读信息！</samll>', '<h3>聊天</h3>')
        }
    });
    check_message_time = setTimeout(function(){check_message();},10000);
}

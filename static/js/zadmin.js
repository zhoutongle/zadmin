
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
                $(window.location).attr('href', '/lock_screen');
            }else{
                if(parseInt(text) != 0){
                    swal("操作失败", "会话超时，请重新登陆！", "error");
                    $(window.location).attr('href', '/lock_screen');
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

//清空form
function form_reset(id){
    document.getElementById(id).reset()
}

//create cookie
function getetCookieookie(p_value){
    if (document.cookie.length>0){
        c_start=document.cookie.indexOf(p_value + "=");
        if (c_start!=-1){
            c_start=c_start + p_value.length+1;
            c_end=document.cookie.indexOf(";",c_start);
            if (c_end==-1) c_end=document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
}

function setCookie(p_value,value,expiretime){
    var exdate=new Date();
    exdate.setDate(exdate.getTime()+expiretime);
    document.cookie=p_value+ "=" +escape(value)+((expiretime==null) ? "" : ";expires="+exdate.toUTCString());
}

//侧边栏根据url切换右边内容页面，根据自己的html来做修改
function urlchange() {
    var url = 'user_manager';
    var element = $('ul.nav a').filter(function () {
        return this.id.indexOf(url) >= 0;
    }).addClass('active').parent().parent().addClass('in').parent();
    if (element.is('li')) {
        element.addClass('active');
    }
}
/*
function custConfirm(title,message,buttons){
    var confdialog = $('<div id="confdialog" title="'+title+'" class="ui-state-error ui-corner-all" style="line-height:25px;"><p><span class="info-icon ui-icon ui-icon-alert"></span><strong
    var defbuttons = {
        Cancel: function() {
            $(this).dialog('close');
        },
        '确定': function() {
            $(this).dialog('close');
        }
    };
    confdialog.dialog({
        bgiframe: true,
        autoOpen: true,
        resizable: false,
        modal: true,
        width: 335,
        buttons: buttons || defbuttons,
        close: function(){
            confdialog.remove();
        }
    });
}

function custLoading(message){
    var loaddialog = $('<div id="loaddialog" title="" style="min-height:75px;"><p class="loadword" style="text-align:center">' + message + '</p><p style="background:url(/static/theme/redmon
    var flag = 0;
    loaddialog.dialog({
        bgiframe: true,
        autoOpen: true,
        resizable: false,
        modal: true,
        height: 130,
        width: 300,
        open: function(){
            $(this).parent().find('.ui-dialog-titlebar').hide();
            //flag = setInterval(getprocessing, 100);
            //getprocessing();
            flag = setInterval(set_second, 1000);
        },
        beforeclose: function(){
            clearInterval(flag);
        },
        close: function(){
            $(this).remove();
        }
    });
}

function custAlert(title,message,callback,options){
    var alertdialog = $('<div id="alertdialog" title="'+title+'"><p>'+message+'</p></div>').appendTo('body');
    alertdialog.dialog({
        bgiframe: true,
        autoOpen: true,
        resizable: false,
        modal: true,
        buttons: {
            '确定': function() {
                $(this).dialog('close');
                if(callback != undefined){
                    callback();
                }
            }
        },
        close: function(){
            alertdialog.remove();
            if(callback != undefined){
                callback();
            }
        }
    });
}

function custWarning(title,message,cancelcallback,comfirmcallback,options){
    var warningdialog = $('<div id="warningdialog" title="'+title+'"><p><span style="margin: 0pt 7px 20px 0pt; float: left;" class="ui-icon ui-icon-alert"/>' + message + '</p></div>').appen
    warningdialog.dialog({
        bgiframe: true,
        autoOpen: true,
        resizable: false,
        modal: true,
        buttons: {
            '取消': function() {
                $(this).dialog('close');
                if(cancelcallback != undefined){
                    cancelcallback();
                }
            },
            '确定': function() {
                $(this).dialog('close');
                if(comfirmcallback != undefined){
                    comfirmcallback();
                }
            }
        },
        close: function(){
            warningdialog.remove();
            //if(cancelcallback != undefined){
            //    cancelcallback();
            //}
        }
    });
}

function set_second(){
    var set_second = parseInt($('#set_second').html());
    set_second++;
    $('#set_second').html(set_second);
}

function custInfo(title,message,callback,options){
    var infodialog = $('<div id="infodialog" title="'+title+'"><p>'+message+'</p></div>').appendTo('body');
    infodialog.dialog({
        bgiframe: true,
        autoOpen: true,
        resizable: false,
        width: 'auto',
        modal: true,
        buttons: {
            '确定': function() {
                $(this).dialog('close');
                if(callback != undefined){
                    callback();
                }
            }
        },
        close: function(){
            infodialog.remove();
            if(callback != undefined){
                callback();
            }
        }
    });
}

function custPopup(title, message,callback){
    //var popupdialog = $('<div class="popup"></div>');
    var old_popup = $('.popup');
    if (old_popup){ old_popup.remove();}
    var popupdialog = $('<div class="popup" title="'+title+'"><p>'+message+'</p></div>').appendTo('body');
    popupdialog.dialog({
        dialogClass: 'myPopup',
        bgiframe: true,
        autoOpen: true,
        resizable: false,
        width: 300,
        height: 80,
        position: { my: "right bottom", at: "right bottom", of: window },
        //modal: true,
        close: function(){
            popupdialog.remove();
            if(callback != undefined){
                callback();
            }
        }
    });
}*/
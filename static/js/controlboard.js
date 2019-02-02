// 用户管理下拉框
function adminList() {
    if (!$('.header .header-body .header-user .login-ul .h-u-h-c-b').hasClass('show')) {
        $('.header .header-body .header-user .login-ul .h-u-h-c-b').addClass('show');
    } else {
        $('.header .header-body .header-user .login-ul .h-u-h-c-b').removeClass('show');
    }
}

// 关闭用户管理下拉框
function reList() {
    $('.header .header-body .header-user .login-ul .h-u-h-c-b').removeClass('show')
}

// 小飞机回到顶部
function showReposBtn() {
    var clientHeight = $(window).height() / 2;
    var scroll = $(document).scrollTop();
    if (scroll > clientHeight) {
        $('.suspension').show();
    } else {
        $('.suspension').hide();
    };
};
window.onload = function () {
    showReposBtn();
};
window.onscroll = function () {
    showReposBtn();
};

// 删除其余子元素的active类
function chosed(that) {
    that.firstElementChild.classList.add('active');
    $(that).parent().siblings().children('li').children('a.active').removeClass('active');
}
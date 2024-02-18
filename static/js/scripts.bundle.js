"use strict";
var AppConfig = AppConfig || {};
$(function () {
    AppConfig = {
        init: function () {
            AppConfig.langCheckedToApply(), AppConfig.initAppScrollbars(), AppConfig.initSlickCarousel(), AppConfig.search(), AppConfig.buttonClickEvents(), AppConfig.materialTab(), AppConfig.initCountdown(), AppConfig.addFavorite(), AppConfig.initTheme()
        }, initTheme: function () {
            $("body").themeSettings()
        }, langCheckedToApply: function () {
            var s = $("#lang .custom-control-input");
            s.on("change", function () {
                $("#langApply").prop("disabled", !s.filter(":checked").length)
            }).trigger("change")
        }, initAppScrollbars: function () {
            $('[data-scrollable="true"]').each(function () {
                new PerfectScrollbar(this, {
                    wheelSpeed: .5,
                    swipeEasing: !0,
                    wheelPropagation: !1,
                    minScrollbarLength: 40,
                    suppressScrollX: !0
                })
            })
        }, slickCarousel: function (s, t, e, i, a) {
            $(s).slick({
                arrows: !0,
                dots: !1,
                infinite: !1,
                slidesToShow: t,
                slidesToScroll: 1,
                speed: 1e3,
                prevArrow: '<button class="btn-prev btn btn-pill btn-air btn-default btn-icon-only"><i class="la la-angle-left"></i></button>',
                nextArrow: '<button class="btn-next btn btn-pill btn-air btn-default btn-icon-only"><i class="la la-angle-right"></i></button>',
                responsive: [{breakpoint: 1440, settings: {slidesToShow: e}}, {
                    breakpoint: 1200,
                    settings: {slidesToShow: i}
                }, {breakpoint: 640, settings: {slidesToShow: a}}, {
                    breakpoint: 380,
                    settings: {slidesToShow: 1, arrows: !1}
                }]
            })
        }, initSlickCarousel: function () {
            AppConfig.slickCarousel(".carousel-item-4", 4, 3, 2, 1), AppConfig.slickCarousel(".carousel-item-5", 5, 4, 3, 2), AppConfig.slickCarousel(".carousel-item-6", 6, 5, 4, 2)
        }, buttonClickEvents: function () {
            $("#toggleSidebar").on("click", function () {
                s.toggleClass("iconic-sidebar")
            }), $("#openSidebar").on("click", function (i) {
                i.stopPropagation(), s.removeClass("open-search"), s.addClass("open-sidebar"), e.addClass("show"), t.removeClass("show")
            }), $("#hideSidebar").on("click", function () {
                s.removeClass("open-sidebar"), e.removeClass("show")
            }), $("#playList").on("click", function () {
                s.toggleClass("open-right-sidebar")
            })
        }, search: function () {
            $("#searchForm").on("click", function (e) {
                e.stopPropagation(), s.addClass("open-search"), t.addClass("show")
            }), s.on("click", function () {
                s.removeClass("open-search"), t.removeClass("show")
            })
        }, materialTab: function () {
            var s = $(".line-tabs .nav-item .active"), t = $(".line-tabs .nav-item");
            $(".line-tabs").append("<span class='tabs-link-line'></span>");
            var e = s.position(), i = s.parent().width();
            $(".tabs-link-line").stop().css({width: i}), t.on("click", function () {
                e = $(this).position(), i = $(this).width(), $(this).parent().parent().find(".tabs-link-line").stop().css({
                    left: e.left,
                    width: i
                })
            })
        }, initCountdown: function () {
            var s = $(".countdown"), t = new Date;
            t.setDate(t.getDate() + 5), s.countdown(t, function (s) {
                $(this).html(s.strftime('<div class="timer-wrapper"><div class="timer-data">%D</div></div><span class="time-separate">:</span><div class="timer-wrapper"><div class="timer-data">%H</div></div><span class="time-separate">:</span><div class="timer-wrapper"><div class="timer-data">%M</div></div><span class="time-separate">:</span><div class="timer-wrapper"><div class="timer-data">%S</div></div>'))
            })
        }, addFavorite: function () {
            var s = $(".favorite"),
                t = '<li><span class="badge badge-pill badge-danger"><i class="la la-heart"></i></span></li>';
            s.on("click", function (s) {
                s.stopPropagation();
                var e = $(this).closest(".custom-card--info"), i = e.find(".custom-card--labels");
                if (i.length && !e.find(".custom-card--labels li .la-heart").length) i.append(t); else {
                    e.prepend('<ul class="custom-card--labels d-flex"><li><span class="badge badge-pill badge-danger"><i class="la la-heart"></i></span></li></ul>')
                }
            })
        }
    };
    var s = $("body"), t = $(".header-backdrop"), e = $(".sidebar-backdrop");
    $(document).ready(AppConfig.init)
}), $(window).on("load", function () {
    // $("#loading").fadeOut(1e3);
    $("#loading").fadeOut(1000);
    // $("#login").modal("show");
}), $("#wrapper").on("scroll", function () {
    $("#header").toggleClass("scrolled", $(this).scrollTop() > 80)
});
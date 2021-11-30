$(document).ready(function () {
    // Add datatable
    let table = $('#table_id').DataTable( {
        responsive: true,
        bPaginate: false,
        paging: false,
        ordering: false,
        info: false,
        bFilter: false
    });

    // Custom scroll bar
    $(window).on("load", function () {
        mCustomScrollbar();
        $("#mCSB_1_scrollbar_horizontal").css('top', 12);
        $("#mCSB_1_container").css('top', 40);
    });
    $(window).on("resize", function () {
        mCustomScrollbar();
        $("#mCSB_1_scrollbar_horizontal").css('top', 12);
        // $("#mCSB_1_container").css('top', 40)
    });
    $(window).trigger("resize");

    function mCustomScrollbar() {
        var w = $(window).width();
        var scrollW = $(".scrollbarX").width();
        var scrollNum;
        if (w >= 1200) {
            scrollNum = 3;
        } else if (w >= 768 && w <= 1199) {
            scrollNum = 2;
        } else {
            scrollNum = 1;
        }
        var itemW = scrollW / scrollNum;

        $(".scrollbarX").mCustomScrollbar({
            axis: "x",
            setWidth: false,
            mouseWheel: {
                enable: false,
                scrollType: "pixels",
                scrollAmount: itemW
            },
            autoExpandScrollbar: false,
            scrollButtons: {
                enable: true,
                scrollType: "pixels",
                scrollAmount: itemW
            },
            advanced: {
                updateOnBrowserResize: true,
                autoExpandHorizontalScroll: true
            }
        });
    }

    // Filter query string
    const urlParams = new URLSearchParams(window.location.search);
    const distreb_param = urlParams.get('distribution');

    // Clear filter
    let clear = $("#clear-filter");
    let clearOptions = $(".clear-filter")
    clear.click(function () {
        clearOptions.each(function () {
            if ($(this).attr('name') === "error") {
                $(this).val('errorClass')
                $('input[name="distribution"]').val("overall");
            } else {
                $(this).val('all');
                $('input[name="distribution"]').val("overall");
            }
            $("#filter_btn").click();
        })
    })

    // show, hide clear filter
    let select = $("select");
    select.each(function () {
        if ($(this).val() !== 'all') {
            clear.css('display', 'block');
            return 0;
        }
    })

    // Send request when select changes
    let select_field = document.querySelectorAll('select');
    let filter_btn = document.getElementById('filter_btn');
    let sub_nav_btn = $("#sub-tab-data");

    for (let i = 0; i < select_field.length; i++) {
        select_field[i].onchange = function () {
            if (select_field[i].value === '单一') {
                sub_nav_btn.val('');
            } else {
                if (distreb_param !== null && (distreb_param === select_field[i].name || distreb_param === 'regular' || distreb_param === 'complex')) {
                    sub_nav_btn.val('overall');
                }
            }
            filter_btn.click()
        }
    }

    // Send request based on sub tabs in response error view
    let sub_nav = $(".sub-navs .nav-link");

    sub_nav.click(function () {
        sub_nav_btn.val($(this).data('distreb'));
        filter_btn.click();
    });
})

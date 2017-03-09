$(function () {

    var manualRadio = $("#manual");
    var autoRadio = $("#auto");

    manualRadio.click(function () {
        if (autoRadio.is(":checked")) {
            autoRadio.prop('checked', false);
            $.ajax({
                url: '/admin/setting-manually',
                type: 'POST',
                success: function () {
                    console.log('Success: Manually setting worker pool')
                }
            });
        }
    });

    autoRadio.click(function () {
        if (manualRadio.is(":checked")) {
            manualRadio.prop('checked', false);
            $.ajax({
                url: '/admin/setting-auto',
                type: 'POST',
                success: function () {
                    console.log('Success: Auto-scaling the worker pool')
                }
            });
        }
    });


});

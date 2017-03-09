$(function () {

    var manualratio = $("#manual");
    var autoratio = $("#auto");
    var cpuGrow = $("#auto1");
    var cpuShrink = $("#auto2");
    var ratioExpand = $("#auto3");
    var ratioShrink = $("#auto4");

    manualratio.click(function () {
        if (autoratio.is(":checked")) {
            autoratio.prop('checked', false);
            $.ajax({
                url: '/admin/setting-manually',
                type: 'POST',
                success: function () {
                    console.log('Success: Manually setting worker pool')
                }
            });
        }
    });

    autoratio.click(function () {
        if (manualratio.is(":checked")) {
            manualratio.prop('checked', false);
            $.ajax({
                url: '/admin/setting-auto',
                type: 'POST',
                success: function () {
                    console.log('Success: Auto-scaling the worker pool')
                }
            });
        }
    });

    cpuGrow.on('change', function () {
        $.ajax({
            url: '/admin/setting-cpu-grow',
            data: {'data': cpuGrow.find("option:selected").text()},
            type: 'POST',
            success: function () {
                console.log('Success: Setting cpu grow threshold')
            }
        });
    });

    cpuShrink.on('change', function () {
        $.ajax({
            url: '/admin/setting-cpu-shrink',
            data: {'data': cpuShrink.find("option:selected").text()},
            type: 'POST',
            success: function () {
                console.log('Success: Setting cpu shrink threshold')
            }
        });
    });

    ratioExpand.on('change', function () {
        $.ajax({
            url: '/admin/setting-ratio-expand',
            data: {'data': ratioExpand.find("option:selected").text()},
            type: 'POST',
            success: function () {
                console.log('Success: Setting worker expand ratio')
            }
        });
    });

    ratioShrink.on('change', function () {
        $.ajax({
            url: '/admin/setting-ratio-shrink',
            data: {'data': ratioShrink.find("option:selected").text()},
            type: 'POST',
            success: function () {
                console.log('Success: Setting worker shrink ratio')
            }
        });
    });


});

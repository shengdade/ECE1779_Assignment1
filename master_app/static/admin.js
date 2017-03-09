$(function () {

    var manual = $("#manual");
    var auto = $("#auto");
    var cpuGrow = $("#auto1");
    var cpuShrink = $("#auto2");
    var ratioExpand = $("#auto3");
    var ratioShrink = $("#auto4");

    $.ajax({
        url: '/admin/setting',
        type: 'GET',
        success: function (data) {
            if (data.autoScaling === 1) {
                manual.prop('checked', false);
                auto.prop('checked', true);
                cpuGrow.attr('disabled', false);
                cpuShrink.attr('disabled', false);
                ratioExpand.attr('disabled', false);
                ratioShrink.attr('disabled', false);
                $('#sel1').attr('disabled', true);
                $('#sel2').attr('disabled', true);
                $('#createWorker').attr('disabled', true);
                $('#destroyWorker').attr('disabled', true);
            }
            cpuGrow.val(data.cpuGrow);
            cpuShrink.val(data.cpuShrink);
            ratioExpand.val(data.ratioExpand);
            ratioShrink.val(data.ratioShrink);
        }
    });

    manual.click(function () {
        if (auto.is(":checked")) {
            auto.prop('checked', false);
            cpuGrow.attr('disabled', true);
            cpuShrink.attr('disabled', true);
            ratioExpand.attr('disabled', true);
            ratioShrink.attr('disabled', true);
            $('#sel1').attr('disabled', false);
            $('#sel2').attr('disabled', false);
            $('#createWorker').attr('disabled', false);
            $('#destroyWorker').attr('disabled', false);
            $.ajax({
                url: '/admin/setting-manually',
                type: 'POST',
                success: function () {
                    console.log('Success: Manually setting worker pool')
                }
            });
        }
    });

    auto.click(function () {
        if (manual.is(":checked")) {
            manual.prop('checked', false);
            cpuGrow.attr('disabled', false);
            cpuShrink.attr('disabled', false);
            ratioExpand.attr('disabled', false);
            ratioShrink.attr('disabled', false);
            $('#sel1').attr('disabled', true);
            $('#sel2').attr('disabled', true);
            $('#createWorker').attr('disabled', true);
            $('#destroyWorker').attr('disabled', true);
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

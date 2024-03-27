import $ from 'jquery';

// Wrok mode filter
$(document).ready(function() {
    // Show all jobs initially
    $('.job-item').show();

    // Handle radio button change event
    $('.work-mode-radio').change(function() {
        var selectedWorkMode = $(this).val();

        // Hide all jobs
        $('.job-item').hide();

        // Show jobs with selected work mode
        $('.job-item[data-work-mode="' + selectedWorkMode + '"]').show();
    });
});
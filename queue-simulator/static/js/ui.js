// Optional interface help only. No JavaScript stack or click handlers.
if (window.jQuery) {
    jQuery(function ($) {
        $('#st_data').trigger('focus');
        // J1: fade in the top item that Jinja marked after Peek.
        $('#queue .peek').hide().fadeIn(1000);
    });
}
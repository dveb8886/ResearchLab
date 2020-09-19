





// Runs when the page is fully loaded
window.addEventListener('load', function(){

    // click listener that switches graph contents when tabs are clicked
    $('.tab').click(function(){
        var clicked_tab_name = $(this).attr('value')

        $('.fund-tab-item').each(function(){
            $(this).addClass('hidden');
            if ($(this).hasClass(clicked_tab_name)) {
                $(this).removeClass('hidden');
            }
        });
    });

    // click listener that show fund contents when fund name is clicked
    $('.fund-name').click(function(){
        var fund_contents = $('.fund-contents', $(this).parent().parent())
        fund_contents.toggleClass('hidden')
    });


})
(function($){
    function close(options, wrapper){
        options.onCleanup.call(this);
        wrapper.fadeOut('fast', function(){
            $(this).remove();
            options.onClosed();
        })
    }
        
    function create_element(tag, cl){
        return $(document.createElement(tag)).addClass(cl);
    }
          
    $.extend({
        notify: function(options, duration) {
            var
            // Default options object
            defaults = {
                inline: false,
                href: '',
                html: '',
                close: '',
                onStart: function(){},
                onComplete: function(){},
                onCleanup: function(){},
                onClosed: function(){}
            },
            
            // Useful variables
            clone,
            iframe = false,
            container, 
            wrapper = $('<li></li>').addClass('notification'),
            north,
            south,
            east,
            west,
            content
            
            options = $.extend(defaults, options);
            options.onStart.call(this);
            
            if($('ul#notification_area').length) {
                container = $('ul#notification_area');
            } 
            else {
                container = $('<ul></ul>').attr('id', 'notification_area');
                $('body').append(container);
            }
            
            if(options.href){
                if(options.inline){
                    clone = $(options.href).clone();
                }
                else {
                    iframe = true;
                    clone = $('<iframe></iframe>').attr('src', options.href).css({width: '100%', height: '100%'});
                }
            }
            else if(options.html){
                clone = $(options.html);
            }
                
            wrapper.append(
                create_element('div', 'notify_top').append(
                    create_element('div', "notify_nw"),
                    north = create_element('div', "notify_n"),
                    create_element('div', "notify_ne")
                ),
                create_element('div', 'notify_center').append(
                   east = create_element('div', "notify_w"),
                    content = create_element('div', 'notify_content').append(clone),
                    west = create_element('div', "notify_e")
                ),
                create_element('div', 'notify_bottom').append(
                    create_element('div', "notify_se"),
                    south = create_element('div', "notify_s"),
                    create_element('div', "notify_sw")
                )
            );
    
            wrapper.css("visibility", "hidden").appendTo(container);
            
            if(options.close){
                var close_elem = $('<span></span>').addClass('cl').html(options.close);
                content.append(close_elem);
            }
            
            var anim_length = 0 - parseInt(wrapper.outerHeight());
            wrapper.css('marginBottom', anim_length);
    
            if(iframe){
                content.height(parseInt(content.find('iframe').height()+16))
            }
            north.width(parseInt(wrapper.width())-40);
            south.width(parseInt(wrapper.width())-40);
            east.height(parseInt(content.height()));
            west.height(parseInt(content.height()));
            
            wrapper.animate({marginBottom: 0}, 'fast', function(){
                wrapper.hide().css('visibility', 'visible').fadeIn('fast');
                if(duration){
                    setTimeout(function(){
                        close(options, wrapper);
                    }, duration); 
                }
                
                if(!options.close){
                    wrapper.bind('click', function(){
                        close(options, wrapper);
                    })
                }
                else {
                    close_elem.bind('click', function(){
                        close(options, wrapper);
                    })
                }
                
                options.onComplete.call(this);
            });
        }
    });
})(jQuery);

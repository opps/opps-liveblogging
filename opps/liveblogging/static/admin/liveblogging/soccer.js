django.jQuery(document).ready(function(){

    django.jQuery('.preview__box').on('activate', '[contenteditable="true"]', function() {
       self = django.jQuery(this);
       if (self.html() == self.attr('data-placeholder')){
           self.empty();
       }
        var range, sel;
        if ( (sel = document.selection) && document.body.createTextRange) {
            range = document.body.createTextRange();
            range.moveToElementText(this);
            range.select();
        }
    });


    django.jQuery('.preview__box').on('blur', '[contenteditable="true"]', function() {
        self = django.jQuery(this);
        if (self.text() == ''){
            self.html(self.attr('data-placeholder'));
        }
    });



    django.jQuery('.preview__box').on('focus', '[contenteditable="true"]', function() {
        if (this.hasChildNodes() && document.createRange && window.getSelection) {

           self = django.jQuery(this);
           if (self.html() == self.attr('data-placeholder')){
               self.empty();
           }

            var range, sel;
            range = document.createRange();
            range.selectNodeContents(this);
            sel = window.getSelection();
            sel.removeAllRanges();
            sel.addRange(range);
        }
    });

});


function _timer(callback)
{
    var time = 0;     //  The default time of the timer
    var mode = 1;     //    Mode: count up or count down
    var status = 0;    //    Status: timer is running or stoped
    var timer_id;    //    This is used by setInterval function

    // this will start the timer ex. start the timer with 1 second interval timer.start(1000)
    this.start = function(interval)
    {
        interval = (typeof(interval) !== 'undefined') ? interval : 1000;

        if(status == 0)
        {
            status = 1;
            timer_id = setInterval(function()
            {
                switch(mode)
                {
                    default:
                    if(time)
                    {
                        time--;
                        generateTime();
                        if(typeof(callback) === 'function') callback(time);
                    }
                    break;

                    case 1:
                    if(time < 86400)
                    {
                        time++;
                        generateTime();
                        if(typeof(callback) === 'function') callback(time);
                    }
                    break;
                }
            }, interval);
        }
    }

    //  Same as the name, this will stop or pause the timer ex. timer.stop()
    this.stop =  function()
    {
        if(status == 1)
        {
            status = 0;
            clearInterval(timer_id);
        }
    }

    // Reset the timer to zero or reset it to your own custom time ex. reset to zero second timer.reset(0)
    this.reset =  function(sec)
    {
        sec = (typeof(sec) !== 'undefined') ? sec : 0;
        time = sec;
        generateTime(time);
    }

    this.confirm_reset = function(sec)
    {
        sec = (typeof(sec) !== 'undefined') ? sec : 0;
        if (confirm("reset timer?")){
            this.reset(sec);
        }
    }

    this.confirm_stop = function()
    {
        if (confirm("stop timer?")){
            this.stop();
        }
    }

    // Change the mode of the timer, count-up (1) or countdown (0)
    this.mode = function(tmode)
    {
        mode = tmode;
    }

    // This methode return the current value of the timer
    this.getTime = function()
    {
        return time;
    }

    // This methode return the current mode of the timer count-up (1) or countdown (0)
    this.getMode = function()
    {
        return mode;
    }

    // This methode return the status of the timer running (1) or stoped (1)
    this.getStatus = function()
    {
        return status;
    }

    // This methode will render the time variable to hour:minute:second format
    function generateTime()
    {
        var second = time % 60;
        var minute = Math.floor(time / 60) % 60;
        var hour = Math.floor(time / 3600) % 60;

        second = (second < 10) ? '0'+second : second;
        minute = (minute < 10) ? '0'+minute : minute;
        hour = (hour < 10) ? '0'+hour : hour;

        django.jQuery('div.timer span.second').html(second);
        django.jQuery('div.timer span.minute').html(minute);
        django.jQuery('div.timer span.hour').html(hour);

        if (supports_html5_storage()){
            localStorage.setItem('minute', minute);
        }
    }
}

var timer;

django.jQuery(document).ready(function(e)
{
    timer = new _timer
    (
        function(time)
        {
            if(time == 0)
            {
                timer.stop();
                alert('time out');
            }
        }
    );

    if (supports_html5_storage()){
        minutes = localStorage.getItem('minute');
        if (minutes){
            timer.reset(parseInt(minutes) * 60);
        }else{
            timer.reset();
        }
    }else{
        timer.reset();
    }

    timer.mode(1);
    timer.start();
});



function supports_html5_storage() {
  try {
    return 'localStorage' in window && window['localStorage'] !== null;
  } catch (e) {
    return false;
  }
}
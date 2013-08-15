django.jQuery(document).ready(function(){

    django.jQuery('[contenteditable="true"]').on('activate', function() {
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


    django.jQuery('[contenteditable="true"]').on('blur', function() {
        self = django.jQuery(this);
        if (self.text() == ''){
            self.html(self.attr('data-placeholder'));
        }
    });



    django.jQuery('[contenteditable="true"]').focus(function() {
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
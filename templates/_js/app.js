

        var names = ["one", "two", "three", "four", "five", "six", "seven", "eight", "space"]
        var ans = ["td_1", "td_2", "td_3", "td_4", "td_5", "td_6", "td_7", "td_8", "td_9"]
        var score = 0

        function move_board(direction) {
            score = score + 1
            var curr_pos = $('#space').parent().attr('id')
            
            $('#score').html('<h1>You\'ve made ' + score + ' moves.</h1>')
            
            switch(direction) {
                case 'left':
                    if ((curr_pos != 'td_1') && (curr_pos != 'td_4') && (curr_pos != 'td_7')) {
                        swap(-1)
                    }
                    break;
                
                case 'up':
                    if ((curr_pos != 'td_1') && (curr_pos != 'td_2') && (curr_pos != 'td_3')) {
                        swap(-3)
                    }
                    break;
                
                case 'right':
                    if ((curr_pos != 'td_3') && (curr_pos != 'td_6') && (curr_pos != 'td_9')) {
                        swap(1)
                    }
                    break;
                
                case 'down':
                    curr_pos = $('#space').parent().attr('id')
                    if ((curr_pos != 'td_7') && (curr_pos != 'td_8') && (curr_pos != 'td_9')) {
                        swap(3)
                    }
                    break;
            }
        }

        function swap(offset) {
            var swap_from, swap_el,swap_pos = ''
            var space = "<div id='space' class='numbers'>"

            swap_from = $('#space').parent().attr('id')
            swap_el = $('#td_' + (parseInt(swap_from.substr(3,1)) + offset)).html()
            swap_pos = $('#td_' + (parseInt(swap_from.substr(3,1)) + offset))

            $('#space').parent().html(swap_el)

            swap_pos.html(space) 
            
            check_board()
        }

        function check_board() {
            var res = []
            // Get current positions
            for(var i=0; i < 9; i++) { 
                res[i] = $('#'+names[i]).parent().attr('id')
            }
        
            // Check if answer match
            if(  (ans[1] == res[1]) && (ans[2] == res[2]) && (ans[3] == res[3]) && 
                 (ans[4] == res[4]) && (ans[5] == res[5]) && (ans[6] == res[6]) && 
                 (ans[7] == res[7]) && (ans[8] == res[8])) {
                 
                $('h4').html('solved') 
                $('#game').addClass('correct')
                $('#score_form').removeClass('hidden')
                $('#score_form').addClass('correct')
                return true
            } else {
                $('#game').removeClass('correct')
                $('#score_form').removeClass('correct')
                $('#score_form').addClass('hidden')
                $('h4').html('unsolved')
                return false;
            }
        }

        $(document).ready(function() {
       
            $(document).keydown(function(e){
                switch(e.keyCode) {
                    case 37:
                        move_board('left')
                        break;
                    case 38:
                        move_board('up')
                        break;
                    case 39:
                        move_board('right')
                        break;
                    case 40:
                        move_board('down')
                        break;
                }
            });
            
            $('#push_left').click(function() {
                move_board('left')
            })
            $('#push_up').click(function() {
                move_board('up')
            })
            $('#push_right').click(function() {
                move_board('right')
            })
            $('#push_down').click(function() {
                move_board('down')
            })

            $('#score_button').click(function() {
                var payload = {
                    score: score,
                    username: $('#username').val(),
                    game_id: $('#game_id').val()
                }

                if(payload.game_id != '') {
                    $.post('/update', {score: score, username: $('#username').val(), game_id: $('#game_id').val()}, function(data) {
                        $('#score_form p').html('Data has been sent')
                        window.location('/')
                    })
                }
            })
        })  
       
        // Device acceleration from iPhone
        //window.ondevicemotion = function(event) {  
        //  var accelerationX = event.accelerationIncludinGravity.x;  
        //  var accelerationY = event.accelerationIncludingGravity.y;  
        //  
        //  $('#x').html('x: ' + accelerationX)
        //  $('#y').html('y: ' + accelerationY)
        //} 
        
        


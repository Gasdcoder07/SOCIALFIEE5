    var socket = io();

    socket.on('message', function(msg){

        var li = document.createElement('li');

        li.innerHTML = msg;

        document.getElementById('messages').appendChild(li);

    });

    function sendMessage(){

        var input = document.getElementById('msg');
        
        socket.send(input.value);

        input.value = '';

    }

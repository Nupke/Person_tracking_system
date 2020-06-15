
$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var numbers_received = [];
    var ValidUsers = {};
    var client = {};
    let charOne =[];
    let charTwo =[];
    let charTree =[];
    let jsonUser =[];
    let jsonObject= [];
    var users;
    var address = [];





    fetch('http://127.0.0.1:5000/api/users')
            .then( response => response.json() )
            .then(data => users = data)
            .then(()=> {
                var users_count = 0;
                var devices_count = 0;
                 for(let i = 0; i < users.length; i++){
                     users_count = i +1;
                     document.getElementById("all_users").innerText = users_count;
                     for(let y =0; y < users[i].devices.length; y++){
                        users[i].devices[y].position = {}
                        if (jQuery.isEmptyObject(users[i].devices[y]['mac_addres'])){

                        } else {
                            devices_count += 1;
                        }
                        document.getElementById("all_devices").innerText = devices_count;


                     }
                 }
                 console.log('users',users);
            })



    console.log('jsonObject', jsonObject);
    //receive details from server
    socket.on('dump', function(msg){
        console.log(msg.data)
        // var rect = $( "#myContainer" ).offset();
        //     console.log('top'+rect );

     Move();


        if (numbers_received.length >= 10){
            numbers_received.shift()
        }

    switch (msg.data['topic']) {

        case 'detectionv1/sensor/ble_devices_scanner/state':
            console.log('one');
            connectTopic( 'drone1', msg.data.address, msg.data.rssi);

            let drone = 1;
            let address = msg.data.address;
            let rssi = msg.data.rssi;

            const isPresent = charOne.map(item => item.address).includes(msg.data.address);
                if (isPresent) {
                  const currentOne = charOne.find(item => item.address === msg.data.address);

                  Object.assign(currentOne, msg.data);
                } else {
                  charOne.push(msg.data);
                  numbers_received.push(msg.data['address']);
                }
                    var s = 0;
                    numbers_string = '';
                    for (var i = 0; i < numbers_received.length; i++){
                        numbers_string = numbers_string + '<p>' + numbers_received[i].toString() + '</p>';
                        console.log(numbers_string)
                        s = i

                    }
                    document.getElementById("all_devices_around").innerText= s;
                    $('#users-devices-list').html(numbers_string);


            return;
        case 'detectionv2/sensor/ble_devices_scanner/state':
            console.log('two');
            connectTopic( 'drone2', msg.data.address, msg.data.rssi)

            const isPresentTwo = charTwo.map(item => item.address).includes(msg.data.address);
                if(isPresentTwo) {
                    const currentTwo = charTwo.find(item => item.address === msg.data.address);

                    Object.assign(currentTwo, msg.data);
                } else {
                    charTwo.push(msg.data);
                }
            return;

        case 'detectionv3/sensor/ble_devices_scanner/state':
            console.log('tree');
            connectTopic( 'drone3', msg.data.address, msg.data.rssi)





            const isPresentTree = charTree.map(item => item.address).includes(msg.data.address);
                if(isPresentTree){
                    const currentTree = charTree.find(item => item.address === msg.data.address);

                    Object.assign(currentTree, msg.data);
                } else {
                    charTree.push(msg.data)
                }
            return;

        default:
            break;

    }


    function connectTopic(drone, address, rssi) {
           for(let i = 0; i < users.length; i++){
               console.log('splitUsers',users[i])
              for(let y =0; y < users[i].devices.length; y++){
                  console.log('test ConnectTopic',users[i].devices[y]);
                  if(users[i].devices[y].mac_addres == address){
                     users[i].devices[y].position[drone] =  rssi;
                     //setTimeout(function () {users[i].devices[y].position[drone] = NaN}, 15000);
                  }
              }
           }
    }

        


    function Move(){
            var rect = document.getElementById('myContainer').getBoundingClientRect();
            var horizontal = rect.width/2;
            var vertical = 0;
            var users_in_room =0;
            var device_in_room =0;
            test_username = '';
            // elem.style.left = position + Math.abs(pos) +"px";
            for(let i = 0; i < users.length; i++){
                for(let y=0; y < users[i].devices.length; y++){
                    if( jQuery.isEmptyObject(users[i].devices[y].position)) {

                    } else {

                        var elem = document.getElementById(users[i].username)
                        test_username = test_username + `<p id=${users[i].username}>` + users[i].username + '</p>';
                        let a = parseFloat(users[i].devices[y].position['drone1']);
                        let b = parseFloat(users[i].devices[y].position['drone2']);
                        let c = parseFloat(users[i].devices[y].position['drone3']);


                        console.log('a b c', a, b ,c);

                        if(a && b   !=NaN ){
                            users_in_room +=1;
                            document.getElementById("users_in_room").innerText = users_in_room;
                            elem.style.display ="block";

                            elem.style.left = (horizontal - ((horizontal / 80) * Math.abs(a)) + ((horizontal / 80) * Math.abs(b)) +"px");
                            elem.style.top =  vertical + ((rect.height / 90) * Math.abs(c) ) + "px";
                        } else {
                            users_in_room -=1;
                            elem.style.display ="none";
                        }
                    }
                }
            }
            $('#test_user').html(test_username);

    }


        $('form#pub').submit(function(event) {
          socket.emit('publish', JSON.stringify({ 'message': $('#pub_msg').val()}));
          return false;

        });



    });



})
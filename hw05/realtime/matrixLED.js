    var socket;
    var firstconnect = true,
        i2cNum  = "0x70",
	disp = [];

// Create a matrix of LEDs inside the <table> tags.
var matrixData;
for(var j=7; j>=0; j--) {
	matrixData += '<tr>';
	for(var i=0; i<8; i++) {
	    matrixData += '<td><div class="LED" id="id'+i+'_'+j+
		'" onclick="LEDclick('+i+','+j+')">'+
		i+','+j+'</div></td>';
	    }
	matrixData += '</tr>';
}
$('#matrixLED').append(matrixData);

// The slider controls the overall brightness
$("#slider1").slider({min:0, max:15, slide: function(event, ui) {
	socket.emit("i2cset",  {i2cNum: i2cNum, i: ui.value+0xe0, disp: 1});
    }});

// Send one column when LED is clicked.
function LEDclick(i, j) {
  // alert(i+","+j+" clicked");
   // Find the red index in the data array for the corresponding position
   var red=(2*i) +1;
  //Check the red and green bit for the clicked LED and change data accordingly. LED goes green to orange to red to off
   if((((disp[red-1]>>j)&0x01)===0)&&((disp[red]>>j)&0x01)===0){
		disp[red-1]^=(0x01<<j);
}
  else if((((disp[red-1]>>j)&0x01)===1)&&((disp[red]>>j)&0x01)===0){
		disp[red]^=(0x01<<j);
}

   else if((((disp[red-1]>>j)&0x01)===1)&&((disp[red]>>j)&0x01)===1){
		disp[red-1]^=(0x01<<j);
}
   else if(((disp[red-1]>>j)&0x01)===0){
	if(((disp[red]>>j)&0x01)===1){
		disp[red]^=(0x01<<j);
}
}




		//Send the new data to the bone
    socket.emit('i2cset', {i2cNum: i2cNum, i: 2*i+1, 
			     disp: '0x'+disp[2*i+1].toString(16)});
    socket.emit('i2cset', {i2cNum: i2cNum, i: 2*i, 
                             disp: '0x'+disp[2*i].toString(16)});


    // Toggle bit on display
    if(((disp[red-1]>>j)&0x01) === 1) {	//Cases added to change color on website
	if(((disp[red]>>j)&0x01)===0){
		 $('#id'+i+'_'+j).addClass('on');
		
    }

}
   if(((disp[red-1]>>j)&0x01)===1){
	if(((disp[red]>>j)&0x01)===1){
		$('#id'+i+'_'+j).removeClass('on');
                 $('#id'+i+'_'+j).addClass('orange');

}
    } 
   if(((disp[red-1]>>j)&0x01)===0){
	if(((disp[red]>>j)&0x01)===1){
       		$('#id'+i+'_'+j).removeClass('orange');
		$('#id'+i+'_'+j).addClass('red');
		//alert("red");
}
    }
   if(((disp[red-1]>>j)&0x01)===0){
	if(((disp[red]>>j)&0x01)===0){
		$('#id'+i+'_'+j).removeClass('on');
		$('#id'+i+'_'+j).removeClass('orange');
		$('#id'+i+'_'+j).removeClass('red');
		//alert("off");
}
}
}


    function connect() {
      if(firstconnect) {
        socket = io.connect(null);

        // See https://github.com/LearnBoost/socket.io/wiki/Exposed-events
        // for Exposed events
        socket.on('message', function(data)
            { status_update("Received: message " + data);});
        socket.on('connect', function()
            { status_update("Connected to Server"); });
        socket.on('disconnect', function()
            { status_update("Disconnected from Server"); });
        socket.on('reconnect', function()
            { status_update("Reconnected to Server"); });
        socket.on('reconnecting', function( nextRetry )
            { status_update("Reconnecting in " + nextRetry/1000 + " s"); });
        socket.on('reconnect_failed', function()
            { message("Reconnect Failed"); });

        socket.on('matrix',  matrix);

    socket.emit('i2cset', {i2cNum: i2cNum, i: 0x21, disp: 1}); // Start oscillator (p10)
    socket.emit('i2cset', {i2cNum: i2cNum, i: 0x81, disp: 1}); // Disp on, blink off (p11)
    socket.emit('i2cset', {i2cNum: i2cNum, i: 0xe7, disp: 1}); // Full brightness (page 15)
    /*
	i2c_smbus_write_byte(file, 0x21); 
	i2c_smbus_write_byte(file, 0x81);
	i2c_smbus_write_byte(file, 0xe7);
    */
        // Read display for initial image.  Store in disp[]
        socket.emit("matrix", i2cNum);

        firstconnect = false;
      }
      else {
        socket.socket.reconnect();
      }
    }

    function disconnect() {
      socket.disconnect();
    }

    // When new data arrives, convert it and display it.
    // data is a string of 16 values, each a pair of hex digits.
    function matrix(data) {
        var i, j;
        disp = [];
        //        status_update("i2c: " + data);
        // Make data an array, each entry is a pair of digits
        data = data.split(" ");
        //        status_update("data: " + data);
        // Every other pair of digits are Green. The others are red.
        // Convert from hex.
        for (i = 0; i < 16; i += 1) {		//Consider all data instead of just green
            disp[i] = parseInt(data[i], 16);
        }
        //        status_update("disp: " + disp);
        // i cycles through each column
        for (i = 0; i < 16; i+=1) {
            // j cycles through each bit
            for (j = 0; j < 8; j+=1) {
		var red = 2*i+1;
		//Change the color on the website according to the red and green bit values for each LED
               // if (((disp[i] >> j) & 0x1) === 0 && disp[i-1]>>j&0x1===1) {
                  if ((((disp[red-1]>>j) & 0x1)===1)&&((disp[red]>>j)&0x01)===0){
		     		$('#id' + i + '_' + j).addClass('on');
}

		else if((((disp[red-1]>>j)&0x1)===1)&&((disp[red]>>j)&0x01)===1){
				$('#id'+i+'_'+j).removeClass('on');
				$('#id'+i+'_'+j).addClass('orange');

                } 
		 else if((((disp[red-1]>>j)&0x1)===0)&&((disp[red]>>j)&0x01)===1){
				$('#id'+i+'_'+j).removeClass('orange');
				$('#id'+i+'_'+j).addClass('red');
}		
		else if(((disp[red-1]>>j)&0x1)===0){
			if(((disp[red]>>j)&0x1)===0){
                    		$('#id' + i + '_' + j).removeClass('red');
				$('#id'+i+'_'+j).removeClass('on');
				$('#id'+i+'_'+j).removeClass('orange');
	
                }
		}
            }
        }
    }

    function status_update(txt){
	$('#status').html(txt);
    }

    function updateFromLED(){
      socket.emit("matrix", i2cNum);    
    }

connect();

$(function () {
    // setup control widget
    $("#i2cNum").val(i2cNum).change(function () {
        i2cNum = $(this).val();
    });
});

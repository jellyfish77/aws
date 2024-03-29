var awsIot = require('aws-iot-device-sdk'); 
//var rpiDhtSensor = require('rpi-dht-sensor'); 
 
//var dht = new rpiDhtSensor.DHT11(2); // `2` => GPIO2 
const NODE_ID = 'DHT11'; 
const INIT_DELAY = 15; 
const TAG = '[' + NODE_ID + '] >>>>>>>>> '; 
 
console.log(TAG, 'Connecting...'); 
 
var thingShadow = awsIot.thingShadow({ 
  keyPath: './certs/78dbb0c521-private.pem.key', 
  certPath: './certs/78dbb0c521-certificate.pem.crt', 
  caPath: './certs/RootCA-VeriSign-Class 3-Public-Primary-Certification-Authority-G5.pem', 
  clientId: NODE_ID, 
  host: 'abvuq2slx5a1s-ats.iot.us-west-2.amazonaws.com', 
  port: 8883, 
  region: 'us-west-2', 
  debug: false, // optional to see logs on console 
}); 
 
thingShadow.on('connect', function() { 
  console.log(TAG, 'Connected.'); 
  thingShadow.register(NODE_ID, {}, function() { 
    console.log(TAG, 'Registered.'); 
    console.log(TAG, 'Reading data in ' + INIT_DELAY + ' seconds.'); 
    setTimeout(sendData, INIT_DELAY * 1000); // wait for `INIT_DELAY` seconds before reading the first record 
  }); 
}); 
 
function fetchData() { 
  //var readout = dht.read(); 
  var temp = Math.random(); 
  var humd = Math.random(); 
 
  return { 
    "temp": temp, 
    "humd": humd 
  }; 
} 
 
function sendData() { 
  var DHT11State = { 
    "state": { 
      "desired": fetchData() 
    } 
  }; 
 
  console.log(TAG, 'Sending Data..', DHT11State); 
 
  var clientTokenUpdate = thingShadow.update(NODE_ID, DHT11State); 
  if (clientTokenUpdate === null) { 
    console.log(TAG, 'Shadow update failed, operation still in progress'); 
  } else { 
    console.log(TAG, 'Shadow update success.'); 
  } 
 
  // keep sending the data every 30 seconds 
  console.log(TAG, 'Reading data again in 30 seconds.'); 
  setTimeout(sendData, 30000); // 30,000 ms => 30 seconds 
} 
 
thingShadow.on('status', function(thingName, stat, clientToken, stateObject) { 
  console.log('received ' + stat + ' on ' + thingName + ':', stateObject); 
}); 
 
thingShadow.on('delta', function(thingName, stateObject) { 
  console.log('received delta on ' + thingName + ':', stateObject); 
}); 
 
thingShadow.on('timeout', function(thingName, clientToken) { 
  console.log('received timeout on ' + thingName + ' with token:', clientToken); 
});
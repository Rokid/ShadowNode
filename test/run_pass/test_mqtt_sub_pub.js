'use strict';

var mqtt = require('mqtt');
var assert = require('assert');
var bridge = 'mqtt://test.mosquitto.org:1883';

var opts = {
  reconnectPeriod: -1,
};

function connect(endpoint, opts) {
  return new Promise(function (resolve, reject) {
    var client = mqtt.connect(endpoint, opts);
    client.once('connect', function() {
      resolve(client);
    });
  });
}

Promise.all([
  connect(bridge, opts),
  connect(bridge, opts),
]).then((results) => {
  var yorkie = results[0];
  var babeee = results[1];

  babeee.subscribe('u/love', function() {
    console.log('babeee subscribed u/love');
    setTimeout(function() {
      yorkie.publish('u/love', 'endless');
      console.log('yorkie sent endless love');
    }, 500);
  });
  babeee.on('message', function(channel, message) {
    assert.equal(channel, 'u/love');
    assert.equal(message + '', 'endless');
    console.log('babeee receives the message from yorkie');

    babeee.disconnect();
    yorkie.disconnect();
  });
});

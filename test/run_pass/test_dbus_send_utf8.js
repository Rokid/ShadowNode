'use strict';

var assert = require('assert');
var dbus = require('dbus');

var myservice = dbus.registerService('session', 'org.myservice');
var myobject = myservice.createObject('/org/myobject');
var myiface = myobject.createInterface('test.dbus.myservice.testSendUtf8');
var bus = dbus.getBus();

myiface.addMethod('test', {
  in: [dbus.Define(String)],
  out: [dbus.Define(String)]
}, (text, cb) => {
  cb(null, text);
});
myiface.update();

function test(str) {
  return new Promise((resolve) => {
    bus.callMethod(
      'org.myservice',
      '/org/myobject',
      'test.dbus.myservice.testSendUtf8', 'test', 's', [str], (err, res) => {
      try {
        assert.equal(err, null);
        assert.equal(res, str);
        return resolve(true);
      } catch (err) {
        return reject(err);
      }
    });
  })
}

Promise.all([
  test('foobar'),
  test('😄'),
  test('😀😃😄😁😆😅😂🤣😊😇🙂🙃😉😌😍😘😗😙😚😋😛😝😜🤪🤨🧐🤓'),
  test('🐶🐱🐭🐹🐰🦊🐻🐼🐨🐯🦁🐮🐷🐽🐸🐵🙈🙉🙊🐒🐔🐧🐦🐤🐣🐥🦆🦅🦉'),
  test('🦇🐺🐗🐴🦄🐝🐛🦋🐌🐚🐞🐜🦗🕷🕸🦂🐢🐍🦎🦖🦕🐙🦑🦐🦀🐡🐠🐟🐬'),
  test('🍏🍎🍐🍊🍋🍌🍉🍇🍓🍈🍒🍑🍍🥥🥝🍅🍆🥑🥦🥒🌶🌽🥕🥔🍠🥐🍞🥖🥨'),
  test('⚽️🏀🏈⚾️🎾🏐🏉🎱🏓🏸🥅🏒🏑🏏⛳️🏹🎣🥊🥋🎽⛸🥌🛷🎿⛷🏂'),
  test('🚗🚕🚙🚌🚎🏎🚓🚑🚒🚐🚚🚛🚜🛴🚲🛵🏍🚨🚔🚍🚘🚖🚡🚠🚟🚃🚋🚞🚝🚄'),
  test('⌚️📱📲💻⌨️🖥🖨🖱🖲🕹🗜💽💾💿📀📼📷📸📹🎥📽🎞📞☎️📟📠📺📻🎙🎚🎛'),
  test('❤️🧡💛💚💙💜🖤💔❣️💕💞💓💗💖💘💝💟☮️✝️☪️🕉☸️✡️🔯🕎☯️☦️🛐⛎♈️♉️♊️♋️♌️♍️♎️♏️♐️♑️♒️'),
  test('→⇒⟹⇨⇾➾⇢☛☞➔➜➙➛➝➞➟➠➡︎➢➣➤➥➦➧➨⥤⇀⇁⥛⥟⇰➩➪➫➬➭➮➯➱➲➳➵➸➻➺➼➽⟶⇉⇶⇛⇏⤃↛↝⤳↣↠↦'),
  test('¡!¿?⸘‽“”‘’‛‟.,‚„^°¸˛&¶†‡@%‰‱¦|/ˉˆ˘ˇ‼︎⁇⁈⁉︎❛❜❝❞❢❣❡'),
  test('☀︎☼☽☾☁︎☂︎☔︎☃︎★☆⭐︎☇☈♠︎♣︎♥︎♦︎♤♧♡♢♚♛♜♘♗♖♕♔♟♞♝♙⚀⚁⚂⚃⚄⚅☻✐✏︎✎✍︎✌︎⚽︎⚾︎✄✃'),
  test('🀥🀦🀨🀩🀪🀡🀠🀟🀞🀝🀜🀛🀚🀙🀘🀗🀖🀏🀎🀍🀌🀋🀂🀃🀅🀆🀇🀈🀉🀊🀁🀀🀄︎'),
  test('+−-×÷±∓∔ℶℵ∞∝∪∩¬=ℷℸℏℇ∀∁∂℮∃∄∅∆∇⊂⊃⊄⊅⊆⊇⊈⊉⊊⊋∈∉∊∋∌∍∧∨<'),
  test('®©℗™℠№ªº℔℥ℨℬℊµΩℹ︎ℌℑ℞ℳ℃℉℀℁℅℆'),
  test('ÀÁÂÃĀĂȦÄẢÅÆⱰǼǢḂƁĆɃƄČƇÇḈȻĐƉƋÈÉƑḞƏƐɆĜḠĠǦḨḪĨĮɈḰǨḴĻḼĿŁḾṂⱮƜŅṊṈȠÕŎƠŔŘƦɌ'),
]).then(
  () => {
    bus.destroy();
    console.log('send utf8 test is ok');
  },
  (err) => {
    bus.destroy();
    assert.fail('failure on testing');
  }
);

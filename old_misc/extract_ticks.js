var fs = require('fs');
var jsgo = require('jsgo');

demo_path = 'data/ast_vp.dem';


fs.readFile(demo_path, function(err, data) {
  var test = new jsgo.Demo().getPlayers();
  console.log(test);
  var targ_list = [];

  var jsdem = new jsgo.Demo();

  jsdem.on('*', function(event) {
    //console.log(jsdem.getTick());
 
        console.log(event);
        console.log(this.getTick())
    
  });

  jsdem.parse(data);

});


const DemoReader = require('csgodemoreader').Reader;
const UserMessages = require('csgodemoreader').UserMessages;
const Teams = require('csgodemoreader').Teams;
const fs = require('fs');
const TinyDB = require('tinydb');

let db = new TinyDB('./test.db');

let buffer = fs.readFileSync(__dirname + '/ast_vp.dem');
let demo = new DemoReader(buffer);

save = function(key, value) {
    db.setInfo(key, value, function(err, key, value) {
        if (err) {
            console.log(err);
            return;
        }        
    });
};


//Event listeners
let logs = Object()
let seq = Object()
let tick_cnt = 0

demo.on('csgo.round_start', _ => {
    console.log('Round ' + demo.getRound());
    
    if (demo.getRound() === 2) {
        
        console.log(logs)
        console.log(seq)
        console.log(tick_cnt)

        demo.stop()
    };
    db.flush();
});


demo.on('tick', event => {
    //console.log(demo.getTeams());
    tick_cnt++
    
    const players = demo.getPlayers()
    const names = players.map(p => p.getName());
    const teams = players.map(p => p.getTeamNumber());
    const yaws = players.map(p => p.getEyeAngle()['yaw'])

    if (Object.keys(seq).length === 0 && seq.constructor === Object) {
        for (j = 0; j < players.length; j++) {
            if (teams[j] === 1) {
                seq[names[j]] = Array();
                logs[names[j]] = 0;
            }
        }
    }
    
    for (obs = 0; obs < players.length; obs++) {
        if (teams[obs] === 1) {
            for (player = 0; player < players.length; player++) {
                if (teams[player] != 1) {
                    if (yaws[obs] === yaws[player]) {
                        logs[names[obs]]++;
                        
                        curseq = seq[names[obs]];
                        if (curseq[curseq.length - 1] != names[player]) {                            
                            curseq.push(names[player]);
                        }
                    }
                }
            }
        }
    }

    //const 
    //console.log('================================================');
});

//Run reader
db.onReady = function() {
    demo.run();
    db.flush();
};
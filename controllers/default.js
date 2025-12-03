const Pty = require('node-pty');
const fs = require('fs');
const path = require('path');

exports.install = function () {

    ROUTE('/');
    WEBSOCKET('/', socket, ['raw']);

};

function socket() {

    this.encodedecode = false;
    this.autodestroy();

    this.on('open', function (client) {

        // Spawn terminal
        client.tty = Pty.spawn('python3', ['run.py'], {
            name: 'xterm-color',
            cols: 80,
            rows: 24,
            cwd: process.env.PWD,
            env: process.env
        });

        client.tty.on('exit', function (code, signal) {
            client.tty = null;
            client.close();
            console.log("Process killed");
        });

        client.tty.on('data', function (data) {
            client.send(data);
        });

    });

    this.on('close', function (client) {
        if (client.tty) {
            client.tty.kill(9);
            client.tty = null;
            console.log("Process killed and terminal unloaded");
        }
    });

    this.on('message', function (client, msg) {
        client.tty && client.tty.write(msg);
    });
}

if (process.env.CREDS != null) {
    console.log("Creating creds/creds.json file.");

    const credsDir = path.join(process.cwd(), 'creds');
    fs.mkdirSync(credsDir, { recursive: true });

    const credsPath = path.join(credsDir, 'creds.json');

    try {
        // Parse the environment variable as JSON first
        const credsJson = JSON.parse(process.env.CREDS);

        // Write valid JSON to creds.json
        fs.writeFileSync(credsPath, JSON.stringify(credsJson, null, 2), 'utf8');

        console.log("creds/creds.json file created successfully.");
    } catch (err) {
        console.error("Invalid JSON in CREDS environment variable:", err);
    }
}




//if (process.env.CREDS != null) {
    //console.log("Creating creds.json file.");
    //fs.writeFile('creds.json', process.env.CREDS, 'utf8', function (err) {
        //if (err) {
        //    console.log('Error writing file: ', err);
      //      socket.emit("console_output", "Error saving credentials: " + err);
    //    }
  //  });
//}
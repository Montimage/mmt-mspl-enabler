const express = require('express');
const router = express.Router();
const { exec } = require('child_process');

router.get('/', function (req, res) {

    // Execute the command to copy the file using Docker
    exec(`sudo docker restart mi_probe`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error restarting Docker container: ${error}`);
            res.status(500).send('Error restarting Docker container');
            return;
        }
        res.send('mi_probe docker restarted successfully! Changes applied.');
    });
});


module.exports = router;

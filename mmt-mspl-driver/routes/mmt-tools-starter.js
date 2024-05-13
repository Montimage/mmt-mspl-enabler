const express = require('express');
const router = express.Router();
const { exec } = require('child_process');

router.get('/', function (req, res) {

    // Execute the command to copy the file using Docker
    exec(`sudo docker compose -f Docker-MMT-Tools/docker-compose.yml up`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error starting Docker containers: ${error}`);
            res.status(500).send('Error starting Docker containers');
            return;
        }
    });
    res.send('MMT-Tools dockers started successfully!');
});


module.exports = router;

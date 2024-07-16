const express = require('express');
const router = express.Router();
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

// Middleware to parse JSON body
router.use(express.json());

router.put('/', function (req, res, next) {
    // Get file content from JSON body
    const fileContent = req.body.fileContent;

    // Define the file path
    const filePath = path.join(__dirname, '../uploads', 'mmt-probe.conf');

    // Write the file content to mmt-probe.conf
    fs.writeFile(filePath, fileContent, 'utf8', (err) => {
        if (err) {
            console.error(`Error writing file: ${err}`);
            res.status(500).send('Error writing file');
            return;
        }

        // Execute the command to copy the file using Docker
        exec(`docker cp ${filePath} mi_probe:/opt/mmt/probe/mmt-probe.conf`, (error, stdout, stderr) => {
            if (error) {
                console.error(`Error copying file to Docker container: ${error}`);
                res.status(500).send('Error copying file to Docker container');
                return;
            }    
            else {
                // Execute command to commit changes to docker image
                exec(`docker commit mi_probe`, (error, stdout, stderr) => {
                    if (error) {
                        console.error(`Error committing Docker container: ${error}`);
                        res.status(500).send('Error committing Docker container. Verify if the container mi_probe is running');
                        return;
                    }    
                    res.send('New config file uploaded, copied, and saved successfully! Restart to apply changes.');
                });
            }
        });
    });
});

module.exports = router;

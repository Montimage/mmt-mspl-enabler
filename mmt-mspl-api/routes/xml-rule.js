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
    const filePath = path.join(__dirname, '../uploads', 'new_rule.xml');

    // Write the file content to new_rule.xml
    fs.writeFile(filePath, fileContent, 'utf8', (err) => {
        if (err) {
            console.error(`Error writing file: ${err}`);
            res.status(500).send('Error writing file');
            return;
        }

        // Execute the command to copy the file using Docker
        exec(`sudo docker cp ${filePath} mi_probe:/opt/mmt/security/bin/new_rule.xml`, (error, stdout, stderr) => {
            if (error) {
                console.error(`Error copying file to Docker container: ${error}`);
                res.status(500).send('Error copying file to Docker container');
                return;
            } else {
                // Execute the command to compile new rule in Docker Container
                exec(`sudo docker exec mi_probe ./opt/mmt/security/bin/compile_rule /opt/mmt/security/rules/114.new.so /opt/mmt/security/bin/new_rule.xml`, (error, stdout, stderr) => {
                    if (error) {
                        console.error(`Error compiling new rule in Docker container: ${error} \n Verify if mi_probe is running`);
                        res.status(500).send('Error compiling new rule in Docker container');
                        return;
                    } else {
                        // Execute command to commit changes to docker image
                        exec(`sudo docker commit mi_probe`, (error, stdout, stderr) => {
                            if (error) {
                                console.error(`Error committing Docker container: ${error}`);
                                res.status(500).send('Error committing Docker container');
                                return;
                            }
                            res.send('New rule uploaded, copied, compiled and saved successfully! Restart to apply changes.');
                        });
                    }
                });
            }
        });
    });
});

module.exports = router;

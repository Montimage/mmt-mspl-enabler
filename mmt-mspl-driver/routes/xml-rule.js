const express = require('express');
const router = express.Router();
const { exec } = require('child_process');
const multer = require('multer');

// Define storage for uploaded files
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'uploads/') // Where uploaded files will be stored
  },
  filename: function (req, file, cb) {
    cb(null, file.originalname) // Use the original filename
  }
})

// Create Multer instance with defined storage
const upload = multer({ storage: storage })

router.put('/', upload.single('file'), function (req, res, next) {

    const filePath = req.file.path;

    // Execute the command to copy the file using Docker
    exec(`sudo docker cp ${filePath} mi_probe:/opt/mmt/security/bin/new_rule.xml`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error copying file to Docker container: ${error}`);
            res.status(500).send('Error copying file to Docker container');
            return;
        }else{

            // Execute the command to compile new rule in Docker Container
            exec(`sudo docker exec mi_probe ./opt/mmt/security/bin/compile_rule /opt/mmt/security/rules/114.new.so /opt/mmt/security/bin/new_rule.xml
            `, (error, stdout, stderr) => {
                if (error) {
                    console.error(`Error compiling new rule in Docker container: ${error} \n Verify if mi_probe is running`);
                    res.status(500).send('Error compiling new rule in Docker container');
                    return;
                }
                else{
                    // Execute comand to commit changes to docker image
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


module.exports = router;

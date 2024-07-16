const express = require('express');
const bodyParser = require('body-parser');
const swaggerUI = require("swagger-ui-express")
const swaggerJsDoc = require("swagger-jsdoc")

const xmlRuleRoutes = require('./routes/xml-rule'); 
const mmtConfigRoutes = require('./routes/mmt-config');
const restartRoutes = require('./routes/restart-mi-probe');
const healthcheckRoutes = require('./routes/healthcheck');

const swaggerFile = require('./swagger.json')

const app = express();

app.use(bodyParser.json());

const specs = swaggerJsDoc(swaggerFile)

app.use("/api-docs", swaggerUI.serve, swaggerUI.setup(specs))

app.use('/xml-rule', xmlRuleRoutes);

app.use('/mmt-config', mmtConfigRoutes); 

app.use('/restart-docker', restartRoutes);

app.use('/healthcheck', healthcheckRoutes);

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

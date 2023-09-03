const express = require('express');
const app = express();
const cors = require("cors");
const { default: axios } = require('axios');
app.use(cors());

app.get("/:models", async(req, res)=> {
    const {models} = req.params;
    const models_array = models.split(",") //[dollhole, adulttime, fabulouscb]
    const requests = models_array.map(async (val) => {
        const data = await axios.get(`http://127.0.0.1:5000/?model=${val}&limit=5`);  
        return data.data; // Return the data from each request
    });
    const responses = await Promise.all(requests);
    res.send({data: responses})
})


app.listen(3000, ()=> {
    console.log("Live on 3000")
})
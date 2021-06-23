const { exec } = require('child_process');

exports.lambdaHandler = async (event,context) => {
    
    exec(`python3 /usr/scr/app/task.py`, (err) => {
        if (err) {
            //some err occurred
            console.error(err)
        }
	   else{
	    console.log("python file created");
	   }
   });
    const response = {
        statusCode: 200,
        body:JSON.stringify({message:"lambda triggered"})
    };
    return response;

};

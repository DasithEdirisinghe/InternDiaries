const { exec } = require('child_process');

exports.lambdaHandler = async (event,context) => {

    const spawn_options = {
    cwd: '/usr/src/node', 
    shell:'bash'
    };
    
    exec(`python3 task.py`,spawn_options, (err) => {
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

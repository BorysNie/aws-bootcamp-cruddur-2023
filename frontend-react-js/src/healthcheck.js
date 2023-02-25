const http = require("http");
const ports = [ 3000, 4567, 5432, 8000 ];

var options = {
  host: "localhost",
  timeout: 2000,
};

ports.forEach((port) => {
  var new_options = options.push(port)
  request = http.request(new_options, (res) => {
  console.log(`STATUS: ${res.statusCode}`);
  if (res.statusCode == 200) {
      process.exit(0);
  } else {
      process.exit(1);
  }
  })
});

request.on("error", function (err) {
  console.log("ERROR");
  process.exit(1);
});

request.end();
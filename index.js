let express = require("express");
let ps = require("python-shell");

const app = express();

app.get("/position", (req, res) =>
{
	let options = {
		mode: "text",
		scriptPath: "./python/tb6600",
	};

	ps.PythonShell.run("get-position.py", options, function (err, results)
	{
		if (err) {
			console.log(err);
			res.json({ "error": err });
			return;
		}
		
		console.log(results);
		res.json({ "position": Number(results[0]) });
	});
});

app.get("/power", (req, res) =>
{
	let options = {
		mode: "text",
		scriptPath: "./python/tb6600",
	};

	ps.PythonShell.run("get-power.py", options, function (err, results)
	{
		if (err) {
			console.log(err);
			res.json({ "error": err });
			return;
		}
		
		console.log(results);
		res.json({ "power": Number(results[0]) });
	});
});

app.put("/move-to/:position", (req, res) =>
{
	let options = {
		mode: "text",
		scriptPath: "./python/tb6600",
		args: [ req.params.position ]
	};

	ps.PythonShell.run("move-to.py", options, function (err, results)
	{
		if (err) {
			console.log(err);
			res.json({ "error": err });
			return;
		}
		
		console.log(results);
		res.json({ "position": Number(results[0]) });
	});
});

app.put("/move-by/:steps", (req, res) =>
{
	let options = {
		mode: "text",
		scriptPath: "./python/tb6600",
		args: [ req.params.steps ]
	};

	ps.PythonShell.run("move-by.py", options, function (err, results)
	{
		if (err) {
			console.log(err);
			res.json({ "error": err });
			return;
		}
		
		console.log(results);
		res.json({ "position": Number(results[0]) });
	});
});

app.put("/force-by/:steps", (req, res) =>
{
	let options = {
		mode: "text",
		scriptPath: "./python/tb6600",
		args: [ req.params.steps ]
	};

	ps.PythonShell.run("force-by.py", options, function (err, results)
	{
		if (err) {
			console.log(err);
			res.json({ "error": err });
			return;
		}
		
		console.log(results);
		res.json({ "result": "ok" });
	});
});

app.put("/calibrate", (req, res) =>
{
	let options = {
		mode: "text",
		scriptPath: "./python/tb6600",
	};

	ps.PythonShell.run("calibrate.py", options, function (err, results)
	{
		if (err) {
			console.log(err);
			res.json({ "error": err });
			return;
		}
		
		console.log(results);
		res.json({ "result": results[0] });
	});
});

app.put("/power/:power", (req, res) =>
{
	let options = {
		mode: "text",
		scriptPath: "./python/tb6600",
		args: [ req.params.power === "1" ? "1" : "0" ]
	};

	ps.PythonShell.run("set-power.py", options, function (err, results)
	{
		if (err) {
			console.log(err);
			res.json({ "error": err });
			return;
		}
		
		console.log(results);
		res.json({ "result": results[0] });
	});
});

app.listen(1337, () =>
	console.log("Screen masking app is listening on port 1337"),
);

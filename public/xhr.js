function banana(t)
{
	var req = new XMLHttpRequest();
	var ookFeed = document.getElementById("ookFeed");
	req.addEventListener("loadend", function()
	{
		if (req.readyState == 4 && req.status == 200)
		{
			var r = req.responseText;
			r = JSON.parse(r);
			ookFeed.innerHTML = "";

			for (var i = 0; i < r.length; i++)
			{
				var tmpString = "<p>" + r[i].Username + " " + r[i].Date + "</br>" + r[i].Data + "</p>";
				ookFeed.innerHTML += tmpString;
			}

			setTimeout(banana, t);
		}
	});
	req.open("GET", "/showFeed.html");
	req.send(null);
}
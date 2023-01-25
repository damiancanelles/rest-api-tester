# rest-api-tester
<h3>Installation Guide:</h3>
<p>Go to the root project and run:</p>
<code>pip install -r requirements.txt</code>
<p>Make sure do you have installed python at least 3.10.0. Add the url of your postgres database to the file database.py and this is all.</p>
<p>Start de project running:</p>
<code>uvicorn main:app --reload</code>

<h3>Test Guide:</h3>
<p>The app in now running in the port 8000 go to (http://localhost:8000/docs#/) and test all the endpoints using the swagger.</p>
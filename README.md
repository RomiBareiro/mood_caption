# Mood caption processing application

## Setup & Installation

Make sure you have the latest version of Python installed.

```bash
pip install -r requirements.txt
```
## Running The App

```bash
python main.py
```
## Backend APIs usage

    Home page- `http://127.0.0.1:5000`
	REST functions doc. page- `http://127.0.0.1:5000/swagger/`

	Happy distribution- `localhost:5000/happy_dist/<str:user>` => put your user name to get the **distances to your stored places if you are happy** (for example: `http://127.0.0.1:5000/happy_dist/romi`)

	Current user mood- `http://127.0.0.1:500/curr_mood/<str:user>`  => put your user name **check your mood and location**
	
	User's mood distribution- `http://127.0.0.1:5000/mood_freq/<str:user>` => put your user name to see your **mood distribution and total mood captions**

## simulated cellphone api response

    Cellphone api simulator- `http://127.0.0.1:5000/curr_mood/` => **insert simulated user data to get Happy distribution, Current user mood and User's mood distribution user data**


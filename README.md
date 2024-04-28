# Deploy

## build
```bash
docker build -t drive_reader .
```

## run
```bash
docker run -it --rm --env-file .env drive_reader streamlit run app.py --server.port=8000 --server.address=0.0.0.0
```

<br>

# Prepare Google API

1. Navigate to [**Google Conscole**](https://console.cloud.google.com/) and click on **API & Services**
 
2. Crate new project or open existing one 

<img src="img/1.jpg" width="80%"/>
<img src="img/2.jpg" width="80%"/>


3.  Enable Drive API

<img src="img/3.jpg" width="80%"/>
<img src="img/4.jpg" width="80%"/>
<img src="img/5.jpg" width="80%"/>

4. Set up consent screen

<img src="img/6.jpg" width="80%"/>
<img src="img/7.jpg" width="80%"/>
<img src="img/8.jpg" width="80%"/>

## Set up Scopes

<img src="img/9.jpg" width="80%"/>

### Choode "auth/drive"  
<img src="img/10.jpg" width="100%"/>
<img src="img/11.jpg" width="100%"/>


4. Create Service Accaoun

<img src="img/12.jpg" width="80%"/>
<img src="img/13.jpg" width="80%"/>

Leave everything to default

5. Create access key

<img src="img/14.jpg" width="80%"/>
<img src="img/15.jpg" width="80%"/>
<img src="img/16.jpg" width="80%"/>

6. Add content of **.json** key to **.env** file as `API_SECRET_KEY` var

<br>

# Usage

1. Copy service account email

<img src="img/add_1.jpg" width="80%"/>

2. Share folder with service account

<img src="img/add_2.jpg" width="80%"/>
<img src="img/add_3.jpg" width="80%"/>

# Update Kanban states

KANBAN_STATES in app/parser.py stores string values ​​describing states in Google Sheets. Update it if the Kanban states have been updated. Order doesn't matter.

VIEW_STATES in app/parser.py stores string values describing what needs to be displayed in a dashboard cell. Order matters. "Total" is necessary.

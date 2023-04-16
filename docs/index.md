Hi Welcome to GS CRUD application

## Installation

### Get credential from google console
https://developers.google.com/workspace/guides/create-credentials

### docker-compose file
Create docker-compose.yaml

```yaml
version: "3.9"
services:
  workflow_engine:
    privileged: true
    image: muthupandiant/gscrud:main
    container_name: gscrud
    volumes:
      - type: bind
        source: ./cred_gscrud.json
        target: /cred_gscrud.json
    ports:
      - "80:80"
```    

### Run the application
```
docker-compose up --build
```

### Check the application

API Base URL: http://localhost

API Documentation: http://localhost/docs
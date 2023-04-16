Hi Welcome to GS CRUD application

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

Run
```
docker-compose up --build
```

Open

http://localhost
http://localhost/docs
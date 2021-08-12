# Dockerizing Django with Redis, MySQL

### Production

Uses app + api + websocket + webhook + redis + mysql.

1. Build the images and run the containers:

    ```sh
    $ docker-compose down && docker-compose up --build
    ```

    Test it out at [http://localhost:8000](http://localhost:8000). No mounted folders. To apply changes, the image must be re-built.

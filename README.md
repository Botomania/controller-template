# Controller
This will setup and start all the `player`, the `manager` and maintain communication between them

## setup
Before running this, arrange the `.env` file from maintainers and place it in project root
```sh
docker-compose up
```

## testing
A simple basic test can be arranged using the sample problems in player/manager.

### init
```sh
http :3000/init <<< '{"players": [{"id": 1, "name": "one", "image": "felicitythreads/interactive:player"},{"id": 2, "name": "two", "image": "felicitythreads/interactive:player"}], "manager": {"image": "felicitythreads/interactive:manager"}}'
```

### start
```sh
http post :3000/begin
```

### controller status
```sh
http get :3000/status
```

### game state
```sh
http get :3000/state
```

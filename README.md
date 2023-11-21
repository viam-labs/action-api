# action-api

Proto API and grpc bindings for action management

*action-api* provides Proto API and grpc bindings for action management

## API

The action resource implements the following API:

### start()

Start the action

### stop()

Stop the action

### is_running()

Returns boolean declaring if the action is currently underway

### status()

Get current status for the action.  Different action models will define their response differently.

## Using action-api with the Python SDK

Because this module uses a custom protobuf-based API, you must include this project in your client code.  One way to do this is to include it in your requirements.txt as follows:

```
action_api @ git+https://github.com/viam-labs/action-api.git@main
```

You can now import and use it in your code as follows:

```
from action_python import Action
api = Action.from_robot(robot, name="actionModel")
api.start()
```

See client.py for an example.

## Using action with the Golang SDK

Because this module uses a custom protobuf-based API, you must import and use in your client code as follows:

``` go
import action "github.com/viam-labs/action-api/src/action_go"

api, err := dock.FromRobot(robot, "action-model")
fmt.Println("err", err)
api.Start(context.Background())
```

See client.go for an example.

## Building

To rebuild the GRPC bindings, run:

``` bash
make generate
```

Then, in `src/dock_python/grpc/action_grpc.py change:

``` python
import action_pb2
```

to:

``` python
from . import action_pb2
```

Then, update the version in pyproject.toml

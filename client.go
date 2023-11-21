package main

import (
	"context"
	"fmt"
	"os"

	action "github.com/viam-labs/action-api/src/action_go"
	"go.viam.com/rdk/logging"
	"go.viam.com/rdk/robot/client"
	"go.viam.com/rdk/utils"
	"go.viam.com/utils/rpc"
)

func main() {
	logger := logging.NewLogger("client")
	robot, err := client.New(
		context.Background(),
		os.Getenv("ROBOT_ADDRESS"),
		logger,
		client.WithDialOptions(rpc.WithCredentials(rpc.Credentials{
			Type:    utils.CredentialsTypeRobotLocationSecret,
			Payload: os.Getenv("ROBOT_SECRET"),
		})),
	)
	if err != nil {
		logger.Fatal(err)
	}

	defer robot.Close(context.Background())
	logger.Info("Resources:")
	logger.Info(robot.ResourceNames())

	act, err := action.FromRobot(robot, "action")
	fmt.Println("err", err)
	if err != nil {
		fmt.Println(err)
	}
	act.IsRunning(context.Background())
}

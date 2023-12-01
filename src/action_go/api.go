// Package action implements the viam-labs.services.action API
package action

import (
	"context"

	"go.viam.com/rdk/logging"
	"go.viam.com/utils/rpc"
	"google.golang.org/protobuf/types/known/structpb"

	pb "github.com/viam-labs/action-api/src/action_go/grpc"
	"go.viam.com/rdk/resource"
	"go.viam.com/rdk/robot"
)

// API is the full API definition.
var API = resource.APINamespace("viam-labs").WithServiceType("action")

// Named is a helper for getting the named Action's typed resource name.
func Named(name string) resource.Name {
	return resource.NewName(API, name)
}

// FromRobot is a helper for getting the named Action from the given Robot.
func FromRobot(r robot.Robot, name string) (Action, error) {
	return robot.ResourceFromRobot[Action](r, Named(name))
}

func init() {
	resource.RegisterAPI(API, resource.APIRegistration[Action]{
		// Reconfigurable, and contents of reconfwrapper.go are only needed for standalone (non-module) uses.
		RPCServiceServerConstructor: NewRPCServiceServer,
		RPCServiceHandler:           pb.RegisterActionServiceHandlerFromEndpoint,
		RPCServiceDesc:              &pb.ActionService_ServiceDesc,
		RPCClient: func(
			ctx context.Context,
			conn rpc.ClientConn,
			remoteName string,
			name resource.Name,
			logger logging.Logger,
		) (Action, error) {
			return NewClientFromConn(conn, remoteName, name, logger), nil
		},
	})
}

// Action defines the Go interface for the component (should match the protobuf methods.)
type Action interface {
	resource.Resource
	Start(ctx context.Context) error
	Stop(ctx context.Context) error
	IsRunning(ctx context.Context) (bool, error)
	Status(ctx context.Context) (map[string]*structpb.Value, error)
}

// serviceServer implements the Action RPC service from action.proto.
type serviceServer struct {
	pb.UnimplementedActionServiceServer
	coll resource.APIResourceCollection[Action]
}

// NewRPCServiceServer returns a new RPC server for the Action API.
func NewRPCServiceServer(coll resource.APIResourceCollection[Action]) interface{} {
	return &serviceServer{coll: coll}
}

func (s *serviceServer) Start(ctx context.Context, req *pb.StartRequest) (*pb.StartResponse, error) {
	g, err := s.coll.Resource(req.Name)
	if err != nil {
		return nil, err
	}
	err = g.Start(ctx)
	if err != nil {
		return nil, err
	}
	return &pb.StartResponse{}, nil
}

func (s *serviceServer) Stop(ctx context.Context, req *pb.StopRequest) (*pb.StopResponse, error) {
	g, err := s.coll.Resource(req.Name)
	if err != nil {
		return nil, err
	}
	err = g.Stop(ctx)
	if err != nil {
		return nil, err
	}
	return &pb.StopResponse{}, nil
}

func (s *serviceServer) IsRunning(ctx context.Context, req *pb.IsRunningRequest) (*pb.IsRunningResponse, error) {
	g, err := s.coll.Resource(req.Name)
	if err != nil {
		return nil, err
	}
	resp, err := g.IsRunning(ctx)
	if err != nil {
		return nil, err
	}
	return &pb.IsRunningResponse{Running: resp}, nil
}

func (s *serviceServer) Status(ctx context.Context, req *pb.StatusRequest) (*pb.StatusResponse, error) {
	g, err := s.coll.Resource(req.Name)
	if err != nil {
		return nil, err
	}
	resp, err := g.Status(ctx)
	if err != nil {
		return nil, err
	}
	return &pb.StatusResponse{Status: resp}, nil
}

// NewClientFromConn creates a new Action RPC client from an existing connection.
func NewClientFromConn(conn rpc.ClientConn, remoteName string, name resource.Name, logger logging.Logger) Action {
	sc := newSvcClientFromConn(conn, remoteName, name, logger)
	return clientFromSvcClient(sc, name.ShortName())
}

func newSvcClientFromConn(conn rpc.ClientConn, remoteName string, name resource.Name, logger logging.Logger) *serviceClient {
	client := pb.NewActionServiceClient(conn)
	sc := &serviceClient{
		Named:  name.PrependRemote(remoteName).AsNamed(),
		client: client,
		logger: logger,
	}
	return sc
}

type serviceClient struct {
	resource.Named
	resource.AlwaysRebuild
	resource.TriviallyCloseable
	client pb.ActionServiceClient
	logger logging.Logger
}

// client is an Action client.
type client struct {
	*serviceClient
	name string
}

func clientFromSvcClient(sc *serviceClient, name string) Action {
	return &client{sc, name}
}

func (c *client) Start(ctx context.Context) error {
	_, err := c.client.Start(ctx, &pb.StartRequest{
		Name: c.name,
	})
	if err != nil {
		return err
	}
	return nil
}

func (c *client) Stop(ctx context.Context) error {
	_, err := c.client.Stop(ctx, &pb.StopRequest{
		Name: c.name,
	})
	if err != nil {
		return err
	}
	return nil
}

func (c *client) IsRunning(ctx context.Context) (bool, error) {
	resp, err := c.client.IsRunning(ctx, &pb.IsRunningRequest{
		Name: c.name,
	})
	if err != nil {
		return false, err
	}
	return resp.Running, nil
}

func (c *client) Status(ctx context.Context) (map[string]*structpb.Value, error) {
	resp, err := c.client.Status(ctx, &pb.StatusRequest{
		Name: c.name,
	})
	if err != nil {
		return nil, err
	}
	return resp.Status, nil
}

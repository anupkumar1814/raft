import argparse  
import queue  

from raft_consensus.actors import Actor, get_system  
from raft_consensus.config import load_user_config  
from raft_consensus.kvstore import KVStore  
from raft_consensus.messages import ClientRequest  
from raft_consensus.raft import RaftNetwork  

response = queue.Queue()  # Queue to store responses from Raft nodes


class Client(Actor):  # Client actor to send requests and handle responses
    def handle_client_response(self, res):
        response.put(res.result)  # Add the result of a client request to the response queue


def main():
    parser = argparse.ArgumentParser(description="Start a node or run a client command")  # Setup command-line parser
    parser.add_argument("-c", "--config", help="Configuration file for cluster setup")  # Cluster config file argument
    parser.add_argument("-l", "--leader", help="Leader address for client commands")  # Leader address for client commands
    parser.add_argument("name", nargs="*", help="Node names or commands if --leader flag is used")  # Node names or commands
    args = parser.parse_args()

    if args.leader:  # If a leader is specified, act as a client
        host, port = args.leader.split(":")  # Parse the leader address

        actor_system = get_system()  # Get the actor system for sending messages
        addr = actor_system.create(("localhost", 12345), Client)  # Register this client in the actor system
        actor_system.send((host, int(port)), ClientRequest(addr, args.name))  # Send client request to the leader

        try:
            res = response.get(timeout=5)  # Wait for a response with a timeout
        except queue.Empty:
            print("Timeout waiting for response")  # Timeout message if no response
        else:
            print(res)  # Print the response
        actor_system.shutdown()  # Clean up the actor system
    else:  # If no leader is specified, start nodes
        config = load_user_config(args.config)  # Load configuration file
        net = RaftNetwork(config, KVStore)  # Initialize the Raft network with config and KVStore

        nodes = [net.create_node(n) for n in args.name]  # Create nodes for each name in args
        return nodes  # Return the created nodes


nodes = main()  # Start the main function

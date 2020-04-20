#ifndef __GRAPH_UTILS__

#define __GRAPH_UTILS__

#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>


namespace s3f {
class Graph;

// Data structure to store graph edges
typedef struct EdgeStruct {
	int endpoint_1, endpoint_2;
    int endpoint_1_timeline, endpoint_2_timeline;
    bool isEndpoint1Router, isEndpoint2Router; 
    double weight;
} Edge;

// Data structure to store Adjacency list nodes
class Node {
    private:
	    int id;
        double nearestHostDist;
        std::vector<Edge> edges;
        std::unordered_map<int, double> nearestTimelineDist;

    public:
        int timelineID;
        bool isRouter;

        void addEdge(int endpoint, int associatedTimeline, double weight,
                    bool isEndpoint1Router, bool isEndpoint2Router);
        int doesEdgeExistTo(int dest);
        double getEdgeWeight(int dest);

        void setNearestHostDist(double nearestHostDist) { 
            nearestHostDist = nearestHostDist; };
        double getNearestHostDist() { return nearestHostDist; };

        void setNearestTimelineDist(int targetTimelineID,
                                    double targetTimelineDist) {
            this->nearestTimelineDist.insert(
                std::make_pair(targetTimelineID, targetTimelineDist));
        };
        double getNearestTimelineDist(int timelineID) {
            auto got = this->nearestTimelineDist.find(timelineID);
            if (got == this->nearestTimelineDist.end())
                return -1;

            return got->second;
        }

        Node(int id, int timelineID, bool isRouter): 
            id(id), timelineID(timelineID), isRouter(isRouter) {
                nearestHostDist = 0;
            };
        ~Node() {};
};



class Graph {

private:
    std::unordered_map<int, Node*> Nodes;
	int numVertices;  // number of nodes in the graph
    int numTimelines;
    double ** shortestDist;
    double ** cost;
    
    void setNearestHostDistTo(int startnode);

    void setNearestTimelineDistTo(int startnode, int targetTimelineID);

    void computeShortestPathsFrom(int startnode);

public:

    void addEdge(int endpoint_1, int endpoint_1_timeline,
                int endpoint_2, int endpoint_2_timeline,
                double weight,
                bool isEndpoint1Router, bool isEndpoint2Router);

    double getShortestDist(int endpoint_1, int endpoint_2);

    double getNearestHostDist(int node);

    double getNearestTimelineDist(int node, int targetTimeline);
    
    void populateAllShortestPaths();
 

	// Constructor
	Graph(int numVertices, int numTimelines)
        : numVertices(numVertices), numTimelines(numTimelines) {
        shortestDist = new double*[numVertices];
        cost = new double*[numVertices];
        
        for(int i = 0; i < numVertices; ++i) {
            shortestDist[i] = new double[numVertices];
            cost[i] = new double[numVertices];
        }

        for (int i = 0; i < numVertices; i++) {
            for (int j = 0; j < numVertices; j++) {
                shortestDist[i][j] = -1;
                cost[i][j] = -1;
            }
            shortestDist[i][i] = 0;
            cost[i][i] = 0;
        }
    };

	// Destructor
	~Graph() {
        for(int i = 0; i < numVertices; ++i) {
            delete [] shortestDist[i];
            delete [] cost[i];
        }
        delete [] shortestDist;
        delete [] cost;

        auto it = this->Nodes.begin();

        while(it != this->Nodes.end()) {
            delete it->second;
            it++;
        }
       
        // cleanup all Nodes
    }
};

}

#endif
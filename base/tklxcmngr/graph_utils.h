#ifndef __GRAPH_UTILS__

#define __GRAPH_UTILS__

#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>

#define US_IN_SEC 1000000
#define NS_IN_USEC 1000


namespace s3f {
class Graph;

// Data structure to store graph edges
typedef struct EdgeStruct {
	int endpoint_1, endpoint_2;
    int endpoint_1_timeline, endpoint_2_timeline;
    bool isEndpoint1Router, isEndpoint2Router; 
    long weight;
} Edge;

// Data structure to store Adjacency list nodes
class Node {
    private:
	    
        long nearestHostDist;
        std::vector<Edge> edges;
        std::unordered_map<int, long> nearestTimelineDist;

    public:
        int id;
        int timelineID;
        bool isRouter;

        void addEdge(int endpoint, int associatedTimeline, long weight,
                    bool isEndpoint1Router, bool isEndpoint2Router);
        int doesEdgeExistTo(int dest);
        long getEdgeWeight(int dest);

        void setNearestHostDist(long nearestHostDist) { 
            this->nearestHostDist = nearestHostDist; };
        long getNearestHostDist() { return this->nearestHostDist; };

        void setNearestTimelineDist(int targetTimelineID,
                                    long targetTimelineDist) {
            this->nearestTimelineDist.insert(
                std::make_pair(targetTimelineID, targetTimelineDist));
        };
        long getNearestTimelineDist(int timelineID) {
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
    
    int numTimelines;
    long ** shortestDist;
    long ** cost;
    
    void setNearestHostDistTo(int startnode);

    void setNearestTimelineDistTo(int startnode, int targetTimelineID);

    void computeShortestPathsFrom(int startnode);

public:

    int numVertices;  // number of nodes in the graph
    
    void addEdge(int endpoint_1, int endpoint_1_timeline,
                int endpoint_2, int endpoint_2_timeline,
                long weight, bool isEndpoint1Router, bool isEndpoint2Router);

    long getShortestDist(int endpoint_1, int endpoint_2);

    long getNearestHostDist(int node);

    long getNearestTimelineDist(int node, int targetTimeline);

    long getTimelineDist(int srcTimeline, int targetTimeline);
    
    
    void populateAllShortestPaths();
 

	// Constructor
	Graph(int numVertices, int numTimelines)
        : numVertices(numVertices), numTimelines(numTimelines) {
        shortestDist = new long*[numVertices];
        cost = new long*[numVertices];
        
        for(int i = 0; i < numVertices; ++i) {
            shortestDist[i] = new long[numVertices];
            cost[i] = new long[numVertices];
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
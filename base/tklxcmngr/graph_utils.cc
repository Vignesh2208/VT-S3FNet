
#include <iostream>
#include <string>
#include <queue>
#include <unordered_map>
#include <assert.h>
#include "graph_utils.h"

#define INFINITY 99999999999

using namespace s3f;

typedef std::pair<long, int> ePair; 

void Node::addEdge(int endpoint, int associatedTimeline, long weight,
                   bool isEndpoint1Router, bool isEndpoint2Router) {
    Edge new_edge;
    int isFound = 0;
    new_edge.endpoint_1 = this->id;
    new_edge.endpoint_2 = endpoint;
    new_edge.endpoint_1_timeline = this->timelineID;
    new_edge.endpoint_2_timeline = associatedTimeline;
    new_edge.isEndpoint1Router = isEndpoint1Router;
    new_edge.isEndpoint2Router = isEndpoint2Router;
    new_edge.weight = weight;

    for (auto & edge: this->edges) {
        if (edge.endpoint_1 == this->id && edge.endpoint_2 == endpoint) {
            isFound = 1;

            if (edge.weight > weight) {
                edge.weight = weight;
                edge.isEndpoint1Router = isEndpoint1Router;
                edge.isEndpoint2Router = isEndpoint2Router;
            }
            break;
        } 
 
    } 

    if (!isFound) {
        this->edges.push_back(new_edge);
    }
}

int Node::doesEdgeExistTo(int dest) {

    if (dest == this->id)
        return 0;

    for (auto & edge: this->edges) {
        if (edge.endpoint_2 == dest)
            return 1;
    } 
    return 0;
}

long Node::getEdgeWeight(int dest) {

    if (dest == this->id)
        return 0;

    for (auto & edge: this->edges) {
        if (edge.endpoint_2 == dest)
            return edge.weight;
    } 

    return INFINITY;
}


void Graph::addEdge(int endpoint_1, int endpoint_1_timeline,
                    int endpoint_2, int endpoint_2_timeline,
                    long weight, bool isEndpoint1Router, bool isEndpoint2Router) {

    auto got_1 = this->Nodes.find(endpoint_1);
    auto got_2 = this->Nodes.find(endpoint_2);

    if (isEndpoint1Router && isEndpoint2Router)
        printf("Adding Edge between: (S%d (%d) - S%d (%d)) with weight: %lu\n",
            endpoint_1, endpoint_1_timeline, endpoint_2, endpoint_2_timeline,
            weight);
    else if (isEndpoint1Router && !isEndpoint2Router)
        printf("Adding Edge between: (S%d (%d) - H%d (%d)) with weight: %lu\n",
            endpoint_1, endpoint_1_timeline, endpoint_2, endpoint_2_timeline,
            weight);
    else if (!isEndpoint1Router && isEndpoint2Router)
        printf("Adding Edge between: (H%d (%d) - S%d (%d)) with weight: %lu\n",
            endpoint_1, endpoint_1_timeline, endpoint_2, endpoint_2_timeline,
            weight);
    else
        printf("Adding Edge between: (H%d (%d) - H%d (%d)) with weight: %lu\n",
            endpoint_1, endpoint_1_timeline, endpoint_2, endpoint_2_timeline,
            weight);

    Node * node1;
    Node * node2;
    if (got_1 == this->Nodes.end()) {
        node1 = new Node(endpoint_1, endpoint_1_timeline, isEndpoint1Router);
        this->Nodes.insert(std::make_pair(endpoint_1, node1));
        
    } else {
        node1 = got_1->second;
    }

    if (got_2 == this->Nodes.end()) {
        node2 = new Node(endpoint_2, endpoint_2_timeline, isEndpoint2Router);
        this->Nodes.insert(std::make_pair(endpoint_2, node2));
    } else {
        node2 = got_2->second;
    }

    node1->addEdge(endpoint_2, endpoint_2_timeline, weight,
                    isEndpoint1Router, isEndpoint2Router);
    node2->addEdge(endpoint_1, endpoint_1_timeline, weight,
                    isEndpoint2Router, isEndpoint1Router);

}

void Graph::computeShortestPathsFrom(int startnode) {
    long * distance;
    int i, N;
    N = numVertices;
    Node * currNode;

    std::priority_queue< ePair, std::vector<ePair> , std::greater<ePair> > pq; 

    assert(startnode >= 0 && startnode < N);
    
    distance = new long[N];
    for(i = 0; i < N; ++i) {
        distance[i] = INFINITY;
    }  

    // Insert source itself in priority queue and initialize 
    // its distance as 0. 
    pq.push(std::make_pair(0, startnode)); 
    distance[startnode] = 0; 
  
    /* Looping till priority queue becomes empty (or all 
      distances are not finalized) */
    while (!pq.empty()) 
    { 
        // The first vertex in pair is the minimum distance 
        // vertex, extract it from priority queue. 
        // vertex label is stored in second of pair (it 
        // has to be done this way to keep the vertices 
        // sorted distance (distance must be first item 
        // in pair) 
        int u = pq.top().second; 
        pq.pop(); 
  
        assert(this->Nodes.find(u) != this->Nodes.end());
        currNode = this->Nodes.find(u)->second;
        //get all adjacent vertices of a vertex 
        for (i = 0; i < N; i++) 
        { 

            if (!currNode->doesEdgeExistTo(i))
                continue;

            // Get vertex label and weight of current adjacent 
            // of u. 
            long weight = cost[u][i]; 

            //printf("u = %d, v = %d\n", u, v);
  
            //  If there is shorted path to v through u. 
            if (distance[i] > distance[u] + weight) 
            { 
                // Updating distance of v 
                distance[i] = distance[u] + weight; 
                pq.push(std::make_pair(distance[i], i)); 
            } 
        } 
    } 
  
  
   for(i=0; i < N; i++) {
        if(i!=startnode) {
            shortestDist[startnode][i] = distance[i];
            shortestDist[i][startnode] = distance[i];

            //if (startnode == 0)
            printf("Shortest distance between : (%d)-(%d) = %lu units\n",
                    startnode, i, distance[i]);
        } 
    }

    delete [] distance;
    
}

void Graph::setNearestHostDistTo(int startnode) {
    long minDist = INFINITY;
    auto targetNode = this->Nodes.find(startnode);
    assert(targetNode != this->Nodes.end());
    
    for(int i = 0; i < numVertices; i++) {
        if (i != startnode && shortestDist[startnode][i] > 0
            && shortestDist[startnode][i] < minDist) {
            if (!this->Nodes.find(i)->second->isRouter) {
                minDist = shortestDist[startnode][i];
            }
        }
    }

    assert(minDist != INFINITY);
    std::cout << "Nearest Host Dist for " << startnode << " = " << minDist << "\n";
    targetNode->second->setNearestHostDist(minDist);
}


void Graph::setNearestTimelineDistTo(int startnode, int targetTimelineID) {
    long minDist = INFINITY;
    auto targetNode = this->Nodes.find(startnode);

    assert(targetNode != this->Nodes.end());
    for(int i = 0; i < numVertices; i++) {
        auto candidateNode = this->Nodes.find(i);

        assert(candidateNode != this->Nodes.end());
        if (i != startnode 
            && shortestDist[startnode][i] > 0
            && shortestDist[startnode][i] < minDist
            && candidateNode->second->timelineID == targetTimelineID) {
                minDist = shortestDist[startnode][i];
            
        }
    }

    if (minDist == INFINITY)
        minDist = 0;
    
    std::cout << "Min Dist[" << startnode << "][" << targetTimelineID << "] = "
              << minDist << std::endl;
    targetNode->second->setNearestTimelineDist(targetTimelineID, minDist);

}


long Graph::getNearestTimelineDist(int startnode, int targetTimelineID) {
    auto targetNode = this->Nodes.find(startnode);
    assert(targetNode != this->Nodes.end());
    return targetNode->second->getNearestTimelineDist(targetTimelineID);
}


long Graph::getTimelineDist(int srcTimeline, int targetTimeline) {
    long shortestDist = 0;
    for (auto it = this->Nodes.begin();
        it != this->Nodes.end(); it++) {
        
        if (it->second->timelineID != srcTimeline)
            continue;
            
        long currDist = this->getNearestTimelineDist(it->second->id, targetTimeline);
        if (shortestDist == 0 || shortestDist > currDist)
            shortestDist = currDist;
    }
    return shortestDist;
}

long Graph::getShortestDist(int endpoint_1, int endpoint_2) {

    assert(shortestDist[endpoint_1][endpoint_2] >= 0);
    return shortestDist[endpoint_1][endpoint_2];
}

long Graph::getNearestHostDist(int node) {

    assert(node >= 0 && node < numVertices);
    auto got = this->Nodes.find(node);

    assert(got != this->Nodes.end());
    return got->second->getNearestHostDist();
}


void Graph::populateAllShortestPaths() {
    Node * currNode;
    for(int i=0; i< this->numVertices; i++) {
        currNode = this->Nodes.find(i)->second;
        for(int j=0; j < this->numVertices; j++) {
            cost[i][j] = currNode->getEdgeWeight(j);
        }
    }
    for (int i = 0; i < this->numVertices; i++) {

        //printf("###################################\n");
        this->computeShortestPathsFrom(i);
        this->setNearestHostDistTo(i);
        for (int j = 0; j < this->numTimelines; j++) {
            this->setNearestTimelineDistTo(i, j);
        }
    }
}




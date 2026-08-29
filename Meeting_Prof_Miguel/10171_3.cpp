#include <bits/stdc++.h>
using namespace std;

const int INF = 1e9;

struct Edge {
    int u, v, weight;
};

vector<int> bellmanFord(
    int source,
    const vector<Edge>& edges
) {
    vector<int> dist(26, INF);
    dist[source] = 0;

    // Relax all edges V-1 times
    for (int i = 0; i < 25; i++) {

        bool changed = false;

        for (const Edge& edge : edges) {

            if (dist[edge.u] == INF)
                continue;

            if (dist[edge.u] + edge.weight < dist[edge.v]) {
                dist[edge.v] =
                    dist[edge.u] + edge.weight;

                changed = true;
            }
        }

        // Early termination if no distance changed
        if (!changed)
            break;
    }

    return dist;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;

    while (cin >> n && n != 0) {

        vector<Edge> youngEdges;
        vector<Edge> matureEdges;

        for (int i = 0; i < n; i++) {

            char age, direction;
            char from, to;
            int cost;

            cin >> age >> direction >> from >> to >> cost;

            int u = from - 'A';
            int v = to - 'A';

            if (age == 'Y') {

                youngEdges.push_back({u, v, cost});

                if (direction == 'B') {
                    youngEdges.push_back({v, u, cost});
                }
            }
            else {

                matureEdges.push_back({u, v, cost});

                if (direction == 'B') {
                    matureEdges.push_back({v, u, cost});
                }
            }
        }

        char myStart, miguelStart;
        cin >> myStart >> miguelStart;

        int mySource = myStart - 'A';
        int miguelSource = miguelStart - 'A';

        // Bellman-Ford on the two independent graphs
        vector<int> youngDist =
            bellmanFord(mySource, youngEdges);

        vector<int> matureDist =
            bellmanFord(miguelSource, matureEdges);

        int minimumCost = INF;
        vector<char> meetingPlaces;

        for (int i = 0; i < 26; i++) {

            if (youngDist[i] == INF ||
                matureDist[i] == INF) {
                continue;
            }

            int totalCost =
                youngDist[i] + matureDist[i];

            if (totalCost < minimumCost) {

                minimumCost = totalCost;

                meetingPlaces.clear();
                meetingPlaces.push_back('A' + i);
            }
            else if (totalCost == minimumCost) {

                meetingPlaces.push_back('A' + i);
            }
        }

        if (minimumCost == INF) {

            cout << "You will never meet.\n";

        }
        else {

            cout << minimumCost;

            for (char place : meetingPlaces) {
                cout << " " << place;
            }

            cout << '\n';
        }
    }

    return 0;
}
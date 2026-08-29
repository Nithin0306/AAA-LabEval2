#include <bits/stdc++.h>
using namespace std;

const int INF = 1e9;

using pii = pair<int, int>;

vector<int> dijkstra(
    int source,
    const vector<vector<pii>>& graph
) {
    int n = 26;

    vector<int> dist(n, INF);

    priority_queue<
        pii,
        vector<pii>,
        greater<pii>
    > pq;

    dist[source] = 0;
    pq.push({0, source});

    while (!pq.empty()) {
        auto [currentDist, u] = pq.top();
        pq.pop();

        if (currentDist != dist[u])
            continue;

        for (auto [v, weight] : graph[u]) {

            if (dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
                pq.push({dist[v], v});
            }
        }
    }

    return dist;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;

    while (cin >> n && n != 0) {

        vector<vector<pii>> young(26);
        vector<vector<pii>> mature(26);

        for (int i = 0; i < n; i++) {

            char age, direction;
            char from, to;
            int cost;

            cin >> age >> direction >> from >> to >> cost;

            int u = from - 'A';
            int v = to - 'A';

            if (age == 'Y') {
                young[u].push_back({v, cost});

                if (direction == 'B') {
                    young[v].push_back({u, cost});
                }
            }
            else {
                mature[u].push_back({v, cost});

                if (direction == 'B') {
                    mature[v].push_back({u, cost});
                }
            }
        }

        char myStart, miguelStart;
        cin >> myStart >> miguelStart;

        int mySource = myStart - 'A';
        int miguelSource = miguelStart - 'A';

        // Shortest distances from each person's starting location
        vector<int> youngDist =
            dijkstra(mySource, young);

        vector<int> matureDist =
            dijkstra(miguelSource, mature);

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
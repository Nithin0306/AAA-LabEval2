#include <bits/stdc++.h>
using namespace std;

const int INF = 1e9;

void floydWarshall(vector<vector<int>>& dist) {
    int n = 26;

    for (int k = 0; k < n; k++) {
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (dist[i][k] == INF || dist[k][j] == INF)
                    continue;

                dist[i][j] = min(dist[i][j],
                                 dist[i][k] + dist[k][j]);
            }
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;

    while (cin >> n && n != 0) {

        vector<vector<int>> young(26, vector<int>(26, INF));
        vector<vector<int>> mature(26, vector<int>(26, INF));

        // Distance from a location to itself is zero.
        for (int i = 0; i < 26; i++) {
            young[i][i] = 0;
            mature[i][i] = 0;
        }

        for (int i = 0; i < n; i++) {
            char age, direction, from, to;
            int cost;

            cin >> age >> direction >> from >> to >> cost;

            int u = from - 'A';
            int v = to - 'A';

            vector<vector<int>>& graph =
                (age == 'Y') ? young : mature;

            graph[u][v] = min(graph[u][v], cost);

            if (direction == 'B') {
                graph[v][u] = min(graph[v][u], cost);
            }
        }

        char myStart, miguelStart;
        cin >> myStart >> miguelStart;

        int sourceYoung = myStart - 'A';
        int sourceMature = miguelStart - 'A';

        floydWarshall(young);
        floydWarshall(mature);

        int minimumCost = INF;
        vector<char> meetingPlaces;

        for (int i = 0; i < 26; i++) {

            if (young[sourceYoung][i] == INF ||
                mature[sourceMature][i] == INF) {
                continue;
            }

            int totalCost =
                young[sourceYoung][i] +
                mature[sourceMature][i];

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
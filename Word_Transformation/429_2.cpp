#include <bits/stdc++.h>
using namespace std;

bool differByOne(const string& a, const string& b) {
    if (a.length() != b.length())
        return false;

    int diff = 0;

    for (int i = 0; i < (int)a.length(); i++) {
        if (a[i] != b[i]) {
            diff++;

            if (diff > 1)
                return false;
        }
    }

    return diff == 1;
}

int bfs(int start, int target,
        const vector<vector<int>>& graph) {

    int n = graph.size();

    vector<int> distance(n, -1);
    queue<int> q;

    distance[start] = 0;
    q.push(start);

    while (!q.empty()) {
        int current = q.front();
        q.pop();

        if (current == target)
            return distance[current];

        for (int next : graph[current]) {
            if (distance[next] == -1) {
                distance[next] = distance[current] + 1;
                q.push(next);
            }
        }
    }

    return -1;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    string line;
    getline(cin, line);
    getline(cin, line);   // consume blank line

    for (int tc = 0; tc < T; tc++) {

        vector<string> words;

        // Read dictionary
        while (getline(cin, line)) {
            if (line == "*")
                break;

            words.push_back(line);
        }

        int n = words.size();

        // Map word -> index
        unordered_map<string, int> index;

        for (int i = 0; i < n; i++) {
            index[words[i]] = i;
        }

        // Build adjacency list
        vector<vector<int>> graph(n);

        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {

                if (differByOne(words[i], words[j])) {
                    graph[i].push_back(j);
                    graph[j].push_back(i);
                }
            }
        }

        // Process queries
        while (getline(cin, line)) {

            if (line.empty())
                break;

            string startWord, targetWord;
            stringstream ss(line);

            ss >> startWord >> targetWord;

            int start = index[startWord];
            int target = index[targetWord];

            int answer = bfs(start, target, graph);

            cout << startWord << " "
                 << targetWord << " "
                 << answer << '\n';
        }

        if (tc != T - 1)
            cout << '\n';
    }

    return 0;
}
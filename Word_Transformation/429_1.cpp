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

int bfs(const string& start,
        const string& target,
        const vector<string>& words) {

    queue<pair<string, int>> q;
    unordered_set<string> visited;

    q.push({start, 0});
    visited.insert(start);

    while (!q.empty()) {
        auto [current, distance] = q.front();
        q.pop();

        if (current == target)
            return distance;

        for (const string& next : words) {
            if (!visited.count(next) && differByOne(current, next)) {
                visited.insert(next);
                q.push({next, distance + 1});
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
    getline(cin, line); // blank line

    for (int tc = 0; tc < T; tc++) {

        vector<string> dictionary;

        while (getline(cin, line)) {
            if (line == "*")
                break;

            dictionary.push_back(line);
        }

        while (getline(cin, line)) {
            if (line.empty())
                break;

            string start, target;
            stringstream ss(line);
            ss >> start >> target;

            int answer = bfs(start, target, dictionary);

            cout << start << " "
                 << target << " "
                 << answer << '\n';
        }

        if (tc != T - 1)
            cout << '\n';
    }

    return 0;
}
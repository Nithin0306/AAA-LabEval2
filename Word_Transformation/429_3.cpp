#include <bits/stdc++.h>
using namespace std;

int bfs(int start, int target,
        const vector<string>& words,
        const unordered_map<string, vector<int>>& patternMap) {

    int n = words.size();

    vector<int> distance(n, -1);

    queue<int> q;

    distance[start] = 0;
    q.push(start);

    // A word of length L can generate L patterns.
    // We use a set to avoid processing the same pattern repeatedly.
    unordered_set<string> usedPatterns;

    while (!q.empty()) {

        int current = q.front();
        q.pop();

        if (current == target)
            return distance[current];

        string word = words[current];

        // Generate all wildcard patterns of the current word
        for (int i = 0; i < (int)word.length(); i++) {

            string pattern = word;
            pattern[i] = '*';

            // Process each pattern only once
            if (usedPatterns.count(pattern))
                continue;

            usedPatterns.insert(pattern);

            auto it = patternMap.find(pattern);

            if (it == patternMap.end())
                continue;

            // All words having this pattern differ
            // from the current word in at most one position.
            for (int next : it->second) {

                if (distance[next] == -1) {
                    distance[next] = distance[current] + 1;
                    q.push(next);
                }
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
        unordered_set<string> seen;

        // Read dictionary
        while (getline(cin, line)) {

            if (line == "*")
                break;

            if (seen.insert(line).second)
                words.push_back(line);
        }

        int n = words.size();

        // Map each word to an integer index
        unordered_map<string, int> index;

        for (int i = 0; i < n; i++) {
            index[words[i]] = i;
        }

        // Build wildcard pattern map
        //
        // Example:
        // hot -> *ot, h*t, ho*
        unordered_map<string, vector<int>> patternMap;

        for (int i = 0; i < n; i++) {

            string word = words[i];

            for (int j = 0; j < (int)word.length(); j++) {

                string pattern = word;
                pattern[j] = '*';

                patternMap[pattern].push_back(i);
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

            int answer = bfs(
                start,
                target,
                words,
                patternMap
            );

            cout << startWord << " "
                 << targetWord << " "
                 << answer << '\n';
        }

        if (tc != T - 1)
            cout << '\n';
    }

    return 0;
}
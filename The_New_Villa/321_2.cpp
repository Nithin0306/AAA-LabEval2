#include <bits/stdc++.h>
using namespace std;

struct ParentInfo {
    int parent;
    string action;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int r, d, s;
    int caseNo = 1;

    while (cin >> r >> d >> s) {
        if (r == 0 && d == 0 && s == 0)
            break;

        vector<vector<int>> doors(r);
        vector<vector<int>> switches(r);

        for (int i = 0; i < d; i++) {
            int u, v;
            cin >> u >> v;
            --u;
            --v;

            doors[u].push_back(v);
            doors[v].push_back(u);
        }

        for (int i = 0; i < s; i++) {
            int u, v;
            cin >> u >> v;
            --u;
            --v;

            switches[u].push_back(v);
        }

        int maskCount = 1 << r;
        int totalStates = r * maskCount;

        auto encode = [&](int room, int mask) {
            return room * maskCount + mask;
        };

        auto getRoom = [&](int state) {
            return state / maskCount;
        };

        auto getMask = [&](int state) {
            return state % maskCount;
        };

        int startState = encode(0, 1);
        int goalState = encode(r - 1, 1 << (r - 1));

        vector<bool> visited(totalStates, false);
        vector<ParentInfo> parent(totalStates);

        queue<int> q;
        q.push(startState);
        visited[startState] = true;

        int finalState = -1;

        while (!q.empty()) {
            int state = q.front();
            q.pop();

            int room = getRoom(state);
            int mask = getMask(state);

            if (state == goalState) {
                finalState = state;
                break;
            }

            for (int target : switches[room]) {
                if (target == room)
                    continue;

                int newMask;

                if (mask & (1 << target))
                    newMask = mask & ~(1 << target);
                else
                    newMask = mask | (1 << target);

                int newState = encode(room, newMask);

                if (!visited[newState]) {
                    visited[newState] = true;

                    string action;

                    if (mask & (1 << target))
                        action = "Switch off light in room ";
                    else
                        action = "Switch on light in room ";

                    action += to_string(target + 1) + ".";

                    parent[newState] = {
                        state,
                        action
                    };

                    q.push(newState);
                }
            }

            for (int nextRoom : doors[room]) {
                if (!(mask & (1 << nextRoom)))
                    continue;

                int newState = encode(nextRoom, mask);

                if (!visited[newState]) {
                    visited[newState] = true;

                    parent[newState] = {
                        state,
                        "Move to room " +
                        to_string(nextRoom + 1) + "."
                    };

                    q.push(newState);
                }
            }
        }

        cout << "Villa #" << caseNo++ << '\n';

        if (finalState == -1) {
            cout << "The problem cannot be solved.\n\n";
            continue;
        }

        vector<string> path;
        int state = finalState;

        while (state != startState) {
            path.push_back(parent[state].action);
            state = parent[state].parent;
        }

        reverse(path.begin(), path.end());

        cout << "The problem can be solved in "
             << path.size() << " steps:\n";

        for (const string& action : path)
            cout << "- " << action << '\n';

        cout << '\n';
    }

    return 0;
}